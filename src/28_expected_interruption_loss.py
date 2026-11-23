"""Step 5: expected annual interruption loss per firm, and the firm risk card (the deliverable).

Expected annual loss (EAL) from plant outages, per firm:
    EAL = sum over plants [ plant cost share x extreme-rain episodes per year at the plant's district
                            x P(site goes dark | its district has an extreme episode) x days dark ]
          / 365 x annual operating profit
  * episodes per year: Nov 2020 - Dec 2025 rate from the official IMD rainfall grid (31_imd_hazard.py;
    NASA POWER if IMD is absent), and a design rate of 0.2 a year (the 5-year return level, by
    construction of the threshold) as a steadier alternative;
  * P(dark | hit) and days dark: from the night-light episode panel (25_ntl_episodes.py: share of
    observed hit plants below 60% of normal, net of the false-alarm rate on control plants; days
    from the episode start until light is back above 80%, cloudy nights counted as dark);
  * operating profit: latest full financial year (screener.in, external/fin_annual.csv).
Three cases: central (net P(dark), median days), high (gross P(dark), 75th-percentile days) and
an upper bound (every episode darkens every plant in the district for 14 days). No catch-up of
output is assumed in any case, so all three overstate the cost of a short stoppage.
Compared with the share-price route (equity elasticity x exposure, 06_pricing.py), which Round 3
showed does not follow physical damage.
Outputs: outputs/tables/pricing_expected_interruption_loss.csv, deliverable_firm_risk_card.csv,
         figs/16_interruption_vs_equity.png
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from es_lib import *
P = plants(); P["w"] = P.project_cost_cr / P.groupby("nse_symbol").project_cost_cr.transform("sum").replace(0, np.nan)
co = companies().set_index("nse_symbol"); co["sector"] = co.primary_industry.map(sector)
# ---- hazard rate per district
src = "IMD" if os.path.exists(TAB + "imd_extreme_episodes_by_district.csv") else "NASA POWER"
ep = pd.read_csv(TAB + ("imd_extreme_episodes_by_district.csv" if src == "IMD" else "rain_extreme_episodes_by_district.csv"), parse_dates=["start"])
ep = ep[(ep.start >= "2020-11-01") & (ep.start <= "2025-12-31")]
YRS = (pd.Timestamp("2025-12-31") - pd.Timestamp("2020-11-01")).days / 365.25
rate = ep.groupby("dist_name").size() / YRS
P["rate"] = P.dist_name.map(rate).fillna(0.0); P["rate_design"] = 0.2
# ---- outage probability and duration from the night-light panels
W = pd.read_csv(TAB + "ntl_episode_summary.csv"); hp = pd.read_csv(TAB + "ntl_episode_plants.csv")
obs = hp[hp.observed == True]                                                   # noqa: E712
p_gross = obs.dark.mean(); fa = W.control_false_alarm.mean()
p_net = max(0.0, p_gross - fa)
days = obs.loc[obs.dark == 1, "night_back_08"].dropna()
d_med, d_p75 = (days.median(), days.quantile(.75)) if len(days) >= 5 else (7.0, 13.0)
d_med, d_p75 = max(d_med, 1.0), max(d_p75, 1.0)
par = dict(rain_source=src, years=round(YRS, 2), p_dark_gross=p_gross, control_false_alarm=fa, p_dark_net=p_net, days_dark_median=d_med, days_dark_p75=d_p75,
           dark_plants_with_recovery_seen=len(days), observed_hit_plants=len(obs))
print("parameters:", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in par.items()})
# ---- operating profit (latest full year) and market cap
fa_ = pd.read_csv(EXT + "fin_annual.csv"); fa_ = fa_[(fa_.statement == "profit-loss") & (fa_["item"] == "Operating Profit")]
fa_ = fa_[fa_.period.str.match(r"^Mar 20\d\d$")]
fa_["yr"] = fa_.period.str[-4:].astype(int); op = fa_.sort_values("yr").groupby("firm").last()
mc = pd.read_csv(EXT + "market_cap.csv").set_index("firm")
# ---- EAL per firm
def eal(d, rcol, pdk, dd):
    return (d.w.fillna(0) * d[rcol] * pdk * dd / 365).sum()
rows = []
for f, d in P.groupby("nse_symbol"):
    opf = op.value.get(f, np.nan); yr = op.yr.get(f, np.nan)
    rows.append(dict(nse_symbol=f, company=co.company.get(f), sector=co.sector.get(f), traded=f in R.columns, op_profit_cr=opf, op_year=yr,
                     market_cap_cr=mc.market_cap_cr.get(f, np.nan), exposure_per_year=(d.w.fillna(0) * d.rate).sum(),
                     frac_year_lost_central=eal(d, "rate", p_net, d_med), frac_year_lost_high=eal(d, "rate", p_gross, d_p75),
                     frac_year_lost_upper=eal(d, "rate", 1.0, 14.0), frac_year_lost_design=eal(d, "rate_design", p_net, d_med)))
E = pd.DataFrame(rows)
for c in ("central", "high", "upper", "design"):
    E[f"eal_{c}_cr"] = E[f"frac_year_lost_{c}"] * E.op_profit_cr.clip(lower=0)
    E[f"eal_{c}_pct_mcap"] = 100 * E[f"eal_{c}_cr"] / E.market_cap_cr
sc = pd.read_csv(TAB + "pricing_firm_hazard_scorecard.csv").set_index("nse_symbol")
E["equity_route_drag_pct_mcap"] = -E.nse_symbol.map(sc.exp_annual_equity_drag_pct)       # positive = loss, from the share-price elasticity (not significant)
E["equity_route_drag_cr"] = E.equity_route_drag_pct_mcap / 100 * E.market_cap_cr
E["equity_over_interruption_upper"] = E.equity_route_drag_cr / E.eal_upper_cr.replace(0, np.nan)
# market-implied cost of outages: price effect per 100% of plant cost dark (25_ntl_episodes.py, 10 days)
# x expected share of plant cost dark per year (exposure x net P(dark)); a mostly temporary markdown
hr = pd.read_csv(TAB + "ntl_episode_horse_race.csv"); hr = hr[(hr["sample"] == "all firm-episodes") & (hr.window == "[0,10]")].iloc[0]
par["b_dark_10d"] = hr.b_dark; par["b_dark_10d_p"] = hr.p_dark
E["market_implied_drag_pct_mcap"] = -100 * hr.b_dark * E.exposure_per_year * p_net
E["market_implied_drag_cr"] = E.market_implied_drag_pct_mcap / 100 * E.market_cap_cr
E.round(5).to_csv(TAB + "pricing_expected_interruption_loss.csv", index=False)
pd.DataFrame([par]).round(4).to_csv(TAB + "pricing_interruption_parameters.csv", index=False)
print("market-implied: b_dark (10 days) =", round(hr.b_dark, 3), "p =", round(hr.p_dark, 4))
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
t = E[E.traded].sort_values("eal_upper_cr", ascending=False)
print(t[["nse_symbol", "sector", "exposure_per_year", "op_profit_cr", "eal_central_cr", "eal_high_cr", "eal_upper_cr", "eal_upper_pct_mcap", "market_implied_drag_cr", "market_implied_drag_pct_mcap", "equity_route_drag_cr"]].head(20).round(3).to_string(index=False))
tt = E[E.traded]
print(f"\n61 traded firms: summed EAL central {tt.eal_central_cr.sum():,.1f} cr, high {tt.eal_high_cr.sum():,.1f} cr, upper {tt.eal_upper_cr.sum():,.1f} cr a year;"
      f" market-implied (dark assets) {tt.market_implied_drag_cr.sum():,.0f} cr; share-price route {tt.equity_route_drag_cr.sum():,.0f} cr a year;"
      f" median firm: EAL upper {tt.eal_upper_pct_mcap.median():.4f}% and market-implied {tt.market_implied_drag_pct_mcap.median():.3f}% of market cap a year")

# ---- risk card: exposure map summary + concentration + interruption bound
ex = exposure(); zs = ex.pivot_table(index="nse_symbol", columns="zone", values="share_cost").add_prefix("share_zone_")
card = E.set_index("nse_symbol")[["company", "sector", "traded", "market_cap_cr", "op_profit_cr", "exposure_per_year", "eal_central_cr", "eal_high_cr", "eal_upper_cr", "eal_upper_pct_mcap", "market_implied_drag_cr", "market_implied_drag_pct_mcap", "equity_route_drag_cr"]]
card = card.join(sc[["top_district", "top_district_share", "hhi_district", "n_districts"]]).join(zs).fillna({c: 0 for c in zs.columns})
oos = TAB + "oos_concentration_vol.csv"
card["note"] = "EAL assumes no catch-up of lost output; plant cost shares are unaudited relative weights; market-implied = dark-asset price effect x expected dark share (mostly temporary); equity_route_drag uses the rainfall-exposure elasticity, which is not significant"
card.round(4).to_csv(TAB + "deliverable_firm_risk_card.csv")
print("\nrisk card written:", len(card), "firms")

# ---- figure: interruption bound vs share-price route, top 20 traded firms by exposure
f = tt[tt.op_profit_cr > 0].sort_values("exposure_per_year", ascending=False).head(20).iloc[::-1]     # loss-making firms have no profit to lose
fig, ax = plt.subplots(figsize=(12.5, 6.4))
y = np.arange(len(f))
ax.hlines(y, f.eal_central_cr.clip(lower=0.01), f.eal_upper_cr.clip(lower=0.01), color="#c9c8c2", lw=3, zorder=1)
ax.scatter(f.eal_central_cr.clip(lower=0.01), y, s=36, color=AQUA, edgecolor=SURF, zorder=3, label="Interruption loss, central")
ax.scatter(f.eal_upper_cr.clip(lower=0.01), y, s=36, color=BLUE, edgecolor=SURF, zorder=3, label="Interruption loss, upper bound")
ax.scatter(f.market_implied_drag_cr.clip(lower=0.01), y, s=44, marker="D", color=ORANGE, edgecolor=SURF, zorder=4, label="Market-implied, from dark-asset price effect (mostly temporary)")
ax.set_yticks(y); ax.set_yticklabels(f.nse_symbol); ax.set_xscale("log")
ax.set_xlabel("Expected annual loss, ₹ crore (log scale)"); ax.grid(axis="y", visible=False)
ax.set_title("Expected annual loss from extreme-rain outages: physical cost vs market markdown\n(20 profitable traded firms with the most plant cost in frequently hit districts)", loc="left")
ax.legend(fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1.0))
fig.text(0.01, 0.01, "Firms with no operating profit (e.g. Parsvnath, Unitech) are left out. Market-implied = 10-day price effect per 100% of plant cost dark x expected dark share per year.", fontsize=7.5, color=MUTED)
fig.tight_layout(rect=[0, 0.03, 1, 1]); fig.savefig(FIG + "16_interruption_vs_equity.png", dpi=200)
