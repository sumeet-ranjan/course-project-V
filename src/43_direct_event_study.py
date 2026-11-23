"""Deliverable 3(i): direct event study on the two key events — a rerun of the existing engine (src/es_lib.py)
with the firm sets of decision G2 (research/realign/g2_decision.csv, written by src/45_g2_decision.py) — and
the quarterly DiD.

Engine (unchanged): market model against NIFTY 500, estimation window [-250,-30] trading days (es_lib.ar_matrix),
CAR = sum of abnormal returns with at least 70% of days present (es_lib.car), placebo-date inference on 1,000
random event days (es_lib.placebo_t0s). Only the return matrix is extended: listed peers outside the sample
(Yahoo adjusted closes, external/prices_peers.csv) and two benchmark indices treated as firms (Nifty PSE, Nifty Realty).

Windows: (-1,+5), (+6,+20), (+21,+60) (non-overlapping), plus (-1,+3) for NCR, which ends on 22 Nov 2024
(before the PSU rally of 25 Nov). NCR caveats: 17 Dec 2024 (re-imposition) is day +20; Stage III was in force
again on 3-5, 9-12, 15-17 Jan and 29 Jan - 3 Feb 2025, all inside (+21,+60).

Statistics (each with a placebo p-value from the same statistic on 1,000 random days):
  NCR      confirmed (NBCC, DLF) and unconfirmed (ANANTRAJ, PARSVNATH, UNITECH) builders, separately:
           mean CAR minus the equal-weighted mean of all eligible developer controls (main);
           mean over builders of [CAR - mean of its two nearest-by-size controls] (robustness).
           NBCC minus the Nifty PSE index. Confirmed builders minus the within-zone firms (same zone, not banned).
           Pooled Stage III starts (31 Oct 2022, 3 Nov 2023, 18 Nov 2024, 17 Dec 2024): mean of per-event statistics,
           placebo drawn jointly (four random days per draw).
  Gujarat  pack footprint (10 chemical firms) and Vadodara sites (4), separately: mean over firms of
           [CAR - equal-weighted mean of the firm's sub-industry pool] (main); nearest two by size within the pool (robustness).
Quarterly DiD: y_it = firm FE + quarter FE + b * exposed_i * post_t; SE clustered by firm; outcomes YoY sales growth (%)
and operating margin (%); post = the event quarter and the next.
Outputs: outputs/deliverables/table1_direct.csv, table1_direct_firms.csv, table1_returns_25nov2024.csv, table1_did.csv
"""
import os, sys, io, time, urllib.request; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import es_lib as E
from common import ROOT, EXT, OUT
DEL = OUT + "deliverables/"; os.makedirs(DEL, exist_ok=True)
G = pd.read_csv(ROOT + "/research/realign/g2_decision.csv", dtype=str).fillna("")
# --- extend the engine's return matrix (same trading calendar) ---------------------------------------------
pp = pd.read_csv(EXT + "prices_peers.csv", parse_dates=["date"])
peer = pp.pivot_table(index="date", columns="asset_id", values="adjclose").sort_index().pct_change(fill_method=None)
ix = pd.read_csv(EXT + "indices_psu_infra.csv", parse_dates=["date"]).pivot_table(index="date", columns="index", values="close").sort_index().pct_change(fill_method=None)
add = pd.concat([peer, ix[["NIFTY_PSE", "NIFTY_REALTY"]]], axis=1).reindex(E.R.index)
E.R = pd.concat([E.R, add[[c for c in add.columns if c not in E.R.columns]]], axis=1)
DAY = {"E_NCR_GRAP_2024": "2024-11-18", "E_NCR_GRAP_2024B": "2024-12-17", "NCR_S3_2022": "2022-10-31", "NCR_S3_2023": "2023-11-03", "E_GJ_FLOOD_2024": "2024-08-26"}
WIN = {"NCR": [(-1, 3), (-1, 5), (6, 20), (21, 60)], "GJ": [(-1, 5), (6, 20), (21, 60)]}
WALL = sorted(set(WIN["NCR"]) | set(WIN["GJ"]))
def cars_at(t0):
    ar = E.ar_matrix(t0, pre=1, post=60)
    return None if ar is None else pd.DataFrame({w: E.car(ar, *w) for w in WALL}), ar
