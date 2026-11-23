"""From exposure to a price: three ways to attach a number to physical climate risk.
 A. Loss-given-event elasticity (lambda): % of equity value lost per unit of asset share hit.
 B. Hazard frequency per firm (2020-25 extreme-rain episodes at its plant districts) ->
    expected annual 'asset-share hit' -> expected annual equity drag, and what it would be worth
    capitalised IF the losses were permanent (they look largely transitory here).
 C. Is geographic concentration / hazard exposure already priced? cross-section of volatility,
    plus trading-volume response and the one fundamentals cross-section the pack allows."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from es_lib import *
import statsmodels.formula.api as smf
co = companies().set_index("nse_symbol"); co["sector"] = co.primary_industry.map(sector)
es = pd.read_csv(TAB + "rain_firm_episode_cars.csv", parse_dates=["start"])
fe = pd.read_csv(TAB + "rain_firm_episodes.csv", parse_dates=["start"])
ep = pd.read_csv(TAB + "rain_extreme_episodes_by_district.csv", parse_dates=["start"])
YRS = (pd.Timestamp("2025-12-31") - pd.Timestamp("2020-11-01")).days / 365.25

# A ---- elasticity ----------------------------------------------------------------------------
es["wk"] = es.start.dt.to_period("W").astype(str); lam = []
for h in (5, 10, 20):
    for dep, nm in [(f"car_0_{h}", "raw CAR"), (f"adj_0_{h}", "CAR minus same-date unexposed")]:
        m = smf.ols(f"{dep} ~ share", es).fit(cov_type="cluster", cov_kwds={"groups": es.wk.astype("category").cat.codes})
        m2 = smf.ols(f"{dep} ~ I(share*sev)", es).fit(cov_type="cluster", cov_kwds={"groups": es.wk.astype("category").cat.codes})
        lam.append(dict(window=f"[0,{h}]", measure=nm, intercept=m.params["Intercept"], lambda_per_100pct_assets=m.params["share"], se=m.bse["share"], p=m.pvalues["share"],
                        lambda_share_x_severity=m2.params.iloc[1], p_sev=m2.pvalues.iloc[1], n=int(m.nobs)))
lam = pd.DataFrame(lam); lam.to_csv(TAB + "pricing_lambda.csv", index=False)
pd.set_option("display.width", 230); pd.set_option("display.max_columns", 30); print(lam.round(4).to_string())
LAM = lam[(lam.window == "[0,10]") & (lam.measure == "CAR minus same-date unexposed")].iloc[0]
lam_tot = LAM.intercept + LAM.lambda_per_100pct_assets       # predicted hit at 100% of assets exposed

# B ---- hazard frequency & expected annual drag ----------------------------------------------
p = plants(); tot = p.groupby("nse_symbol").project_cost_cr.sum()
freq = ep.groupby("dist_name").size() / YRS                      # extreme episodes per year, by district
p["dist_freq"] = p.dist_name.map(freq).fillna(0)
p["w"] = p.project_cost_cr / p.nse_symbol.map(tot)
f = p.groupby("nse_symbol").apply(lambda d: pd.Series({
    "exp_annual_share_hit": (d.w * d.dist_freq).sum(),            # expected asset-share-years hit per year
    "hhi_district": (d.groupby("dist_name").w.sum() ** 2).sum(),  # geographic concentration of assets
    "top_district": d.groupby("dist_name").w.sum().idxmax(), "top_district_share": d.groupby("dist_name").w.sum().max(),
    "n_districts": d.dist_name.nunique()}), include_groups=False)
f["episodes_per_year_ge10pct"] = fe[fe.share >= .10].groupby("nse_symbol").size().reindex(f.index).fillna(0) / YRS
f["exp_annual_equity_drag_pct"] = 100 * f.exp_annual_share_hit * LAM.lambda_per_100pct_assets
# if (and only if) each hit were a permanent value loss: PV of the perpetual drag at r-g = 8%
f["discount_if_permanent_pct"] = f.exp_annual_equity_drag_pct / 0.08
f = f.join(co[["company", "sector", "role"]]); f["has_stock"] = f.index.isin(R.columns)
f.sort_values("exp_annual_share_hit", ascending=False).to_csv(TAB + "pricing_firm_hazard_scorecard.csv")
print(f[f.has_stock].sort_values("exp_annual_share_hit", ascending=False).head(15)[["sector", "top_district", "top_district_share", "hhi_district", "exp_annual_share_hit", "episodes_per_year_ge10pct", "exp_annual_equity_drag_pct", "discount_if_permanent_pct"]].round(3).to_string())
dz = p.groupby("dist_name").agg(plants=("lat", "size"), firms=("nse_symbol", "nunique"), cost=("project_cost_cr", "sum")).join(freq.rename("episodes_per_year")).fillna(0)
dz["cost_share_of_sample"] = dz.cost / dz.cost.sum(); dz.sort_values("cost", ascending=False).to_csv(TAB + "district_asset_hazard_map.csv")
print(dz.sort_values("cost", ascending=False).head(12).round(3).to_string())

# C ---- is it priced? -------------------------------------------------------------------------
beta = {}; ivol = {}; mret = {}
for c in R.columns:
    d = pd.concat([R[c], MKT], axis=1).dropna()
    b = np.cov(d.iloc[:, 0], d.iloc[:, 1])[0, 1] / d.iloc[:, 1].var(); beta[c] = b
    ivol[c] = (d.iloc[:, 0] - b * d.iloc[:, 1]).std() * np.sqrt(250); mret[c] = (d.iloc[:, 0] - b * d.iloc[:, 1]).mean() * 250
x = f[f.has_stock].copy(); x["ivol"] = pd.Series(ivol); x["alpha"] = pd.Series(mret); x["beta"] = pd.Series(beta)
x["lsize"] = np.log(co.total_project_cost_cr.reindex(x.index).clip(lower=1))
cs = []
for dep in ["ivol", "alpha"]:
    m = smf.ols(f"{dep} ~ exp_annual_share_hit + hhi_district + lsize + beta", x).fit(cov_type="HC1")
    for v in ["exp_annual_share_hit", "hhi_district"]:
        cs.append(dict(dependent=dep, regressor=v, coef=m.params[v], se=m.bse[v], p=m.pvalues[v], n=int(m.nobs), r2=m.rsquared))
cs = pd.DataFrame(cs); cs.to_csv(TAB + "pricing_cross_section.csv", index=False); print(cs.round(4).to_string())

# volume response to extreme-rain episodes
V = stock().pivot(index="date", columns="asset_id", values="volume").reindex(R.index)
vr = []
for _, r_ in es[es.share >= .10].iterrows():
    t0 = t0_of(r_.start); v = V[r_.nse_symbol]
    a, b = v.iloc[t0:t0 + 6].mean(), v.iloc[t0 - 60:t0 - 10].mean()
    un = [c for c in V.columns if c not in set(fe.nse_symbol[(fe.start - r_.start).abs().dt.days <= 10])]
    bench = np.log(V[un].iloc[t0:t0 + 6].mean() / V[un].iloc[t0 - 60:t0 - 10].mean()).mean()
    vr.append(dict(firm=r_.nse_symbol, wk=r_.wk, abn_log_vol=np.log(a / b) - bench, abs_car=abs(r_.adj_0_5)))
vr = pd.DataFrame(vr).replace([np.inf, -np.inf], np.nan).dropna(); g = vr.groupby("wk").abn_log_vol.mean()
print("abnormal log volume [0,5], share>=10%:", round(vr.abn_log_vol.mean(), 4), "t(week-clustered)=", round(g.mean() / (g.std() / np.sqrt(len(g))), 2), "n=", len(vr))
pd.DataFrame([dict(mean_abn_log_volume=vr.abn_log_vol.mean(), t_week_clustered=g.mean() / (g.std() / np.sqrt(len(g))), n=len(vr))]).to_csv(TAB + "pricing_volume_response.csv", index=False)

# fundamentals: the pack has ONE cross-section (quarter ending Dec-2024) -> exposure to 2024 H2 hazards
fin = pd.read_csv(D + "financials_annual.csv").query("fund_period=='2025Q3'").set_index("nse_symbol")
h2 = fe[(fe.start >= "2024-07-01") & (fe.start <= "2024-12-31")].groupby("nse_symbol").share.sum().clip(upper=1)
ex = exposure(); ncr = ex[ex.zone == "NCR"].set_index("nse_symbol").share_cost
y = fin.join(h2.rename("rain_share_h2_2024")).join(ncr.rename("ncr_share")).fillna({"rain_share_h2_2024": 0, "ncr_share": 0})
y = y[(y.f_g_log_sales.abs() < 1) & (y.f_ebitda_margin.abs() < 0.9)]
fr = []
for dep in ["f_g_log_sales", "f_ebitda_margin"]:
    m = smf.ols(f"{dep} ~ rain_share_h2_2024 + ncr_share", y).fit(cov_type="HC1")
    for v in ["rain_share_h2_2024", "ncr_share"]: fr.append(dict(dependent=dep, regressor=v, coef=m.params[v], se=m.bse[v], p=m.pvalues[v], n=int(m.nobs)))
fr = pd.DataFrame(fr); fr.to_csv(TAB + "fundamentals_cross_section.csv", index=False); print(fr.round(4).to_string())

# ---- figure: firm hazard scorecard ------------------------------------------------------------
t = f[f.has_stock].sort_values("exp_annual_share_hit").tail(20)
fig, ax = plt.subplots(figsize=(8, 5.6))
ax.barh(t.index, t.exp_annual_share_hit * 100, color=BLUE, height=.62)
for i, (k, v) in enumerate(t.iterrows()):
    ax.text(v.exp_annual_share_hit * 100 + 1, i, f"{v.top_district} ({v.top_district_share:.0%})", va="center", fontsize=7.5, color=MUTED)
ax.set_xlabel("Expected % of plant assets hit by an extreme-rain episode per year (2020–25 frequency)"); ax.grid(axis="y", visible=False)
ax.set_title("Physical-hazard scorecard: which firms' assets sit where extremes keep happening\n(label = largest asset district and its share of firm assets)", loc="left")
fig.tight_layout(); fig.savefig(FIG + "04_firm_hazard_scorecard.png", dpi=200)
