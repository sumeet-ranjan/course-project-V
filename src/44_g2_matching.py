"""Proposal for decision G2: eligible controls and size-matched pairs (a proposal only; the user decides).

Eligible control = same industry group, documented to have no project/plant in the event zone:
  - outside the sample: the sub-agent tables research/realign/controls_ncr_developers.csv (any_ncr == "no")
    and research/realign/controls_gj_chemicals.csv (any_gujarat_plant == "no"), quotes checked by src/42;
  - inside the sample: firms whose plants (data/plants.csv) include none in the zone, same broad industry.
Matching: for each exposed firm, the two eligible controls nearest in log market cap at the last trading day
before the event (with replacement).
Output: research/realign/g2_proposal.csv
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from common import ROOT
RE = ROOT + "/research/realign/"
X = pd.read_csv(RE + "g2_exposed_sets.csv"); Y = pd.read_csv(RE + "g2_control_candidates.csv")
qc = pd.read_csv(RE + "quote_check_realign.csv")
def verified_no(fn, col, no="no"):
    p = RE + fn
    if not os.path.exists(p): return set(), pd.DataFrame()
    d = pd.read_csv(p, dtype=str).fillna("")
    ok = qc[(qc.file == fn) & (qc.status == "verified")].key
    return set(d[(d[col].str.lower() == no) & d.nse_symbol.isin(ok)].nse_symbol), d
ncr_ok, ncr_tab = verified_no("controls_ncr_developers.csv", "any_ncr")
gj_ok, gj_tab = verified_no("controls_gj_chemicals.csv", "any_gujarat_plant")
EXPOSED = {"NCR builders": ("E_NCR_GRAP_2024 (18 Nov 2024)", ["NBCC", "DLF", "ANANTRAJ", "UNITECH", "PARSVNATH"]),
           "Gujarat chemicals": ("E_GJ_FLOOD_2024 (26 Aug 2024)", ["KIRIINDUS", "GUJALKALI", "BODALCHEM", "GNFC", "SRF", "GSFC", "AARTIIND", "UPL", "DCMSHRIRAM", "ZUARI"])}
IN_SAMPLE_OK = {"NCR builders": {"LODHA", "VASCONEQ"}, "Gujarat chemicals": set()}   # RAJESHEXPO: mixed jewellery/housing plants in the pack
rows = []
for grp, (ev, ex) in EXPOSED.items():
    ok = (ncr_ok if grp == "NCR builders" else gj_ok) | IN_SAMPLE_OK[grp]
    pool = Y[(Y.group == grp) & Y.nse_symbol.isin(ok) & Y.mcap_at_event_cr.notna()].copy()
    for e in ex:
        me = X[(X.event == ev) & (X.nse_symbol == e)].mcap_at_event_cr
        if me.empty or pd.isna(me.iloc[0]): continue
        pool["dist"] = (np.log(pool.mcap_at_event_cr) - np.log(me.iloc[0])).abs()
        for r in pool.nsmallest(2, "dist").itertuples():
            rows.append(dict(group=grp, event=ev, exposed=e, exposed_mcap_cr=me.iloc[0], control=r.nse_symbol, control_mcap_cr=r.mcap_at_event_cr,
                             size_ratio=round(r.mcap_at_event_cr / me.iloc[0], 2), control_source=r.source))
P = pd.DataFrame(rows); P.to_csv(RE + "g2_proposal.csv", index=False)
pd.set_option("display.width", 200)
print("eligible NCR developer controls:", sorted(ncr_ok | IN_SAMPLE_OK["NCR builders"]))
print("eligible Gujarat chemical controls:", sorted(gj_ok))
print(P.to_string(index=False))
