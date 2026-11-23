"""Deliverable 3(ii) dose-response and 3(iii) placebos (Step E / §7 step 5; decisions G1-G7 applied).

3(ii) Dose-response across all verified links (INSTRUCTIONS §4: downstream CAR or delta-margin on dependence weight x
supplier hit severity).
  Panel A, NCR (backward, H3): within-zone contractors linked to the confirmed hit builders. Dose = builder's share of the
    contractor's sales (verified_links.csv, bracket low/high, midpoint) x the builder's exposure concentration (share of
    its plant cost in NCR districts, data/plants.csv: NBCC 0.94, DLF 0.42). The event (GRAP Stage III/IV) is common to
    all links, so event severity is a constant. Zero-dose rows: the five contractors screened and found unlinked.
    Outcomes: CARs (stepC_ncr_node_cars.csv) and Q3 FY25 sales YoY and OPM change YoY (screener.in). Fit: OLS slope of
    outcome on dose with an exact permutation p-value (all 8! assignments of the doses to the 8 firms). Own direct
    exposure, sector and size cannot be controlled with n = 8; own NCR exposure is listed where documented.
  Panel B, Gujarat (forward, H2): the one verified forward link, Tata Chemicals -> Tata Consumer. One observation, so no
    slope: dose, severity and the buyer's outcomes are listed.
  Panel C, market level (not a firm link): the cement test of G4 R3 / G5 (binary dose: northern capacity).
3(iii) Placebos: the same CAR test on (A) the unexposed, unlinked placebo firms (placebo_firms.csv; the Gujarat list is
  provisional), (B) the G2 control firms, (C) the unlinked comparison contractors. Equal-weighted mean CAR, two-sided
  placebo-date p-value (same group statistic on 1,000 random days), and the share of firms whose own CAR has p < 0.05
  (about 5% expected under the null).
Outputs: outputs/deliverables/table2_dose_response.csv, table2_dose_response_fit.csv, table3_placebo.csv
"""
import os, sys, itertools; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import es_lib as E
from common import EXT, OUT
DEL = OUT + "deliverables/"
pp = pd.read_csv(EXT + "prices_peers.csv", parse_dates=["date"])
peer = pp.pivot_table(index="date", columns="asset_id", values="adjclose").sort_index().pct_change(fill_method=None)
add = peer.reindex(E.R.index); E.R = pd.concat([E.R, add[[c for c in add.columns if c not in E.R.columns]]], axis=1)
L = pd.read_csv(DEL + "verified_links.csv", dtype=str).fillna("")
NC = pd.read_csv(DEL + "stepC_ncr_node_cars.csv"); Q = pd.read_csv(DEL + "stepC_ncr_quarterly.csv")
# ---------------- 3(ii) Panel A ----------------
SEV = {"DLF": 0.42, "NBCC": 0.94}   # share of plant cost in NCR districts (evidence_NCR.csv node 1)
OWN = {"AHLUCONT": "33.3% of order book in Delhi NCR (31 Dec 2024)", "BLKASHYAP": "order book Haryana 45.4%, Delhi 10.1% (31 Dec 2024)",
       "JKIL": "not established", "NCC": "not established", "PSPPROJECT": "not established", "CEMPRO": "yes (IKEA building, Noida)", "LT": "not established", "CAPACITE": "yes (NCR an operating region)"}
links = {"AHLUCONT": "N001", "BLKASHYAP": "N002", "JKIL": "N004"}
COMP = ["NCC", "PSPPROJECT", "CEMPRO", "LT", "CAPACITE"]
OUTC = [("18 Nov 2024", "(-1,5)"), ("18 Nov 2024", "(6,20)"), ("18 Nov 2024", "(21,60)"), ("17 Dec 2024", "(-1,5)"), ("17 Dec 2024", "(6,20)")]
rows = []
for f in list(links) + COMP:
    r = dict(panel="A: NCR backward (H3), within-zone contractors", nse_symbol=f)
    if f in links:
        l = L[L.link_id == links[f]].iloc[0]; lo, hi = float(l.w_supplier_sales_low), float(l.w_supplier_sales_high); s = SEV[l.buyer_symbol]
        r.update(link_id=l.link_id, buyer=l.buyer_symbol, link_status=l.status, w_low=lo, w_high=hi, w_mid=(lo + hi) / 2, buyer_exposure=s)
    else:
        r.update(link_id="(comparison: no link found)", buyer="", link_status="zero dose", w_low=0.0, w_high=0.0, w_mid=0.0, buyer_exposure=np.nan)
    for k in ("low", "high", "mid"): r[f"dose_{k}"] = r[f"w_{k}"] * (r["buyer_exposure"] if f in links else 0.0)
    r["own_ncr_exposure"] = OWN[f]
    for ev, w in OUTC:
        x = NC[(NC.nse_symbol == f) & (NC.event == ev) & (NC.window == w)]
        r[f"car_{ev[:6].replace(' ', '')}_{w}"] = x.car.iloc[0] if len(x) else np.nan
    q = Q[(Q.nse_symbol == f) & (Q.quarter == "2024-12-31")]; q2 = Q[(Q.nse_symbol == f) & (Q.quarter == "2024-09-30")]
    r["q3fy25_sales_yoy_pct"] = q.sales_yoy_pct.iloc[0] if len(q) else np.nan; r["q3fy25_opm_change_pp"] = q.opm_change_yoy_pp.iloc[0] if len(q) else np.nan
    r["q2fy25_sales_yoy_pct_preban"] = q2.sales_yoy_pct.iloc[0] if len(q2) else np.nan   # placebo outcome: the quarter before the ban
    r["q3_minus_q2_sales_yoy_pp"] = r["q3fy25_sales_yoy_pct"] - r["q2fy25_sales_yoy_pct_preban"]
    rows.append(r)
