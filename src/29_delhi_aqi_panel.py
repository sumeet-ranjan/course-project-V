"""Step 3: Delhi air quality as a continuous treatment, 25 Oct - 31 Dec of 2022, 2023, 2024.

Daily abnormal returns (market model vs NIFTY 500, estimated on the 250 trading days ending 30 Sep
of each year). Long-short series each trading day:
  NCR builders  = real-estate/construction firms with >= 25% of plant cost in NCR (NBCC, Anant Raj,
                  Unitech, Parsvnath, DLF) minus firms with no NCR plants;
  all NCR firms = every firm with >= 25% of plant cost in NCR minus firms with no NCR plants
                  (IGL is dropped on 18-19 Nov 2024, the gas-allocation confound in README 5.1/5.6).
Treatments (all known before the market opens on day t):
  * the Delhi daily AQI of the previous calendar day (4 pm bulletin; research/proxy/delhi_aqi_daily.csv);
  * the highest GRAP stage in force, built from the 21 orders read from the government press
    releases (research/proxy/official_hazard_records.csv). An order with a stated effective time
    (8 am) counts from that day; an "immediate effect" order, all posted in the evening or at a
    weekend, counts from the next calendar day.
Regressions pool the three winters with winter fixed effects; Newey-West standard errors (5 lags).
Outputs: outputs/tables/delhi_aqi_panel.csv, delhi_aqi_daily_longshort.csv, figs/14_delhi_aqi.png
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from es_lib import *
import statsmodels.formula.api as smf
co = companies().set_index("nse_symbol"); co["sector"] = co.primary_industry.map(sector)
ncr = exposure().query("zone == 'NCR'").set_index("nse_symbol").share_cost.reindex(R.columns).fillna(0)
BUILD = [c for c in R.columns if ncr[c] >= .25 and co.sector.get(c) == "Realty/Construction"]
NCRALL = [c for c in R.columns if ncr[c] >= .25]; NONE = [c for c in R.columns if ncr[c] == 0]

# ---- GRAP stage in force, daily
o = pd.read_csv(ROOT + "/research/proxy/official_hazard_records.csv", dtype=str).fillna("")
o = o[(o.task == "A_grap_orders") & (o.item == "order")].copy()
o["eff"] = [pd.Timestamp(t.split("on ")[1][:10]) if "08:00 on" in t else pd.Timestamp(d) + pd.Timedelta(days=1) for d, t in zip(o.date, o.time)]
cal = pd.date_range("2022-10-01", "2025-01-31")
s3 = pd.Series(0, index=cal); s4 = pd.Series(0, index=cal)
for r in o.sort_values("eff").itertuples():
    on = 1 if r.action == "invoke" else 0
    if "III" in r.stage_or_station and "IV" not in r.stage_or_station.replace("III", ""): s3.loc[r.eff:] = on
    if "IV" in r.stage_or_station.replace("III", "") or r.stage_or_station.endswith("IV"):
        s4.loc[r.eff:] = on
    if "Stage IV and Stage III" in r.stage_or_station: s3.loc[r.eff:] = on; s4.loc[r.eff:] = on
stage = pd.Series(np.where(s4 == 1, 4, np.where(s3 == 1, 3, 2)), index=cal)

# ---- AQI, previous calendar day
aq = pd.read_csv(ROOT + "/research/proxy/delhi_aqi_daily.csv", parse_dates=["date"]).set_index("date").aqi.astype(float)
rows = []
for yr in (2022, 2023, 2024):
    days = DATES[(DATES >= f"{yr}-10-25") & (DATES <= f"{yr}-12-31")]
    t_first = t0_of(days[0]); est_end = t0_of(f"{yr}-09-30")
    t0 = est_end + 30                     # estimation window [-250, -30] then ends on 30 Sep: same window for the whole winter
    ar = ar_matrix(t0, pre=t0 - t_first, post=t0_of(days[-1]) - t0)
    if ar is None: continue
    ar.index = DATES[t_first: t_first + len(ar)]
    for d in days:
        if d not in ar.index: continue
        a = ar.loc[d]; b = [c for c in BUILD if c in a.index]; n_ = [c for c in NCRALL if c in a.index and not (c == "IGL" and str(d.date()) in ("2024-11-18", "2024-11-19"))]
        prev = d - pd.Timedelta(days=1)
        nn = [c for c in NONE if c in a.index]
        rows.append(dict(date=d, winter=yr, ls_builders=a[b].mean() - a[nn].mean(), ls_ncr=a[n_].mean() - a[nn].mean(),
                         aqi_prev=aq.get(prev, np.nan), aqi_change=aq.get(prev, np.nan) - aq.get(prev - pd.Timedelta(days=1), np.nan),
                         stage=stage.get(d, 2), stage_prev_trading=np.nan))
p = pd.DataFrame(rows).sort_values("date")
p["stage_prev_trading"] = p.stage.shift(1); p.loc[p.winter != p.winter.shift(1), "stage_prev_trading"] = np.nan
p["s3"] = (p.stage == 3).astype(int); p["s4"] = (p.stage == 4).astype(int); p["s34"] = (p.stage >= 3).astype(int)
p["tighten"] = (p.stage > p.stage_prev_trading).astype(int); p["loosen"] = (p.stage < p.stage_prev_trading).astype(int)
p["aqi100"] = p.aqi_prev / 100; p["daqi100"] = p.aqi_change / 100
p.round(5).to_csv(TAB + "delhi_aqi_daily_longshort.csv", index=False)
res = []
for dep, lab in (("ls_builders", "NCR builders minus no-NCR firms"), ("ls_ncr", "all NCR firms minus no-NCR firms")):
    for f, nm in (("aqi100", "AQI previous day, per 100"), ("daqi100", "AQI change previous day, per 100"), ("s3 + s4", "Stage III / IV in force"),
                  ("tighten + loosen", "first day of a tighter / looser stage")):
        x = p.dropna(subset=[dep] + [v.strip() for v in f.split("+")])
        m = smf.ols(f"{dep} ~ {f} + C(winter)", x).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
        for v in [v.strip() for v in f.split("+")]:
            res.append(dict(portfolio=lab, treatment=nm, regressor=v, coef_pct_per_day=100 * m.params[v], se=100 * m.bse[v], p=m.pvalues[v], n_days=int(m.nobs)))
res = pd.DataFrame(res); res.round(4).to_csv(TAB + "delhi_aqi_panel.csv", index=False)
pd.set_option("display.width", 250)
print("builders:", BUILD, "| all NCR:", NCRALL, "| no-NCR firms:", len(NONE))
print("days by stage in force:", p.stage.value_counts().sort_index().to_dict(), "| AQI coverage:", p.aqi_prev.notna().sum(), "of", len(p))
print(res.round(3).to_string(index=False))
cum = p.groupby(["winter", "stage"]).agg(days=("ls_builders", "size"), builders_cum_pct=("ls_builders", lambda v: 100 * v.sum()), builders_mean_bp=("ls_builders", lambda v: 1e4 * v.mean()))
print("\nlong-short (builders) by winter and stage in force:"); print(cum.round(2).to_string())

fig, axs = plt.subplots(2, 3, figsize=(15, 6.4), sharex="col", gridspec_kw={"height_ratios": [1.6, 1]})
def shade(ax, yr):
    st = stage.loc[f"{yr}-10-25":f"{yr}-12-31"]
    run = (st != st.shift()).cumsum()
    for _, g in st.groupby(run):
        if g.iloc[0] >= 3:
            ax.axvspan(g.index[0], g.index[-1] + pd.Timedelta(days=1), color="#f3d3c4" if g.iloc[0] == 3 else "#e8a68a", lw=0, zorder=0)
for j, yr in enumerate((2022, 2023, 2024)):
    x = p[p.winter == yr]; a1, a2 = axs[0, j], axs[1, j]
    for ax in (a1, a2): shade(ax, yr)
    a1.plot(x.date, 100 * x.ls_builders.cumsum(), color=ORANGE, lw=1.8); a1.axhline(0, color="#c9c8c2", lw=.8)
    a1.set_title(f"Winter {yr}", loc="left")
    aqd = aq.loc[f"{yr}-10-25":f"{yr}-12-31"]; a2.plot(aqd.index, aqd.values, color=BLUE, lw=1.4)
    a2.tick_params(axis="x", labelrotation=30, labelsize=7.5)
axs[0, 0].set_ylabel("NCR builders minus no-NCR firms,\ncumulative abnormal return, %"); axs[1, 0].set_ylabel("Delhi daily AQI")
axs[0, 2].text(0.99, 0.03, "light shading = Stage III in force\ndark shading = Stage IV in force", transform=axs[0, 2].transAxes, ha="right", va="bottom", fontsize=7.5, color=MUTED)
fig.suptitle("Delhi air quality, pollution-control stages and NCR builders' stock returns (25 Oct–31 Dec)", x=0.01, ha="left", fontweight="bold")
fig.tight_layout(); fig.savefig(FIG + "14_delhi_aqi.png", dpi=200)

# ---- robustness of the AQI coefficient (builders and all-NCR long-short)
import statsmodels.api as sm
rb = []
pp = p.copy(); pp["trend"] = pp.groupby("winter").cumcount()
for dep in ("ls_builders", "ls_ncr"):
    def coef(f, d, v="aqi100", robust=False):
        x = d.dropna(subset=[dep, v])
        m = (smf.rlm(f"{dep} ~ {f}", x, M=sm.robust.norms.HuberT()).fit() if robust else smf.ols(f"{dep} ~ {f}", x).fit(cov_type="HAC", cov_kwds={"maxlags": 5}))
        return 100 * m.params[v], m.pvalues[v], int(m.nobs)
    for lab, f, d, v, rob in (("base: AQI + winter effects", "aqi100 + C(winter)", pp, "aqi100", False),
                              ("+ within-winter linear trends", "aqi100 + C(winter) + C(winter):trend", pp, "aqi100", False),
                              ("+ Stage III and IV dummies", "aqi100 + s3 + s4 + C(winter)", pp, "aqi100", False),
                              ("Huber robust regression", "aqi100 + C(winter)", pp, "aqi100", True)):
        c, pv, n = coef(f, d, v, rob); rb.append(dict(portfolio=dep, check=lab, coef_pct_per_100aqi=c, p=pv, n=n))
    for sh in (1, 2):                                           # placebo: another winter's AQI on the same calendar day
        q = pp.copy(); mp = {}
        for yr in (2022, 2023, 2024):
            src = 2022 + ((yr - 2022 + sh) % 3)
            for dd in q.date[q.winter == yr]:
                prev = dd - pd.Timedelta(days=1); mp[dd] = aq.get(prev.replace(year=src), np.nan) if not (prev.month == 2 and prev.day == 29) else np.nan
        q["aqi_pl"] = q.date.map(mp) / 100
        c, pv, n = coef("aqi_pl + C(winter)", q, "aqi_pl"); rb.append(dict(portfolio=dep, check=f"placebo: AQI of the winter {sh} year(s) later, same dates", coef_pct_per_100aqi=c, p=pv, n=n))
    for yr in (2022, 2023, 2024):
        c, pv, n = coef("aqi100", pp[pp.winter == yr]); rb.append(dict(portfolio=dep, check=f"winter {yr} alone", coef_pct_per_100aqi=c, p=pv, n=n))
rb = pd.DataFrame(rb); rb.round(4).to_csv(TAB + "delhi_aqi_robustness.csv", index=False)
print("\nrobustness:"); print(rb.round(3).to_string(index=False))