PT = E.placebo_t0s(n=1000, post=60)
PLAC = [cars_at(t)[0] for t in PT]
PLAC = [p for p in PLAC if p is not None]
def m(C, firms): return C.reindex(firms).mean() if len(firms) else pd.Series(np.nan, index=C.columns)
def one(C, f): return C.loc[f] if f in C.index else pd.Series(np.nan, index=C.columns)
def stat_pool(C, ex, ctl): return m(C, ex) - m(C, ctl)
def stat_matched(C, ex, ctl_of):
    d = [C.loc[e] - m(C, [c for c in ctl_of(e) if c in C.index]) for e in ex if e in C.index]
    return pd.DataFrame(d).mean() if d else pd.Series(np.nan, index=C.columns)
rows, firm_rows = [], []
def record(event, group, bench, fn, n_ex, n_ctl, windows, note=""):
    C0 = CARS[event]; a = fn(C0)
    pl = pd.DataFrame([fn(P) for P in PLAC])
    for w in windows:
        ps = pl[w].dropna()
        rows.append(dict(event=event, event_day=DAY[event], group=group, benchmark=bench, window=f"({w[0]},{w[1]})", n_exposed=n_ex, n_benchmark=n_ctl,
                         statistic=a[w], p_two_sided=(ps.abs() >= abs(a[w])).mean(), p_one_sided_neg=(ps <= a[w]).mean(), placebo_sd=ps.std(), n_placebo=len(ps), note=note))
CARS, ARS = {}, {}
for ev, d in DAY.items():
    CARS[ev], ARS[ev] = cars_at(E.t0_of(d))
def sel(ev, role=None, group=None):
    g = G[G.event == ev]
    if role: g = g[g.role == role]
    if group: g = g[g.group == group]
    return list(g.nse_symbol)
# ---------------- NCR ----------------
for ev in ("E_NCR_GRAP_2024", "E_NCR_GRAP_2024B"):
    C = CARS[ev]; ctl = [c for c in sel(ev, "control") if c in C.index]; nn = G[(G.event == ev) & (G.role == "control_nn")]
    for grp in ("confirmed", "unconfirmed"):
        ex = [c for c in sel(ev, "exposed", grp) if c in C.index]
        record(ev, f"{grp} builders ({', '.join(ex)})", "all eligible developer controls, equal-weighted (main)", lambda X, ex=ex, ctl=ctl: stat_pool(X, ex, ctl), len(ex), len(ctl), WIN["NCR"])
        record(ev, f"{grp} builders ({', '.join(ex)})", "two nearest controls by size (robustness)",
               lambda X, ex=ex: stat_matched(X, ex, lambda e: list(nn[nn.match_for == e].nse_symbol)), len(ex), 2, WIN["NCR"])
    wz = [c for c in sel(ev, "within_zone") if c in C.index]; conf = [c for c in sel(ev, "exposed", "confirmed") if c in C.index]
    record(ev, "within-zone firms (" + ", ".join(wz) + ")", "market model only (mean CAR)", lambda X, wz=wz: m(X, wz), len(wz), 0, WIN["NCR"])
    record(ev, "confirmed builders minus within-zone firms", "within-zone firms (same zone, not under the ban)", lambda X, wz=wz, conf=conf: stat_pool(X, conf, wz), len(conf), len(wz), WIN["NCR"])
    record(ev, "NBCC", "Nifty PSE index (PSU benchmark)", lambda X: one(X, "NBCC") - one(X, "NIFTY_PSE"), 1, 1, WIN["NCR"])
    record(ev, "NBCC", "all eligible developer controls, equal-weighted", lambda X, ctl=ctl: one(X, "NBCC") - m(X, ctl), 1, len(ctl), WIN["NCR"])
    record(ev, "DLF", "all eligible developer controls, equal-weighted", lambda X, ctl=ctl: one(X, "DLF") - m(X, ctl), 1, len(ctl), WIN["NCR"])
    for f in sorted(set(sel(ev))):
        if f in C.index:
            r = G[(G.event == ev) & (G.nse_symbol == f)].iloc[0]
            firm_rows.append(dict(event=ev, nse_symbol=f, group=r.group, role=r.role, **{f"car_{w[0]}_{w[1]}": C.loc[f, w] for w in WIN["NCR"]}))
