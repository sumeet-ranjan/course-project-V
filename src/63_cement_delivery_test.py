"""Cement delivery test (checkpoint-5 review). Specification written before the run: outputs/deliverables/table2_notes.md,
frozen copy research/realign/cement_test_spec_20261123.md (sha256 9d8a486702838d4252c8f88aa657a672feb04c0b181a17746746f2c99b3b5e21),
with one amendment made before the run (geocode rule, recorded in the notes).

Inputs: outputs/deliverables/cement_plants_geo.csv (src/62: plants from original documents, road km to Delhi),
research/realign/cement_kpis_{A,B,C}.csv (stated capacity, volumes, realisation, lead distance; quotes checked by src/42),
research/realign/cement_unit_counts.csv (the Ambuja group's own count of units, the denominator of its doses),
research/realign/cement_events_q3fy25.csv (Q2 results dates, M&A and capacity events, Oct-Dec 2024).
Maker units: listed entities, consolidated: Ambuja = Ambuja + ACC + Sanghi + Penna (ACC also on its own);
JK Lakshmi = JK Lakshmi + Udaipur Cement Works; Sagar = Sagar + Andhra Cements. India Cements is on its own (an
UltraTech associate in Nov 2024, consolidated only from late Dec 2024).
Denominator: the larger of the stated total capacity (Sep or Dec 2024) and the sum of plant capacities found.
Doses (amendment 2, made before the run): near300_n, near150_n = share of the maker's grey-cement plants within 300 / 150 km
of Delhi by road; north_rest_n = share in the northern states beyond 300 km; near_lead_n within its own Q3 FY25 lead distance;
near300_cap / north_rest_cap = capacity-weighted, only where every plant's capacity is documented.
Outcomes and inference as specified: CARs (es_lib market model) with placebo-date p for the near-dose coefficient (the same
regression on the placebo days, doses fixed); quarterly volume and realisation YoY (Q3 FY25; Q2 FY25 pre-ban check) with a
permutation p (10,000 permutations of the near dose, north_rest held). Results with and without takeover-related makers.
Outputs: outputs/deliverables/table2_cement_makers.csv (doses, outcomes, flags), table2_cement_fit.csv (coefficients, p)
"""
import os, sys, re; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import es_lib as E
from common import ROOT, EXT, OUT
RE = ROOT + "/research/realign/"; DEL = OUT + "deliverables/"
NORTH = {"delhi", "haryana", "punjab", "chandigarh", "himachal pradesh", "jammu and kashmir", "jammu & kashmir", "uttarakhand", "rajasthan", "uttar pradesh", "ladakh"}
UNITS = {"AMBUJACEM": ["AMBUJACEM", "ACC", "SANGHIIND"], "JKLAKSHMI": ["JKLAKSHMI", "UDAICEMENT"], "SAGCEM": ["SAGCEM", "ANDHRACEMT"]}
DAYS_S3, QDAYS = 30.0, 92.0
num = lambda v: pd.to_numeric(pd.Series([str(v).replace(",", "")]).str.extract(r"(-?\d+(?:\.\d+)?)")[0], errors="coerce").iloc[0]
qc = pd.read_csv(RE + "quote_check_realign.csv")
okrows = lambda f: set(qc[(qc.file == f) & (qc.status == "verified")].row)
# ---------- plants and doses ----------
P = pd.read_csv(DEL + "cement_plants_geo.csv", dtype=str).fillna("")
P["cap"] = P.cement_capacity_mtpa.map(num); P["road_km"] = pd.to_numeric(P.road_km, errors="coerce")
P["north"] = P.state.str.lower().str.strip().isin(NORTH)
# grey cement plants only; India Cements' plants filed under UltraTech are excluded for Nov 2024 (a subsidiary only from 24 Dec 2024)
P = P[~P.plant_type.str.lower().str.contains("white|clinker only")]
P = P[~((P.maker_symbol == "ULTRACEMCO") & P.owner_entity.str.contains("India Cements"))]
P = P[P.place.str.strip() != ""]          # placeholder rows (firm totals without a plant list: Nuvoco; agent B's Ambuja and ACC rows) are not plants
# the Ambuja group's denominator is its own unit count at 30 Sep 2024 (research/realign/cement_unit_counts.csv): the annual-report
# site lists give 34 of the 43 units; the rest (Sanghi, Tuticorin, Penna) lie outside the northern states (deck map)
UC = pd.read_csv(RE + "cement_unit_counts.csv", dtype=str).fillna("") if os.path.exists(RE + "cement_unit_counts.csv") else pd.DataFrame(columns=["maker_symbol", "units_total"])
UC = UC[UC.index.isin(okrows("cement_unit_counts.csv"))]
UNIT_DEN = {r.maker_symbol: float(r.units_total) for r in UC.itertuples()}
K = pd.concat([pd.read_csv(RE + f"cement_kpis_{k}.csv", dtype=str).fillna("").reset_index().rename(columns={"index": "rowid"}).assign(srcfile=f"cement_kpis_{k}.csv")
               for k in "ABC" if os.path.exists(RE + f"cement_kpis_{k}.csv")], ignore_index=True)
