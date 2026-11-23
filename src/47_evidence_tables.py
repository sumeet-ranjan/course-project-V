"""Deliverable 1 (evidence table per node) — assembled only from checked, original-document evidence.

One row per piece of evidence, grouped by node: event -> exposed plants -> hit firm -> verified link -> downstream/
upstream firm. Columns follow INSTRUCTIONS §6: date, source, quote, CAR, delta-financial, lag.
Rows enter only if their quote passed src/42_check_quotes_realign.py (or, for the official orders, the original
PIB release text). Nodes still waiting for a step are listed with status 'pending' so the table shows where the
chain stands (and, if it breaks, where).
Output: outputs/deliverables/evidence_NCR.csv (Gujarat follows in Step 4)
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd, numpy as np
from common import ROOT, OUT
RE = ROOT + "/research/realign/"; DEL = OUT + "deliverables/"
qc = pd.read_csv(RE + "quote_check_realign.csv")
ok = lambda f: set(qc[(qc.file == f) & (qc.status == "verified")].row)
F = pd.read_csv(DEL + "table1_direct_firms.csv"); F = F[F.event == "E_NCR_GRAP_2024"].drop_duplicates("nse_symbol").set_index("nse_symbol")
rows = []
def add(node, firm, role, date, source, url, quote, car=None, dfin="", lag="", status="evidence", note=""):
    c = F.loc[firm] if firm in F.index else None
    rows.append(dict(node=node, firm=firm, role=role, date=date, source=source, source_url=url, quote=quote,
                     car_m1_3=None if c is None else round(c["car_-1_3"], 4), car_m1_5=None if c is None else round(c["car_-1_5"], 4),
                     car_6_20=None if c is None else round(c["car_6_20"], 4), car_21_60=None if c is None else round(c["car_21_60"], 4),
                     delta_financial=dfin, lag=lag, status=status, note=note))
# node 0: the event (official orders, original PIB text)
h = pd.read_csv(ROOT + "/research/proxy/official_hazard_records.csv", dtype=str).fillna("")
h = h[(h.task == "A_grap_orders") & (h.event == "GRAP_winter_2024") & (h.item.isin(["order", "construction_clause"]))]
for r in h.sort_values("date").itertuples():
    add("0 event: GRAP orders (CAQM)", "", f"{r.stage_or_station} {r.action}".strip(), r.date, r.source_name, r.source_url, r.source_quote, note=r.time)
# node 1: exposed plants (pack data)
from common import plants, ZONES
p = plants(); tot = p.groupby("nse_symbol").project_cost_cr.sum()
for f in ("NBCC", "DLF"):
    z = p[(p.nse_symbol == f) & p.dist_name.isin(ZONES["NCR"])]
    add("1 exposed plants (pack)", f, "hit firm's NCR sites", "", "data/plants.csv", "", f"{len(z)} NCR sites; {z.project_cost_cr.sum() / tot[f]:.0%} of plant cost",
        note="districts: " + ", ".join(sorted(z.dist_name.unique())))
# node 2: hit firms (Step A, G3)
A = pd.read_csv(RE + "ncr_stepA_evidence.csv", dtype=str).fillna("")
for i, r in A.iterrows():
    if r.nse_symbol in ("NBCC", "DLF") and i in ok("ncr_stepA_evidence.csv") and r.what_it_shows in ("names_ban", "delay_or_stoppage"):
        add("2 hit firm (confirmed, G3)", r.nse_symbol, "builder under the construction ban", r.document_date, r.document_title, r.source_url, r.quote,
            dfin="pending Step C (Q3 FY25 results)", lag="same quarter (Oct-Dec 2024), per the company", note=r.notes)
for f in ("NBCC", "DLF"):
    n = A[(A.nse_symbol == f) & (A.what_it_shows == "no_mention")]
    add("2 hit firm (confirmed, G3)", f, "documents read with no mention", "", "; ".join(n.document_title), "", "", status="documented absence")
# node 3+: links and suppliers (Step B pending G4)
add("3 verified link (Step B)", "", "builder -> cement/steel supplier", "", "", "", "", status="pending: Step B evidence being collected; decision G4")
add("4 upstream supplier (Step C)", "", "cement/steel supplier", "", "", "", "", status="pending: after G4")
o = pd.DataFrame(rows); o.to_csv(DEL + "evidence_NCR.csv", index=False)
print(o.groupby(["node", "status"]).size().to_string())
