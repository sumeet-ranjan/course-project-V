"""Market-level cement test for the NCR ban (decision G4 R3). This is NOT a firm-to-firm link test.

The user's design: dose = North capacity share, placebo = cement makers with no northern capacity, ACC and Ambuja left
out. The documents read (research/realign/cement_capacity_regions.csv; nothing dated after Dec 2024) give a North
capacity figure for UltraTech only (33.3 of 150.7 mtpa in Oct 2024, about 22%) and a lower bound for Shree ("more than
half"); for the others they give only plant states. So the test is run on the binary dose (any northern capacity or none),
and the continuous share is reported where stated.
  North (documented plant states): ULTRACEMCO, SHREECEM, JKLAKSHMI, BIRLACORPN, NUVOCO.
  None: STARCEMENT, PRSMJOHNSN (owned plants) documented; DALBHARAT, NCLIND, RAMCOCEM inferred (no northern plant in the text read).
  Excluded: ACC, AMBUJACEM (user: Adani group); INDIACEM (being acquired by UltraTech, per UltraTech's Q3 FY25 deck 'Inorganic
  growth: India Cements Limited'); JKCEMENT, MANGLMCEM, HEIDELBERG, ORIENTCEM, SAGCEM, KCP, DECCANCE (no capacity document read).
Statistic: mean CAR of makers with northern capacity minus mean CAR of makers with none (main: all five 'none';
robustness, dropped at G5 because it rests on two firms: documented zeros only). Placebo p-values from the same statistic on 1,000 random event days.
Engine: es_lib market model (NIFTY 500, [-250,-30]).
Windows: 18 Nov 2024 (-1,+3) [ends 22 Nov], (-1,+5), (+6,+20), (+21,+60); 17 Dec 2024 (-1,+5), (+6,+20).
Outputs: outputs/deliverables/cement_market_test.csv, cement_market_test_firms.csv, cement_market_test_doses.csv
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import es_lib as E
from common import ROOT, EXT, OUT
DEL = OUT + "deliverables/"
DOSE = [  # symbol, group, north share (if stated), basis
    ("ULTRACEMCO", "north", 33.3 / 150.7, "Q2 FY25 deck: North 33.3 mtpa of 140.8 at Mar-24; 9.9 added to Oct-24, none in North"),
    ("SHREECEM", "north", np.nan, "AR FY24: 'more than half of our cement and clinker capacity' in the North (share > 0.5, not stated exactly)"),
    ("JKLAKSHMI", "north", np.nan, "AR FY24: plants at Sirohi, Udaipur (Rajasthan) and Jhajjar (Haryana); amount not stated"),
    ("BIRLACORPN", "north", np.nan, "AR FY24: plants at Chanderia (Rajasthan) and Raebareli (Uttar Pradesh); amount not stated"),
    ("NUVOCO", "north", np.nan, "Q2 FY25 deck: plants named include Nimbol and Chittor (Rajasthan); amount not stated"),
    ("STARCEMENT", "none (documented)", 0.0, "Q2 FY25 deck: units in Meghalaya, Assam and Siliguri"),
    ("PRSMJOHNSN", "none (documented)", 0.0, "Q2 FY25 deck: own plant only at Satna (MP); third-party UP grinding units under supply agreements not owned"),
    ("DALBHARAT", "none (inferred)", 0.0, "Q2 FY25 deck: markets 'East, North-East and South'; no plant list"),
    ("NCLIND", "none (inferred)", 0.0, "AR FY24: only plant found is Mattapalli (Telangana)"),
    ("RAMCOCEM", "none (inferred)", 0.0, "Q2 FY25 update: units in AP, TN, Odisha, West Bengal; no northern unit mentioned")]
Dd = pd.DataFrame(DOSE, columns=["nse_symbol", "group", "north_share", "basis"])
pp = pd.read_csv(EXT + "prices_peers.csv", parse_dates=["date"])
peer = pp.pivot_table(index="date", columns="asset_id", values="adjclose").sort_index().pct_change(fill_method=None).reindex(E.R.index)
E.R = pd.concat([E.R, peer[[c for c in peer.columns if c not in E.R.columns]]], axis=1)
firms = [f for f in Dd.nse_symbol if f in E.R.columns]
NORTH = [f for f in firms if Dd.set_index("nse_symbol").group[f] == "north"]
NONE_ALL = [f for f in firms if Dd.set_index("nse_symbol").group[f].startswith("none")]
NONE_DOC = [f for f in firms if Dd.set_index("nse_symbol").group[f] == "none (documented)"]
EV = {"18 Nov 2024": ("2024-11-18", [(-1, 3), (-1, 5), (6, 20), (21, 60)]), "17 Dec 2024": ("2024-12-17", [(-1, 5), (6, 20)])}
PL = [a.reindex(columns=firms) for a in (E.ar_matrix(t, pre=1, post=60) for t in E.placebo_t0s(n=1000, post=60)) if a is not None]
def gap(ar, w, none):
    c = E.car(ar[firms], *w); return c.reindex(NORTH).mean() - c.reindex(none).mean(), c
rows, frows = [], []
for lab, (day, wins) in EV.items():
    ar = E.ar_matrix(E.t0_of(day), pre=1, post=60).reindex(columns=firms)
    for w in wins:
        for spec, none in (("main: north vs all 'none'", NONE_ALL), ("robustness: north vs documented zeros", NONE_DOC)):
            g, c = gap(ar, w, none); ps = pd.Series([gap(P, w, none)[0] for P in PL]).dropna()
            rows.append(dict(event=lab, window=f"({w[0]},{w[1]})", spec=spec, n_north=int(c.reindex(NORTH).notna().sum()), n_none=int(c.reindex(none).notna().sum()),
                             car_north=c.reindex(NORTH).mean(), car_none=c.reindex(none).mean(), gap_north_minus_none=g,
                             p_two_sided=(ps.abs() >= abs(g)).mean(), p_one_sided_neg=(ps <= g).mean(), n_placebo=len(ps),
                             label="market-level test (not a firm link); binary dose; ACC, Ambuja, India Cements excluded",
                             status=("result (G5: report +2.5 pp over (-1,+5) as the result; coarse, labelled test with little power)" if spec.startswith("main") else
                                     "dropped (G5): rests on two firms, Star Cement and Prism Johnson; no company news found for Star in 14-26 Nov 2024; Prism's fall follows its loss-making Q2 FY25 results of 13 Nov (research/realign/news_checks.csv)")))
        for f in firms: frows.append(dict(event=lab, window=f"({w[0]},{w[1]})", nse_symbol=f, group=Dd.set_index("nse_symbol").group[f], car=E.car(ar[[f]], *w).iloc[0]))
T = pd.DataFrame(rows); T.round(4).to_csv(DEL + "cement_market_test.csv", index=False)
pd.DataFrame(frows).round(4).to_csv(DEL + "cement_market_test_firms.csv", index=False); Dd.round(3).to_csv(DEL + "cement_market_test_doses.csv", index=False)
pd.set_option("display.width", 220); print(T.drop(columns=["label"]).round(3).to_string(index=False))
print(pd.DataFrame(frows).pivot_table(index=["nse_symbol", "group"], columns=["event", "window"], values="car").round(3).to_string())
