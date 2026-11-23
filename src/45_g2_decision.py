"""Write the user's decision G2 (23 Nov 2026) as data, and the placebo list (deliverable 3(iii) inputs).

Outputs:
  research/realign/g2_decision.csv   event, group, role, nse_symbol, match_for, pool, note
  outputs/deliverables/placebo_firms.csv   event, nse_symbol, company, included, reason
Decisions encoded here (user, 23 Nov 2026):
  NCR    confirmed builders NBCC, DLF; unconfirmed ANANTRAJ, PARSVNATH, UNITECH (reported separately).
         Main benchmark: all eligible developer controls, equal-weighted; robustness: nearest two by size.
         NBCC: PSU benchmark (Nifty PSE index) and a window ending 22 Nov 2024.
         Dropped: IGL, ADANIENT, ADANIGREEN, ADANIPOWER, TORNTPOWER (controls). ACC flagged contaminated for Step C.
  Gujarat both footprints; the Vadodara footprint is defined by sites (any plant in Vadodara district).
         Controls by sub-industry first (fertiliser pool, specialty pool), size second; DCW excluded;
         all ten firms kept, with the five without a size match flagged as such.
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from common import *
RE = ROOT + "/research/realign/"; DEL = OUT + "deliverables/"; os.makedirs(DEL, exist_ok=True)
c = companies(); p = plants(); e = exposure(); R = returns_wide()
traded = set(R.columns[R.notna().sum() > 300])
X = pd.read_csv(RE + "g2_exposed_sets.csv"); Y = pd.read_csv(RE + "g2_control_candidates.csv")
mcap = pd.concat([X.set_index("nse_symbol").mcap_at_event_cr, Y.drop_duplicates("nse_symbol").set_index("nse_symbol").mcap_at_event_cr])
mcap = mcap[~mcap.index.duplicated()]
rows = []
def add(event, group, role, sym, match_for="", pool="", note=""):
    rows.append(dict(event=event, group=group, role=role, nse_symbol=sym, match_for=match_for, pool=pool, note=note))
def nearest(sym, pool_syms, k=2):
    d = (np.log(mcap.reindex(pool_syms)) - np.log(mcap[sym])).abs().dropna().nsmallest(k)
    return [(s, mcap[s] / mcap[sym]) for s in d.index]
# ---------------- NCR ----------------
NCR_CTL = ["BRIGADE", "PURVA", "AJMERA", "RUSTOMJEE", "KOLTEPATIL", "SUNTECK", "LODHA", "VASCONEQ"]
for ev in ("E_NCR_GRAP_2024", "E_NCR_GRAP_2024B", "NCR_S3_2022", "NCR_S3_2023"):
    for s in ("NBCC", "DLF"): add(ev, "confirmed", "exposed", s, note="names the ban in its own Q3 FY25 call (G3)")
    for s in ("ANANTRAJ", "PARSVNATH", "UNITECH"): add(ev, "unconfirmed", "exposed", s, note="exposed (NCR plant cost >= 25%), no disclosure found (G3)")
    for s in NCR_CTL: add(ev, "controls", "control", s, note="developer with no NCR project (own Q2 FY25 deck, or pack plants for LODHA/VASCONEQ)")
    for ex in ("NBCC", "DLF", "ANANTRAJ", "PARSVNATH", "UNITECH"):
        for s, ratio in nearest(ex, NCR_CTL): add(ev, "controls_nn", "control_nn", s, match_for=ex, note=f"nearest two by size; ratio {ratio:.2f}")
    for s in ("MARUTI", "MAXHEALTH", "TATACOMM", "FORTIS", "RPOWER", "RVNL"): add(ev, "within_zone", "within_zone", s, note="NCR plants, not under the construction ban")
    add(ev, "psu_benchmark", "benchmark", "NIFTY_PSE", match_for="NBCC", note="Nifty PSE index (Yahoo ^CNXPSE); NBCC is a PSU")
# ---------------- Gujarat ----------------
FERT, SPEC = ["CHAMBLFERT", "NFL", "PARADEEP"], ["VINATIORGA", "CLEAN", "SUDARSCHEM"]
fert_share = p[p.industry_name.str.contains("Fertil", case=False)].groupby("nse_symbol").project_cost_cr.sum() / p.groupby("nse_symbol").project_cost_cr.sum()
fert_share = fert_share.reindex(p.nse_symbol.unique()).fillna(0)
PACK10 = ["KIRIINDUS", "GUJALKALI", "BODALCHEM", "GNFC", "SRF", "GSFC", "AARTIIND", "UPL", "DCMSHRIRAM", "ZUARI"]
vad_sites = set(p[(p.dist_name == "Vadodara")].nse_symbol) & set(PACK10)
ev = "E_GJ_FLOOD_2024"
for grp, firms in (("pack_footprint", PACK10), ("vadodara_sites", sorted(vad_sites))):
    for s in firms:
        pool = "fertiliser" if fert_share.get(s, 0) >= 0.25 else "specialty"
        add(ev, grp, "exposed", s, pool=pool, note=f"fertiliser share of plant cost {fert_share.get(s, 0):.2f}")
        for cs, ratio in nearest(s, FERT if pool == "fertiliser" else SPEC):
            add(ev, grp + "_nn", "control_nn", cs, match_for=s, pool=pool,
                note=f"nearest two by size within the {pool} pool; ratio {ratio:.2f}" + ("" if 0.5 <= ratio <= 2 else "; NOT size-matched"))
for s in FERT: add(ev, "controls", "control", s, pool="fertiliser", note="no plant in Gujarat (own FY2023-24 document)")
for s in SPEC: add(ev, "controls", "control", s, pool="specialty", note="no plant in Gujarat (own FY2023-24 document)")
G = pd.DataFrame(rows); G.to_csv(RE + "g2_decision.csv", index=False)
# ---------------- placebo lists: unexposed, unlinked firms ----------------
GUJ_DIST = {"Ahmadabad", "Amreli", "Anand", "Banas Kantha", "Bharuch", "Bhavnagar", "Gandhinagar", "Gir Somnath", "Gujarat", "Gujarat Districts", "Jamnagar",
            "Junagadh", "Kachchh", "Kachchh Offshore", "Kheda", "Mahesana", "Panch Mahals", "Panchmahal", "Patan", "Porbandar", "Rajkot", "Surat", "Surendranagar",
            "Vadodara", "Valsad", "Navsari", "Tapi", "Dang", "Narmada", "Dohad", "Dahod", "Sabar Kantha", "Morbi", "Botad", "Devbhumi Dwarka", "Aravalli", "Mahisagar", "Chhota Udaipur"}
ncr_any = set(e[(e.zone == "NCR") & (e.share_cost > 0)].nse_symbol)
guj_any = set(p[p.dist_name.isin(GUJ_DIST)].nse_symbol)
ADANI = {"ADANIENT", "ADANIGREEN", "ADANIPOWER", "ADANIPORTS", "ADANITRANS", "ADANIENSOL", "ACC", "AMBUJACEM"}
CONSTR_INPUT = {"ACC", "ULTRACEMCO", "SHREECEM", "JPASSOCIAT", "JINDALSTEL", "JSL", "JSWSTEEL", "SAIL", "TATASTEEL", "JINDALSAW", "NMDC", "TATASTLBSL", "JSWISPAT", "SAURASHCEM"}
DEV = set(c[c.primary_industry.str.contains("Housing", na=False)].nse_symbol)
GJ_LINKED = {"GAIL", "IOC", "BPCL", "TORNTPOWER", "NATIONALUM"}          # held / candidate links in verified_links.csv
CHEM_DOWN = {s for s in c.nse_symbol if sector(c.set_index("nse_symbol").primary_industry.get(s, "")) in ("Chemicals", "Healthcare/Pharma", "Auto/Tyres")} | {"HINDUNILVR"}
pl = []
for s in sorted(traded):
    nm = c.set_index("nse_symbol").company.get(s, "")
    # NCR
    why = []
    if s in ncr_any: why.append("has a plant in NCR (exposed or within-zone)")
    if s in ADANI: why.append("Adani group: indictment news on 21 Nov 2024 inside the window")
    if s in CONSTR_INPUT: why.append("cement/steel/iron ore: candidate supplier of the NCR builders (Step B pending)")
    if s in DEV and s not in ncr_any: why.append("developer: used as a control or excluded from controls")
    if s == "IGL": why.append("own gas-allocation cut on 18 Nov 2024")
    if s == "HCC": why.append("construction contractor (Hindustan Construction Co.); the pack lists only 3 sites, so its NCR project exposure is unknown")
    if s == "TORNTPOWER": why.append("not a clean placebo: verified Petronet customer (user, 22 Nov 2026)")
    pl.append(dict(event="E_NCR_GRAP_2024", nse_symbol=s, company=nm, included="no" if why else "yes", reason="; ".join(why) if why else "no NCR plant, no candidate link"))
    # Gujarat (provisional until Gujarat Step B)
    why = []
    if s in guj_any: why.append("has a plant in Gujarat")
    if s in GJ_LINKED: why.append("held/candidate link to a Gujarat hit firm (Petronet offtaker or GNAL caustic-soda buyer)")
    if s in CHEM_DOWN and s not in guj_any: why.append("chemical, pharma, tyre or FMCG firm: possible downstream buyer (Step B pending)")
    if s == "TORNTPOWER": why.append("pack 'control' but a verified Petronet customer (user, 22 Nov 2026)")
    if s == "IGL": why.append("buys most of its gas from GAIL, a held Petronet offtaker (second-order link)")
    pl.append(dict(event="E_GJ_FLOOD_2024 (provisional)", nse_symbol=s, company=nm, included="no" if why else "yes", reason="; ".join(why) if why else "no Gujarat plant, no candidate link"))
P = pd.DataFrame(pl); P.to_csv(DEL + "placebo_firms.csv", index=False)
pd.set_option("display.width", 220); pd.set_option("display.max_colwidth", 120)
print(G[G.event.isin(["E_NCR_GRAP_2024", "E_GJ_FLOOD_2024"])].to_string(index=False))
for ev_ in P.event.unique():
    q = P[P.event == ev_]; print(f"\n{ev_}: {int((q.included == 'yes').sum())} included, {int((q.included == 'no').sum())} excluded")
    print("included:", ", ".join(q[q.included == "yes"].nse_symbol))
