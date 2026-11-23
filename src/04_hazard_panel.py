"""Data-driven physical-hazard panel: NASA POWER daily rainfall at every plant district (2000-2025).
 1. validate the pack's named flood events against rainfall
 2. detect ALL extreme-rain episodes 2020-2025 in any plant district (3-day total above the
    district's own 5-year return level, 2000-2019 baseline)
 3. firm-level 'assets under water' share per episode -> event study on every firm-episode
 4. monthly panel regression of abnormal return on hazard-exposed asset share (firm + month FE)"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from es_lib import *
import statsmodels.formula.api as smf
rain = pd.read_csv(EXT + "rain_daily.csv.gz", parse_dates=["date"]).sort_values(["dist_name", "date"])
rain["r3"] = rain.groupby("dist_name").mm.transform(lambda s: s.rolling(3, min_periods=1).sum())
base = rain[rain.date.dt.year <= 2019]
amax = base.groupby(["dist_name", base.date.dt.year]).r3.max().unstack()
thr = pd.DataFrame({"rl5": amax.quantile(0.8, axis=1), "rl2": amax.quantile(0.5, axis=1), "rl20": amax.quantile(0.95, axis=1), "max20y": amax.max(axis=1)})
rain = rain.merge(thr, left_on="dist_name", right_index=True)
rain["sev"] = rain.r3 / rain.rl5

# 1 ---- validate named events ------------------------------------------------------------------
val = []
for ev, dists, a, b in [("Gujarat flood 2024", ["Vadodara", "Bharuch", "Anand", "Kheda"], "2024-08-24", "2024-09-05"),
                        ("Gujarat flood 2023", ["Bharuch", "Vadodara", "Narmada"], "2023-09-15", "2023-09-22"),
                        ("Himachal flood 2023", ["Solan", "Shimla", "Kullu", "Una", "Sirmaur"], "2023-07-07", "2023-07-25"),
                        ("Chennai Michaung 2023", ["Chennai", "Kancheepuram", "Thiruvallur"], "2023-12-02", "2023-12-12")]:
    for d in dists:
        x = rain[(rain.dist_name == d) & rain.date.between(a, b)]
        if len(x) == 0: continue
        i = x.r3.idxmax(); pk = x.loc[i]
        rank = (amax.loc[d] >= pk.r3).sum()
        val.append(dict(event=ev, district=d, peak_date=pk.date.date(), peak_3day_mm=pk.r3, rl2_mm=pk.rl2, rl5_mm=pk.rl5, rl20_mm=pk.rl20,
                        ratio_to_5yr_level=pk.sev, baseline_years_exceeding=f"{rank}/20"))
val = pd.DataFrame(val); val.to_csv(TAB + "rain_validation_named_events.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30); print(val.round(2).to_string())

# 2 ---- detect extreme episodes 2020-2025 ------------------------------------------------------
r = rain[(rain.date >= "2020-11-01") & (rain.sev >= 1)].copy()
r["gap"] = r.groupby("dist_name").date.diff().dt.days.fillna(999)
r["ep"] = (r.gap > 30).groupby(r.dist_name).cumsum()
ep = r.groupby(["dist_name", "ep"]).agg(start=("date", "min"), peak_sev=("sev", "max"), peak_mm=("r3", "max")).reset_index()
ep.to_csv(TAB + "rain_extreme_episodes_by_district.csv", index=False)
print("district-episodes:", len(ep), "districts:", ep.dist_name.nunique(), ep.start.dt.year.value_counts().sort_index().to_dict())

# 3 ---- firm-episode exposure -------------------------------------------------------------------
p = plants(); tot = p.groupby("nse_symbol").project_cost_cr.sum()
pe = p.merge(ep, on="dist_name")
pe["wk"] = pe.start.dt.to_period("W")                      # plants hit in the same week = one firm-episode
fe = pe.groupby(["nse_symbol", "wk"]).agg(start=("start", "min"), hit_cost=("project_cost_cr", "sum"), n_plants_hit=("lat", "size"),
        sev=("peak_sev", "max"), districts=("dist_name", lambda s: "|".join(sorted(set(s))[:5]))).reset_index()
fe["share"] = fe.hit_cost / fe.nse_symbol.map(tot)
fe = fe[fe.nse_symbol.isin(R.columns)]
fe.drop(columns="wk").to_csv(TAB + "rain_firm_episodes.csv", index=False)
print("firm-episodes:", len(fe), " with share>=10%:", (fe.share >= .1).sum(), " >=25%:", (fe.share >= .25).sum())

def firm_cars(firm, date):
    ar = ar_matrix(t0_of(date), pre=1, post=25)
    if ar is None or firm not in ar: return None
    # same-date benchmark: firms with NO plant in any extreme-rain district that week (kills
    # seasonality / market-wide monsoon-month effects that a random-date placebo cannot)
    hit = set(fe.nse_symbol[(fe.start - pd.Timestamp(date)).abs().dt.days <= 10])
    un = [c for c in ar.columns if c not in hit]
    o = {f"car_0_{h}": ar[firm].loc[0:h].sum() for h in (1, 5, 10, 20)}
    o.update({f"adj_0_{h}": ar[firm].loc[0:h].sum() - ar[un].loc[0:h].sum().mean() for h in (5, 10, 20)})
    o["n_bench"] = len(un)
    return o
rows = []
for _, x in fe[fe.share >= 0.02].iterrows():
    c = firm_cars(x.nse_symbol, x.start)
    if c: rows.append({**x.drop("wk").to_dict(), **c})
es = pd.DataFrame(rows); es.to_csv(TAB + "rain_firm_episode_cars.csv", index=False)
# placebo: same firms, random dates
rng = np.random.default_rng(5); PLC = placebo_t0s(400, seed=3, post=30)
AR_PL = {int(t): ar_matrix(int(t), pre=1, post=25) for t in PLC}
def placebo_mean(firms, col_h, n=400):
    out = []
    keys = list(AR_PL)
    for _ in range(n):
        v = [AR_PL[keys[rng.integers(len(keys))]].get(f, pd.Series(dtype=float)).loc[0:col_h].sum() for f in firms]
        out.append(np.nanmean(v))
    return np.array(out)
summ = []
for lab, m in [("share 2-10%", (es.share < .10)), ("share 10-25%", (es.share >= .10) & (es.share < .25)), ("share >=25%", es.share >= .25),
               ("share >=25% & severity >=1.5x 5yr level", (es.share >= .25) & (es.sev >= 1.5))]:
    d = es[m]
    for h in (5, 10, 20):
        pl = placebo_mean(d.nse_symbol.tolist(), h)
        v = d[f"car_0_{h}"]
        summ.append(dict(bucket=lab, n=len(d), firms=d.nse_symbol.nunique(), window=f"[0,{h}]", mean_car=v.mean(), median_car=v.median(),
                         frac_neg=(v < 0).mean(), mean_adj_vs_same_date_unexposed=d[f"adj_0_{h}"].mean(),
                         t_adj_clustered_by_week=(lambda g: g.mean() / (g.std() / np.sqrt(len(g))))(d.groupby(d.start.dt.to_period("W"))[f"adj_0_{h}"].mean()),
                         n_weeks=d.start.dt.to_period("W").nunique(), placebo_mean=pl.mean(), p_two_sided=np.mean(np.abs(pl - pl.mean()) >= abs(v.mean() - pl.mean()))))
summ = pd.DataFrame(summ); summ.to_csv(TAB + "rain_episode_event_study.csv", index=False); print(summ.round(4).to_string())

# 4 ---- monthly panel ---------------------------------------------------------------------------
beta = {}
for f in R.columns:
    d = pd.concat([R[f], MKT], axis=1).dropna()
    beta[f] = np.cov(d.iloc[:, 0], d.iloc[:, 1])[0, 1] / d.iloc[:, 1].var() if len(d) > 200 else np.nan
AR = R - np.outer(MKT.values, pd.Series(beta).reindex(R.columns).values)
mar = AR.groupby(AR.index.to_period("M")).sum(min_count=10).stack().rename("abret").reset_index()
mar.columns = ["month", "firm", "abret"]
fe["month"] = fe.start.dt.to_period("M")
hz = fe.groupby(["nse_symbol", "month"]).agg(haz_share=("share", "sum"), haz_sev=("sev", "max")).reset_index().rename(columns={"nse_symbol": "firm"})
pn = mar.merge(hz, how="left", on=["firm", "month"]).fillna({"haz_share": 0, "haz_sev": 0})
pn["haz_share"] = pn.haz_share.clip(upper=1); pn = pn[pn.month >= "2020-11"].dropna(subset=["abret"]).reset_index(drop=True)
pn = pn.sort_values(["firm", "month"]); pn["haz_l1"] = pn.groupby("firm").haz_share.shift(1).fillna(0)
pn["m"] = pn.month.astype(str); pn["vol"] = 0.0
m1 = smf.ols("abret ~ haz_share + haz_l1 + C(firm) + C(m)", pn).fit(cov_type="cluster", cov_kwds={"groups": pn.m.astype("category").cat.codes})
pt = pd.DataFrame({"coef": m1.params[["haz_share", "haz_l1"]], "se": m1.bse[["haz_share", "haz_l1"]], "p": m1.pvalues[["haz_share", "haz_l1"]]})
pt["n_obs"] = int(m1.nobs); pt["firm_months_with_hazard"] = int((pn.haz_share > 0).sum())
pt.to_csv(TAB + "rain_monthly_panel.csv"); print(pt.round(4))
pn.drop(columns=["m", "vol"]).to_csv(TAB + "firm_month_hazard_panel.csv", index=False)

# ---- figures ----------------------------------------------------------------------------------
fig, axs = plt.subplots(1, 4, figsize=(15, 3.4))
for ax, (d, a, b, t) in zip(axs, [("Vadodara", "2024-06-01", "2024-10-15", "Vadodara, 2024 monsoon"), ("Bharuch", "2023-06-01", "2023-10-15", "Bharuch, 2023 monsoon"),
                                  ("Solan", "2023-06-01", "2023-09-15", "Solan (Baddi belt), 2023"), ("Chennai", "2023-10-15", "2023-12-31", "Chennai, NE monsoon 2023")]):
    x = rain[(rain.dist_name == d) & rain.date.between(a, b)]
    ax.plot(x.date, x.r3, color=BLUE, lw=1.6)
    ax.axhline(x.rl5.iloc[0], color=ORANGE, lw=1.2, ls="--"); ax.text(x.date.iloc[2], x.rl5.iloc[0], " 5-yr level", va="bottom", color=MUTED, fontsize=7.5)
    ax.set_title(t, loc="left"); ax.tick_params(axis="x", labelrotation=30, labelsize=7.5)
axs[0].set_ylabel("3-day rainfall, mm")
fig.suptitle("Do the named flood events show up as rainfall extremes at the plant districts? (NASA POWER, ~50 km grid)", x=0.01, ha="left", fontweight="bold")
fig.tight_layout(); fig.savefig(FIG + "02_rain_validation.png", dpi=200)

fig, ax = plt.subplots(figsize=(7.5, 4.2))
d = es[es.share >= .02]
ax.axhline(0, color="#c9c8c2", lw=.8)
ax.scatter(d.share * 100, d.adj_0_10 * 100, s=14 + 10 * d.sev.clip(upper=4), color=BLUE, alpha=.55, edgecolor=SURF, linewidth=.6)
bins = pd.cut(d.share, [0.02, .05, .1, .25, .5, 1.01]); g = d.groupby(bins, observed=True).agg(x=("share", "mean"), y=("adj_0_10", "mean"))
ax.plot(g.x * 100, g.y * 100, color=ORANGE, marker="o", ms=6, label="Bin mean")
ax.set_xlabel("Share of firm's plant assets in districts with extreme rain, %"); ax.set_ylabel("CAR [0,+10] minus same-date unexposed firms, pp"); ax.set_ylim(-40, 40)
ax.set_title("Every firm × extreme-rain episode, 2020–2025: stock reaction vs assets exposed", loc="left"); ax.legend()
fig.tight_layout(); fig.savefig(FIG + "03_rain_dose_response.png", dpi=200)
