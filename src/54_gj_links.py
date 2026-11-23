"""Gujarat forward chain (H2) link: Tata Chemicals (Mithapur salt) -> Tata Consumer Products (edible salt). Decision G7 pending.
Appended to the links file by src/40_links_file.py. Weights are for FY2023-24 (before the Aug 2024 storm), from the two
firms' own documents (research/realign/gj_tata_chain_docs.csv, quotes checked by src/42):
  purchases: Tata Consumer's related-party disclosures, Rs 758.46 cr (H1 FY24) + Rs 818.18 cr (H2 FY24) = Rs 1,576.64 cr;
  Tata Chemicals' standalone note: one customer = 36% of FY24 revenue (Rs 4,384 cr -> about Rs 1,578 cr, matching the purchases);
  w_supplier_sales  = Rs 1,576.64 cr / Tata Chemicals FY24 revenue: 10.2% (consolidated Rs 15,421 cr) to 36% (standalone);
  w_buyer_input_cost = Rs 1,576.64 cr / Tata Consumer FY24 cost of materials consumed + purchases of stock-in-trade:
                      18.2% (consolidated Rs 8,685.51 cr) to 24.0% (standalone Rs 6,569.08 cr).
Output: research/realign/links_new_gj.csv
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from common import ROOT
P = 758.46 + 818.18
ws = (P / 15421, 0.36); wb = (P / (5730.20 + 2955.31), P / (4040.26 + 2528.82))
row = dict(link_id="G001", chain="GJ", supplier="Tata Chemicals Ltd (Mithapur)", supplier_symbol="TATACHEM", buyer="Tata Consumer Products Ltd", buyer_symbol="TATACONSUM",
           in_sample="False", supplier_external="yes", supplier_in_pack_footprint="no (Mithapur, Devbhumi Dwarka)", buyer_external="yes", buyer_in_pack_footprint="no",
           product="edible salt (vacuum-evaporated, Tata Salt)", trade="input supply (salt)", status="candidate: decision G7 pending",
           status_reason=("documented on both sides: Tata Chemicals AR FY2024-25 'For edible Salt, Tata Consumer Products Limited (TCPL) continues to be a single customer'; "
                          "Tata Consumer's related-party filings (FY24 purchases Rs 1,576.64 cr). The 'more than 85% of its salt' statement was not found in the IAR 2022-23 as read"),
           decided="", live_from="long-standing (FY24 and FY25 documents)", live_to="", live_at_event="yes",
           w_supplier_sales_low=f"{ws[0]:.3f}", w_supplier_sales_high=f"{ws[1]:.3f}",
           w_supplier_sales_basis="FY24 purchases Rs 1,576.64 cr / Tata Chemicals revenue: consolidated Rs 15,421 cr (10.2%); standalone 36% (Tata Chemicals' one-customer note, matching the purchases)",
           w_buyer_input_cost_low=f"{wb[0]:.3f}", w_buyer_input_cost_high=f"{wb[1]:.3f}",
           w_buyer_input_cost_basis="FY24 purchases / Tata Consumer cost of materials consumed + purchases of stock-in-trade: consolidated Rs 8,685.51 cr (18.2%); standalone Rs 6,569.08 cr (24.0%)",
           legacy_dependence="", legacy_period="FY2023-24", legacy_strength="",
           source_url="Tata Chemicals Integrated Annual Report FY2024-25; TCPL related-party disclosures H1 and H2 FY2023-24 (BSE); TCPL IAR 2024-25 financial statements (FY24 comparatives)",
           source_quote="For edible Salt, Tata Consumer Products Limited (TCPL) continues to be a single customer.", read_mode="original re-read 23 Nov 2026",
           saved_text="research/realign/docs/tatachain__TATACHEM__AR2024-25.txt", notes="the column meaning of the half-yearly related-party filings is inferred (758.46 actual against an approved limit of 1,640)")
pd.DataFrame([row]).to_csv(ROOT + "/research/realign/links_new_gj.csv", index=False)
print({k: row[k] for k in ("w_supplier_sales_low", "w_supplier_sales_high", "w_buyer_input_cost_low", "w_buyer_input_cost_high")})
