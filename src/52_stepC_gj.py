"""Step C (Gujarat, outside the pack): node CARs, results-day returns and quarterly numbers.

Hit-firm candidates (G7 pending): TATACHEM (Mithapur), ACI (Archean, Kutch), GVT&D (GE T&D India, Vadodara), ADANIPORTS
(Mundra, Tuna); confound firm GHCL (soda ash, planned boiler shutdown from 16 Sep 2024); downstream node TATACONSUM
(edible salt bought from Tata Chemicals). Engine: es_lib (market model vs NIFTY 500, [-250,-30]), return matrix
extended with Yahoo prices; placebo p-values from each firm's own CAR on 1,000 random days.
  - Storm windows from 26 Aug 2024: (-1,+5), (+6,+20), (+21,+60).
  - Results days (decision: measure Tata Consumer on its results days, not on 26 Aug): abnormal returns on each listed day
    and their sum, from the market model estimated before 26 Aug 2024 (so the storm is not in the estimation window).
Quarterly numbers: screener.in quarterly Sales and OPM %, Jun 2024 - Mar 2025, YoY and QoQ.
Outputs: outputs/deliverables/stepC_gj_node_cars.csv, stepC_gj_results_days.csv, stepC_gj_quarterly.csv
"""
import os, sys, io, time, urllib.request; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import es_lib as E
from common import EXT, OUT
DEL = OUT + "deliverables/"
pp = pd.read_csv(EXT + "prices_peers.csv", parse_dates=["date"])
peer = pp.pivot_table(index="date", columns="asset_id", values="adjclose").sort_index().pct_change(fill_method=None)
add = peer.reindex(E.R.index)
E.R = pd.concat([E.R, add[[c for c in add.columns if c not in E.R.columns]]], axis=1)
NODES = {"TATACHEM": "hit-firm candidate (Mithapur)", "ACI": "hit-firm candidate (Kutch)", "GVT&D": "hit-firm candidate (Vadodara)",
         "ADANIPORTS": "hit-firm candidate (Mundra, Tuna)", "GHCL": "soda ash peer (confound)", "TATACONSUM": "downstream buyer of Tata Chemicals' salt"}
firms = list(NODES)
WIN = [(-1, 5), (6, 20), (21, 60)]
PL = [a.reindex(columns=firms) for a in (E.ar_matrix(t, pre=1, post=60) for t in E.placebo_t0s(n=1000, post=60)) if a is not None]
t0 = E.t0_of("2024-08-26"); ar = E.ar_matrix(t0, pre=1, post=60).reindex(columns=firms)
rows = []
for f in firms:
    for w in WIN:
        c = E.car(ar[[f]], *w).iloc[0]; ps = pd.Series([E.car(P[[f]], *w).iloc[0] for P in PL]).dropna()
        rows.append(dict(event="26 Aug 2024 (storm)", nse_symbol=f, node=NODES[f], window=f"({w[0]},{w[1]})", car=c,
                         p_two_sided=(ps.abs() >= abs(c)).mean() if pd.notna(c) else np.nan, p_one_sided_neg=(ps <= c).mean() if pd.notna(c) else np.nan, n_placebo=len(ps)))
T = pd.DataFrame(rows); T.round(4).to_csv(DEL + "stepC_gj_node_cars.csv", index=False)
pd.set_option("display.width", 200); print(T.round(3).to_string(index=False))
# results days: abnormal returns from the market model estimated on [-250,-30] before 26 Aug 2024
RESULTS = {"TATACONSUM": ["2024-10-17", "2024-10-18", "2024-10-21"], "TATACHEM": ["2024-10-17", "2024-10-18", "2024-10-21"]}   # release times (NSE filing names): Tata Chemicals 17 Oct 2024 18:01 IST -> priced 18 Oct; Tata Consumer 18 Oct 2024 16:52 IST -> priced 21 Oct (17-18 Oct shown as the user asked)
if os.path.exists(DEL + "results_days_extra.csv"):
    for r in pd.read_csv(DEL + "results_days_extra.csv", dtype=str).itertuples(): RESULTS.setdefault(r.nse_symbol, []).append(r.date)
