"""Step B (NCR) links for decision G4: contractor links found in original documents, and a verdict on every scaffold
pair of a cement/steel firm with an NCR builder. Appended to the links file by src/40_links_file.py.

Dependence weight w_supplier_sales = the builder's share of the upstream firm's sales (backward test, H3),
bracketed from the contractors' own documents (stepB_contractors.csv, quotes checked by src/42):
  AHLUCONT <- DLF   low: The Arbour run-rate Rs 11-12 cr/month x 12 / FY24 income from operations Rs 3,855.3 cr;
                    high: DLF's unexecuted orders (Rs 5,269 + 10,947 mn) / total unexecuted order book (Rs 162,584 mn), 31 Dec 2024
  BLKASHYAP <- DLF  low: DLF orders listed in the 31 Dec 2024 order book (924.11 + 222.66 cr) / order book 3,311 cr;
                    high: Mall of India Downtown Ph-2 (924.11 cr over 21 months, annualised) / FY24 revenue 1,214.23 cr
  JKIL <- NBCC      low: Hari Nagar DTC depot (334.25 cr) / order book 20,529 cr (31 Dec 2024);
                    high: the same contract annualised over 24 months / FY24 revenue 4,879 cr
Output: research/realign/links_new.csv
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from common import ROOT
RE = ROOT + "/research/realign/"
D = "research/realign/docs/"
G4 = "candidate: decision G4 pending"
WZ = "the upstream firm's own NCR sites were under the same ban, so it is a within-zone node, not an out-of-zone propagation target"
rows = []
def link(i, sup, sup_sym, buy, buy_sym, product, status, why, lf, lt, live, ws, src, quote, saved, note=""):
    rows.append(dict(link_id=f"N{i:03d}", chain="NCR", supplier=sup, supplier_symbol=sup_sym, buyer=buy, buyer_symbol=buy_sym, in_sample="False", product=product,
                     status=status, status_reason=why, decided="", live_from=lf, live_to=lt, live_at_event=live,
                     w_supplier_sales_low=ws[0], w_supplier_sales_high=ws[1], w_supplier_sales_basis=ws[2],
                     w_buyer_input_cost_low="", w_buyer_input_cost_high="", w_buyer_input_cost_basis="buyer's construction spend not disclosed",
                     legacy_dependence="", legacy_period="", legacy_strength="", source_url=src, source_quote=quote, read_mode="original re-read 23 Nov 2026", saved_text=saved, notes=note))
ah = 132 / 3855.3; ah2 = 144 / 3855.3; ahb = (5269 + 10947) / 162584
link(1, "Ahluwalia Contracts (India) Ltd", "AHLUCONT", "DLF Ltd", "DLF",
     "construction contracts: The Arbour (North Parcel), Sector 63 Gurugram (Rs 744.68 cr, May 2023); DLF City Center Downtown (Rs 1,094.7 cr, nothing executed by 31 Dec 2024)",
     G4, "documented contracts running in Nov-Dec 2024 (The Arbour at Rs 11-12 cr/month in Nov 2024); " + WZ, "2023-05-03", "", "yes (The Arbour)",
     (f"{ah:.3f}", f"{ahb:.3f}", f"low: Arbour run-rate Rs 11-12 cr/month annualised / FY24 income Rs 3,855 cr ({ah:.1%}-{ah2:.1%}); high: DLF share of unexecuted order book at 31 Dec 2024 ({ahb:.1%})"),
     "NSE filing 3 May 2023; Q2 FY25 call (Nov 2024); Q3 FY25 presentation and call (Feb 2025)",
     "has secured an order for Construction of Civil Structure & waterproofing works including Rough finishing works for North Parcel of “The Arbour Project” located at Sec-63, Gurugram (HR) worth of Rs. 744.68 Crores from DLF Home Developers Ltd.",
     D + "stepB_contractor__AHLUCONT__*", "33.3% of Ahluwalia's unexecuted order book is in Delhi NCR (31 Dec 2024)")
bk_lo = (924.11 + 222.66) / 3311; bk_hi = (924.11 / 1.75) / 1214.23
link(2, "B.L. Kashyap and Sons Ltd", "BLKASHYAP", "DLF Ltd (DLF City Centre Ltd)", "DLF",
     "civil and composite steel structural works, Mall of India DLF Downtown Phase-2 (Rs 924.11 cr, LOI 11 Jun 2024, 21 months); DLF The Arbour (Rs 222.66 cr)",
     G4, "documented contract running in Nov-Dec 2024 (21-month term from Jun 2024); " + WZ, "2024-06-11", "2026-03 (21 months, approx.)", "yes",
     (f"{bk_lo:.3f}", f"{bk_hi:.3f}", f"low: DLF orders listed in the 31 Dec 2024 order book / order book Rs 3,311 cr ({bk_lo:.1%}); high: Downtown Ph-2 annualised over 21 months / FY24 revenue Rs 1,214 cr ({bk_hi:.1%})"),
     "NSE filing 11 Jun 2024; Q3 FY25 investor presentation (7 Feb 2025)", "MALL OF INDIA DLF DOWNTOWN PHASE -2 924.11 Cr", D + "stepB_contractor__BLKASHYAP__*",
     "order book by state at 31 Dec 2024: Haryana 45.4%, Delhi 10.1%. The listed order-book values may be total contract values, not the unexecuted part.")
jk_lo = 334.25 / 20529; jk_hi = (334.25 / 2) / 4879
link(3, "J. Kumar Infraprojects Ltd", "JKIL", "NBCC (India) Ltd", "NBCC",
     "EPC contract: development of Hari Nagar Depot of DTC, New Delhi (Rs 334.25 cr, LOA 18 Mar 2024, 24 months)",
     G4, "documented contract running in Nov-Dec 2024 (24-month term from Mar 2024); " + WZ, "2024-03-18", "2026-03 (24 months)", "yes",
     (f"{jk_lo:.3f}", f"{jk_hi:.3f}", f"low: contract / order book Rs 20,529 cr at 31 Dec 2024 ({jk_lo:.1%}); high: contract annualised over 24 months / FY24 revenue Rs 4,879 cr ({jk_hi:.1%})"),
     "NSE filing (LOA 18 Mar 2024)",
     "is in receipt of LOA in the capacity of sole bidder, from M/s. NBCC (India) Limited for the work of “Development of Hari Nagar Depot of Delhi Transport Corporation (DTC) in Delhi at Hari Nagar, New Delhi on EPC basis for the total contract value of Rs. 334,25,00,000/-",
     D + "stepB_contractor__JKIL__*", "NBCC's other J. Kumar contract named in Q3 FY25 (Silicon City Phase-IV) has no location in the text read and a truncated value; not counted")
link(4, "Capacit'e Infraprojects Ltd", "CAPACITE", "NBCC (India) Ltd", "NBCC", "NBCC project for Supreme Court monitored housing, Noida (about Rs 1,120 cr, Feb 2025)",
     "rejected: not live at the event date", "awarded in Feb 2025, after the Nov-Dec 2024 ban", "2025-02", "", "no", ("", "", ""),
     "Q3 FY25 call (17 Feb 2025)", "With the order win of yesterday from NBCC, nearly 76% of our projects are central government or government funded", D + "stepB_contractor__CAPACITE__*")
# verdict on the scaffold's guesses for the NCR builders
S = pd.read_csv(ROOT + "/data/supply_chain_scaffold.csv")
S = S[S.buyer.isin(["NBCC", "DLF", "ANANTRAJ", "PARSVNATH", "UNITECH"])]
CONC = {"SHREECEM", "ACC", "TATASTEEL", "SAIL", "JINDALSTEL", "JSL"}  # Ind AS 108 'no customer >= 10%' read (stepB_supplier_side.csv)
for k, r in enumerate(S.itertuples(), start=10):
    if r.buyer in ("NBCC", "DLF"):
        why = ("not verified: no relationship found in either party's documents. NBCC does not procure construction materials (BRSR FY2024-25); "
               "DLF names no supplier and has nil related-party purchases (BRSR FY2024-25); the supplier's documents read do not mention NBCC or DLF")
        if r.supplier in CONC: why += "; the supplier states no customer is 10% or more of its revenue (so the builder's share is below 10%)"
        st = "not verified"
    else:
        why, st = "not searched: the builder is exposed but not a confirmed hit firm (G3)", "not searched"
    rows.append(dict(link_id=f"N{k:03d}", chain="NCR", supplier=r.supplier, supplier_symbol=r.supplier, buyer=r.buyer, buyer_symbol=r.buyer, in_sample="True",
                     product=f"scaffold guess ({r.hint})", status=st, status_reason=why, decided="", live_from="", live_to="", live_at_event="",
                     w_supplier_sales_low="", w_supplier_sales_high="0.10" if (r.buyer in ("NBCC", "DLF") and r.supplier in CONC) else "",
                     w_supplier_sales_basis="Ind AS 108 major-customer note" if (r.buyer in ("NBCC", "DLF") and r.supplier in CONC) else "",
                     w_buyer_input_cost_low="", w_buyer_input_cost_high="", w_buyer_input_cost_basis="", legacy_dependence="", legacy_period="", legacy_strength="",
                     source_url="research/realign/stepB_builder_side.csv; research/realign/stepB_supplier_side.csv", source_quote="", read_mode="see the two Step B tables",
                     saved_text="", notes="replaces the scaffold's industry-level guess"))
o = pd.DataFrame(rows); o.to_csv(RE + "links_new.csv", index=False)
print(o.groupby("status").size().to_string()); print(o[o.link_id < "N010"][["supplier_symbol", "buyer_symbol", "status", "w_supplier_sales_low", "w_supplier_sales_high"]].to_string(index=False))