K = K[[(int(r.rowid) in okrows(r.srcfile)) for r in K.itertuples()]] if len(K) else K     # only rows whose quote passed src/42
K["v"] = K.value.map(num)
K["quarter"] = K.quarter.astype(str).str.replace(r"\s+", "", regex=True).str.upper()     # "Q2 FY24" and "Q2FY24" -> "Q2FY24"
IS_CAP = lambda m: bool(re.search(r"capacity", m)) and bool(re.search(r"total", m)) and not re.search(r"add", m)
IS_VOL = lambda m: bool(re.search(r"volume", m)) and not re.search(r"yoy|growth|pct|%", m)
IS_REAL = lambda m: bool(re.search(r"reali[sz]ation", m)) and not re.search(r"yoy|growth|pct|%", m)
VOL_PRI = ["sales_volume_mt", "cement_sales_volume", "sales_volume", "sales_volume_cement_clinker", "cement_and_clinker_sales_volume"]
def stated_total(sym):
    x = K[(K.maker_symbol == sym) & K.metric.map(IS_CAP)]
    x = x.assign(qq=x.quarter.str.contains("Q3FY25|DEC2024|31DEC", regex=True)).sort_values("qq", ascending=False)
    return x.v.dropna().iloc[0] if len(x.v.dropna()) else np.nan
def lead(sym):
    x = K[(K.maker_symbol == sym) & K.metric.str.contains("lead") & K.quarter.str.contains("Q3FY25")]
    return x.v.dropna().iloc[0] if len(x.v.dropna()) else np.nan
def doses(unit, g, st, L):
    """amendment 2: main doses are plant-count shares; the capacity-weighted share is kept where every plant's capacity is documented"""
    n = UNIT_DEN.get(unit, len(g)); plant_sum = g.cap.sum(); tot = np.nanmax([plant_sum, st]) if pd.notna(st) else plant_sum
    full_cap = n > 0 and g.cap.notna().all() and unit not in UNIT_DEN
    d = dict(maker=unit, n_plants=n, n_plants_listed=len(g), n_plants_with_capacity=int(g.cap.notna().sum()), plant_capacity_sum=plant_sum, stated_total=st, total_capacity=tot,
             near300_n=(g.road_km <= 300).sum() / n, near150_n=(g.road_km <= 150).sum() / n,
             north_rest_n=(g.north & (g.road_km > 300)).sum() / n, north_rest150_n=(g.north & (g.road_km > 150)).sum() / n,
             near300_cap=(g[g.road_km <= 300].cap.sum() / tot) if full_cap else np.nan, north_rest_cap=(g[g.north & (g.road_km > 300)].cap.sum() / tot) if full_cap else np.nan,
             lead_km=L, near_lead_n=((g.road_km <= L).sum() / n) if pd.notna(L) else np.nan,
             nearest_plant_km=g.road_km.min(), plants_within_300=", ".join(g[g.road_km <= 300].place.str[:28]), plants_without_distance=int(g.road_km.isna().sum()))
    d["max_loss_share_q3"] = d["near300_n"] * DAYS_S3 / QDAYS
    return d
rows = []
subs = sum([v[1:] for v in UNITS.values()], [])
for unit in sorted(set(P.maker_symbol) | set(UNITS)):
    if unit in subs: continue
    g = P[P.maker_symbol.isin(UNITS.get(unit, [unit]))]
    if len(g): rows.append(dict(members=" ".join(UNITS.get(unit, [unit])), **doses(unit, g, stated_total(unit), lead(unit))))
