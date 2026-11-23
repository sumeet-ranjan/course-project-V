"""Hit-firm registers for both events (scope change, 23 Nov 2026).

Every listed firm whose own filing, results document or call attributes an effect to the event, plus every firm
screened with no such statement (status 'screened: no mention') or whose documents could not be read. Rows come only
from tables whose quotes passed src/42_check_quotes_realign.py (read_mode = original), or the saved transcripts.
Columns: firm, nse_symbol, external (not in the pack's 81), in_pack_footprint, market_cap_cr (shares x close on the last
trading day before the event; current share count, so approximate), status, what_it_said, number_given, date,
document, source_url, read_mode.
Outputs: outputs/deliverables/hit_register_NCR.csv, hit_register_GJ.csv
"""
import os, sys, io, time, urllib.request; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd, numpy as np
from bs4 import BeautifulSoup
from common import ROOT, EXT, OUT, companies, exposure, stock
RE = ROOT + "/research/realign/"; DEL = OUT + "deliverables/"
C = companies(); PACK = set(C.nse_symbol); NAME = dict(zip(C.nse_symbol, C.company)); E = exposure()
FP = {z: set(E[(E.zone == z) & (E.share_cost > 0)].nse_symbol) for z in ("NCR", "GJ")}
qc = pd.read_csv(RE + "quote_check_realign.csv")
def verified(fn): return set(qc[(qc.file == fn) & (qc.status == "verified")].row)
def load(fn):
    p = RE + fn
    return pd.read_csv(p, dtype=str).fillna("") if os.path.exists(p) else pd.DataFrame()
# ---- market cap at the event ----
S = stock(); pp = pd.read_csv(EXT + "prices_peers.csv", parse_dates=["date"])
sh = pd.read_csv(EXT + "market_cap.csv").set_index("firm").shares_cr.to_dict()
sh.update(pd.read_csv(EXT + "market_cap_peers.csv").set_index("firm").shares_cr.dropna().to_dict())
SHP = EXT + "shares_register.csv"; extra = pd.read_csv(SHP).set_index("firm").shares_cr.to_dict() if os.path.exists(SHP) else {}
sh.update(extra)
def shares(sym):
    if sym in sh and pd.notna(sh[sym]): return sh[sym]
    for cons in (True, False):
        try:
            u = f"https://www.screener.in/company/{sym.replace('&', '%26')}/" + ("consolidated/" if cons else "")
            s = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=40).read().decode(), "lxml")
            r = {li.find("span", class_="name").get_text(strip=True): li.find("span", class_="number").get_text(strip=True) for li in s.select("#top-ratios li")}
            mc, px = (float(str(r.get(k, "nan")).replace(",", "") or "nan") for k in ("Market Cap", "Current Price"))
            if mc == mc and px == px and px:
                extra[sym] = sh[sym] = mc / px; pd.DataFrame({"firm": list(extra), "shares_cr": list(extra.values())}).to_csv(SHP, index=False); return sh[sym]
        except Exception: pass
        time.sleep(1.5)
    return np.nan
def mcap(sym, day):
    day = pd.Timestamp(day)
    x = S[(S.asset_id == sym) & (S.date < day)] if sym in PACK else pp[(pp.asset_id == sym) & (pp.date < day)]
    px = x.sort_values("date").close.iloc[-1] if len(x) else np.nan
    return round(px * shares(sym), 0) if pd.notna(px) else np.nan
rows = {"NCR": [], "GJ": []}
GRADE = {("NCR", "NBCC"): "confirmed hit firm (G3)", ("NCR", "DLF"): "confirmed hit firm (G3)",
         ("NCR", "AHLUCONT"): "within-zone contractor, material (G4; mechanism accepted at G5 on documents and quarterly numbers)",
         ("GJ", "TATACHEM"): "material hit (G7): about 10 days, 30,000 t soda ash, 40,000 t salt; loss dated 'July and August', not separable between the two rain episodes",
         ("GJ", "ACI"): "material hit (G7): Rs 40.18 cr salt stock lost to the late-August storm (Asna)",
         ("GJ", "ADANIPORTS"): "confirmed, immaterial (G7): 4 days equivalent; August 2024 cargo still +5% YoY",
         ("GJ", "GVT&D"): "confirmed, immaterial (G7): production disruption, no damage; sales +59%"}
