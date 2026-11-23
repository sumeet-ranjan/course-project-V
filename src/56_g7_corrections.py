"""G7 corrections (Gujarat, decision of 23 Nov 2026).

1. Rain: the two episodes that hit the Saurashtra-Kutch coast, from external/rain_daily.csv.gz (NASA POWER, district
   means; "Jamnagar" is the pre-2013 district and includes Devbhumi Dwarka, where Mithapur is): 18-24 Jul 2024 and
   25-31 Aug 2024, totals and wettest day; and each district's largest 7-day Jun-Sep total by year, 2000-2025.
   Purpose: Tata Chemicals dates its loss to "July and August", so the loss cannot be split between the episodes from its
   documents; Archean's loss is booked to the late-August storm ("Asna cyclone") alone.
2. Archean's price fall at the storm (CAR -15.8% over (-1,+5) from 26 Aug 2024) compared with specialty-chemical peers in
   the same window: main = the three G2 specialty controls with no Gujarat plant in their own documents (VINATIORGA, CLEAN,
   SUDARSCHEM); wider = those plus five specialty names whose plant locations were not verified (BALAMINES, CHEMPLASTS,
   FINEORG, GALAXYSURF, NOCIL). Net = CAR(ACI) - mean CAR(peers), placebo p from the same difference on 1,000 random days.
   Also Archean's daily abnormal returns 22 Aug - 4 Sep 2024 (to place the fall in time for the news check), and the size
   of the fall in rupees (market cap on 23 Aug 2024 x CAR) against the Rs 40.18 cr booked loss.
Engine: es_lib (market model vs NIFTY 500, [-250,-30]); return matrix extended with Yahoo adjusted-close prices.
Outputs: outputs/deliverables/gj_rain_episodes.csv, gj_rain_7day_max.csv, gj_archean_vs_peers.csv, gj_archean_daily_ar.csv (daily abnormal returns
22 Aug - 3 Sep 2024 beside daily rain in Kachchh; checkpoint-4 review). Reading of the fall: not attributed (the user's reading).
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import es_lib as E
from common import EXT, OUT
DEL = OUT + "deliverables/"
# 1. rain
r = pd.read_csv(EXT + "rain_daily.csv.gz", parse_dates=["date"]); r = r[r.dist_name.isin(["Jamnagar", "Porbandar", "Kachchh"])]
ep = []
for lab, a, b in (("18-24 Jul 2024", "2024-07-18", "2024-07-24"), ("25-31 Aug 2024", "2024-08-25", "2024-08-31")):
    x = r[(r.date >= a) & (r.date <= b)].groupby("dist_name").mm.agg(["sum", "max", "idxmax"])
    for d, row in x.iterrows():
        ep.append(dict(episode=lab, district=d, total_mm=round(row["sum"], 1), wettest_day_mm=round(row["max"], 1), wettest_day=r.loc[row["idxmax"], "date"].date(),
                       note="Jamnagar = pre-2013 district incl. Devbhumi Dwarka (Mithapur)" if d == "Jamnagar" else ("Archean's Hajipir works and Adani's Mundra/Tuna are in Kachchh" if d == "Kachchh" else "")))
EP = pd.DataFrame(ep); EP.to_csv(DEL + "gj_rain_episodes.csv", index=False); print(EP.pivot(index="district", columns="episode", values="total_mm"))
mx = []
for d in ["Jamnagar", "Porbandar", "Kachchh"]:
    s = r[r.dist_name == d].set_index("date").mm.sort_index(); roll = s.rolling(7).sum(); roll = roll[roll.index.month.isin([6, 7, 8, 9])]
    yr = roll.groupby(roll.index.year).agg(["max", "idxmax"])
    for y, row in yr.iterrows(): mx.append(dict(district=d, year=y, max_7day_jjas_mm=round(row["max"], 1), window_end=row["idxmax"].date()))
MX = pd.DataFrame(mx); MX.to_csv(DEL + "gj_rain_7day_max.csv", index=False)
for d, g in MX.groupby("district"):
    g = g.sort_values("max_7day_jjas_mm", ascending=False).reset_index(drop=True); k = g.index[g.year == 2024][0]
    print(d, f"2024 largest 7-day total {g.loc[k,'max_7day_jjas_mm']:.0f} mm (ending {g.loc[k,'window_end']}), rank {k+1} of {len(g)}; next: {g.loc[1 if k==0 else 0,'max_7day_jjas_mm']:.0f} mm in {g.loc[1 if k==0 else 0,'year']}")
# 2. Archean vs specialty-chemical peers
pp = pd.read_csv(EXT + "prices_peers.csv", parse_dates=["date"])
peer = pp.pivot_table(index="date", columns="asset_id", values="adjclose").sort_index().pct_change(fill_method=None)
add = peer.reindex(E.R.index); E.R = pd.concat([E.R, add[[c for c in add.columns if c not in E.R.columns]]], axis=1)
MAIN = ["VINATIORGA", "CLEAN", "SUDARSCHEM"]; WIDE = MAIN + ["BALAMINES", "CHEMPLASTS", "FINEORG", "GALAXYSURF", "NOCIL"]
firms = ["ACI"] + WIDE
PL = [a.reindex(columns=firms) for a in (E.ar_matrix(t, pre=2, post=60) for t in E.placebo_t0s(n=1000, post=60)) if a is not None]
t0 = E.t0_of("2024-08-26"); ar = E.ar_matrix(t0, pre=2, post=60).reindex(columns=firms)
rows = []
for w in [(-1, 3), (-1, 5), (6, 20), (21, 60)]:
    c = E.car(ar[["ACI"]], *w).iloc[0]; pc = pd.Series([E.car(P[["ACI"]], *w).iloc[0] for P in PL]).dropna()
    for lab, grp in (("main: 3 G2 specialty controls (no Gujarat plant)", MAIN), ("wider: 8 specialty names (5 with unverified plant locations)", WIDE)):
        m = E.car(ar[grp], *w).mean(); d = c - m
        pdist = pd.Series([E.car(P[["ACI"]], *w).iloc[0] - E.car(P[grp], *w).mean() for P in PL]).dropna()
        rows.append(dict(window=f"({w[0]},{w[1]})", dates=f"{E.DATES[t0+w[0]].date()} to {E.DATES[t0+w[1]].date()}", peers=lab, car_aci=c, p_aci=(pc.abs() >= abs(c)).mean(),
                         peer_mean=m, net_of_peers=d, p_net_two_sided=(pdist.abs() >= abs(d)).mean(), p_net_one_sided_neg=(pdist <= d).mean(), n_placebo=len(pdist),
                         peers_each="; ".join(f"{p} {E.car(ar[[p]], *w).iloc[0]:+.3f}" for p in grp)))
T = pd.DataFrame(rows)
mc = pd.read_csv(EXT + "market_cap_peers.csv") if os.path.exists(EXT + "market_cap_peers.csv") else None
cap = 9880.0   # Rs cr on 23 Aug 2024 (hit_register_GJ.csv)
T["rupee_value_of_car_cr"] = (T.car_aci * cap).round(0); T["rupee_value_net_cr"] = (T.net_of_peers * cap).round(0); T["booked_loss_cr"] = 40.18
T.round(4).to_csv(DEL + "gj_archean_vs_peers.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 120); print(T.drop(columns=["peers_each"]).round(3).to_string(index=False)); print(T[["window", "peers_each"]].to_string(index=False))
# daily abnormal returns 22 Aug - 3 Sep 2024 beside daily rain in Kachchh (calendar days; weekends have rain but no return)
cal = pd.date_range("2024-08-22", "2024-09-03", freq="D")
rk = r[r.dist_name == "Kachchh"].set_index("date").mm
rows_d = []
for d in cal:
    trade = d in E.DATES
    k = int(np.searchsorted(E.DATES.values, np.datetime64(d))) - t0 if trade else None
    rows_d.append(dict(date=d.date(), weekday=d.strftime("%a"), trading_day="yes" if trade else "no", event_day=k if trade else "",
                       ar_aci=ar.loc[k, "ACI"] if trade else np.nan, peer_mean_main=ar.loc[k, MAIN].mean() if trade else np.nan,
                       ar_aci_net_of_peers=(ar.loc[k, "ACI"] - ar.loc[k, MAIN].mean()) if trade else np.nan,
                       raw_aci=E.R.loc[d, "ACI"] if trade else np.nan, market=E.MKT.loc[d] if trade else np.nan, rain_kachchh_mm=rk.get(d, np.nan)))
dd = pd.DataFrame(rows_d); dd.round(4).to_csv(DEL + "gj_archean_daily_ar.csv", index=False); print(dd.round(4).to_string(index=False))
# 3. Tata Chemicals' own price evidence (checkpoint-4 review): abnormal returns from the market model estimated on [-250,-30]
#    before 26 Aug 2024 (as in src/52), daily over 26-30 Aug, on its results day (18 Oct), and the daily s.d.
s = "TATACHEM"; a_, b_ = t0 - 250, t0 - 30
y = E.R.iloc[a_:b_][s]; m = E.MKT.iloc[a_:b_]; okm = y.notna()
beta_ = np.cov(y[okm], m[okm])[0, 1] / np.var(m[okm], ddof=1); alpha_ = y[okm].mean() - beta_ * m[okm].mean()
res = y[okm] - (alpha_ + beta_ * m[okm])
arf = lambda d: E.R.loc[pd.Timestamp(d), s] - (alpha_ + beta_ * E.MKT.loc[pd.Timestamp(d)])
days = ["2024-08-26", "2024-08-27", "2024-08-28", "2024-08-29", "2024-08-30"]
PLT = [x for x in (E.ar_matrix(t, pre=1, post=60) for t in E.placebo_t0s(n=1000, post=60)) if x is not None and s in x.columns]
c04 = E.car(E.ar_matrix(t0, pre=1, post=60)[[s]], 0, 4).iloc[0]; dist = pd.Series([E.car(P[[s]], 0, 4).iloc[0] for P in PLT]).dropna()
TP = pd.DataFrame([dict(item=f"abnormal return {d}", value=arf(d)) for d in days] +
                  [dict(item="sum of daily abnormal returns, 26-30 Aug 2024", value=sum(arf(d) for d in days)),
                   dict(item="engine CAR (0,+4) from 26 Aug 2024", value=c04), dict(item="placebo p, CAR (0,+4)", value=(dist.abs() >= abs(c04)).mean()),
                   dict(item="abnormal return 18 Oct 2024 (results day; filed 17 Oct 18:01)", value=arf("2024-10-18")),
                   dict(item="daily s.d. of raw returns, estimation window", value=y[okm].std(ddof=1)),
                   dict(item="daily s.d. of market-model residuals, estimation window", value=res.std(ddof=1))])
TP.round(5).to_csv(DEL + "gj_tatachem_price.csv", index=False); print(TP.round(4).to_string(index=False))