if "ACC" in set(P.maker_symbol):          # ACC on its own (listed separately)
    g = P[P.maker_symbol == "ACC"]; rows.append(dict(members="ACC", **doses("ACC", g, stated_total("ACC"), lead("ACC"))))
M = pd.DataFrame(rows).drop_duplicates("maker")
# ---------- flags: takeover-related and Q2 results in the windows ----------
EVp = RE + "cement_events_q3fy25.csv"
EVd = pd.read_csv(EVp, dtype=str).fillna("") if os.path.exists(EVp) else pd.DataFrame(columns=["nse_symbol", "event_type", "an_dt", "what_happened", "counterparty"])
tk = EVd[EVd.event_type.isin(["merger_acquisition", "stake"])]
# Takeover-related (the specification's rule: an open offer, a stake purchase or an acquisition of control announced or pending in
# 1 Oct-31 Dec 2024), read as a party, acquirer or target, to a deal in a cement business. Each entry rests on the events file.
# The first run flagged every merger or stake filing; that version is kept as takeover_flag_broad and reported in the notes.
TAKEOVER = {"AMBUJACEM": "acquirer: Orient Cement, share purchase agreements and open offer (22 Oct 2024)",
            "ORIENTCEM": "target: Ambuja's open offer (public announcement 22 Oct 2024)",
            "ULTRACEMCO": "acquirer: India Cements (CCI approval 20 Dec, control 24 Dec 2024); Kesoram's cement business (NCLT sanction 26 Nov 2024); Star Cement minority stake (27 Dec 2024)",
            "INDIACEM": "target: UltraTech's share purchase and open offer (20-26 Dec 2024)",
            "STARCEMENT": "target: UltraTech's minority stake purchase (27 Dec 2024); report of an Adani bid, clarified 4 Dec 2024",
            "KESORAMIND": "party: cement business transferred to UltraTech (NCLT sanction 26 Nov 2024)"}
NOT_FLAGGED = {"SHREECEM": "internal amalgamation of two wholly owned subsidiaries", "JKCEMENT": "amalgamation of its subsidiary Toshali Cements",
               "BIRLACORPN": "3.12% of a captive wind-solar power company", "HEIDELBERG": "3.51% of a captive power company",
               "MANGLMCEM": "promoter inter-se transfers", "RAMCOCEM": "sale of Ramco Industries shares to the promoter group",
               "PRSMJOHNSN": "rights shares of its own insurance subsidiary", "DALBHARAT": "'Acquisition' filing of 24 Oct 2024 unread (403): unclassified"}
M["takeover_flag"] = M.maker.map(lambda m: TAKEOVER.get(m, ""))
M["other_corporate_events"] = M.maker.map(lambda m: NOT_FLAGGED.get(m, ""))
M["takeover_flag_broad"] = M.maker.map(lambda m: "; ".join(f"{r.an_dt[:11]} {r.what_happened[:90]}" for r in tk[tk.nse_symbol == m].itertuples()))
q2 = EVd[EVd.event_type == "q2_results"].copy(); q2["d"] = pd.to_datetime(q2.an_dt.str[:11], format="%d-%b-%Y", errors="coerce")
def in_win(m, lo, hi):
    d = q2[q2.nse_symbol == m].d.dropna()
    return bool(len(d)) and any((x >= pd.Timestamp(lo)) & (x <= pd.Timestamp(hi)) for x in d)
