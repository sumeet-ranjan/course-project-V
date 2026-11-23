"""NCR Step B links, with the user's decision G4 (23 Nov 2026) applied. Appended to the links file by src/40_links_file.py.

G4: R1 the cement/steel firm-level hop is not verified; a materiality bound is added: DLF's construction outflow
    (Q3 FY25 presentation: Rs 1,642 cr in FY24) against each supplier's FY24 revenue (an upper bound on DLF's share
    of that supplier's sales even if all of DLF's construction spend went to it); NBCC buys no construction materials
    itself (BRSR FY2024-25), so its direct share is zero.
    R2 all contractors are within-zone upstream nodes. AHLUCONT <- DLF verified and material (Downtown Phase-2 awarded
    11 Oct 2024, live; 3-10% bracket kept). BLKASHYAP <- DLF verified link, hit at the site not yet documented;
    BLKASHYAP <- ANANTRAJ (Rs 250 cr, 7 Nov 2024) held. JKIL <- NBCC verified, not material (low-dose row only).
    Comparison rows for the contractors screened and found unlinked, with their NCR presence.
Rules (G4): trade class (civil/structural/ready-mix work is banned under Stage III; plumbing, electrical, carpentry and
interiors are permitted); no weight dated after Dec 2024; "ACC India Pvt Ltd" (Arabian Construction Company) is not
ACC Ltd; every firm flagged external (not in the pack's 81) and in_pack_footprint.
Output: research/realign/links_new.csv
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd, numpy as np
from common import ROOT, EXT, companies, exposure
RE = ROOT + "/research/realign/"; D = "research/realign/docs/"
PACK = set(companies().nse_symbol); E = exposure(); NCR_FP = set(E[(E.zone == "NCR") & (E.share_cost > 0)].nse_symbol)
def ext(s): return "" if not s else ("no" if s in PACK else "yes")
def fp(s, ext_fp=""):
    if not s: return ""
    return ("yes" if s in NCR_FP else "no") if s in PACK else (ext_fp or "not established")
r2 = pd.read_csv(RE + "ncr_round2_docs.csv", dtype=str).fillna("") if os.path.exists(RE + "ncr_round2_docs.csv") else pd.DataFrame(columns=["nse_symbol", "task", "quote", "source_url", "saved_text", "document_date"])
def r2q(sym, task):
    x = r2[(r2.nse_symbol == sym) & (r2.task.astype(str) == str(task)) & (r2.quote != "")]
    x = x.sort_values("read_mode", key=lambda c: c != "original_pdf")   # prefer the original filing
    return (x.quote.iloc[0], x.source_url.iloc[0], x.saved_text.iloc[0], x.document_date.iloc[0]) if len(x) else ("", "", "", "")
rows = []
def link(i, sup, ss, buy, bs, product, trade, status, why, lf, lt, live, ws, src, quote, saved, read, note="", s_fp="", b_fp=""):
    rows.append(dict(link_id=f"N{i:03d}", chain="NCR", supplier=sup, supplier_symbol=ss, buyer=buy, buyer_symbol=bs, in_sample=str(ss in PACK and bs in PACK),
                     supplier_external=ext(ss), supplier_in_pack_footprint=fp(ss, s_fp), buyer_external=ext(bs), buyer_in_pack_footprint=fp(bs, b_fp),
                     product=product, trade=trade, status=status, status_reason=why, decided="G4 (user, 23 Nov 2026)", live_from=lf, live_to=lt, live_at_event=live,
                     w_supplier_sales_low=ws[0], w_supplier_sales_high=ws[1], w_supplier_sales_basis=ws[2],
                     w_buyer_input_cost_low="", w_buyer_input_cost_high="", w_buyer_input_cost_basis="buyer's construction spend by supplier not disclosed",
                     legacy_dependence="", legacy_period="", legacy_strength="", source_url=src, source_quote=quote, read_mode=read, saved_text=saved, notes=note))
WZ = "within-zone upstream node: its own NCR sites were under the same ban"
CIVIL = "civil/structural (banned under Stage III)"
# --- contractor links (R2) ---
ah = (132 / 3855.3, (5269 + 10947) / 162584)
q11, u11, s11, d11 = r2q("AHLUCONT", 1)
link(1, "Ahluwalia Contracts (India) Ltd", "AHLUCONT", "DLF Ltd", "DLF",
     "The Arbour (North Parcel), Sector 63 Gurugram: Rs 744.68 cr, awarded 3 May 2023, Rs 11-12 cr/month in Nov 2024; Downtown Phase-2 (Blocks 5-7, Sector 25A, Gurugram) for DLF City Centre: Rs 1,094.67 cr, awarded 11 Oct 2024",
     CIVIL, "verified (G4): material", WZ + "; both contracts live in Nov-Dec 2024", "2023-05-03 (Arbour); 2024-10-11 (Downtown Ph-2)", "", "yes",
     (f"{ah[0]:.3f}", f"{ah[1]:.3f}", "low: Arbour run-rate Rs 11-12 cr/month annualised / FY24 income Rs 3,855 cr (3.4-3.7%); high: DLF share of unexecuted order book at 31 Dec 2024 (10.0%)"),
     "NSE filings 3 May 2023 and 11 Oct 2024; Q2 FY25 call (Nov 2024); Q3 FY25 presentation and call (12 Feb 2025)" + (f"; {u11}" if u11 else ""),
     q11 or "has secured an order for Construction of Civil Structure & waterproofing works including Rough finishing works for North Parcel of “The Arbour Project” located at Sec-63, Gurugram (HR) worth of Rs. 744.68 Crores from DLF Home Developers Ltd.",
     s11 or D + "stepB_contractor__AHLUCONT__award_DLF_Arbour_20230503.txt", "original re-read 23 Nov 2026" + ("" if q11 else "; the 11 Oct 2024 filing: pending"),
     "33.3% of Ahluwalia's unexecuted order book is in Delhi NCR (31 Dec 2024)", s_fp="yes (NCR sites)", b_fp="")
bk = ((924.11 + 222.66) / 3311, (924.11 / 1.75) / 1214.23)
link(2, "B.L. Kashyap and Sons Ltd", "BLKASHYAP", "DLF Ltd (DLF City Centre Ltd)", "DLF",
     "civil and composite steel structural works, Mall of India DLF Downtown Phase-2 (Rs 924.11 cr, LOI 11 Jun 2024, 21 months); DLF The Arbour (Rs 222.66 cr)",
     CIVIL, "verified (G4): link; hit at the site not yet documented", WZ + "; contracts live in Nov-Dec 2024, but no document says these sites stopped",
     "2024-06-11", "about 2026-03", "yes", (f"{bk[0]:.3f}", f"{bk[1]:.3f}", "low: DLF orders in the 31 Dec 2024 order book / order book Rs 3,311 cr (34.6%); high: Downtown Ph-2 annualised over 21 months / FY24 revenue Rs 1,214 cr (43.5%)"),
     "NSE filing 11 Jun 2024; Q3 FY25 investor presentation", "MALL OF INDIA DLF DOWNTOWN PHASE -2 924.11 Cr", D + "stepB_contractor__BLKASHYAP__*", "original re-read 23 Nov 2026",
     "order book by state at 31 Dec 2024: Haryana 45.4%, Delhi 10.1%", s_fp="yes (NCR sites)")
q7, u7, s7, d7 = r2q("BLKASHYAP", 2)
link(3, "B.L. Kashyap and Sons Ltd", "BLKASHYAP", "Anant Raj Ltd", "ANANTRAJ", "order from Anant Raj, about Rs 250 cr (7 Nov 2024)", CIVIL,
     "held (G4)", "buyer is exposed but not a confirmed hit firm (G3); " + WZ, "2024-11-07", "", "yes (awarded a week before the ban)",
     ("", "", "Rs 250 cr / FY24 revenue Rs 1,214 cr = 20.6% of one year's revenue (contract value, not annualised)"),
     u7 or "NSE filing 7 Nov 2024", q7, s7, "original re-read 23 Nov 2026" if q7 else "pending: filing to be read", s_fp="yes (NCR sites)")
jk = (334.25 / 20529, (334.25 / 2) / 4879)
link(4, "J. Kumar Infraprojects Ltd", "JKIL", "NBCC (India) Ltd", "NBCC", "EPC: Hari Nagar Depot of DTC, New Delhi (Rs 334.25 cr, LOA 18 Mar 2024, 24 months)", CIVIL,
     "verified (G4): not material (low-dose row only)", WZ + "; NBCC's branch stays open: no contractor identified on Amrapali or GPRA", "2024-03-18", "about 2026-03", "yes",
     (f"{jk[0]:.3f}", f"{jk[1]:.3f}", "low: contract / order book Rs 20,529 cr at 31 Dec 2024 (1.6%); high: contract annualised over 24 months / FY24 revenue Rs 4,879 cr (3.4%)"),
     "NSE filing (LOA 18 Mar 2024)", "is in receipt of LOA in the capacity of sole bidder, from M/s. NBCC (India) Limited for the work of “Development of Hari Nagar Depot of Delhi Transport Corporation (DTC) in Delhi at Hari Nagar, New Delhi on EPC basis for the total contract value of Rs. 334,25,00,000/-",
     D + "stepB_contractor__JKIL__*", "original re-read 23 Nov 2026", s_fp="yes (Delhi site)")
link(5, "Capacit'e Infraprojects Ltd", "CAPACITE", "NBCC (India) Ltd", "NBCC", "Supreme Court monitored housing, Noida (about Rs 1,120 cr, Feb 2025)", CIVIL,
     "rejected: not live at the event date", "awarded Feb 2025, after the ban", "2025-02", "", "no", ("", "", ""), "Q3 FY25 call (Feb 2025)",
     "With the order win of yesterday from NBCC, nearly 76% of our projects are central government or government funded", D + "stepB_contractor__CAPACITE__*", "original re-read 23 Nov 2026", s_fp="yes (operating region; Noida order Feb 2025)")
# comparison rows: contractors screened and found unlinked to NBCC or DLF
COMPS = [("NCC Ltd", "NCC", "not established in the documents read"), ("PSP Projects Ltd", "PSPPROJECT", "not established in the documents read"),
         ("ITD Cementation India (now Cemindia, CEMPRO)", "CEMPRO", "yes: IKEA building 'at Delhi Noida' (Q3 FY25 call)"),
         ("Larsen & Toubro Ltd", "LT", "not established in the documents read"),
         ("Capacit'e Infraprojects Ltd", "CAPACITE", "yes: NCR listed among operating regions; Signature Global work order of 25 Oct 2024 (filing file name only, not read)")]
for k, (nm, s, ncr) in enumerate(COMPS, start=6):
    link(k, nm, s, "(none)", "", "screened: no NBCC or DLF contract in the announcement lists and Q3 FY25 documents read", "civil/structural", "comparison (no link found)",
         "contractor screened in Step B and found unlinked; used as the comparison group for the contractor nodes", "", "", "", ("", "", ""),
         "research/realign/stepB_contractors.csv", "", "", "see the Step B table", note="NCR presence: " + ncr, s_fp=("yes" if ncr.startswith("yes") else "not established"))
# --- R1: verdict on the scaffold's guesses, with the materiality bound ---
rev = {"ULTRACEMCO": 70908, "SHREECEM": 20404, "ACC": 19959, "TATASTEEL": 229171, "JSWSTEEL": 175006, "SAIL": 105378, "JINDALSTEL": 50354, "JSL": 38562}
fa = pd.read_csv(EXT + "fin_annual_peers.csv"); rev.update(dict(zip(fa.firm, fa.sales_fy24_cr)))
CONC = {"SHREECEM", "ACC", "AMBUJACEM", "JKLAKSHMI", "DALBHARAT", "TATASTEEL", "SAIL", "JINDALSTEL", "JSL"}
OUTFLOW_FY24 = 1642.0
S = pd.read_csv(ROOT + "/data/supply_chain_scaffold.csv"); S = S[S.buyer.isin(["NBCC", "DLF", "ANANTRAJ", "PARSVNATH", "UNITECH"])][["supplier", "buyer", "hint"]]
extra = pd.DataFrame([(s, b, "cement->construction" if s != "APLAPOLLO" else "steel->construction") for s in ["AMBUJACEM", "JKCEMENT", "JKLAKSHMI", "DALBHARAT", "APLAPOLLO"] for b in ["NBCC", "DLF"]],
                     columns=["supplier", "buyer", "hint"])
S = pd.concat([S, extra], ignore_index=True)
for k, r in enumerate(S.itertuples(), start=20):
    trade = "material for civil work (cement; ready-mix plants banned under Stage III)" if "cement" in r.hint else "material for civil/structural work (steel)"
    if r.buyer == "DLF":
        b = OUTFLOW_FY24 / rev[r.supplier] if r.supplier in rev else np.nan
        hi = min([x for x in [b, 0.10 if r.supplier in CONC else np.nan] if pd.notna(x)], default=np.nan)
        basis = "; ".join([x for x in [f"DLF construction outflow FY24 Rs 1,642 cr / supplier FY24 revenue Rs {rev[r.supplier]:,.0f} cr = {b:.1%}" if pd.notna(b) else "",
                                       "supplier's Ind AS 108 note: no customer >= 10% of revenue" if r.supplier in CONC else ""] if x])
        why = ("not verified (G4 R1): no relationship found in either party's documents (DLF names no supplier, nil related-party purchases; the supplier's documents read do not mention DLF). "
               "Materiality bound: even if all of DLF's construction outflow went to this supplier, DLF would be at most the share shown of its sales")
        st = "not verified"; ws = ("", f"{hi:.3f}" if pd.notna(hi) else "", basis)
    elif r.buyer == "NBCC":
        why = "not verified (G4 R1): NBCC does not procure construction materials itself (BRSR FY2024-25); its contractors do. No document links this supplier to NBCC or its contractors"
        st = "not verified"; ws = ("0", "0", "NBCC's direct purchases of construction materials: none (BRSR FY2024-25)")
    else:
        why, st, ws = "not searched: the builder is exposed but not a confirmed hit firm (G3)", "not searched", ("", "", "")
    note = "replaces the scaffold's industry-level guess" if r.supplier not in extra.supplier.values else "supplier screened in Step B (outside the pack)"
    if r.supplier == "ACC":
        note += "; trap: 'ACC India Pvt Ltd' (contractor on DLF Privana South) is the Arabian Construction Company subsidiary, not ACC Ltd; not matched to the cement firm"
    link(k, r.supplier, r.supplier, r.buyer, r.buyer, f"scaffold guess ({r.hint})" if r.supplier not in extra.supplier.values else f"candidate supplier ({r.hint})",
         trade, st, why, "", "", "", ws, "research/realign/stepB_builder_side.csv; research/realign/stepB_supplier_side.csv", "", "", "see the two Step B tables", note=note)
o = pd.DataFrame(rows); o.to_csv(RE + "links_new.csv", index=False)
print(o.groupby("status").size().to_string())
print(o[o.link_id < "N011"][["supplier_symbol", "buyer_symbol", "status", "w_supplier_sales_low", "w_supplier_sales_high", "read_mode"]].to_string(index=False))
print(o[(o.buyer_symbol == "DLF") & (o.status == "not verified")][["supplier_symbol", "w_supplier_sales_high", "w_supplier_sales_basis"]].to_string(index=False))
