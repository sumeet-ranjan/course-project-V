"""Deliverable 1, NCR: evidence table per node along the traced pathway (decisions G3, G4).

event (GRAP orders) -> hit firms (NBCC, DLF) -> within-zone upstream contractors (AHLUCONT material, BLKASHYAP site hit
not documented, JKIL not material) -> cement/steel (firm-level hop not verified; market-level branch shown separately).
Columns follow INSTRUCTIONS §6 (date, source, quote, CAR, delta-financial, lag) plus the flags required by G4
(external = not in the pack's 81; in_pack_footprint; trade). Quotes come only from tables that passed
src/42_check_quotes_realign.py, or from the official PIB releases in the record. CARs: stepC_ncr_node_cars.csv
(market model; p-values from each firm's own placebo distribution). Quarterly changes: stepC_ncr_quarterly.csv (screener.in)
and, where stated, the company's own document.
Output: outputs/deliverables/evidence_NCR.csv
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd, numpy as np
from common import ROOT, OUT, plants, ZONES, companies
RE = ROOT + "/research/realign/"; DEL = OUT + "deliverables/"
PACK = set(companies().nse_symbol)
qc = pd.read_csv(RE + "quote_check_realign.csv")
ok = lambda f: set(qc[(qc.file == f) & (qc.status == "verified")].row)
NC = pd.read_csv(DEL + "stepC_ncr_node_cars.csv"); Q = pd.read_csv(DEL + "stepC_ncr_quarterly.csv")
NET = pd.read_csv(DEL + "stepC_ncr_contractor_net.csv") if os.path.exists(DEL + "stepC_ncr_contractor_net.csv") else pd.DataFrame(columns=["nse_symbol"])
def net(sym):
    """G5: every contractor window net of the unlinked-contractor mean, placebo p for the difference (src/55)."""
    x = NET[NET.nse_symbol == sym]
    if not len(x): return ""
    lab = lambda r: ("18 Nov" if r.event.startswith("18 Nov") else "17 Dec" if r.event.startswith("17 Dec") else "12 Feb") + " " + r.window
    def one(r):
        t = f"{lab(r)} {r.net_of_unlinked:+.3f} (p={r.p_net_two_sided:.2f}); without the takeover targets {r.net_ex_targets:+.3f} (p={r.p_net_ex_targets_two_sided:.2f})"
        if pd.notna(getattr(r, "net_of_unlinked_zero_alpha", np.nan)): t += f"; zero-alpha {r.net_of_unlinked_zero_alpha:+.3f} (p={r.p_net_zero_alpha:.2f})"
        return t
    return " | ".join(one(r) for r in x.itertuples())
def car(sym, ev, w):
    x = NC[(NC.nse_symbol == sym) & (NC.event == ev) & (NC.window == w)]
    return f"{x.car.iloc[0]:+.3f} (p={x.p_two_sided.iloc[0]:.2f})" if len(x) and pd.notna(x.car.iloc[0]) else ""
def dq(sym):
    x = Q[(Q.nse_symbol == sym) & (Q.quarter == "2024-12-31")]
    if not len(x): return ""
    r = x.iloc[0]; return f"Q3 FY25 sales {r.sales_yoy_pct:+.1f}% YoY, {r.sales_qoq_pct:+.1f}% QoQ; OPM {r.opm_pct:.1f}% ({r.opm_change_yoy_pp:+.1f} pp YoY) [screener.in]"
rows = []
def add(node, sym, role, date, source, url, quote, dfin="", lag="", status="evidence", note="", trade="", ext=None, fp=None):
    rows.append(dict(node=node, firm_symbol=sym, external=(ext if ext is not None else ("" if not sym else ("no" if sym in PACK else "yes"))),
                     in_pack_footprint=(fp if fp is not None else ""), role=role, trade=trade, date=date, source=source, source_url=url, quote=quote,
                     car_18nov_m1_3=car(sym, "18 Nov 2024", "(-1,3)") if sym else "", car_18nov_m1_5=car(sym, "18 Nov 2024", "(-1,5)") if sym else "",
                     car_18nov_6_20=car(sym, "18 Nov 2024", "(6,20)") if sym else "", car_18nov_21_60=car(sym, "18 Nov 2024", "(21,60)") if sym else "",
                     car_17dec_m1_5=car(sym, "17 Dec 2024", "(-1,5)") if sym else "", car_17dec_6_20=car(sym, "17 Dec 2024", "(6,20)") if sym else "",
                     net_of_unlinked_contractors=net(sym) if sym in ("AHLUCONT", "BLKASHYAP", "JKIL") else "",
                     delta_financial=dfin, lag=lag, status=status, note=note))
# 0 event
h = pd.read_csv(ROOT + "/research/proxy/official_hazard_records.csv", dtype=str).fillna("")
h = h[(h.task == "A_grap_orders") & (h.event == "GRAP_winter_2024") & (h.item.isin(["order", "construction_clause"]))]
for r in h.sort_values("date").itertuples():
    add("0 event: GRAP orders (CAQM)", "", f"{r.stage_or_station} {r.action}".strip(), r.date, r.source_name, r.source_url, r.source_quote, note=r.time)
# 1-2 hit firms
p = plants(); tot = p.groupby("nse_symbol").project_cost_cr.sum()
A = pd.read_csv(RE + "ncr_stepA_evidence.csv", dtype=str).fillna(""); va = ok("ncr_stepA_evidence.csv")
for f in ("NBCC", "DLF"):
    z = p[(p.nse_symbol == f) & p.dist_name.isin(ZONES["NCR"])]
    add("1 exposed plants (pack)", f, "hit firm's NCR sites", "", "data/plants.csv", "", f"{len(z)} NCR sites; {z.project_cost_cr.sum() / tot[f]:.0%} of plant cost", fp="yes",
        note="districts: " + ", ".join(sorted(z.dist_name.unique())))
for i, r in A.iterrows():
    if r.nse_symbol in ("NBCC", "DLF") and i in va and r.what_it_shows in ("names_ban", "delay_or_stoppage"):
        add("2 hit firm (confirmed, G3)", r.nse_symbol, "builder under the construction ban", r.document_date, r.document_title, r.source_url, r.quote, fp="yes",
            dfin=dq(r.nse_symbol), lag="same quarter (Oct-Dec 2024), per the company", note=r.notes, trade="developer / project manager (civil work on site banned)")
add("2 hit firm (confirmed, G3)", "DLF", "construction outflow by quarter", "2025-01-24", "DLF Q3 FY25 investor presentation (cash flow slide)", "",
    "Outflow •Construction 1,642 1,535 424 521 591", fp="yes",
    dfin="construction outflow Rs 424 cr (Q1 FY25), 521 cr (Q2), 591 cr (Q3, the ban quarter): +13% QoQ; FY24 Rs 1,642 cr; 9M FY25 Rs 1,535 cr", lag="none visible in the cash spend",
    note="columns: FY24, 9MFY25, Q1FY25, Q2FY25, Q3FY25 (saved text research/realign/docs/ncrA__DLF__Q3FY25_investor_presentation.txt)")
add("2 hit firm (confirmed, G3)", "DLF", "the two delayed malls (G4 R4: Summit Plaza, Gurugram; Midtown Plaza, Delhi)", "2025-01-27", "DLF Q3 FY25 call; DLF Q3 FY25 investor presentation", "",
    "The construction on the 3 malls, which are in the DLF portfolio, which totalled up to 1.3 million, is moving… [audio drop] … Which was in the 2 malls in the Delhi NCR were a little delayed because of the GRAP and the stoppage of construction. | Summit Plaza, DLF 5, Gurugram [0.4 msf] ; Midtown Plaza, Delhi [0.3 msf]; DLF Promenade, Goa [0.7 msf]",
    fp="yes", note="identification by the user (G4 R4); contractor of the two plazas not identified (Tata Projects / ONE Midtown being checked)")
for f in ("NBCC", "DLF"):
    n = A[(A.nse_symbol == f) & (A.what_it_shows == "no_mention")]
    add("2 hit firm (confirmed, G3)", f, "documents read with no mention", "", "; ".join(n.document_title), "", "", status="documented absence", fp="yes")
# 3 contractors (within-zone upstream)
L = pd.read_csv(DEL + "verified_links.csv", dtype=str).fillna("")
for r in L[L.link_id.isin(["N001", "N002", "N003", "N004"])].itertuples():
    add("3 within-zone upstream contractor (G4)", r.supplier_symbol, f"{r.status}; link {r.supplier_symbol} <- {r.buyer_symbol}", r.live_from, r.source_url, "", r.source_quote,
        dfin=dq(r.supplier_symbol), lag="", trade=r.trade, fp="yes (NCR sites)",
        note=f"{r.product}. Builder's share of the contractor's sales: {r.w_supplier_sales_low or '?'}-{r.w_supplier_sales_high or '?'} ({r.w_supplier_sales_basis})")
AH = pd.read_csv(RE + "ahlucont_q2q3_quotes.csv", dtype=str).fillna(""); vah = ok("ahlucont_q2q3_quotes.csv")
for i, r in AH.iterrows():
    if i in vah:
        add("3 within-zone upstream contractor (G4)", "AHLUCONT", "breadcrumb: " + r.notes, r.document_date, r.document_title, r.source_url, r.quote, trade="civil/structural (banned under Stage III)",
            fp="yes (NCR sites)", lag="Q3 FY25 and January 2025; restart 3-4 Feb 2025" if "Q3" in r.document_title else "Q3 FY25 (expected in Nov 2024)",
            note="own Q2 FY25 results 14 Nov 2024 after the close and call on 18 Nov fall in the (-1,+5) window" if "Q2" in r.document_title else "")
TD = RE + "g5_timing_docs.csv"
if os.path.exists(TD):
    G5 = pd.read_csv(TD, dtype=str).fillna(""); vg5 = ok("g5_timing_docs.csv")
    for i, r in G5.iterrows():
        if i not in vg5: continue
        out = r.task.startswith("outcome")
        add("3 within-zone upstream contractor (G4)", "AHLUCONT", r.task, r.document_date, r.document_title, r.source_url, r.quote, trade="civil/structural (banned under Stage III)", fp="yes (NCR sites)",
            dfin=("Q4 FY25 turnover Rs 1,215.84 cr, +4.48% YoY; FY25 Rs 4,098.62 cr vs 3,855.29 cr, +6.3%, below the 8.5-9% guided on 12 Feb 2025 (company's own figures)" if out else ""),
            lag=("about two months of Q3 FY25 and nearly a month of Q4 FY25 (company's account)" if "lost months" in r.task else ""), status="evidence", note=r.notes)
    add("3 within-zone upstream contractor (G4)", "AHLUCONT", "price evidence (corrected at G5)", "", "outputs/deliverables/stepC_ncr_contractor_net.csv, stepC_ncr_disclosure_days.csv", "",
        "", trade="civil/structural (banned under Stage III)", fp="yes (NCR sites)", status="measurement",
        note="Results days and call days, net of the unlinked contractors; in brackets, without the two takeover targets (PSP Projects: Adani Infra open offer, 19 Nov 2024; Cemindia, then ITD Cementation: Renew Exim DMCC open offer, 25 Oct 2024). "
             "18 Nov 2024 = day 0 of the ban and Ahluwalia's Q2 results day; not separable: -4.7% (p=0.04) [-4.4%, p=0.05]. Beside it, B.L. Kashyap, which filed nothing between 11 Nov and 31 Dec 2024: -5.4% (p=0.06) [-5.0%, p=0.07]. "
             "19 Nov = first day the Q2 call is priced (call 3.00 pm on 18 Nov; GRAP-IV statement on page 8 of 13): -1.3% (p=0.55) [-0.1%, p=0.95]. "
             "12 Feb 2025 = Q3 results day: -4.0% (p=0.08) [-4.2%, p=0.06]. 13 Feb = first day the Q3 call (guidance cut) is priced: -2.2% (p=0.28) [-2.7%, p=0.24]. "
             "The call days, which price the company's ban statements, are not distinguishable from zero. "
             "(-1,+5) from 18 Nov: Ahluwalia -7.8% (p=0.21) [-11.6%, p=0.08]; B.L. Kashyap +0.1% (p=0.99) [-3.7%, p=0.61]. "
             "Late falls: (+21,+60) from 18 Nov -31.9% (p=0.04) [-25.6%, p=0.11]; zero-alpha -26.7% (p=0.06) [-19.4%, p=0.15]. (+6,+20) from 17 Dec -17.5% (p=0.07) [-14.1%, p=0.13]; zero-alpha -17.1% (p=0.08). "
             "They contain no Ahluwalia disclosure and are not attributed.")
    OB = RE + "contractor_ncr_orderbook.csv"
    if os.path.exists(OB):
        ob = pd.read_csv(OB, dtype=str).fillna(""); vob = ok("contractor_ncr_orderbook.csv")
        for i, r in ob.iterrows():
            if i in vob and r.nse_symbol in ("AHLUCONT", "BLKASHYAP") and r.metric in ("ncr_share_of_order_book", "state_share_of_order_book"):
                add("3 within-zone upstream contractor (G4)", r.nse_symbol, "own direct exposure: NCR share of order book (" + r.geography_detail + ")", r.as_of, r.document_title, r.source_url, r.quote,
                    trade="civil/structural (banned under Stage III)", fp="yes (NCR sites)", status="evidence",
                    note=("directly exposed: a third of its order book is in NCR (checkpoint-4 review)" if r.nse_symbol == "AHLUCONT" and r.metric == "ncr_share_of_order_book" else r.notes))
    NWp = RE + "news_checks.csv"
    if os.path.exists(NWp):
        nw = pd.read_csv(NWp, dtype=str).fillna(""); vnw = ok("news_checks.csv")
        for i, r in nw[nw.nse_symbol == "AHLUCONT"].iterrows():
            if i in vnw: add("3 within-zone upstream contractor (G4)", "AHLUCONT", "timing: Q2 results day, morning", r.event_date, r.document_title, r.source_url, r.quote,
                             trade="civil/structural (banned under Stage III)", fp="yes (NCR sites)", status="evidence", note=r.notes)
NWp2 = RE + "news_checks.csv"
if os.path.exists(NWp2):
    nw2 = pd.read_csv(NWp2, dtype=str).fillna(""); vnw2 = ok("news_checks.csv")
    for i, r in nw2[nw2.nse_symbol.isin(["PSPPROJECT", "CEMPRO", "BLKASHYAP"])].iterrows():
        if i in vnw2:
            add("3 comparison contractors: flags (checkpoint-5 review)", r.nse_symbol, r.what_happened, r.event_date, r.document_title, r.source_url, r.quote,
                status=("flag: takeover target in the windows" if r.nse_symbol != "BLKASHYAP" else "clean comparison: no filing 12 Nov - 30 Dec 2024"), note=r.notes)
NBp = RE + "nbcc_contractors.csv"
if os.path.exists(NBp):
    nb = pd.read_csv(NBp, dtype=str).fillna(""); vnb = ok("nbcc_contractors.csv")
    for i, r in nb.iterrows():
        if r.task in ("A_link", "C_capacite") and (i in vnb or r.read_mode == "search_snippet"):
            add("3 NBCC's upstream branch (closed at checkpoint 4)", "", f"{r.task}: {r.contractor_entity} ({r.project})", r.document_date, r.document_title, r.source_url, r.quote,
                status=("break: contractor unlisted: no price or filed quarterly data" if r.task == "A_link" else "after the event"), note=f"listed in Nov 2024: {r.listed_nov2024}; {r.notes}")
# 4 cement/steel: firm-level hop not verified; market-level branch
add("4 cement/steel supplier (firm level)", "", "builder -> cement/steel supplier", "", "outputs/deliverables/verified_links.csv (rows N020 onward)", "", "",
    status="break: not verified (G4 R1)", trade="material for civil work",
    note="no relationship in either side's documents; DLF's FY24 construction outflow is at most 0.7%-14% of any listed supplier's FY24 revenue (10% cap where the supplier states no customer >= 10%)")
SP = pd.read_csv(RE + "stepB_supplier_side.csv", dtype=str).fillna(""); vs = ok("stepB_supplier_side.csv")
for i, r in SP.iterrows():
    if r.relation_type == "ncr_ban_mention" and i in vs:
        add("4b cement market-level branch (not a firm link, G4 R3)", r.nse_symbol, "supplier statement", r.document_date, r.document_title, r.source_url,
            "North ✓ Housing segment registered growth in both rural and urban areas. ✓ Infrastructure segment registered degrowth on account of pollution control measures taken in Delhi and surrounding regions, projects on hold due to farmers agitation in Punjab and completion of major projects like RRTS. ✓ Commercial segment registered overall growth.",
            status="market-level evidence", trade="cement", fp="no", note="UltraTech's full North row (Q3 FY25 sectoral update): housing and commercial grew; only infrastructure fell, for three stated reasons")
# checkpoint-5 review: cement makers that deliver to NCR (main cement result), with the CCI order's district bids as corroboration
CF = DEL + "table2_cement_fit.csv"; CMK = DEL + "table2_cement_makers.csv"
if os.path.exists(CF) and os.path.exists(CMK):
    cf = pd.read_csv(CF); mk = pd.read_csv(CMK)
    main = cf[(cf["sample"].str.startswith("all")) & (cf.dose == "near300_n") & (cf.control.fillna("") == "north_rest_n")]
    for r in main.itertuples():
        tk = cf[(cf.outcome == r.outcome) & (cf["sample"] == r.sample.replace("all", "without takeover-related")) & (cf.dose == "near300_n") & (cf.control.fillna("") == "north_rest_n")]
        tks = f"; without takeover-related makers {tk.coef.iloc[0]:+.3f} (p={tk.p_two_sided.iloc[0]:.2f}, n={int(tk.n.iloc[0])})" if len(tk) and pd.notna(tk.coef.iloc[0]) else ""
        for lab, smp, dz, ct in (("capacity-weighted", r.sample, "near300_cap", "north_rest_cap"), ("without Mangalam", r.sample.replace("all", "all, without Mangalam"), "near300_n", "north_rest_n")):
            q_ = cf[(cf.outcome == r.outcome) & (cf["sample"] == smp) & (cf.dose == dz) & (cf.control.fillna("") == ct)]
            if len(q_) and pd.notna(q_.coef.iloc[0]): tks += f"; {lab} {q_.coef.iloc[0]:+.3f} (p={q_.p_two_sided.iloc[0]:.2f})"
        add("4c cement makers that deliver to NCR (main cement result, checkpoint 5)", "", f"test: {r.outcome}", "", "outputs/deliverables/table2_cement_fit.csv", "",
            f"coefficient on near300_n (share of the maker's cement plants within 300 km of Delhi by road), controlling for its other northern plants: {r.coef:+.3f} "
            f"(p={r.p_two_sided:.2f}, n={int(r.n)}, of which {int(r.n_exposed)} with plants near Delhi){tks}; other northern plants {r.coef_control:+.3f}",
            status="market-level test (specification written before the run; null)", trade="cement",
            note=(f"implied by a full 30-day stop of all NCR-near output: {r.implied_full_loss_coef:+.3f} against a null s.d. of {r.null_sd:.3f}; detectable: {r.detectable}" if pd.notna(r.implied_full_loss_coef)
                  else "a hit would make the coefficient negative; the largest possible loss (30 days of near-Delhi sales) is too small for a CAR test to detect (table2_notes.md)"))
    for r in mk[mk.near300_n > 0].sort_values("near300_n", ascending=False).itertuples():
        add("4c cement makers that deliver to NCR (main cement result, checkpoint 5)", r.maker, "dose: share of its cement plants within 300 km of Delhi by road (plant count)", "Nov 2024", "outputs/deliverables/table2_cement_makers.csv (plants from original documents; OSRM road km)", "",
            f"plants within 300 km: {r.plants_within_300} ({r.near300_n:.2f} of its {int(r.n_plants)} plants; within 150 km {r.near150_n:.2f}; northern plants beyond 300 km {r.north_rest_n:.2f}); largest possible Q3 loss about {r.max_loss_share_q3:.1%} of output",
            status="dose", trade="cement", note=(f"takeover-related: {r.takeover_flag}" if isinstance(r.takeover_flag, str) and r.takeover_flag else ""))
    # Q3 FY25 statements on NCR by the makers with plants near Delhi (checkpoint-5 review)
    near = set(mk[mk.near300_n > 0].maker)
    for k in "ABC":
        f = RE + f"cement_kpis_{k}.csv"
        if not os.path.exists(f): continue
        kk = pd.read_csv(f, dtype=str).fillna(""); vk = ok(f"cement_kpis_{k}.csv")
        for i, r in kk.iterrows():
            if r.maker_symbol in near and r.metric in ("none_found", "ncr_statement") and r.quarter.replace(" ", "").upper() == "Q3FY25":
                add("4c cement makers that deliver to NCR: Q3 FY25 statements on NCR", r.maker_symbol, "Q3 FY25 call or deck: Delhi, NCR, pollution, GRAP or ban", r.document_date, r.document_title, r.source_url,
                    r.quote if i in vk else "", status=("statement (not about the ban)" if r.metric == "ncr_statement" else "none found"), trade="cement", note=r.notes)
MAK = RE + "nbcc_makes_cci_rmc.csv"
if os.path.exists(MAK):
    mak = pd.read_csv(MAK, dtype=str).fillna(""); vmak = ok("nbcc_makes_cci_rmc.csv")
    for i, r in mak.iterrows():
        if i in vmak and r.task.startswith("C_"):
            add("4c who delivers: CCI order of 19 Jan 2017 (Haryana tender of 2012)", r.maker_or_brand, r["item"], r.document_date, r.document_title, r.source_url, r.quote,
                status="corroboration (not in the regression)", trade="cement", note=(r.location_or_district + "; " + r.notes).strip("; "))
        elif r.task.startswith(("A_", "D_")) and r["item"] in ("none_found", "failed_fetch"):     # r["item"]: r.item is the pandas method
            add("4c who delivers: NBCC approved makes and NCR ready-mix plants", "", f"{r.task}: {r['item']}", r.document_date, r.document_title, r.source_url, "",
                status="not obtained", trade="cement / rebar", note=r.notes)
add("4d steel (rebar)", "", "approved rebar makes and mill locations", "", "NBCC tender documents (not readable: e-procurement portal behind a CAPTCHA, not attempted)", "", "",
    status="stops at the materiality bound (no regression)", trade="steel",
    note="DLF's FY24 construction outflow (Rs 1,642 cr) is at most 0.7% (Tata Steel), 0.9% (JSW Steel), 1.6% (SAIL), 3.3% (JSPL), 4.3% (Jindal Stainless) of a steel maker's FY24 revenue (verified_links.csv)")
if os.path.exists(DEL + "cement_market_test.csv"):
    T = pd.read_csv(DEL + "cement_market_test.csv"); T = T[T.spec.str.startswith("main")]
    add("4b cement market-level branch (not a firm link, G4 R3)", "", "variant against the two documented zero-capacity makers only", "", "outputs/deliverables/cement_market_test.csv", "", "",
        status="run, not interpreted (G5)", trade="cement", note="+10.6 pp over (-1,+5), p = 0.005; not interpreted because it rests on two firms: Star Cement (-9.2%), with no company news found for 14-26 Nov 2024, and Prism Johnson (-5.9%), whose fall follows its loss-making Q2 FY25 results of 13 Nov 2024")
    for r in T.itertuples():
        add("4b cement market-level branch, northern capacity share (comparison; superseded at checkpoint 5)", "", f"market test {r.event} {r.window}", "", "outputs/deliverables/cement_market_test.csv", "",
            f"{r.spec}: makers with northern capacity minus makers with none {r.gap_north_minus_none:+.3f} (p={r.p_two_sided:.2f}); CAR north {r.car_north:+.3f} (n={r.n_north}), none {r.car_none:+.3f} (n={r.n_none})",
            status="market-level test (G5: the result; little power)", trade="cement")
else:
    add("4b cement market-level branch (not a firm link, G4 R3)", "", "market test", "", "", "", "", status="pending: capacity data")
o = pd.DataFrame(rows); o.to_csv(DEL + "evidence_NCR.csv", index=False)
print(o.groupby(["node", "status"]).size().to_string())
