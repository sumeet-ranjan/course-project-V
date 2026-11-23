"""Step C (NCR): node CARs and quarterly numbers for the traced nodes (decision G4).

Nodes: hit firms DLF, NBCC; within-zone upstream contractors AHLUCONT (<- DLF, material), BLKASHYAP (<- DLF, hit at the
site not documented), JKIL (<- NBCC, not material). Comparison: contractors screened and found unlinked (NCC, PSPPROJECT,
CEMPRO, LT, CAPACITE). Engine: es_lib (market model vs NIFTY 500, [-250,-30]); return matrix extended with the
peers' Yahoo prices. Each firm's CAR gets a placebo p-value from its own CAR on 1,000 random days.
Windows: 18 Nov 2024 (-1,+3) [ends 22 Nov], (-1,+5), (+6,+20), (+21,+60); 17 Dec 2024 (-1,+5), (+6,+20).
Ahluwalia: its Q2 FY25 results came out on 14 Nov 2024 after the close and its call was on 18 Nov, the event day,
so its (-1,+5) mixes the ban with its own results; the 17 Dec window and the quarterly numbers are shown alongside.
Quarterly numbers: screener.in quarterly results (Sales, OPM %) for every node, used for YoY/QoQ comparisons; the
original-document numbers are in the evidence table.
Outputs: outputs/deliverables/stepC_ncr_node_cars.csv, stepC_ncr_quarterly.csv
"""
import os, sys, io, time, urllib.request; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import es_lib as E
from common import EXT, OUT
DEL = OUT + "deliverables/"
pp = pd.read_csv(EXT + "prices_peers.csv", parse_dates=["date"])
peer = pp.pivot_table(index="date", columns="asset_id", values="adjclose").sort_index().pct_change(fill_method=None)
ix = pd.read_csv(EXT + "indices_psu_infra.csv", parse_dates=["date"]).pivot_table(index="date", columns="index", values="close").sort_index().pct_change(fill_method=None)
add = pd.concat([peer, ix], axis=1).reindex(E.R.index)
E.R = pd.concat([E.R, add[[c for c in add.columns if c not in E.R.columns]]], axis=1)
NODES = {"DLF": "hit firm (confirmed)", "NBCC": "hit firm (confirmed)", "AHLUCONT": "contractor <- DLF (material)",
         "BLKASHYAP": "contractor <- DLF (site hit not documented)", "JKIL": "contractor <- NBCC (not material)"}
COMP = ["NCC", "PSPPROJECT", "CEMPRO", "LT", "CAPACITE"]
BENCH = ["NIFTY_REALTY", "NIFTY_INFRA", "NIFTY_PSE"]
EV = {"18 Nov 2024": ("2024-11-18", [(-1, 3), (-1, 5), (6, 20), (21, 60)]), "17 Dec 2024": ("2024-12-17", [(-1, 5), (6, 20)])}
firms = list(NODES) + COMP + BENCH
PT = E.placebo_t0s(n=1000, post=60)
PL = []
for t in PT:
    ar = E.ar_matrix(t, pre=1, post=60)
    if ar is not None: PL.append(ar.reindex(columns=firms))
rows = []
for lab, (day, wins) in EV.items():
    ar = E.ar_matrix(E.t0_of(day), pre=1, post=60).reindex(columns=firms)
    comp_mean = {w: E.car(ar[COMP], *w).mean() for w in wins}
    for f in firms:
        for w in wins:
            c = E.car(ar[[f]], *w).iloc[0]
            ps = pd.Series([E.car(P[[f]], *w).iloc[0] for P in PL]).dropna()
            rows.append(dict(event=lab, nse_symbol=f, node=NODES.get(f, "comparison contractor (unlinked)" if f in COMP else "benchmark index"), window=f"({w[0]},{w[1]})",
                             car=c, p_two_sided=(ps.abs() >= abs(c)).mean() if pd.notna(c) else np.nan, p_one_sided_neg=(ps <= c).mean() if pd.notna(c) else np.nan,
                             car_minus_unlinked_contractors=c - comp_mean[w] if f in NODES else np.nan, n_placebo=len(ps),
                             note=("own Q2 FY25 results 14 Nov 2024 after close and call on 18 Nov fall in this window" if (f == "AHLUCONT" and lab == "18 Nov 2024" and w[0] == -1) else "")))
T = pd.DataFrame(rows); T.round(4).to_csv(DEL + "stepC_ncr_node_cars.csv", index=False)
pd.set_option("display.width", 220)
print(T[T.nse_symbol.isin(list(NODES))].drop(columns=["note"]).round(3).to_string(index=False))
print(T[~T.nse_symbol.isin(list(NODES))].groupby(["event", "window", "node"]).car.mean().round(3).to_string())
# quarterly numbers (screener.in), with YoY and QoQ for the event quarter (Dec 2024) and the next (Mar 2025)
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
QP = EXT + "fin_quarterly_peers.csv"
have = pd.read_csv(QP) if os.path.exists(QP) else pd.DataFrame(columns=["firm"])
q0 = pd.read_csv(EXT + "fin_quarterly.csv")
need = [s for s in list(NODES) + COMP if s not in set(q0.firm) and s not in set(have.firm)]
new = [quarters(s) for s in need]
have = pd.concat([have] + [n for n in new if n is not None], ignore_index=True); have.to_csv(QP, index=False)
q = pd.concat([q0, have], ignore_index=True)
q["value"] = pd.to_numeric(q.value.astype(str).str.replace(",", "").str.replace("%", ""), errors="coerce")
q["qe"] = pd.to_datetime(q.period.astype(str).str.strip().str[:8], format="%b %Y", errors="coerce") + pd.offsets.MonthEnd(0)
q = q.dropna(subset=["qe", "value"]).drop_duplicates(["firm", "item", "qe"])
out = []
for f in list(NODES) + COMP:
    s = q[(q.firm == f) & (q["item"] == "Sales")].set_index("qe").value.sort_index(); m = q[(q.firm == f) & (q["item"] == "OPM %")].set_index("qe").value.sort_index()
    for qe in ("2024-09-30", "2024-12-31", "2025-03-31"):
        qe = pd.Timestamp(qe); prev = qe - pd.offsets.QuarterEnd(1); ly = qe - pd.DateOffset(years=1) + pd.offsets.MonthEnd(0)
        out.append(dict(nse_symbol=f, node=NODES.get(f, "comparison contractor (unlinked)"), quarter=qe.date(), sales_cr=s.get(qe), sales_yoy_pct=100 * (s.get(qe) / s.get(ly) - 1) if s.get(ly) else np.nan,
                        sales_qoq_pct=100 * (s.get(qe) / s.get(prev) - 1) if s.get(prev) else np.nan, opm_pct=m.get(qe), opm_change_yoy_pp=(m.get(qe) - m.get(ly)) if (m.get(qe) is not None and m.get(ly) is not None) else np.nan))
Q = pd.DataFrame(out); Q.round(2).to_csv(DEL + "stepC_ncr_quarterly.csv", index=False); print(Q.round(1).to_string(index=False))