A = pd.DataFrame(rows)
fits = []
outcomes = [c for c in A.columns if c.startswith("car_")] + ["q3fy25_sales_yoy_pct", "q3fy25_opm_change_pp", "q2fy25_sales_yoy_pct_preban", "q3_minus_q2_sales_yoy_pp"]
for dose, sample in (("dose_mid", "all 8"), ("dose_low", "all 8"), ("dose_high", "all 8"), ("dose_mid", "without B.L. Kashyap")):
    AA = A if sample == "all 8" else A[A.nse_symbol != "BLKASHYAP"].reset_index(drop=True)
    d = AA[dose].values
    perms = np.array(list(itertools.permutations(range(len(d)))))
    for o in outcomes:
        y = AA[o].values; ok = ~np.isnan(y)
        if ok.sum() < 4: continue
        dd, yy = d[ok], y[ok]
        def slope(dv): dv = dv - dv.mean(); return (dv * (yy - yy.mean())).sum() / (dv ** 2).sum()
        b = slope(dd)
        P = np.array(list(itertools.permutations(range(len(dd))))) if ok.sum() != len(d) else perms
        bs = np.array([slope(dd[p]) for p in P])
        fits.append(dict(panel="A: NCR backward (H3)", dose=dose, sample=sample, outcome=o, n=int(ok.sum()), n_linked=int((dd > 0).sum()), slope=b,
                         effect_at_ahluwalia_dose=b * float(A.loc[A.nse_symbol == "AHLUCONT", dose].iloc[0]),
                         perm_p_two_sided=(np.abs(bs) >= abs(b) - 1e-12).mean(), n_permutations=len(bs),
                         note=("placebo outcome: the quarter before the ban" if o == "q2fy25_sales_yoy_pct_preban" else "slope per unit of dose (dose = weight x buyer's NCR exposure)")))
F = pd.DataFrame(fits)
# ---------------- Panel B ----------------
g = L[L.link_id == "G001"].iloc[0]
GN = pd.read_csv(DEL + "stepC_gj_node_cars.csv"); TS = pd.read_csv(DEL + "stepC_gj_tcpl_salt.csv"); RD = pd.read_csv(DEL + "stepC_gj_results_days.csv")
gc = lambda w: GN[(GN.nse_symbol == "TATACONSUM") & (GN.window == w)].car.iloc[0]
ts = TS.set_index("period")
B = pd.DataFrame([dict(panel="B: Gujarat forward (H2)", nse_symbol="TATACONSUM", link_id="G001", buyer="TATACONSUM (buyer); supplier TATACHEM", link_status=g.status,
    w_low=float(g.w_buyer_input_cost_low), w_high=float(g.w_buyer_input_cost_high), w_mid=(float(g.w_buyer_input_cost_low) + float(g.w_buyer_input_cost_high)) / 2,
    buyer_exposure=np.nan, own_ncr_exposure="supplier hit severity: about 10 days at Mithapur; 40,000 t salt lost against 13.48 lakh t of annual salt demand from Tata Consumer (about 3% of a year)",
    **{"car_26Aug_(-1,5)": gc("(-1,5)"), "car_26Aug_(6,20)": gc("(6,20)"), "car_26Aug_(21,60)": gc("(21,60)")},
    results_day_21oct_ar=RD[(RD.nse_symbol == "TATACONSUM") & (RD.date == "2024-10-21")].abnormal_return.iloc[0],
    salt_price_mix_q1_q3_q4_pp=f"{ts.loc['Q1 FY25','implied_price_mix_pp']:+.0f} / {ts.loc['Q3 FY25','implied_price_mix_pp']:+.0f} / {ts.loc['Q4 FY25','implied_price_mix_pp']:+.0f}",
    salt_volume_q1_q4_pct=" / ".join(f"{ts.loc[q,'salt_volume_growth_pct']:+.0f}" for q in ("Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25")),
    note="one link: no slope. Weight = Tata Chemicals' share of Tata Consumer's material input cost (FY24). The buyer's response is a retail price increase (Rs 2 on Rs 28, about 7%, from Oct 2024) with margin held; results-day return is tea-driven (company)")])