# pooled Stage III starts
EVS = ["NCR_S3_2022", "NCR_S3_2023", "E_NCR_GRAP_2024", "E_NCR_GRAP_2024B"]
rng = np.random.default_rng(11)
for grp in ("confirmed", "unconfirmed"):
    per = {}
    for ev in EVS:
        C = CARS[ev]; ex = [c for c in sel(ev, "exposed", grp) if c in C.index]; ctl = [c for c in sel(ev, "control") if c in C.index]
        per[ev] = stat_pool(C, ex, ctl)
    per = pd.DataFrame(per).T; a = per.mean()
    ex0 = sel("E_NCR_GRAP_2024", "exposed", grp); ctl0 = sel("E_NCR_GRAP_2024", "control")
    pl = []
    for k in range(1000):
        idx = rng.choice(len(PLAC), size=len(EVS), replace=False)
        pl.append(pd.DataFrame([stat_pool(PLAC[i], ex0, ctl0) for i in idx]).mean())
    pl = pd.DataFrame(pl)
    for w in WIN["NCR"]:
        ps = pl[w].dropna()
        rows.append(dict(event="NCR pooled Stage III starts", event_day="; ".join(DAY[e] for e in EVS), group=f"{grp} builders", benchmark="all eligible developer controls, equal-weighted",
                         window=f"({w[0]},{w[1]})", n_exposed=len(ex0), n_benchmark=len(ctl0), statistic=a[w], p_two_sided=(ps.abs() >= abs(a[w])).mean(),
                         p_one_sided_neg=(ps <= a[w]).mean(), placebo_sd=ps.std(), n_placebo=len(ps),
                         note="per event: " + "; ".join(f"{e} {per.loc[e, w]:+.4f}" for e in EVS)))
# returns on 25 Nov 2024 (day +4 of the 18 Nov event): raw and abnormal
ar = ARS["E_NCR_GRAP_2024"]; day25 = pd.Timestamp("2024-11-25"); i25 = E.t0_of("2024-11-25") - E.t0_of("2024-11-18")
lst = sel("E_NCR_GRAP_2024", "exposed") + sel("E_NCR_GRAP_2024", "control") + ["NIFTY_PSE", "NIFTY_REALTY"]
t25 = pd.DataFrame([dict(nse_symbol=f, role=("benchmark index" if f.startswith("NIFTY") else G[(G.event == "E_NCR_GRAP_2024") & (G.nse_symbol == f)].group.iloc[0]),
                         raw_return_25nov=E.R.loc[day25, f], abnormal_return_25nov=ar.loc[i25, f] if f in ar.columns else np.nan) for f in lst])
t25 = pd.concat([t25, pd.DataFrame([dict(nse_symbol="NIFTY500 (market)", role="market", raw_return_25nov=E.MKT.loc[day25], abnormal_return_25nov=np.nan)])], ignore_index=True)
t25.round(4).to_csv(DEL + "table1_returns_25nov2024.csv", index=False)
# ---------------- Gujarat ----------------
ev = "E_GJ_FLOOD_2024"; C = CARS[ev]
pool_of = G[(G.event == ev) & (G.role == "control")].groupby("pool").nse_symbol.apply(list).to_dict()
for grp in ("pack_footprint", "vadodara_sites"):
    g = G[(G.event == ev) & (G.group == grp) & (G.role == "exposed")]; ex = [c for c in g.nse_symbol if c in C.index]
    pool = dict(zip(g.nse_symbol, g.pool)); nn = G[(G.event == ev) & (G.group == grp + "_nn")]
    record(ev, f"{grp} ({', '.join(ex)})", "own sub-industry pool, equal-weighted (main)", lambda X, ex=ex, pool=pool: stat_matched(X, ex, lambda e: pool_of[pool[e]]), len(ex), 3, WIN["GJ"])
    record(ev, f"{grp} ({', '.join(ex)})", "two nearest by size within the sub-industry pool (robustness)",
           lambda X, ex=ex, nn=nn: stat_matched(X, ex, lambda e: list(nn[nn.match_for == e].nse_symbol)), len(ex), 2, WIN["GJ"],
           note="five firms have no size match within their pool (SRF, UPL, KIRIINDUS, BODALCHEM, ZUARI); they are kept but are not size-matched")
    for f in ex:
        firm_rows.append(dict(event=ev, nse_symbol=f, group=grp, role="exposed", pool=pool[f], **{f"car_{w[0]}_{w[1]}": C.loc[f, w] for w in WIN["GJ"]}))
for pl_, cs in pool_of.items():
    for f in cs:
        if f in C.index: firm_rows.append(dict(event=ev, nse_symbol=f, group="controls", role="control", pool=pl_, **{f"car_{w[0]}_{w[1]}": C.loc[f, w] for w in WIN["GJ"]}))