M["q2_results_in_m1_5"] = M.maker.map(lambda m: in_win(m, "2024-11-13", "2024-11-26"))   # results after the close on 13 Nov are priced on 14 Nov (day -1)
# ---------- quarterly outcomes ----------
def series(sym, test):
    """per maker: the first metric (in priority order) reported for all four quarters, so each YoY uses one definition"""
    x = K[(K.maker_symbol == sym) & K.metric.map(test)]
    # a group unit (e.g. JK Lakshmi with Udaipur Cement Works) uses its consolidated figures: standalone rows go last
    x = x.assign(_sa=(sym in UNITS) & (x.unit + " " + x.notes).str.lower().str.contains("standalone")).sort_values("_sa", kind="stable")
    mets = sorted(set(x.metric), key=lambda m: VOL_PRI.index(m) if m in VOL_PRI else 99)
    for met in mets:
        y = x[x.metric == met]; d = {q: y[y.quarter == q].v.dropna().iloc[0] for q in ("Q2FY24", "Q3FY24", "Q2FY25", "Q3FY25") if len(y[y.quarter == q].v.dropna())}
        if len(d) == 4: return d, met
    for met in mets:   # fall back to any metric with both Q3 quarters
        y = x[x.metric == met]; d = {q: y[y.quarter == q].v.dropna().iloc[0] for q in ("Q2FY24", "Q3FY24", "Q2FY25", "Q3FY25") if len(y[y.quarter == q].v.dropna())}
        if "Q3FY25" in d and "Q3FY24" in d: return d, met
    return {}, ""
for out, test in (("vol", IS_VOL), ("real", IS_REAL)):
    got = [series(m, test) for m in M.maker]
    M[f"{out}_metric"] = [g[1] for g in got]
    M[f"{out}_yoy_q3fy25"] = [(g[0]["Q3FY25"] / g[0]["Q3FY24"] - 1) if {"Q3FY25", "Q3FY24"} <= set(g[0]) else np.nan for g in got]
    M[f"{out}_yoy_q2fy25"] = [(g[0]["Q2FY25"] / g[0]["Q2FY24"] - 1) if {"Q2FY25", "Q2FY24"} <= set(g[0]) else np.nan for g in got]
# ---------- CARs ----------
pp = pd.read_csv(EXT + "prices_peers.csv", parse_dates=["date"])
peer = pp.pivot_table(index="date", columns="asset_id", values="adjclose").sort_index().pct_change(fill_method=None)
add = peer.reindex(E.R.index); E.R = pd.concat([E.R, add[[c for c in add.columns if c not in E.R.columns]]], axis=1)
M["has_prices"] = M.maker.isin(E.R.columns)
ADANI = {"ACC", "AMBUJACEM"}
WINS = [("18 Nov 2024", "2024-11-18", (-1, 1), True), ("18 Nov 2024", "2024-11-18", (-1, 5), False), ("18 Nov 2024", "2024-11-18", (6, 20), False),
        ("17 Dec 2024", "2024-12-17", (-1, 5), False), ("17 Dec 2024", "2024-12-17", (6, 20), False)]
cm = list(M[M.has_prices].maker)
PL = [a.reindex(columns=cm) for a in (E.ar_matrix(t, pre=1, post=60) for t in E.placebo_t0s(n=1000, post=60)) if a is not None]
def ols(y, X, full=False):
    """OLS of y on a constant and X; returns the first slope (or all slopes with full=True) and n. Not identified (nan)
    when fewer than two makers in the sample have a non-zero dose"""
    ok = ~np.isnan(y) & ~np.isnan(X).any(axis=1)
    if ok.sum() < X.shape[1] + 3 or (X[ok][:, 0] > 0).sum() < 2: return (np.full(X.shape[1], np.nan) if full else np.nan), int(ok.sum())
    b = np.linalg.lstsq(np.column_stack([np.ones(ok.sum()), X[ok]]), y[ok], rcond=None)[0]; return (b[1:] if full else b[1]), int(ok.sum())