def add(ev, sym, firm, status, said, number, date, doc, url, read, fp_ext=""):
    fpz = "NCR" if ev == "NCR" else "GJ"
    rows[ev].append(dict(firm=firm or NAME.get(sym, sym), nse_symbol=sym, external="no" if sym in PACK else "yes",
                         in_pack_footprint=(("yes" if sym in FP[fpz] else "no") if sym in PACK else (fp_ext or "not established")),
                         status=status, grade=GRADE.get((ev, sym), ""), what_it_said=said, number_given=number, date=date, document=doc, source_url=url, read_mode=read))
# ================= NCR =================
A = load("ncr_stepA_evidence.csv"); va = verified("ncr_stepA_evidence.csv")
for i, r in A.iterrows():
    if r.what_it_shows in ("names_ban", "delay_or_stoppage") and i in va:
        add("NCR", r.nse_symbol, "", "attributes effect", r.quote, r.dates_mentioned, r.document_date, r.document_title, r.source_url, r.read_mode)
for sym in ("ANANTRAJ", "PARSVNATH", "UNITECH", "NBCC", "DLF"):
    x = A[(A.nse_symbol == sym) & (A.what_it_shows.isin(["no_mention", "other"]))]
    if len(x):
        unread = x.notes.str.contains("FETCH FAILED|NOT READ|not read", case=False)
        if (~unread).any():
            add("NCR", sym, "", "screened: no mention", "", "", "", "; ".join(x[~unread].document_title), "", "original_pdf")
        if unread.any() and sym == "UNITECH" and (~unread).sum() == 0:
            add("NCR", sym, "", "not readable", "", "", "", "; ".join(x.document_title), "", "fetch failed (403 or image-only PDF)")
K = load("stepB_contractors.csv"); vk = verified("stepB_contractors.csv")
for i, r in K.iterrows():
    if r.relation_type == "ncr_ban_mention" and i in vk:
        add("NCR", r.nse_symbol, "", "attributes effect", r.quote, r.value, r.document_date, r.document_title, r.source_url, r.read_mode, fp_ext="yes (NCR sites)")
AH = load("ahlucont_q2q3_quotes.csv")
import re as _re
_seen = {_re.sub(r"\W+", "", x["what_it_said"].lower())[:80] for x in rows["NCR"] if x["nse_symbol"] == "AHLUCONT"}
for r in AH.itertuples():
    k = _re.sub(r"\W+", "", r.quote.lower())[:80]
    if any(k[:60] in s_ or s_[:60] in k for s_ in _seen):   # same passage already entered from the Step B table: keep one, dated to the call
        for x in rows["NCR"]:
            if x["nse_symbol"] == "AHLUCONT" and _re.sub(r"\W+", "", x["what_it_said"].lower())[:60] == k[:60]: x["date"], x["document"] = r.document_date, r.document_title
        continue
    _seen.add(k)
    add("NCR", "AHLUCONT", "", "attributes effect", r.quote, r.number_given, r.document_date, r.document_title, r.source_url, "original_pdf", fp_ext="yes (NCR sites)")
for sym in sorted(set(K[K.relation_type == "no_mention"].nse_symbol)):
    s2 = "CEMPRO" if sym == "ITDCEM" else sym
    add("NCR", s2, "", "screened: no mention", "", "", "", "; ".join(K[(K.nse_symbol == sym) & (K.relation_type == "no_mention")].document_title), "", "original_pdf",
        fp_ext="yes" if s2 in ("CEMPRO", "CAPACITE") else "not established")
SP = load("stepB_supplier_side.csv"); vs = verified("stepB_supplier_side.csv")
for i, r in SP.iterrows():
    if r.relation_type == "ncr_ban_mention" and i in vs:
        add("NCR", r.nse_symbol, "", "attributes effect (one of three stated reasons)", r.quote, "", r.document_date, r.document_title, r.source_url, r.read_mode)
for sym in sorted(set(SP[SP.relation_type == "no_mention"].nse_symbol) - set(SP[SP.relation_type == "ncr_ban_mention"].nse_symbol)):
    add("NCR", sym, "", "screened: no mention", "", "", "", "; ".join(SP[(SP.nse_symbol == sym) & (SP.relation_type == "no_mention")].document_title), "", "original_pdf")