# ---------------- Panel C ----------------
CT = pd.read_csv(DEL + "cement_market_test.csv"); CT = CT[CT.spec.str.startswith("main")]
C = pd.DataFrame([dict(panel="C: NCR market level (not a firm link)", nse_symbol=f"cement makers: {r.n_north} with northern capacity vs {r.n_none} with none", link_id="binary dose",
    link_status="G5: coarse, labelled test; +2.5 pp over (-1,+5) is the result", buyer=f"{r.event} {r.window}", w_mid=np.nan,
    note=f"gap north minus none {r.gap_north_minus_none:+.3f} (p={r.p_two_sided:.2f}); a hit would make the gap negative") for r in CT.itertuples()])
T2 = pd.concat([A, B, C], ignore_index=True); T2.round(4).to_csv(DEL + "table2_dose_response.csv", index=False); F.round(4).to_csv(DEL + "table2_dose_response_fit.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 60)
print(A[["nse_symbol", "w_mid", "buyer_exposure", "dose_mid"] + outcomes].round(3).to_string(index=False))
print(F[["dose", "sample", "outcome", "n", "slope", "effect_at_ahluwalia_dose", "perm_p_two_sided"]].round(3).to_string(index=False))
# ---------------- 3(iii) placebos ----------------
if os.environ.get("SKIP_PLACEBO"): sys.exit(0)
PF = pd.read_csv(DEL + "placebo_firms.csv"); PF = PF[PF.included == "yes"]
GROUPS = [("A: unexposed, unlinked placebo firms", "NCR", sorted(PF[PF.event == "E_NCR_GRAP_2024"].nse_symbol)),
          ("A: unexposed, unlinked placebo firms (list provisional)", "GJ", sorted(PF[PF.event.str.startswith("E_GJ")].nse_symbol)),
          ("B: G2 control firms (developers with no NCR project)", "NCR", ["BRIGADE", "PURVA", "AJMERA", "RUSTOMJEE", "KOLTEPATIL", "SUNTECK", "LODHA", "VASCONEQ"]),
          ("B: G2 control firms (fertiliser and specialty, no Gujarat plant)", "GJ", ["CHAMBLFERT", "NFL", "PARADEEP", "VINATIORGA", "CLEAN", "SUDARSCHEM"]),
          ("C: unlinked comparison contractors (zero dose)", "NCR", COMP)]
EVW = {"NCR": [("18 Nov 2024", "2024-11-18", [(-1, 3), (-1, 5), (6, 20), (21, 60)]), ("17 Dec 2024", "2024-12-17", [(-1, 5), (6, 20)])],
       "GJ": [("26 Aug 2024", "2024-08-26", [(-1, 5), (6, 20), (21, 60)])]}
allf = sorted({f for _, _, fs in GROUPS for f in fs}); allf = [f for f in allf if f in E.R.columns]
PL = [a.reindex(columns=allf) for a in (E.ar_matrix(t, pre=1, post=60) for t in E.placebo_t0s(n=1000, post=60)) if a is not None]
out = []
for lab, ev, fs in GROUPS:
    fs = [f for f in fs if f in E.R.columns]
    for evl, day, wins in EVW[ev]:
        ar = E.ar_matrix(E.t0_of(day), pre=1, post=60).reindex(columns=allf)
        for w in wins:
            cars = E.car(ar[fs], *w); m = cars.mean()
            dist = pd.Series([E.car(P[fs], *w).mean() for P in PL]).dropna()
            indiv = []
            for f in fs:
                if pd.isna(cars[f]): continue
                pf = pd.Series([E.car(P[[f]], *w).iloc[0] for P in PL]).dropna()
                indiv.append((pf.abs() >= abs(cars[f])).mean())
            indiv = np.array(indiv)
            out.append(dict(test=lab, event=evl, window=f"({w[0]},{w[1]})", n_firms=int(cars.notna().sum()), mean_car=m, p_two_sided=(dist.abs() >= abs(m)).mean(),
                            placebo_sd=dist.std(), share_firms_p_below_05=(indiv < 0.05).mean() if len(indiv) else np.nan, n_firms_p_below_05=int((indiv < 0.05).sum()),
                            expected_share=0.05, n_placebo_days=len(dist), firms=" ".join(fs)))
T3 = pd.DataFrame(out); T3.round(4).to_csv(DEL + "table3_placebo.csv", index=False)
print(T3.drop(columns=["firms"]).round(3).to_string(index=False))