fits = []
for evl, day, w, with_adani in WINS:
    t0 = E.t0_of(day); ar = E.ar_matrix(t0, pre=1, post=60).reindex(columns=cm)
    for f in cm: M.loc[M.maker == f, f"car_{day[5:7]}{day[8:10]}_{w[0]}_{w[1]}"] = E.car(ar[[f]], *w).iloc[0]
    for sample in ("all", "without takeover-related", "without any merger or stake filing (broad)"):
        S = M[M.has_prices & (with_adani | ~M.maker.isin(ADANI))]
        if sample == "without takeover-related": S = S[S.takeover_flag == ""]
        if sample.endswith("(broad)"): S = S[S.takeover_flag_broad == ""]
        for dose, ctrl in (("near300_n", "north_rest_n"), ("near300_n", None), ("near150_n", "north_rest150_n"), ("near300_cap", "north_rest_cap")):
            S_ = S.dropna(subset=[dose] + ([ctrl] if ctrl else []))
            X = S_[[dose] + ([ctrl] if ctrl else [])].values.astype(float); fs = list(S_.maker)
            y = np.array([E.car(ar[[f]], *w).iloc[0] for f in fs], dtype=float)
            bb, n = ols(y, X, full=True); b = bb[0]
            BS = np.array([ols(np.array([E.car(P_[[f]], *w).iloc[0] for f in fs], dtype=float), X, full=True)[0] for P_ in PL]); BS = BS[~np.isnan(BS[:, 0])] if len(BS) else BS
            bs = BS[:, 0] if len(BS) else np.array([])
            bc = bb[1] if ctrl else np.nan; bcs = BS[:, 1] if (ctrl and len(BS)) else np.array([])
            fits.append(dict(outcome=f"CAR {evl} ({w[0]},{w[1]})", sample=sample + ("" if with_adani else "; ACC and Ambuja excluded"), dose=dose, control=ctrl or "", n=n,
                             n_exposed=int((S_[dose] > 0).sum()), exposed=" ".join(S_[S_[dose] > 0].maker),
                             coef=b, p_two_sided=(np.abs(bs) >= abs(b)).mean() if len(bs) and pd.notna(b) else np.nan, null_sd=bs.std() if len(bs) else np.nan, n_null=len(bs),
                             coef_control=bc, p_control=(np.abs(bcs) >= abs(bc)).mean() if len(bcs) and pd.notna(bc) else np.nan,
                             implied_full_loss_coef=np.nan, detectable=""))
rng = np.random.default_rng(5)
for out in ("vol_yoy_q3fy25", "vol_yoy_q2fy25", "real_yoy_q3fy25", "real_yoy_q2fy25"):
    for sample in ("all", "without takeover-related", "without any merger or stake filing (broad)"):
        S = M if sample == "all" else (M[M.takeover_flag == ""] if sample == "without takeover-related" else M[M.takeover_flag_broad == ""])
        for dose, ctrl in (("near300_n", "north_rest_n"), ("near300_n", None)):
            S2 = S.dropna(subset=[out]); y = S2[out].values.astype(float); Xd = S2[dose].values.astype(float)
            Xc = S2[[ctrl]].values.astype(float) if ctrl else np.empty((len(S2), 0))
            bb, n = ols(y, np.column_stack([Xd, Xc]), full=True); b = bb[0]; bc = bb[1] if ctrl else np.nan
            BS = np.array([ols(y, np.column_stack([rng.permutation(Xd), Xc]), full=True)[0] for _ in range(10000)]) if (n >= 5 and pd.notna(b)) else np.empty((0, 2))
            bs = BS[:, 0][~np.isnan(BS[:, 0])] if len(BS) else np.array([])
            full = -DAYS_S3 / QDAYS if out.startswith("vol") else np.nan        # every NCR-near tonne lost for the 30 days
            fits.append(dict(outcome=out + (" (pre-ban check)" if "q2" in out else ""), sample=sample, dose=dose, control=ctrl or "", n=n,
                             n_exposed=int((S2[dose] > 0).sum()), exposed=" ".join(S2[S2[dose] > 0].maker), coef_control=bc, p_control=np.nan,
                             cross_maker_sd=float(np.nanstd(y, ddof=1)) if n > 1 else np.nan, coef=b,
                             p_two_sided=(np.abs(bs) >= abs(b)).mean() if len(bs) and pd.notna(b) else np.nan, null_sd=bs.std() if len(bs) else np.nan, n_null=len(bs),
                             implied_full_loss_coef=full, detectable=("yes" if (pd.notna(full) and len(bs) and abs(full) > 2 * bs.std()) else ("no" if pd.notna(full) and len(bs) else ""))))
F = pd.DataFrame(fits)
M.round(4).to_csv(DEL + "table2_cement_makers.csv", index=False); F.round(4).to_csv(DEL + "table2_cement_fit.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 50)
print(M[["maker", "n_plants", "n_plants_with_capacity", "total_capacity", "near300_n", "near150_n", "north_rest_n", "near300_cap", "lead_km", "max_loss_share_q3", "takeover_flag", "has_prices"]].round(3).to_string(index=False))
print(F.round(3).to_string(index=False))
