"""Uses the newly fetched data:
 A. river-discharge flood episodes (GloFAS) - validate named events, event study on firm-episodes
 B. quarterly fundamentals panel (13 quarters, Sep-2023 ->): do sales growth / margins react to
    assets hit (named events, rain episodes, river episodes)?  firm + quarter fixed effects
 C. rupee value of the named-event stock moves (market cap = current shares x adjusted price)
 D. Delhi PM2.5 (modelled) around each GRAP-IV order"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from es_lib import *
import statsmodels.formula.api as smf
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
co = companies().set_index("nse_symbol"); co["sector"] = co.primary_industry.map(sector)
p = plants(); tot = p.groupby("nse_symbol").project_cost_cr.sum(); ex = exposure()

# A ---- river ----------------------------------------------------------------------------------
rv = pd.read_csv(EXT + "river_daily.csv.gz", parse_dates=["date"]).dropna(subset=["q"]).sort_values(["dist_name", "date"])
rv["q3"] = rv.groupby("dist_name").q.transform(lambda s: s.rolling(3, min_periods=1).mean())
b = rv[rv.date.dt.year <= 2019]; amax = b.groupby(["dist_name", b.date.dt.year]).q3.max().unstack()
rv = rv.merge(pd.DataFrame({"rl5": amax.quantile(.8, axis=1), "rl2": amax.quantile(.5, axis=1)}), left_on="dist_name", right_index=True)
rv["sev"] = rv.q3 / rv.rl5
val = []
for ev, dists, a, e_ in [("Gujarat flood 2024", ["Vadodara", "Bharuch", "Anand", "Kheda"], "2024-08-24", "2024-09-05"), ("Gujarat flood 2023", ["Bharuch", "Vadodara"], "2023-09-15", "2023-09-24"),
                         ("Himachal flood 2023", ["Solan", "Una", "Sirmaur", "Kullu"], "2023-07-07", "2023-07-20"), ("Chennai Michaung 2023", ["Chennai", "Kancheepuram", "Thiruvallur"], "2023-12-02", "2023-12-12")]:
    for d in dists:
        x = rv[(rv.dist_name == d) & rv.date.between(a, e_)]
        if len(x) == 0: continue
        pk = x.loc[x.q3.idxmax()]
        val.append(dict(event=ev, district=d, peak_date=pk.date.date(), peak_flow_m3s=pk.q3, level_2yr=pk.rl2, level_5yr=pk.rl5, ratio_to_5yr=pk.sev,
                        baseline_years_exceeding=f"{(amax.loc[d] >= pk.q3).sum()}/20", river_cell=f"{pk.cell_lat:.2f},{pk.cell_lon:.2f}"))
val = pd.DataFrame(val); val.to_csv(TAB + "river_validation_named_events.csv", index=False); print(val.round(2).to_string())
r = rv[(rv.date >= "2020-11-01") & (rv.sev >= 1)].copy()
r["ep"] = (r.groupby("dist_name").date.diff().dt.days.fillna(999) > 30).groupby(r.dist_name).cumsum()
ep = r.groupby(["dist_name", "ep"]).agg(start=("date", "min"), peak_sev=("sev", "max")).reset_index(); ep.to_csv(TAB + "river_extreme_episodes_by_district.csv", index=False)
pe = p[p.nse_symbol.isin(R.columns)].merge(ep, on="dist_name"); pe["wk"] = pe.start.dt.to_period("W")
fr = pe.groupby(["nse_symbol", "wk"]).agg(start=("start", "min"), hit=("project_cost_cr", "sum"), sev=("peak_sev", "max"), districts=("dist_name", lambda s: "|".join(sorted(set(s))[:4]))).reset_index()
fr["share"] = fr.hit / fr.nse_symbol.map(tot); fr = fr.drop(columns="wk"); fr.to_csv(TAB + "river_firm_episodes.csv", index=False)
print("river district-episodes", len(ep), "in", ep.dist_name.nunique(), "of", rv.dist_name.nunique(), "districts; firm-episodes", len(fr), ">=10%:", (fr.share >= .1).sum())
rain_fe = pd.read_csv(TAB + "rain_firm_episodes.csv", parse_dates=["start"])
rows = []
for _, x in fr[fr.share >= .05].iterrows():
    ar = ar_matrix(t0_of(x.start), pre=1, post=25)
    if ar is None or x.nse_symbol not in ar: continue
    hit = set(fr.nse_symbol[(fr.start - x.start).abs().dt.days <= 10]) | set(rain_fe.nse_symbol[(rain_fe.start - x.start).abs().dt.days <= 10])
    un = [c for c in ar.columns if c not in hit]
    rows.append({**x.to_dict(), **{f"adj_0_{h}": ar[x.nse_symbol].loc[0:h].sum() - ar[un].loc[0:h].sum().mean() for h in (5, 10, 20)}})
es = pd.DataFrame(rows); es["wk"] = es.start.dt.to_period("W").astype(str); es.to_csv(TAB + "river_firm_episode_cars.csv", index=False)
out = []
for lab, m in [("share 5-25%", es.share < .25), ("share >=25%", es.share >= .25)]:
    for h in (5, 10, 20):
        d = es[m]; g = d.groupby("wk")[f"adj_0_{h}"].mean()
        out.append(dict(bucket=lab, window=f"[0,{h}]", n=len(d), firms=d.nse_symbol.nunique(), weeks=len(g), mean_adj_car=d[f"adj_0_{h}"].mean(), frac_neg=(d[f"adj_0_{h}"] < 0).mean(), t_week_clustered=g.mean() / (g.std() / np.sqrt(len(g)))))
out = pd.DataFrame(out); out.to_csv(TAB + "river_episode_event_study.csv", index=False); print(out.round(4).to_string())

# B ---- quarterly fundamentals -------------------------------------------------------------------
q = pd.read_csv(EXT + "fin_quarterly.csv"); q["period"] = q.period.str.replace(r"\s*\(S\)", "", regex=True)
q["pe"] = pd.to_datetime(q.period, format="%b %Y") + pd.offsets.MonthEnd(0)
w = q[q.item.isin(["Sales", "OPM %", "YoY Sales growth", "Operating Profit", "Net Profit"])].pivot_table(index=["firm", "pe"], columns="item", values="value", aggfunc="first").reset_index()
w.columns = ["firm", "pe", "np", "opm", "op", "sales", "yoy"]; w = w[(w.pe >= "2023-09-30") & (w.pe <= "2025-12-31")].sort_values(["firm", "pe"])
w["qtr"] = w.pe.dt.to_period("Q"); w["opm"] = w.opm.clip(-100, 100); w["yoy"] = w.yoy.clip(-100, 150)
w["d_opm_yoy"] = w.opm - w.groupby("firm").opm.shift(4); w["sector"] = w.firm.map(co.sector)
def qshare(fe):
    fe = fe.copy(); fe["qtr"] = fe.start.dt.to_period("Q")
    return fe.groupby(["nse_symbol", "qtr"]).share.sum().clip(upper=1)
w = w.join(qshare(rain_fe).rename("rain"), on=["firm", "qtr"]).join(qshare(fr).rename("river"), on=["firm", "qtr"]).fillna({"rain": 0, "river": 0})
NAMED = {"CHE": ["2023Q4"], "GJ": ["2024Q3", "2023Q3"], "NCR": ["2024Q4"], "HP": ["2023Q3"]}
w["named"] = 0.0
for z, qs in NAMED.items():
    s = ex[ex.zone == z].set_index("nse_symbol").share_cost
    m = w.qtr.astype(str).isin(qs); w.loc[m, "named"] += w.loc[m, "firm"].map(s).fillna(0)
for v in ["rain", "river", "named"]: w[v + "_l1"] = w.groupby("firm")[v].shift(1).fillna(0)
w["qs"] = w.qtr.astype(str); w.to_csv(TAB + "firm_quarter_panel.csv", index=False)
res = []
for dep in ["yoy", "opm", "d_opm_yoy"]:
    d = w.dropna(subset=[dep]).reset_index(drop=True)
    for fe_lab, fes in [("firm + quarter FE", "C(firm) + C(qs)")]:
        if dep == "yoy": fes = fes.replace("C(firm) + ", "") if False else fes
        m = smf.ols(f"{dep} ~ named + named_l1 + rain + rain_l1 + river + river_l1 + {fes}", d).fit(cov_type="cluster", cov_kwds={"groups": d.firm.astype("category").cat.codes})
        for v in ["named", "named_l1", "rain", "rain_l1", "river", "river_l1"]:
            res.append(dict(outcome={"yoy": "YoY sales growth, pp", "opm": "Operating margin, pp", "d_opm_yoy": "Change in margin vs year-ago quarter, pp"}[dep], spec=fe_lab,
                            regressor=v, coef_per_100pct_assets=m.params[v], se=m.bse[v], p=m.pvalues[v], n=int(m.nobs), treated_obs=int((d[v] > 0).sum())))
res = pd.DataFrame(res); res.to_csv(TAB + "fundamentals_panel.csv", index=False); print(res.round(3).to_string())
# named events, simple before/after table
ne = []
for z, qs, lab in [("CHE", "2023Q4", "Chennai Michaung, Oct-Dec 2023"), ("GJ", "2024Q3", "Gujarat flood, Jul-Sep 2024"), ("NCR", "2024Q4", "GRAP-IV, Oct-Dec 2024")]:
    s = ex[ex.zone == z].set_index("nse_symbol").share_cost; d = w[w.qs == qs].copy(); d["x"] = d.firm.map(s).fillna(0)
    nx = w[w.qtr == (pd.Period(qs) + 1)].set_index("firm"); d = d.set_index("firm")
    for g, m in [("exposed (>=25% assets)", d.x >= .25), ("unexposed (0%)", d.x == 0)]:
        ne.append(dict(event=lab, group=g, n=int(m.sum()), yoy_sales_growth_event_qtr=d.yoy[m].median(), yoy_sales_growth_next_qtr=nx.yoy.reindex(d.index[m]).median(),
                       margin_event_qtr=d.opm[m].median(), margin_change_vs_year_ago=d.d_opm_yoy[m].median() if d.d_opm_yoy[m].notna().any() else np.nan, margin_next_qtr=nx.opm.reindex(d.index[m]).median()))
ne = pd.DataFrame(ne); ne.to_csv(TAB + "fundamentals_named_events.csv", index=False); print(ne.round(1).to_string())

# C ---- rupees -----------------------------------------------------------------------------------
mc = pd.read_csv(EXT + "market_cap.csv").set_index("firm"); px = stock().pivot(index="date", columns="asset_id", values="close").reindex(R.index).ffill()
cars = pd.read_csv(TAB + "event_study_firm_cars.csv"); rp = []
for (eid, col, lab) in [("E_CHE_FLOOD_2023", "car_0_5", "Chennai Michaung, days 0 to +5"), ("E_NCR_GRAP4_2024", "car_m1_1", "GRAP-IV 18 Nov 2024, days -1 to +1"), ("E_GJ_FLOOD_2024", "car_0_20", "Gujarat flood 2024, days 0 to +20")]:
    d = cars[cars.event_id == eid].set_index("nse_symbol"); t0 = t0_of(EVENTS.set_index("event_id").start[eid])
    d["mcap_cr"] = mc.shares_cr.reindex(d.index) * px.iloc[t0 - 1].reindex(d.index)
    d["rel"] = d[col] - d[col][d.share_cost == 0].mean(); d["loss_cr"] = d.rel * d.mcap_cr
    h = d[d.share_cost >= .25]
    for nm, hh in [("all exposed firms", h)] + ([("excluding IGL (fell on a gas-allocation cut)", h.drop("IGL"))] if eid == "E_NCR_GRAP4_2024" else []) + ([("excluding Hindustan Unilever", h.drop("HINDUNILVR"))] if eid == "E_CHE_FLOOD_2023" else []):
        rp.append(dict(event=lab, set=nm, n=len(hh), market_cap_before_cr=hh.mcap_cr.sum(), value_change_vs_unexposed_cr=hh.loss_cr.sum(), pct_of_mcap=100 * hh.loss_cr.sum() / hh.mcap_cr.sum(),
                       largest_losers="; ".join(f"{k} {v:,.0f}" for k, v in hh.loss_cr.nsmallest(3).items())))
    d[["share_cost", "sector", col, "rel", "mcap_cr", "loss_cr"]].sort_values("loss_cr").to_csv(TAB + f"rupee_loss_{eid}.csv")
rp = pd.DataFrame(rp); rp.to_csv(TAB + "rupee_losses_named_events.csv", index=False); print(rp.round(1).to_string())

# D ---- Delhi PM2.5 --------------------------------------------------------------------------------
aq = pd.read_csv(EXT + "pm25_daily_cams.csv", parse_dates=["date"]); dl = aq[aq.city == "New Delhi"].set_index("date").pm2_5
aqt = []
for lab, a, e_ in [("GRAP-IV 2022 (3-6 Nov)", "2022-11-03", "2022-11-06"), ("GRAP-IV 2023 (5-18 Nov)", "2023-11-05", "2023-11-18"), ("GRAP-IV 2024 1st (18 Nov-5 Dec)", "2024-11-18", "2024-12-05"), ("GRAP-IV 2024 2nd (16-24 Dec)", "2024-12-16", "2024-12-24")]:
    aqt.append(dict(episode=lab, days=len(dl[a:e_]), mean_pm25=dl[a:e_].mean(), peak_pm25=dl[a:e_].max(), mean_prior_30d=dl[pd.Timestamp(a) - pd.Timedelta(days=30):pd.Timestamp(a) - pd.Timedelta(days=1)].mean(),
                    mumbai_same_days=aq[aq.city == "Mumbai"].set_index("date").pm2_5[a:e_].mean(), chennai_same_days=aq[aq.city == "Chennai"].set_index("date").pm2_5[a:e_].mean()))
aqt = pd.DataFrame(aqt); aqt.to_csv(TAB + "delhi_pm25_grap_episodes.csv", index=False); print(aqt.round(0).to_string())

# ---- figures -------------------------------------------------------------------------------------
fig, axs = plt.subplots(1, 3, figsize=(14, 3.6))
for ax, (d, a, e_, t) in zip(axs, [("Bharuch", "2023-08-15", "2023-10-15", "Narmada near Bharuch, Sep 2023"), ("Vadodara", "2024-08-01", "2024-09-30", "River near Vadodara, Aug 2024"), ("Chennai", "2023-11-15", "2023-12-31", "River near Chennai, Dec 2023")]):
    x = rv[(rv.dist_name == d) & rv.date.between(a, e_)]
    if len(x) == 0: continue
    ax.plot(x.date, x.q3, color=BLUE); ax.axhline(x.rl5.iloc[0], color=ORANGE, ls="--", lw=1.2); ax.text(x.date.iloc[1], x.rl5.iloc[0], " 5-yr level", va="bottom", fontsize=7.5, color=MUTED)
    ax.set_title(t, loc="left"); ax.tick_params(axis="x", labelrotation=30, labelsize=7.5)
axs[0].set_ylabel("River flow, m³/s (3-day mean)")
fig.suptitle("River discharge catches the floods that local rainfall misses (GloFAS reanalysis)", x=0.01, ha="left", fontweight="bold"); fig.tight_layout(); fig.savefig(FIG + "05_river_validation.png", dpi=200)