M = load("ncr_maruti_screen.csv")
if len(M): add("NCR", "MARUTI", "", "screened: no mention (call transcript not read)", "", "", "2025-01-29", "; ".join(M.document_title), "", "original_pdf")
R2 = load("ncr_round2_docs.csv"); v2 = verified("ncr_round2_docs.csv")
FPX = {"ASHIANA": "not established (it attributes the fall to GRAP restrictions in Delhi-NCR; sites not named in the update)", "SIGNATURE": "yes (Gurugram)", "GODREJPROP": "yes (NCR projects)", "SOBHA": "yes (Gurugram, Greater Noida)", "MAXESTATES": "yes (Noida, Gurugram)"}
for i, r in R2.iterrows():
    if r.nse_symbol in FPX:
        if r.what_it_shows == "attributes_effect" and i in v2:
            add("NCR", r.nse_symbol, r.firm, "attributes effect", r.quote, r.number_given, r.document_date, r.document_title, r.source_url, r.read_mode, fp_ext=FPX[r.nse_symbol] or "see notes")
        elif r.what_it_shows == "none_found" and r.read_mode == "search_snippet":
            add("NCR", r.nse_symbol, r.firm, "not readable", "", "", r.document_date, r.document_title, "", "fetch failed (404 or CAPTCHA; not bypassed)", fp_ext=FPX[r.nse_symbol] or "not established")
        elif r.what_it_shows in ("no_mention", "none_found") and r.read_mode != "search_snippet":
            add("NCR", r.nse_symbol, r.firm, "screened: no mention", "", "", r.document_date, r.document_title, r.source_url, r.read_mode, fp_ext=FPX[r.nse_symbol] or "not established")
# ================= Gujarat =================
GH = load("gj_hit_firms_docs.csv"); vg = verified("gj_hit_firms_docs.csv")
FPG = {"TATACHEM": "no (Mithapur, Devbhumi Dwarka)", "ACI": "no (Kutch)", "GVT&D": "yes (Vadodara)", "ADANIPORTS": "no (Mundra, Tuna in Kutch)", "GHCL": "no (Sutrapada, Gir Somnath)"}
for i, r in GH.iterrows():
    if r.nse_symbol in FPG and i in vg and r.what_it_shows in ("attributes_effect", "confound", "no_mention"):
        st = {"attributes_effect": "attributes effect", "confound": "confound (not storm-related)", "no_mention": "screened: no mention"}[r.what_it_shows]
        add("GJ", r.nse_symbol, r.firm, st, r.quote, r.number_given, r.document_date, r.document_title, r.source_url, r.read_mode, fp_ext=FPG[r.nse_symbol])
TC = load("gj_tata_chain_docs.csv"); vt = verified("gj_tata_chain_docs.csv")
for i, r in TC.iterrows():
    if r.nse_symbol == "TATACONSUM" and str(r.task).startswith("3") and i in vt:
        add("GJ", "TATACONSUM", r.firm, "downstream node (H2): statement", r.quote, r.number_given, r.document_date, r.document_title, r.source_url, r.read_mode, fp_ext="no (buyer outside Gujarat footprint)")
# pack chemical belt: Q2 FY25 calls and exchange filings screened (Step 1 of the earlier rounds; transcripts saved)
kh = pd.read_csv(ROOT + "/research/transcript_keyword_hits.csv", dtype=str).fillna("")
for f in sorted(os.listdir(ROOT + "/research/transcripts")):
    if f.startswith("gujarat_2024_"):
        sym = f.split("_")[2]; url = kh[(kh.case == "gujarat_2024") & (kh.symbol == sym)].source_url
        add("GJ", sym, "", "screened: no mention of the flood", "", "", "", f"Q2 FY25 earnings call ({f.split('_')[-1][:-4]}); NSE filings 25 Aug - 30 Sep 2024: no flood notice", url.iloc[0] if len(url) else "", "original_pdf (saved transcript)")
for ev, fn, day in (("NCR", "hit_register_NCR.csv", "2024-11-18"), ("GJ", "hit_register_GJ.csv", "2024-08-26")):
    o = pd.DataFrame(rows[ev])
    if o.empty: continue
    o.insert(4, "market_cap_cr", [mcap(s, day) for s in o.nse_symbol])
    o.sort_values(["status", "nse_symbol"]).to_csv(DEL + fn, index=False)
    print(ev, len(o), "rows;", o.groupby("status").nse_symbol.nunique().to_string())
