"""Step 6 with the existing 61 firms: fit on Nov 2020 - Dec 2024, test on Jan 2025 - Nov 2026.

Inputs: the pack's returns (date-fixed, common.stock()) through its last date, then Yahoo Finance
adjusted-close returns (26_fetch_extend.py, validated against the pack on the 2024-25 overlap);
NIFTY 500 the same way; rainfall 2000-2025 plus 2026 (NASA POWER).
Extreme-rain episodes use exactly the rule of 04_hazard_panel.py: 3-day rain at a plant district
above that district's own 5-year return level (2000-2019 baseline); episodes > 30 days apart;
plants hit in the same week = one firm-episode; benchmark = same-date firms with no plant in an
extreme district within 10 days.
Tests
  A. Loss elasticity: fit CAR-minus-benchmark ~ share on 2020-24 firm-episodes; does it predict 2025-26?
  B. Hazard persistence: do districts / firms hit more often in 2020-24 get hit more in 2025-26?
  C. Concentration -> idiosyncratic volatility: does the 2020-24 cross-section predict 2025-26?
Test period ends 30 Sep 2026 for rainfall (the source model changes on 1 Oct 2026); returns run to 17 Nov 2026,
so 20-day windows are complete for every test episode.
Outputs: outputs/tables/oos_*.csv, outputs/figs/12_out_of_sample.png
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, statsmodels.formula.api as smf
from scipy import stats
from common import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from es_lib import BLUE, ORANGE, AQUA, MUTED, SURF, INK
SPLIT = pd.Timestamp("2025-01-01")

# ---------------- returns and market, extended ----------------
s = stock()
y = pd.read_csv(EXT + "prices_yahoo_2024_2026.csv", parse_dates=["date"]).sort_values(["asset_id", "date"]).drop_duplicates(["asset_id", "date"])
y["ret"] = y.groupby("asset_id").adjclose.pct_change(fill_method=None)
last = s.groupby("asset_id").date.max()
y = y[y.date > y.asset_id.map(last)]
y.loc[y.ret.abs() > 0.40, "ret"] = np.nan
R = pd.concat([s[["asset_id", "date", "ret"]], y[["asset_id", "date", "ret"]]]).pivot(index="date", columns="asset_id", values="ret").sort_index()
i0 = pd.read_csv(EXT + "indices_daily.csv", parse_dates=["date"]); i1 = pd.read_csv(EXT + "indices_daily_2026.csv", parse_dates=["date"])
ix = pd.concat([i0, i1[i1.date > i0.date.max()]]).pivot_table(index="date", columns="index", values="close").sort_index().pct_change(fill_method=None)
MKT = ix["NIFTY500"].reindex(R.index).fillna(ix["NIFTY50"].reindex(R.index)).fillna(R.mean(axis=1))
R = R[R.index.dayofweek < 5]; MKT = MKT.reindex(R.index)
DATES = R.index; EST = (-250, -30)
def t0_of(d): return int(np.searchsorted(DATES.values, np.datetime64(pd.Timestamp(d))))
def ar_matrix(t0, pre=1, post=25, min_obs=120):
    a, b = t0 + EST[0], t0 + EST[1]
    if a < 0 or t0 + post >= len(DATES): return None
    yy, m = R.iloc[a:b], MKT.iloc[a:b]; ok = yy.notna().sum() >= min_obs; mc = m - m.mean()
    beta = (yy.sub(yy.mean())).mul(mc, axis=0).sum() / ((yy.notna()).mul(mc ** 2, axis=0).sum()); alpha = yy.mean() - beta * m.mean()
    w = R.iloc[t0 - pre:t0 + post + 1]
    ar = w - (alpha.values[None, :] + np.outer(MKT.iloc[t0 - pre:t0 + post + 1].values, beta.values))
    ar = ar.loc[:, ok]; ar.index = range(-pre, post + 1); return ar

# ---------------- rainfall episodes, extended ----------------
r0 = pd.read_csv(EXT + "rain_daily.csv.gz", parse_dates=["date"]); r1 = pd.read_csv(EXT + "rain_daily_2026.csv.gz", parse_dates=["date"])
rain = pd.concat([r0, r1[r1.date > r0.date.max()]]).sort_values(["dist_name", "date"])
# NASA POWER rainfall comes from MERRA-2 up to 30 Sep 2026 and from the near-real-time GEOS-IT model
# from 1 Oct 2026 (checked in the API response headers). Keep one source: stop at 30 Sep 2026.
RAIN_END = pd.Timestamp("2026-09-30"); rain = rain[rain.date <= RAIN_END]
rain["r3"] = rain.groupby("dist_name").mm.transform(lambda v: v.rolling(3, min_periods=1).sum())
base = rain[rain.date.dt.year <= 2019]
amax = base.groupby(["dist_name", base.date.dt.year]).r3.max().unstack()
rain = rain.merge(amax.quantile(0.8, axis=1).rename("rl5"), left_on="dist_name", right_index=True); rain["sev"] = rain.r3 / rain.rl5
r = rain[(rain.date >= "2020-11-01") & (rain.sev >= 1)].copy()
r["gap"] = r.groupby("dist_name").date.diff().dt.days.fillna(999); r["ep"] = (r.gap > 30).groupby(r.dist_name).cumsum()
ep = r.groupby(["dist_name", "ep"]).agg(start=("date", "min"), peak_sev=("sev", "max"), peak_mm=("r3", "max")).reset_index()
ep["period"] = np.where(ep.start < SPLIT, "fit 2020-24", "test 2025-26")
ep.to_csv(TAB + "oos_district_episodes.csv", index=False)
p = plants(); tot = p.groupby("nse_symbol").project_cost_cr.sum()
pe = p.merge(ep, on="dist_name"); pe["wk"] = pe.start.dt.to_period("W")
fe = pe.groupby(["nse_symbol", "wk"]).agg(start=("start", "min"), hit_cost=("project_cost_cr", "sum"), n_plants_hit=("lat", "size"),
        sev=("peak_sev", "max"), districts=("dist_name", lambda v: "|".join(sorted(set(v))[:5]))).reset_index()
fe["share"] = fe.hit_cost / fe.nse_symbol.map(tot); fe = fe[fe.nse_symbol.isin(R.columns)]

def firm_cars(firm, date):
    ar = ar_matrix(t0_of(date))
    if ar is None or firm not in ar: return None
    hit = set(fe.nse_symbol[(fe.start - pd.Timestamp(date)).abs().dt.days <= 10]); un = [c for c in ar.columns if c not in hit]
    o = {f"car_0_{h}": ar[firm].loc[0:h].sum(min_count=max(1, int(0.7 * (h + 1)))) for h in (5, 10, 20)}
    o.update({f"adj_0_{h}": o[f"car_0_{h}"] - ar[un].loc[0:h].sum().mean() for h in (5, 10, 20)}); o["n_bench"] = len(un)
    a40 = ar_matrix(t0_of(date), post=45)                     # 40-day window where the data run long enough
    if a40 is not None and firm in a40:
        u40 = [c for c in a40.columns if c not in hit]
        o["car_0_40"] = a40[firm].loc[0:40].sum(min_count=29); o["adj_0_40"] = o["car_0_40"] - a40[u40].loc[0:40].sum().mean()
    return o
rows = []
for _, x in fe[fe.share >= 0.02].iterrows():
    c = firm_cars(x.nse_symbol, x.start)
    if c: rows.append({**x.drop("wk").to_dict(), **c})
es = pd.DataFrame(rows); es["period"] = np.where(es.start < SPLIT, "fit 2020-24", "test 2025-26"); es["wk"] = es.start.dt.to_period("W").astype(str)
es.to_csv(TAB + "oos_firm_episode_cars.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print("returns to", DATES[-1].date(), "| rainfall to", RAIN_END.date())
print("district-episodes:", ep.groupby("period").size().to_dict(), "| firm-episodes (share>=2%) with returns:", es.groupby("period").size().to_dict())

# ---------------- A. elasticity ----------------
A = []
fit, test = es[es.period == "fit 2020-24"], es[es.period == "test 2025-26"]
for h in (5, 10, 20):
    dep = f"adj_0_{h}"; f_ = fit.dropna(subset=[dep]); t_ = test.dropna(subset=[dep])
    m = smf.ols(f"{dep} ~ share", f_).fit(cov_type="cluster", cov_kwds={"groups": f_.wk.astype("category").cat.codes})
    mt = smf.ols(f"{dep} ~ share", t_).fit(cov_type="cluster", cov_kwds={"groups": t_.wk.astype("category").cat.codes})
    pred = m.params["Intercept"] + m.params["share"] * t_.share
    sse_m = ((t_[dep] - pred) ** 2).sum(); sse_0 = ((t_[dep] - 0) ** 2).sum(); sse_mean = ((t_[dep] - f_[dep].mean()) ** 2).sum()
    hi_f, hi_t = f_[f_.share >= .25], t_[t_.share >= .25]
    A.append(dict(window=f"[0,{h}]", n_fit=len(f_), n_test=len(t_), slope_fit=m.params["share"], se_fit=m.bse["share"], p_fit=m.pvalues["share"],
                  slope_test=mt.params["share"], se_test=mt.bse["share"], p_test=mt.pvalues["share"],
                  z_slopes_differ=(mt.params["share"] - m.params["share"]) / np.hypot(m.bse["share"], mt.bse["share"]),
                  oos_r2_vs_zero=1 - sse_m / sse_0, oos_r2_vs_fit_mean=1 - sse_m / sse_mean,
                  n_hi_fit=len(hi_f), mean_hi_fit=hi_f[dep].mean(), n_hi_test=len(hi_t), mean_hi_test=hi_t[dep].mean(),
                  predicted_hi_test=(m.params["Intercept"] + m.params["share"] * hi_t.share).mean(),
                  median_hi_test=hi_t[dep].median(), frac_neg_hi_test=(hi_t[dep] < 0).mean(),
                  t_hi_test_week_clustered=(lambda g: g.mean() / (g.std() / np.sqrt(len(g))))(hi_t.groupby("wk")[dep].mean()),
                  weeks_hi_test=hi_t.wk.nunique()))
A = pd.DataFrame(A); A.round(4).to_csv(TAB + "oos_elasticity.csv", index=False)
print("\n=== A. loss elasticity (CAR minus same-date unexposed, per 100% of assets hit) ==="); print(A.round(3).to_string(index=False))

# ---------------- B. hazard persistence ----------------
yrs_fit = (SPLIT - pd.Timestamp("2020-11-01")).days / 365.25; yrs_test = (RAIN_END - SPLIT).days / 365.25
dfreq = ep.groupby(["dist_name", "period"]).size().unstack(fill_value=0).reindex(rain.dist_name.unique(), fill_value=0)
dfreq["rate_fit"] = dfreq.get("fit 2020-24", 0) / yrs_fit; dfreq["rate_test"] = dfreq.get("test 2025-26", 0) / yrs_test
p["w"] = p.project_cost_cr / p.nse_symbol.map(tot)
fz = p.assign(rf=p.dist_name.map(dfreq.rate_fit).fillna(0), rt=p.dist_name.map(dfreq.rate_test).fillna(0)).groupby("nse_symbol").apply(
    lambda d: pd.Series({"exp_share_hit_fit": (d.w * d.rf).sum(), "exp_share_hit_test": (d.w * d.rt).sum()}), include_groups=False)
fz = fz[fz.index.isin(R.columns)]
B = pd.DataFrame([
    dict(level="district (478)", spearman=stats.spearmanr(dfreq.rate_fit, dfreq.rate_test)[0], p=stats.spearmanr(dfreq.rate_fit, dfreq.rate_test)[1],
         mean_rate_fit=dfreq.rate_fit.mean(), mean_rate_test=dfreq.rate_test.mean(),
         p_hit_in_test_if_top_quintile_fit=(dfreq.rate_test[dfreq.rate_fit >= dfreq.rate_fit.quantile(.8)] > 0).mean(),
         p_hit_in_test_if_bottom_80pct_fit=(dfreq.rate_test[dfreq.rate_fit < dfreq.rate_fit.quantile(.8)] > 0).mean(),
         p_hit_in_test_all=(dfreq.rate_test > 0).mean()),
    dict(level="firm (61 traded)", spearman=stats.spearmanr(fz.exp_share_hit_fit, fz.exp_share_hit_test)[0], p=stats.spearmanr(fz.exp_share_hit_fit, fz.exp_share_hit_test)[1],
         mean_rate_fit=fz.exp_share_hit_fit.mean(), mean_rate_test=fz.exp_share_hit_test.mean())])
B.round(4).to_csv(TAB + "oos_hazard_persistence.csv", index=False); fz.round(4).to_csv(TAB + "oos_firm_hazard_rates.csv")
print(f"\n=== B. hazard persistence (episodes per year; fit {yrs_fit:.2f} yrs, test {yrs_test:.2f} yrs) ==="); print(B.round(3).to_string(index=False))

# ---------------- C. concentration -> idiosyncratic volatility ----------------
co = companies().set_index("nse_symbol")
hhi = p.groupby("nse_symbol").apply(lambda d: (d.groupby("dist_name").w.sum() ** 2).sum(), include_groups=False)
def vol_table(a, b):
    out = {}
    for c in R.columns:
        d = pd.concat([R[c], MKT], axis=1).loc[a:b].dropna()
        if len(d) < 150: continue
        be = np.cov(d.iloc[:, 0], d.iloc[:, 1])[0, 1] / d.iloc[:, 1].var()
        out[c] = dict(beta=be, ivol=(d.iloc[:, 0] - be * d.iloc[:, 1]).std() * np.sqrt(250))
    return pd.DataFrame(out).T
v_f, v_t = vol_table("2020-11-01", "2024-12-31"), vol_table("2025-01-01", DATES[-1])
X = pd.DataFrame({"hhi": hhi, "lsize": np.log(co.total_project_cost_cr.clip(lower=1))}).join(fz.exp_share_hit_fit)
cf = X.join(v_f).dropna(); ct = X.join(v_t).dropna()
mf = smf.ols("ivol ~ hhi + exp_share_hit_fit + lsize + beta", cf).fit(cov_type="HC1")
mt = smf.ols("ivol ~ hhi + exp_share_hit_fit + lsize + beta", ct).fit(cov_type="HC1")
pred = mf.predict(ct)
C = pd.DataFrame([dict(sample=lab, n=int(m.nobs), coef_hhi=m.params["hhi"], se_hhi=m.bse["hhi"], p_hhi=m.pvalues["hhi"],
                       coef_hazard=m.params["exp_share_hit_fit"], p_hazard=m.pvalues["exp_share_hit_fit"], r2=m.rsquared) for lab, m in (("fit 2020-24", mf), ("test 2025-26", mt))])
C["corr_predicted_vs_actual_ivol_test"] = [np.nan, np.corrcoef(pred, ct.ivol)[0, 1]]
C["rank_corr_ivol_fit_vs_test"] = [np.nan, stats.spearmanr(cf.ivol.reindex(ct.index), ct.ivol, nan_policy="omit")[0]]
C.round(4).to_csv(TAB + "oos_concentration_vol.csv", index=False)
print("\n=== C. concentration and idiosyncratic volatility ==="); print(C.round(3).to_string(index=False))

# ---------------- the largest test-period hits ----------------
big = test[test.share >= .25].sort_values("sev", ascending=False)
big.round(3).to_csv(TAB + "oos_largest_test_episodes.csv", index=False)
print("\n=== test period: firm-episodes with >=25% of plant cost in extreme-rain districts ===")
print(big[["nse_symbol", "start", "districts", "sev", "share", "adj_0_5", "adj_0_10", "adj_0_20"]].round(3).to_string(index=False))
top = ep[ep.period == "test 2025-26"].sort_values("peak_sev", ascending=False).head(15)
print("\nmost severe test-period district-episodes (any plant):"); print(top[["dist_name", "start", "peak_sev", "peak_mm"]].round(2).to_string(index=False))

# ---------------- figure ----------------
fig, axs = plt.subplots(1, 3, figsize=(15, 4.6))
ax = axs[0]
for d, col, lab in ((fit, BLUE, "fit 2020–24"), (test, ORANGE, "test 2025–26")):
    b = pd.cut(d.share, [0.02, .05, .1, .25, .5, 1.01]); g = d.groupby(b, observed=True).agg(x=("share", "mean"), y=("adj_0_10", "mean"), n=("share", "size"))
    ax.plot(g.x * 100, g.y * 100, color=col, marker="o", ms=6, label=f"{lab} (n={len(d)})")
xx = np.linspace(0.02, 1, 50); a10 = A[A.window == "[0,10]"].iloc[0]
m10 = smf.ols("adj_0_10 ~ share", fit.dropna(subset=["adj_0_10"])).fit()
ax.plot(xx * 100, (m10.params["Intercept"] + m10.params["share"] * xx) * 100, color=BLUE, lw=1, ls="--", label="fitted on 2020–24")
ax.axhline(0, color="#c9c8c2", lw=.8); ax.set_xlabel("Share of plant cost in extreme-rain districts, %"); ax.set_ylabel("CAR days 0–10 minus unexposed, % (bin means)")
ax.set_title("A. Loss elasticity: fit vs test", loc="left"); ax.legend(fontsize=7.5)
ax = axs[1]
nf = dfreq.get("fit 2020-24", pd.Series(0, index=dfreq.index)).clip(upper=4)
g = pd.DataFrame({"nf": nf, "hit": dfreq.rate_test > 0}).groupby("nf").agg(share=("hit", "mean"), n=("hit", "size"))
ax.bar(g.index, g.share * 100, color=BLUE, width=.62)
for k, v in g.iterrows(): ax.text(k, v.share * 100 + 1.5, f"{v.share:.0%}\n(n={int(v.n)})", ha="center", fontsize=7.5, color=MUTED)
ax.set_xticks(g.index); ax.set_xticklabels([str(int(k)) if k < 4 else "4+" for k in g.index])
ax.set_xlabel("Extreme-rain episodes in the district, Nov 2020–Dec 2024"); ax.set_ylabel(f"Districts with ≥1 episode, Jan 2025–{RAIN_END:%b %Y}, %")
ax.set_ylim(0, 100); ax.set_title(f"B. Do the same districts get hit? Spearman {B.spearman.iloc[0]:.2f}", loc="left")
ax = axs[2]
ax.scatter(pred * 100, ct.ivol * 100, s=22, color=AQUA, edgecolor=SURF)
lim = [min(pred.min(), ct.ivol.min()) * 100, max(pred.max(), ct.ivol.max()) * 100]; ax.plot(lim, lim, color="#c9c8c2", lw=.9)
ax.set_xlabel("Idiosyncratic volatility predicted from 2020–24 model, %"); ax.set_ylabel("Actual 2025–26, %")
ax.set_title(f"C. Concentration and volatility: r = {C.corr_predicted_vs_actual_ivol_test.iloc[1]:.2f}", loc="left")
fig.suptitle("Out-of-sample test: fit on Nov 2020–Dec 2024, test on Jan 2025–Sep 2026 (61 firms)", x=0.01, ha="left", fontweight="bold")
fig.tight_layout(); fig.savefig(FIG + "12_out_of_sample.png", dpi=200)
