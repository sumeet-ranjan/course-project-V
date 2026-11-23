"""Deliverable 1, Gujarat: evidence table per node (scope change of 23 Nov 2026; decision G7 pending).

Branches:
  A. storm (IMD) -> hit firms outside the pack: Tata Chemicals (Mithapur), Archean (Kutch), Adani Ports (Mundra, Tuna),
     GE T&D India (Vadodara) -> forward chain (H2): Tata Chemicals -> Tata Consumer (edible salt).
  B. the pack's chemical belt (Vadodara/Bharuch): sites dark on 30 Aug 2024 (night lights), no company statement -> break at Step A.
Columns: node, firm_symbol, external, in_pack_footprint, role, date, source, source_url, quote, number, CARs (storm windows),
results-day abnormal returns, delta-financial, lag, status, note. Quotes only from tables that passed src/42.
Output: outputs/deliverables/evidence_GJ.csv
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd, numpy as np
from common import ROOT, OUT, companies
RE = ROOT + "/research/realign/"; DEL = OUT + "deliverables/"
PACK = set(companies().nse_symbol)
qc = pd.read_csv(RE + "quote_check_realign.csv"); ok = lambda f: set(qc[(qc.file == f) & (qc.status == "verified")].row)
NC = pd.read_csv(DEL + "stepC_gj_node_cars.csv"); Q = pd.read_csv(DEL + "stepC_gj_quarterly.csv"); RD = pd.read_csv(DEL + "stepC_gj_results_days.csv")
def car(sym, w):
    x = NC[(NC.nse_symbol == sym) & (NC.window == w)]
    return f"{x.car.iloc[0]:+.3f} (p={x.p_two_sided.iloc[0]:.2f})" if len(x) and pd.notna(x.car.iloc[0]) else ""
def rday(sym):
    x = RD[RD.nse_symbol == sym]
    return "; ".join(f"{r.date}: {r.abnormal_return:+.3f} (t={r.t_vs_own_sd:+.1f})" for r in x.itertuples() if pd.notna(r.abnormal_return))
def dq(sym, qe="2024-09-30"):
    x = Q[(Q.nse_symbol == sym) & (Q.quarter == qe)]
    if not len(x): return ""
    r = x.iloc[0]; return f"{qe[:7]} quarter: sales {r.sales_yoy_pct:+.1f}% YoY, {r.sales_qoq_pct:+.1f}% QoQ; OPM {r.opm_pct:.0f}% ({r.opm_change_yoy_pp:+.0f} pp YoY) [screener.in]"
FPG = {"TATACHEM": "no (Mithapur, Devbhumi Dwarka)", "ACI": "no (Kutch)", "GVT&D": "yes (Vadodara)", "ADANIPORTS": "no (Mundra, Tuna in Kutch)", "GHCL": "no (Sutrapada, Gir Somnath)",
       "TATACONSUM": "no (buyer outside Gujarat footprint)"}
rows = []
def add(node, sym, role, date, source, url, quote, number="", dfin="", lag="", status="evidence", note=""):
    rows.append(dict(node=node, firm_symbol=sym, external=("" if not sym or sym == "IMD" else ("no" if sym in PACK else "yes")), in_pack_footprint=FPG.get(sym, ""),
                     role=role, date=date, source=source, source_url=url, quote=quote, number_given=number,
                     car_26aug_m1_5=car(sym, "(-1,5)") if sym else "", car_26aug_6_20=car(sym, "(6,20)") if sym else "", car_26aug_21_60=car(sym, "(21,60)") if sym else "",
                     results_day_abnormal=rday(sym) if sym else "", delta_financial=dfin, lag=lag, status=status, note=note))
G = pd.read_csv(RE + "gj_hit_firms_docs.csv", dtype=str).fillna(""); vg = ok("gj_hit_firms_docs.csv")
for i, r in G.iterrows():
    if i not in vg: continue
    if r.nse_symbol == "IMD":
        add("0 event: storm (IMD)", "IMD", "official weather record", r.document_date, r.document_title, r.source_url, r.quote)
for sym, role in (("TATACHEM", "hit firm: Mithapur soda ash and salt"), ("ACI", "hit firm: Kutch salt"), ("ADANIPORTS", "hit firm: Mundra and Tuna ports"), ("GVT&D", "hit firm: Vadodara plant")):
    for i, r in G[G.nse_symbol == sym].iterrows():
        if i not in vg: continue
        sec = "Business Standard" in r.document_title
        add("1 hit firm outside the pack (Step A, G7 pending)", sym, role + (" (secondary: news relay of the company notice)" if sec else ""), r.document_date, r.document_title, r.source_url,
            r.quote, r.number_given, dfin=dq(sym), lag="Q2 FY25 (Jul-Sep 2024)", status="evidence" if r.what_it_shows != "no_mention" else "documented absence", note=r.notes)
for i, r in G[G.nse_symbol == "GHCL"].iterrows():
    if i in vg: add("confound", "GHCL", "soda ash peer: planned boiler maintenance", r.document_date, r.document_title, r.source_url, r.quote, r.number_given, dfin=dq("GHCL"), status="confound", note=r.notes)
# forward chain (H2)
TP = RE + "gj_tata_chain_docs.csv"
if os.path.exists(TP):
    T = pd.read_csv(TP, dtype=str).fillna(""); vt = ok("gj_tata_chain_docs.csv")
    lab = {"1a": "2 link: Tata Chemicals -> Tata Consumer (edible salt)", "1b": "2 link: Tata Chemicals -> Tata Consumer (edible salt)", "2a": "2 link weight (FY24)", "2b": "2 link weight (FY24)",
           "3a": "3 downstream node: Tata Consumer (Q2 FY25)", "3b": "3 downstream node: Tata Consumer (Q3 FY25, lag)", "4": "confound (supplier side)"}
    for i, r in T.iterrows():
        if i in vt or (r.quote == "" and r.read_mode != "search_snippet"):
            node = lab.get(str(r.task), "other")
            add(node, r.nse_symbol, str(r.task), r.document_date, r.document_title, r.source_url, r.quote, r.number_given + (" " + r.unit if r.unit else ""),
                dfin=dq(r.nse_symbol, "2024-12-31" if str(r.task) == "3b" else "2024-09-30") if node.startswith("3") else "", status="evidence" if r.quote else "documented absence", note=r.notes)
else:
    add("2 link: Tata Chemicals -> Tata Consumer (edible salt)", "", "", "", "", "", "", status="pending: link documents being collected")
add("3 downstream node: Tata Consumer (market)", "TATACONSUM", "results-day returns (Q2 FY25)", "2024-10-17", "stepC_gj_results_days.csv", "", "", dfin=dq("TATACONSUM") + " | " + dq("TATACONSUM", "2024-12-31"),
    status="measurement", note="abnormal returns from the market model estimated before 26 Aug 2024. Release times from the NSE filing names: Tata Consumer 18 Oct 2024 16:52 IST (after the close) -> first trading day to price it is 21 Oct; Tata Chemicals 17 Oct 2024 18:01 IST -> priced on 18 Oct")
# branch B: the pack's chemical belt
n = pd.read_csv(OUT + "tables/ntl_plant_event.csv"); n = n[(n.event_id == "E_GJ_FLOOD_2024") & (n.dist_name == "Vadodara") & n.nse_symbol.isin(["GSFC", "GUJALKALI", "BODALCHEM", "KIRIINDUS"])]
for sym, g in n.groupby("nse_symbol"):
    obs = g[g.observed == True]; dark = obs[obs.dark == True]
    add("B pack chemical belt (Vadodara sites)", sym, "night lights at the firm's Vadodara sites", "2024-08-30", "outputs/tables/ntl_plant_event.csv (NASA Black Marble)", "",
        f"{len(g)} sites; {len(obs)} with a usable reading; {len(dark)} dark on 30 Aug (ratio {obs.ratio_first.min():.2f}-{obs.ratio_first.max():.2f})" if len(obs) else f"{len(g)} sites; no usable reading",
        status="physical proxy only", note="footprint defined by sites (user, G2)")
for sym in ("GSFC", "GUJALKALI", "BODALCHEM", "KIRIINDUS", "GNFC", "SRF", "AARTIIND", "UPL", "DCMSHRIRAM", "ZUARI"):
    add("B pack chemical belt (Step A)", sym, "company statement", "", "Q2 FY25 calls read (where filed) and NSE filings 25 Aug - 30 Sep 2024", "", "",
        status="break: no company statement attributes an effect to the flood", note="see hit_register_GJ.csv; Gujarat Alkalies filed no Q2 FY25 transcript (M11)")
o = pd.DataFrame(rows); o.to_csv(DEL + "evidence_GJ.csv", index=False)
print(o.groupby(["node", "status"]).size().to_string())