T = pd.DataFrame(rows); T.round(4).to_csv(DEL + "table1_direct.csv", index=False)
pd.DataFrame(firm_rows).round(4).to_csv(DEL + "table1_direct_firms.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 70)
print(T.drop(columns=["note", "placebo_sd", "event_day"]).round(3).to_string(index=False))
print(t25.round(4).to_string(index=False))
# ---------------- quarterly DiD -----------------------------------------------------------------------
import statsmodels.formula.api as smf
from bs4 import BeautifulSoup
def screener_quarters(sym):
    for cons in (True, False):
        try:
            u = f"https://www.screener.in/company/{sym}/" + ("consolidated/" if cons else "")
            s = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=40).read().decode(), "lxml")
            t = s.find("section", id="quarters").find("table"); d = pd.read_html(io.StringIO(str(t)))[0]
            d = d.rename(columns={d.columns[0]: "item"}); d["item"] = d.item.str.replace("+", "", regex=False).str.strip()
            if d.shape[1] > 3: return d.melt(id_vars="item", var_name="period", value_name="value").assign(firm=sym, basis="consolidated" if cons else "standalone")
        except Exception: pass
        time.sleep(1.5)
    return None
QP = EXT + "fin_quarterly_peers.csv"
q = pd.read_csv(EXT + "fin_quarterly.csv")
need = sorted(set(G[G.role.isin(["exposed", "control"])].nse_symbol) - set(q.firm))
have = pd.read_csv(QP) if os.path.exists(QP) else pd.DataFrame(columns=["firm"])
new = [screener_quarters(s) for s in need if s not in set(have.firm)]
have = pd.concat([have] + [n for n in new if n is not None], ignore_index=True); have.to_csv(QP, index=False)
q = pd.concat([q, have], ignore_index=True)
q["value"] = pd.to_numeric(q.value.astype(str).str.replace(",", "").str.replace("%", ""), errors="coerce")
q["qe"] = pd.to_datetime(q.period.astype(str).str.strip().str[:8], format="%b %Y", errors="coerce") + pd.offsets.MonthEnd(0)
q = q.dropna(subset=["qe", "value"]).drop_duplicates(["firm", "item", "qe"])
sales = q[q.item == "Sales"].pivot_table(index="qe", columns="firm", values="value")
gro = (sales / sales.shift(4) - 1) * 100
opm = q[q.item == "OPM %"].pivot_table(index="qe", columns="firm", values="value")
panel = pd.concat([gro.stack().rename("sales_growth_yoy_pct"), opm.stack().rename("operating_margin_pct")], axis=1).reset_index().rename(columns={"level_1": "firm"})
POST = {"E_NCR_GRAP_2024": ["2024-12-31", "2025-03-31"], "E_GJ_FLOOD_2024": ["2024-09-30", "2024-12-31"]}
did = []
for ev, post in POST.items():
    groups = ["confirmed", "unconfirmed"] if ev.startswith("E_NCR") else ["pack_footprint", "vadodara_sites"]
    ctl = sel(ev, "control")
    for grp in groups:
        ex = sel(ev, "exposed", grp)
        d = panel[panel.firm.isin(ex + ctl) & (panel.qe >= "2023-09-30") & (panel.qe <= "2025-09-30")].copy()
        d["treat_post"] = (d.firm.isin(ex) & d.qe.isin(pd.to_datetime(post))).astype(float); d["qtr"] = d.qe.dt.strftime("%Y-%m")
        for y in ("sales_growth_yoy_pct", "operating_margin_pct"):
            dd = d.dropna(subset=[y])
            if dd.firm.nunique() < 4 or dd.treat_post.sum() == 0: continue
            r = smf.ols(f"{y} ~ treat_post + firm + qtr", data=dd).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(dd.firm)[0]})
            did.append(dict(event=ev, group=grp, outcome=y, post_quarters=" & ".join(post), coef=r.params["treat_post"], se_cluster_firm=r.bse["treat_post"],
                            p=r.pvalues["treat_post"], n_obs=int(r.nobs), n_firms=dd.firm.nunique(), n_exposed=dd[dd.firm.isin(ex)].firm.nunique()))
D = pd.DataFrame(did); D.round(4).to_csv(DEL + "table1_did.csv", index=False); print(D.round(3).to_string(index=False))
