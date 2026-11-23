"""Deliverable 2 (working version): the verified supply-chain links file that replaces the scaffold.

Built from the 32 legacy rows in research/verified_links_all.csv, classified by the user's decision G1
(23 Nov 2026), with the columns the plan requires:
  status / status_reason / decided    verified | candidate | held | rejected | removed | out_of_scope
  live_from, live_to, live_at_event   was the link operating on the event date?
  w_supplier_sales_low/high/basis     buyer's share of the supplier's sales (backward test, H3)
  w_buyer_input_cost_low/high/basis   supplier's share of the buyer's input cost (forward test, H2)
  read_mode, saved_text               a row enters a result only once its original document is read
New links found in Steps B (NCR, Gujarat) are appended from research/realign/links_new.csv when it exists.
Output: outputs/deliverables/verified_links.csv
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from common import ROOT, OUT
DEL = OUT + "deliverables/"; os.makedirs(DEL, exist_ok=True)
L = pd.read_csv(ROOT + "/research/verified_links_all.csv", dtype=str).fillna("")
G1 = "G1 (user, 23 Nov 2026)"
PET_HOLD = ("held: link documented (ICRA), but no disruption at Petronet's Dahej terminal was found for Aug 2024, so it "
            "cannot carry a propagation result unless Gujarat Step A confirms a hit")
WRONG_NCR = "removed: built on a wrong NCR hit firm (the hit firms are the NCR builders under the construction ban)"
# row index -> (chain, status, reason, live_at_event, w_supplier_sales (low, high, basis), w_buyer_input_cost (low, high, basis), notes)
C = {
 0: ("GJ", "held", PET_HOLD, "unknown (evidence dated Apr 2026)", ("0.60", "0.60", "share of Petronet's long-term committed Dahej R-LNG volume (volume, not revenue)"), ("", "", ""), ""),
 1: ("GJ", "held", PET_HOLD, "unknown (evidence dated Apr 2026)", ("0.30", "0.30", "share of Petronet's long-term committed Dahej R-LNG volume (volume, not revenue)"), ("", "", ""), ""),
 2: ("GJ", "held", PET_HOLD, "unknown (evidence dated Apr 2026)", ("0.10", "0.10", "share of Petronet's long-term committed Dahej R-LNG volume (volume, not revenue)"), ("", "", ""), ""),
 3: ("GJ", "held", PET_HOLD, "unknown (evidence dated Apr 2026)", ("0.303", "0.303", "share of Dahej tolling capacity (capacity, not revenue)"), ("", "", ""), ""),
 4: ("GJ", "held", PET_HOLD, "unknown (evidence dated Apr 2026)", ("0.182", "0.182", "share of Dahej tolling capacity (capacity, not revenue)"), ("", "", ""), ""),
 5: ("GJ", "held", PET_HOLD, "unknown (evidence dated Apr 2026)", ("0.121", "0.121", "share of Dahej tolling capacity (capacity, not revenue)"), ("", "", ""), ""),
 6: ("GJ", "held", PET_HOLD, "unknown (evidence dated Apr 2026)", ("0.121", "0.121", "share of Dahej tolling capacity (capacity, not revenue)"), ("", "", ""),
     "Torrent Power is a 'control' in the pack; as a Petronet customer it is not a clean placebo (user, 22 Nov 2026)"),
 7: ("GJ", "held", PET_HOLD + "; buyer not listed in the sample", "unknown (evidence dated Apr 2026)", ("0.273", "0.273", "share of Dahej tolling capacity"), ("", "", ""), ""),
 8: ("GJ", "out_of_scope", "out of scope: foreign supplier upstream of Petronet, not a propagation path to a listed Indian firm", "", ("", "", ""), ("", "", ""), ""),
 9: ("GJ", "held", PET_HOLD + "; corroboration of the tolling row from a news report", "booking for 20 years from 2017 (news, 2015)", ("", "", ""), ("", "", ""), "secondary source (news)"),
10: ("NCR", "removed", WRONG_NCR + "; IGL fell on its own gas-allocation cut (IGL filing, 15 Nov 2024)", "", ("", "", ""), ("", "", ""), ""),
11: ("NCR", "removed", WRONG_NCR + "; IGL fell on its own gas-allocation cut (IGL filing, 15 Nov 2024)", "", ("", "", ""), ("", "", ""), ""),
12: ("GJ", "candidate", "candidate, pending Gujarat Step A: the supplying plant (GNAL, 60% Gujarat Alkalies, 40% NALCO) is at Dahej, where no Aug 2024 disruption is documented",
     "yes (same wording in CARE's Aug 2024 rationale, per the legacy row; to be re-read)", ("0.5625", "", "at least 450 of GNAL's 800 tonnes/day caustic-soda capacity goes to NALCO (capacity share of the JV, not of Gujarat Alkalies)"), ("", "", "NALCO's caustic-soda cost share not yet estimated"),
     "NALCO owns 40% of the supplier as well as buying from it"),
13: ("GJ", "rejected", "not live at the event date as a dependence measure: related-party ceiling approved for 12 months from the Jul 2026 AGM (a ceiling, not actual sales)", "no", ("", "", ""), ("", "", ""),
     "same link as the candidate row; only the measure is rejected"),
14: ("GJ", "rejected", "not live at the event date: the joint venture 'is expected to commence commercial supplies by Q1 FY 2026-27' (Aarti press release, 23 May 2024); both partners are inside the Gujarat zone anyway",
     "no", ("", "", ""), ("", "", ""), "the same release mentions an 'existing relationship of AIL and UPL that spans over two decades' (direction and size not stated)"),
15: ("NCR", "removed", WRONG_NCR + "; contract reported May 2026, after the event", "no", ("", "", ""), ("", "", ""), ""),
16: ("NCR", "out_of_scope", "out of scope: buyer is a ministry, and RVNL is not an NCR hit firm", "", ("", "", ""), ("", "", ""), ""),
17: ("other", "out_of_scope", "out of scope: not on either deep-dive chain", "", ("", "", ""), ("", "", ""), ""),
18: ("other", "out_of_scope", "out of scope: buyer is a ministry; not on either deep-dive chain", "", ("", "", ""), ("", "", ""), ""),
19: ("NCR", "removed", WRONG_NCR, "", ("", "", ""), ("0.78", "0.78", "approx. share of IGL's gas purchases from GAIL (derived, mixed VAT basis; upper bound)"), ""),
20: ("NCR", "removed", WRONG_NCR, "", ("", "", ""), ("", "", ""), ""),
21: ("NCR", "removed", WRONG_NCR + "; an equity link, not a supply link", "", ("", "", ""), ("", "", ""), ""),
22: ("NCR", "removed", WRONG_NCR, "", ("", "", ""), ("", "", ""), ""),
23: ("NCR", "removed", WRONG_NCR + "; joint CNG promotion, not a supply contract", "", ("", "", ""), ("", "", ""), "Maruti is a within-zone comparison for NCR (user, 22 Nov 2026)"),
24: ("other", "out_of_scope", "out of scope: Chennai event, not a deep-dive", "", ("", "", ""), ("", "", ""), ""),
25: ("other", "out_of_scope", "out of scope: Chennai tyre segment shares, no named buyer", "", ("", "", ""), ("", "", ""), ""),
26: ("other", "out_of_scope", "out of scope: Chennai tyre segment shares, no named buyer", "", ("", "", ""), ("", "", ""), ""),
27: ("other", "out_of_scope", "out of scope: unnamed raw-material suppliers", "", ("", "", ""), ("", "", ""), ""),
28: ("other", "out_of_scope", "out of scope: Chennai tyre segment shares, no named buyer", "", ("", "", ""), ("", "", ""), ""),
29: ("other", "out_of_scope", "out of scope: Chennai tyre segment shares, no named buyer", "", ("", "", ""), ("", "", ""), ""),
30: ("NCR", "candidate", "candidate fallback weight for the NCR chain (decision G4): Shree's market share in the North, which is not the share of Shree's sales made in the North",
     "", ("", "", "needed: share of Shree's sales in the North/NCR; source is a broker note"), ("", "", ""), "secondary source (broker note)"),
31: ("NCR", "candidate", "context for NCR Step A (exposure of a hit firm), not a supply link", "", ("", "", ""), ("", "", ""), ""),
}
rows = []
for i, r in L.iterrows():
    ch, st, why, live, ws, wb, nt = C[i]
    rows.append(dict(link_id=f"L{i:03d}", chain=ch, supplier=r.supplier, supplier_symbol=r.supplier_symbol, buyer=r.buyer, buyer_symbol=r.buyer_symbol,
                     in_sample=r.in_sample, product=r["product"], status=st, status_reason=why, decided=G1, live_from="", live_to="", live_at_event=live,
                     w_supplier_sales_low=ws[0], w_supplier_sales_high=ws[1], w_supplier_sales_basis=ws[2],
                     w_buyer_input_cost_low=wb[0], w_buyer_input_cost_high=wb[1], w_buyer_input_cost_basis=wb[2],
                     legacy_dependence=f"{r.dependence_metric}: {r.dependence_value}", legacy_period=r.period, legacy_strength=r.evidence_strength,
                     source_url=r.source_url, source_quote=r.source_quote,
                     read_mode="original re-read 23 Nov 2026" if i == 14 else "not yet re-read",
                     saved_text="research/realign/docs/links__AARTIIND_UPL__pressrelease.txt" if i == 14 else "", notes=nt))
o = pd.DataFrame(rows)
new = ROOT + "/research/realign/links_new.csv"
if os.path.exists(new): o = pd.concat([o, pd.read_csv(new, dtype=str).fillna("")], ignore_index=True)
o.to_csv(DEL + "verified_links.csv", index=False)
print(o.groupby(["chain", "status"]).size().to_string())
