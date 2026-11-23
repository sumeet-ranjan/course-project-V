"""G5 corrections (NCR, decision of 23 Nov 2026): the contractors' price evidence, restated.

1. Disclosure days (Ahluwalia). Release times from the NSE filings and the call notices (research/realign/g5_timing_docs.csv):
   - Q2 FY25 results filed 14 Nov 2024 17:16 IST (after the close); 15 Nov was a market holiday, so 18 Nov 2024 is the first
     trading day to price them. It is also the ban's day 0. The Q2 call began at 3.00 pm on 18 Nov, 30 minutes before the
     close, so 19 Nov prices most of the call.
   - Q3 FY25 results filed 11 Feb 2025 16:43 IST (after the close): first priced on 12 Feb 2025. The Q3 call (with the
     guidance cut to 8.5-9%) began at 4.00 pm IST on 12 Feb, after the close: first priced on 13 Feb 2025.
   Reported: abnormal return on each day (0,0), the next day (+1,+1) and the two together (0,+1).
2. Every window net of the unlinked-contractor average (NCC, PSPPROJECT, CEMPRO, LT, CAPACITE): the difference
   CAR(node) - mean CAR(unlinked) with a placebo p-value from the same difference on 1,000 random days (es_lib placebo
   dates). Robustness: the unlinked small and mid caps only (LT excluded), because of the small- and mid-cap sell-off of
   Jan-Feb 2025. Done for all three within-zone contractor nodes (AHLUCONT, BLKASHYAP, JKIL).
Engine: es_lib market model vs NIFTY 500, estimation window [-250,-30] before each event day; return matrix extended with
Yahoo adjusted-close prices for the peers. For 12-13 Feb 2025 the estimation window contains Nov-Dec 2024, so the abnormal
returns are also shown from the model estimated before 18 Nov 2024 (column ar_model_pre_18nov).
Outputs: outputs/deliverables/stepC_ncr_contractor_net.csv, stepC_ncr_disclosure_days.csv
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import es_lib as E
from common import EXT, OUT
DEL = OUT + "deliverables/"
pp = pd.read_csv(EXT + "prices_peers.csv", parse_dates=["date"])
peer = pp.pivot_table(index="date", columns="asset_id", values="adjclose").sort_index().pct_change(fill_method=None)
add = peer.reindex(E.R.index)
E.R = pd.concat([E.R, add[[c for c in add.columns if c not in E.R.columns]]], axis=1)
NODES = {"AHLUCONT": "contractor <- DLF (material)", "BLKASHYAP": "contractor <- DLF (site hit not documented)", "JKIL": "contractor <- NBCC (not material)"}
COMP = ["NCC", "PSPPROJECT", "CEMPRO", "LT", "CAPACITE"]; COMP_SM = [c for c in COMP if c != "LT"]
firms = list(NODES) + COMP
EV = {"18 Nov 2024 (ban day 0; Ahluwalia Q2 results day; Q2 call priced from 19 Nov)": ("2024-11-18", [(-1, 3), (-1, 5), (6, 20), (21, 60), (0, 0), (1, 1), (0, 1)]),
      "17 Dec 2024 (re-imposition)": ("2024-12-17", [(-1, 5), (6, 20)]),
      "12 Feb 2025 (Ahluwalia Q3 results day; Q3 call priced from 13 Feb)": ("2025-02-12", [(0, 0), (1, 1), (0, 1)])}
PL = [a.reindex(columns=firms) for a in (E.ar_matrix(t, pre=1, post=60) for t in E.placebo_t0s(n=1000, post=60)) if a is not None]
NOTE = {("BLKASHYAP", "2024-11-18"): "not its own disclosure day: its Q2 FY25 results came out on 11 Nov 2024 at 13:56 (in market hours)",
        ("BLKASHYAP", "2025-02-12"): "not its own disclosure day: its Q3 FY25 results came out on 7 Feb 2025 at 17:13; it still fell on 12 Feb, so the 12 Feb move is not Ahluwalia-specific",
        ("JKIL", "2024-11-18"): "Ahluwalia's disclosure day; J. Kumar's own results dates not checked", ("JKIL", "2025-02-12"): "Ahluwalia's disclosure day; J. Kumar's own results dates not checked",
        ("AHLUCONT", "2024-11-18"): "(0,0) = 18 Nov, Q2 results day (and the ban's day 0); (+1,+1) = 19 Nov, first day the Q2 call (GRAP-IV statement) is priced",
        ("AHLUCONT", "2024-12-17"): "no Ahluwalia disclosure in 26 Dec 2024 - 15 Jan 2025 (NSE announcement list)",
        ("AHLUCONT", "2025-02-12"): "(0,0) = 12 Feb, Q3 results day (the deck filed at 12:33 does not mention the ban); (+1,+1) = 13 Feb, first day the Q3 call (guidance cut) is priced"}
def stat(ar, f, w, comp):
    c = E.car(ar[[f]], *w).iloc[0]; m = E.car(ar[comp], *w).mean()
    return c, m, c - m
rows = []
for lab, (day, wins) in EV.items():
    t0 = E.t0_of(day); ar = E.ar_matrix(t0, pre=1, post=60).reindex(columns=firms)
    dates = E.DATES
    for w in wins:
        span = f"{dates[t0 + w[0]].date()} to {dates[t0 + w[1]].date()}"
        indiv = "; ".join(f"{c} {E.car(ar[[c]], *w).iloc[0]:+.3f}" for c in COMP)
        for f in NODES:
            c, m, d = stat(ar, f, w, COMP); _, m2, d2 = stat(ar, f, w, COMP_SM)
            pc = pd.Series([E.car(P[[f]], *w).iloc[0] for P in PL]).dropna()
            pd_ = pd.Series([stat(P, f, w, COMP)[2] for P in PL]).dropna(); pd2 = pd.Series([stat(P, f, w, COMP_SM)[2] for P in PL]).dropna()
            rows.append(dict(event=lab, window=f"({w[0]},{w[1]})", dates=span, nse_symbol=f, node=NODES[f], car=c,
                             p_two_sided=(pc.abs() >= abs(c)).mean(), unlinked_mean=m, net_of_unlinked=d,
                             p_net_two_sided=(pd_.abs() >= abs(d)).mean(), p_net_one_sided_neg=(pd_ <= d).mean(),
                             unlinked_small_mid_mean=m2, net_of_unlinked_small_mid=d2, p_net_sm_two_sided=(pd2.abs() >= abs(d2)).mean(),
                             n_placebo=len(pd_), unlinked_each=indiv, note=NOTE.get((f, day), "")))
T = pd.DataFrame(rows); T.round(4).to_csv(DEL + "stepC_ncr_contractor_net.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 60)
print(T.drop(columns=["node", "unlinked_each", "event"]).round(3).to_string(index=False))
# disclosure days, Ahluwalia: abnormal return from the engine (own window) and from the model estimated before 18 Nov 2024
t18 = E.t0_of("2024-11-18"); y = E.R.iloc[t18 - 250:t18 - 30]; mk = E.MKT.iloc[t18 - 250:t18 - 30]
beta = ((y - y.mean()).mul(mk - mk.mean(), axis=0)).sum() / ((y.notna()).mul((mk - mk.mean()) ** 2, axis=0)).sum(); alpha = y.mean() - beta * mk.mean()
sd = pd.Series(np.nanstd(y.values - (np.outer(mk.values, beta.values) + alpha.values[None, :]), axis=0, ddof=1), index=y.columns)
WHAT = {"2024-11-18": "Q2 results day: Q2 FY25 results filed 14 Nov 17:16 (after the close; 15 Nov holiday); down 2.78% by 10:32 IST on the profit fall (Business Standard); also the ban's day 0",
        "2024-11-19": "first day the Q2 call is priced: call began 3.00 pm on 18 Nov, 30 min before the close; the GRAP-IV statement is on page 8 of 13 of the transcript",
        "2025-02-12": "Q3 results day: Q3 FY25 results filed 11 Feb 16:43 (after the close), revenue -7.3% YoY; the deck filed at 12:33 does not mention the ban",
        "2025-02-13": "first day the Q3 call is priced: call began 4.00 pm on 12 Feb, after the close; FY25 growth guidance cut to 8.5-9%"}
dd = []
for d, what in WHAT.items():
    ts = pd.Timestamp(d); t0 = E.t0_of(d); ar = E.ar_matrix(t0, pre=1, post=60).reindex(columns=firms)
    a_pre = E.R.loc[ts, "AHLUCONT"] - (alpha["AHLUCONT"] + beta["AHLUCONT"] * E.MKT.loc[ts])
    pc = pd.Series([P[["AHLUCONT"]].loc[0].iloc[0] for P in PL]).dropna()
    dd.append(dict(date=d, what_it_priced=what, raw_return=E.R.loc[ts, "AHLUCONT"], market_return=E.MKT.loc[ts], ar_engine=ar.loc[0, "AHLUCONT"],
                   p_two_sided=(pc.abs() >= abs(ar.loc[0, "AHLUCONT"])).mean(), unlinked_mean_ar=ar.loc[0, COMP].mean(),
                   net_of_unlinked=ar.loc[0, "AHLUCONT"] - ar.loc[0, COMP].mean(), ar_model_pre_18nov=a_pre, t_vs_own_sd=a_pre / sd["AHLUCONT"]))
DD = pd.DataFrame(dd); DD.round(4).to_csv(DEL + "stepC_ncr_disclosure_days.csv", index=False); print(DD.round(4).to_string(index=False))