y = E.R.iloc[t0 - 250:t0 - 30]; m = E.MKT.iloc[t0 - 250:t0 - 30]
beta = ((y - y.mean()).mul(m - m.mean(), axis=0)).sum() / ((y.notna()).mul((m - m.mean()) ** 2, axis=0)).sum(); alpha = y.mean() - beta * m.mean()
sd = pd.Series(np.nanstd(y.values - (np.outer(m.values, beta.values) + alpha.values[None, :]), axis=0, ddof=1), index=y.columns)
rr = []
for f, days in RESULTS.items():
    for d in days:
        d = pd.Timestamp(d)
        if d not in E.R.index: rr.append(dict(nse_symbol=f, date=d.date(), note="not a trading day")); continue
        a = E.R.loc[d, f] - (alpha[f] + beta[f] * E.MKT.loc[d])
        rr.append(dict(nse_symbol=f, date=d.date(), raw_return=E.R.loc[d, f], market_return=E.MKT.loc[d], abnormal_return=a, t_vs_own_sd=a / sd[f]))
RR = pd.DataFrame(rr); RR.round(4).to_csv(DEL + "stepC_gj_results_days.csv", index=False); print(RR.round(4).to_string(index=False))
# quarterly numbers
from bs4 import BeautifulSoup
def quarters(sym):
    for cons in (True, False):
        try:
            u = f"https://www.screener.in/company/{sym}/" + ("consolidated/" if cons else "")
            s = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=40).read().decode(), "lxml")
            d = pd.read_html(io.StringIO(str(s.find("section", id="quarters").find("table"))))[0]
            d = d.rename(columns={d.columns[0]: "item"}); d["item"] = d["item"].str.replace("+", "", regex=False).str.strip()
            if d.shape[1] > 3: return d.melt(id_vars="item", var_name="period", value_name="value").assign(firm=sym, basis="consolidated" if cons else "standalone")
        except Exception: pass
        time.sleep(1.5)
    return None
QP = EXT + "fin_quarterly_peers.csv"; have = pd.read_csv(QP) if os.path.exists(QP) else pd.DataFrame(columns=["firm"])
q0 = pd.read_csv(EXT + "fin_quarterly.csv")
need = [s for s in firms if s not in set(q0.firm) and s not in set(have.firm)]
have = pd.concat([have] + [n for n in (quarters(s.replace("&", "%26")) for s in need) if n is not None], ignore_index=True)
have["firm"] = have["firm"].str.replace("%26", "&"); have.to_csv(QP, index=False)
q = pd.concat([q0, have], ignore_index=True)
q["value"] = pd.to_numeric(q.value.astype(str).str.replace(",", "").str.replace("%", ""), errors="coerce")
q["qe"] = pd.to_datetime(q.period.astype(str).str.strip().str[:8], format="%b %Y", errors="coerce") + pd.offsets.MonthEnd(0)
q = q.dropna(subset=["qe", "value"]).drop_duplicates(["firm", "item", "qe"])
out = []
for f in firms:
    s = q[(q.firm == f) & (q["item"] == "Sales")].set_index("qe").value.sort_index(); mm = q[(q.firm == f) & (q["item"] == "OPM %")].set_index("qe").value.sort_index()
    for qe in ("2024-06-30", "2024-09-30", "2024-12-31", "2025-03-31"):
        qe = pd.Timestamp(qe); prev = qe - pd.offsets.QuarterEnd(1); ly = qe - pd.DateOffset(years=1) + pd.offsets.MonthEnd(0)
        out.append(dict(nse_symbol=f, node=NODES[f], quarter=qe.date(), sales_cr=s.get(qe), sales_yoy_pct=100 * (s.get(qe) / s.get(ly) - 1) if s.get(ly) else np.nan,
                        sales_qoq_pct=100 * (s.get(qe) / s.get(prev) - 1) if s.get(prev) else np.nan, opm_pct=mm.get(qe),
                        opm_change_yoy_pp=(mm.get(qe) - mm.get(ly)) if (mm.get(qe) is not None and mm.get(ly) is not None) else np.nan))
Q = pd.DataFrame(out); Q.round(2).to_csv(DEL + "stepC_gj_quarterly.csv", index=False); print(Q.round(1).to_string(index=False))
