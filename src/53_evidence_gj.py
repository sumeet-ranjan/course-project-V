"""Deliverable 1, Gujarat: evidence table per node (scope change of 23 Nov 2026; decision G7 of 23 Nov 2026 applied).

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
GRADE = {"TATACHEM": "material hit", "ACI": "material hit", "ADANIPORTS": "confirmed, immaterial", "GVT&D": "confirmed, immaterial"}
# 0b the two rain episodes (G7): Tata Chemicals dates its loss to "July and August"
if os.path.exists(DEL + "gj_rain_episodes.csv"):
    EP = pd.read_csv(DEL + "gj_rain_episodes.csv")
    for epi, g in EP.groupby("episode", sort=False):
        add("0 event: rain episodes (NASA POWER district rainfall)", "", "rain episode", epi, "external/rain_daily.csv.gz (outputs/deliverables/gj_rain_episodes.csv)", "",
            "; ".join(f"{r.district} {r.total_mm:.0f} mm (wettest day {r.wettest_day_mm:.0f} mm on {r.wettest_day})" for r in g.itertuples()), status="measurement",
            note="Jamnagar = pre-2013 district incl. Devbhumi Dwarka (Mithapur). Tata Chemicals dates its loss to 'July and August': the loss cannot be split between the two episodes from company documents. Archean's loss is booked to the late-August storm (Asna) alone. Largest 7-day Jun-Sep totals in 2024 were the highest since 2000 in Jamnagar (534 mm, to 30 Aug) and Porbandar (794 mm, to 22 Jul) and second in Kachchh (364 mm, to 30 Aug) (gj_rain_7day_max.csv)")
for sym, role in (("TATACHEM", "hit firm: Mithapur soda ash and salt"), ("ACI", "hit firm: Kutch salt"), ("ADANIPORTS", "hit firm: Mundra and Tuna ports"), ("GVT&D", "hit firm: Vadodara plant")):
    for i, r in G[G.nse_symbol == sym].iterrows():
        if i not in vg: continue
        sec = "Business Standard" in r.document_title
        add("1 hit firm outside the pack (Step A, G7: " + GRADE[sym] + ")", sym, role + (" (secondary: news relay of the company notice)" if sec else ""), r.document_date, r.document_title, r.source_url,
            r.quote, r.number_given, dfin=dq(sym), lag="Q2 FY25 (Jul-Sep 2024)", status="evidence" if r.what_it_shows != "no_mention" else "documented absence", note=r.notes)
G7D = RE + "g7_docs.csv"; G7 = pd.read_csv(G7D, dtype=str).fillna("") if os.path.exists(G7D) else pd.DataFrame(columns=["task"]); v7 = ok("g7_docs.csv")
for i, r in G7[G7.task.str.startswith("grade")].iterrows():
    if i in v7: add("1 hit firm outside the pack (Step A, G7: confirmed, immaterial)", r.nse_symbol, r.task, r.document_date, r.document_title, r.source_url, r.quote, status="evidence", note=r.notes)
if os.path.exists(DEL + "gj_archean_vs_peers.csv"):
    AP = pd.read_csv(DEL + "gj_archean_vs_peers.csv"); m = AP[AP.window == "(-1,5)"]
    a3, a8 = m.iloc[0], m.iloc[1]
    add("1 hit firm outside the pack (Step A, G7: material hit)", "ACI", "price fall at the storm vs specialty-chemical peers (G7)", "2024-08-23 to 2024-09-02", "outputs/deliverables/gj_archean_vs_peers.csv, gj_archean_daily_ar.csv", "",
        f"CAR {a3.car_aci:+.3f} (p={a3.p_aci:.2f}); net of the 3 G2 specialty controls {a3.net_of_peers:+.3f} (two-sided p={a3.p_net_two_sided:.2f}, one-sided {a3.p_net_one_sided_neg:.2f}); net of 8 specialty names {a8.net_of_peers:+.3f} (p={a8.p_net_two_sided:.2f})",
        status="measurement", dfin=f"rupee value of the fall about Rs {abs(a3.rupee_value_of_car_cr):,.0f} cr (Rs {abs(a3.rupee_value_net_cr):,.0f} cr net of peers) against Rs 40.18 cr booked",
        note="not attributed (the user's reading, checkpoint-4 review). The fall is spread over the window and follows a +7.5% abnormal return on 22 Aug; daily abnormal returns beside daily Kachchh rain in gj_archean_daily_ar.csv: "
             "-1.7%, -2.1%, -1.0%, -2.6% on 26-29 Aug (rain 61, 71, 98, 92 mm), and the largest fall, -4.8%, on 2 Sep (rain 1 mm). Filings 21 Aug - 24 Sep 2024 and free news show no other company event (news_checks.csv; one immaterial GST penalty on 20 Aug). "
             "Its size is 30-40 times the booked loss. Placebo days: 494 (Archean listed Nov 2022)")
TPp = DEL + "gj_tatachem_price.csv"
if os.path.exists(TPp):
    tp = pd.read_csv(TPp).set_index("item").value
    add("1 hit firm outside the pack (Step A, G7: material hit)", "TATACHEM", "own share price at the storm and on its results day (checkpoint-4 review)", "2024-08-26 to 2024-08-30; 2024-10-18",
        "outputs/deliverables/gj_tatachem_price.csv (market model estimated before 26 Aug 2024)", "",
        f"abnormal return 26-30 Aug {100*tp['sum of daily abnormal returns, 26-30 Aug 2024']:+.1f}% (CAR (0,+4) {100*tp['engine CAR (0,+4) from 26 Aug 2024']:+.1f}%, p={tp['placebo p, CAR (0,+4)']:.2f}); 18 Oct (results day) {100*tp['abnormal return 18 Oct 2024 (results day; filed 17 Oct 18:01)']:+.1f}%; daily s.d. {100*tp['daily s.d. of raw returns, estimation window']:.1f}% (raw), {100*tp['daily s.d. of market-model residuals, estimation window']:.1f}% (residual)",
        status="measurement", note="the source shock is documented in statements and tonnes and is not visible in the share price (agrees with the user's check)")
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
    status="measurement", note="abnormal returns from the market model estimated before 26 Aug 2024. Release times from the NSE filing names: Tata Consumer 18 Oct 2024 16:52 IST (after the close) -> 21 Oct is its results day: -6.7%, tea-driven by the company's account, not attributable to salt (G7 R4). Tata Chemicals 17 Oct 2024 18:01 IST -> its results day is 18 Oct (+1.1%); 10 Oct (+4.3%, after Ratan Tata's death) and 21 Oct (+10.4%, RBI ruling on Tata Sons' listing) are unrelated moves")
KP = RE + "tcpl_salt_kpis.csv"
if os.path.exists(KP):
    K = pd.read_csv(KP, dtype=str).fillna(""); vk = ok("tcpl_salt_kpis.csv")
    for i, r in K[K.metric == "sourcing_share"].iterrows():
        if i in vk: add("2 link: Tata Chemicals -> Tata Consumer (edible salt)", "TATACONSUM", "buyer side: share of salt sourced from Tata Chemicals (closes the 85% item)", r.document_date, r.document_title, r.source_url, r.quote,
                        number=r.value + " " + r.unit, status="evidence", note="Tata Consumer IAR 2022-23, Responsible Sourcing section (company web page)")
if os.path.exists(DEL + "stepC_gj_tcpl_salt.csv"):
    TS = pd.read_csv(DEL + "stepC_gj_tcpl_salt.csv")
    for r in TS.itertuples():
        add("3 downstream node: Tata Consumer salt by quarter (G7 R4 propagation measure)", "TATACONSUM", "salt revenue, volume and price " + r.period, "", "outputs/deliverables/stepC_gj_tcpl_salt.csv (from tcpl_salt_kpis.csv)", "",
            "", dfin=f"salt revenue {r.salt_revenue_growth_pct:+.0f}%, volume {r.salt_volume_growth_pct:+.0f}%, implied price/mix {r.implied_price_mix_pp:+.0f} pp".replace("nan%", "n/a").replace("+nan", "n/a"),
            lag={"Q2 FY25": "cost lagged into Q3", "Q3 FY25": "price increase in effect"}.get(r.period, ""), status="measurement",
            note=f"price action: {r.retail_price_action}; Mithapur: {r.mithapur_mentioned}; {r.note if isinstance(r.note, str) else ''}")
MGp = DEL + "stepC_gj_salt_magnitude.csv"
if os.path.exists(MGp):
    mg = pd.read_csv(MGp)
    add("3b last step: retail price of Tata Salt", "TATACONSUM", "magnitude: storm cost against the value of the 7% increase (checkpoint-4 review)", "", "outputs/deliverables/stepC_gj_salt_magnitude.csv", "",
        "", dfin="; ".join(f"{r.item}: {'not given in any document' if pd.isna(r.value_cr) else ('Rs ' + format(r.value_cr, ',.1f') + ' cr' if 'ratio' not in r.item else format(r.value_cr, '.1f') + 'x')}" for r in mg.itertuples()),
        status="measurement", note="the increase is worth about 2.8 times the storm's whole cost to Tata Chemicals in a year: partly a catch-up after two years without an increase (the company's own words)")
for i, r in G7[G7.task.str.startswith(("retail", "confound"))].iterrows():
    if i in v7: add("3b last step: retail price of Tata Salt" if r.task.startswith("retail") else "confound (downstream)", r.nse_symbol, r.task, r.document_date, r.document_title, r.source_url, r.quote,
                    status="evidence" if r.task.startswith("retail") else "confound", note=r.notes)
NW = RE + "news_checks.csv"
if os.path.exists(NW):
    N = pd.read_csv(NW, dtype=str).fillna(""); vn = ok("news_checks.csv")
    for i, r in N[(N.nse_symbol == "TATACHEM") & N.index.isin(vn)].iterrows():
        add("confound: unrelated Tata Chemicals moves (G7 R4)", "TATACHEM", r.what_happened, r.event_date, r.document_title, r.source_url, r.quote, status="confound",
            note="abnormal return " + {"2024-10-10": "+4.3% (t=+2.2) on 10 Oct 2024, the first trading day after Ratan Tata's death", "2024-10-21": "+10.4% (t=+5.3) on 21 Oct 2024"}.get(r.event_date, ""))
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
