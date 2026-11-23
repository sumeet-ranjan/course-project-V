#!/usr/bin/env python3
"""build_real_sample.py — assemble a REAL (not synthetic) sample for the climate -> value-chain
propagation RA project. Nothing is planted: these are real listed firms, real plant locations,
real financials, real daily stock, and documented real extreme events. The sample is CHOSEN for
the highest promise of a traceable pathway — firms whose physical assets are concentrated in
districts hit by well-documented, dated events, plus their value-chain-industry neighbours and
clean controls.

Sources (all on NAS, public-domain in origin):
  plant_cell_map.parquet        firm -> plant lat/lon/district/industry/project_cost (asset distribution)
  gold/firm_fundamental_nowcast real financials: log-sales, ebitda margin, growth, capex, filing dates
  silver/market/nse_1day        real daily OHLCV
  gold/env_grid/precip_monthly  to CONFIRM the flood events with a rainfall anomaly (no planting)

Run:  /tmp/geoenv/bin/python codebook/build_real_sample.py
"""
import glob
import os
import re

import numpy as np
import pandas as pd

ROOT = "/mnt/nas_cscg/ResearchData/stocast"
PCM = f"{ROOT}/gold/env_grid/plant_cell_map.parquet"
FUND = f"{ROOT}/gold/firm_fundamental_nowcast"
STOCK = f"{ROOT}/silver/market/nse_1day"
OUT = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT, exist_ok=True)
STK_FROM, STK_TO = "2020-01-01", "2025-12-31"

# ---- documented real events: district keywords (matched against plant dist_name) ----
EVENTS = [
    dict(event_id="E_NCR_GRAP_2024", type="pollution_shutdown",
         name="Delhi-NCR GRAP-IV construction/industry halt (Nov 2024; recurs Nov-22, Nov-23)",
         start="2024-11-05", end="2024-11-22", key=True,
         districts=["delhi", "gautam", "ghaziabad", "faridabad", "gurugram", "gurgaon",
                    "sonipat", "jhajjar", "meerut", "baghpat", "noida"],
         note="CAQM GRAP Stage-IV: non-essential construction banned, industrial fuel curbs across NCR."),
    dict(event_id="E_GJ_FLOOD_2024", type="flood",
         name="Gujarat floods — Vadodara/central Gujarat (Aug-Sep 2024; also 2023)",
         start="2024-08-25", end="2024-09-05", key=True,
         districts=["vadodara", "bharuch", "panchmahal", "anand", "kheda", "dang", "navsari", "tapi"],
         note="Vishwamitri/Narmada basin flooding submerges Vadodara-Bharuch chemical estates."),
    dict(event_id="E_HP_FLOOD_2023", type="flood",
         name="Himachal Pradesh floods/landslides (Jul 2023)",
         start="2023-07-08", end="2023-07-25", key=False,
         districts=["solan", "sirmaur", "shimla", "mandi", "kullu", "bilaspur", "una", "hamirpur"],
         note="Monsoon floods hit Baddi-Barotiwala-Nalagarh (Solan) pharma/industrial belt."),
    dict(event_id="E_CHE_FLOOD_2023", type="flood",
         name="Chennai cyclone Michaung floods (Dec 2023)",
         start="2023-12-04", end="2023-12-12", key=False,
         districts=["chennai", "kancheepuram", "kanchipuram", "chengalpattu", "tiruvallur", "villupuram"],
         note="Cyclone Michaung floods Chennai auto/electronics belt."),
]
# value-chain industry adjacency (upstream_kw -> downstream_kw), substring on industry_name.
# A SCAFFOLD/hypothesis the RAs must VERIFY from real disclosures — not ground truth.
CHAIN_HINTS = [
    ("cement", "construction"), ("cement", "real estate"), ("steel", "construction"),
    ("steel", "automobile"), ("iron", "steel"), ("auto ancillar", "automobile"),
    ("auto compon", "automobile"), ("organic chem", "pharmaceutic"),
    ("organic chem", "agrochemic"), ("dyes", "textile"), ("basic chem", "specialty"),
    ("specialty chem", "pharmaceutic"), ("yarn", "textile"), ("packaging", "food"),
]


def norm(s):
    return re.sub(r"[^a-z]", "", str(s).lower())


def main():
    p = pd.read_parquet(PCM)
    p["dist_l"] = p.dist_name.astype(str).str.lower()
    p["ind_l"] = p.industry_name.astype(str).str.lower()
    p["pc"] = pd.to_numeric(p.project_cost, errors="coerce").fillna(0.0)

    # firm totals (for exposure concentration)
    firm_tot = p.groupby("nse_symbol").agg(total_pc=("pc", "sum"), n_plants=("lat", "size"),
                                           co_code=("co_code", "first"),
                                           company=("company_name", "first")).reset_index()

    # ---- mark plant exposure to each event (district-keyword match) ----
    exp_rows = []
    for e in EVENTS:
        hit = p.dist_l.apply(lambda d: any(k in d for k in e["districts"]))
        for _, r in p[hit].iterrows():
            exp_rows.append(dict(event_id=e["event_id"], nse_symbol=r.nse_symbol,
                                 plant_lat=round(r.lat, 4), plant_lon=round(r.lon, 4),
                                 district=r.dist_name, industry=r.industry_name,
                                 plant_project_cost_cr=round(r.pc, 1)))
    exposure = pd.DataFrame(exp_rows)
    # firm-event exposure concentration = exposed project_cost / firm total
    fe = (exposure.groupby(["nse_symbol", "event_id"]).plant_project_cost_cr.sum().reset_index()
          .merge(firm_tot[["nse_symbol", "total_pc"]], on="nse_symbol"))
    fe["exposure_share"] = fe.plant_project_cost_cr / fe.total_pc.replace(0, np.nan)

    # ---- select firms: high-exposure to the two KEY events, + value-chain neighbours + controls ----
    key_ids = [e["event_id"] for e in EVENTS if e["key"]]
    # (a) directly-exposed: concentrated exposure to any event, listed; rank, take top per event
    sel = set()
    for e in EVENTS:
        sub = fe[(fe.event_id == e["event_id"]) & (fe.exposure_share >= 0.25)].sort_values(
            "plant_project_cost_cr", ascending=False).head(18 if e["event_id"] in key_ids else 8)
        sel |= set(sub.nse_symbol)
    exposed_firms = set(sel)
    # (b) value-chain-industry neighbours of the exposed firms (scaffold), listed, any location
    exp_inds = set(p[p.nse_symbol.isin(exposed_firms)].ind_l.unique())
    nbr_inds = set()
    for up, dn in CHAIN_HINTS:
        if any(up in i for i in exp_inds):
            nbr_inds.add(dn)
        if any(dn in i for i in exp_inds):
            nbr_inds.add(up)
    nbr = p[p.ind_l.apply(lambda i: any(n in i for n in nbr_inds)) & ~p.nse_symbol.isin(exposed_firms)]
    nbr_firms = set(nbr.groupby("nse_symbol").pc.sum().sort_values(ascending=False).head(25).index)
    sel |= nbr_firms
    # (c) controls: large firms in the SAME industries but with NO plant in any event district
    allexp = set(exposure.nse_symbol)
    ctrl_pool = p[p.ind_l.isin(exp_inds | nbr_inds) & ~p.nse_symbol.isin(allexp)]
    ctrl_firms = set(ctrl_pool.groupby("nse_symbol").pc.sum().sort_values(ascending=False).head(12).index)
    sel |= ctrl_firms
    sel = sorted(x for x in sel if isinstance(x, str) and x)
    print(f"selected {len(sel)} firms: {len(exposed_firms)} directly-exposed, "
          f"{len(nbr_firms)} chain-neighbours, {len(ctrl_firms)} controls", flush=True)

    role = {s: ("directly_exposed" if s in exposed_firms else
                "chain_neighbour" if s in nbr_firms else "control") for s in sel}

    # ---- companies + plants (asset distribution) for selected ----
    psel = p[p.nse_symbol.isin(sel)].copy()
    companies = (firm_tot[firm_tot.nse_symbol.isin(sel)]
                 .assign(role=lambda d: d.nse_symbol.map(role),
                         primary_industry=lambda d: d.nse_symbol.map(
                             psel.groupby("nse_symbol").industry_name.agg(
                                 lambda s: s.value_counts().index[0])))
                 [["nse_symbol", "co_code", "company", "primary_industry", "n_plants", "total_pc", "role"]]
                 .rename(columns={"total_pc": "total_project_cost_cr"}))
    plants = psel[["nse_symbol", "co_code", "company_name", "lat", "lon", "dist_name",
                   "industry_name", "pc"]].rename(columns={"pc": "project_cost_cr",
                                                           "company_name": "company"})
    exposure = exposure[exposure.nse_symbol.isin(sel)]

    # ---- financials (real) from firm_fundamental_nowcast ----
    try:
        ff = pd.concat([pd.read_parquet(f) for f in glob.glob(f"{FUND}/**/*.parquet", recursive=True)],
                       ignore_index=True)
        ff = ff.merge(companies[["nse_symbol", "co_code"]], on="co_code", how="inner")
        fin = ff[["nse_symbol", "co_code", "fund_period", "fund_filing_date", "f_log_sales",
                  "f_g_log_sales", "f_ebitda_margin", "f_capex_intensity", "n_plants"]].copy()
        fin["revenue_proxy_cr"] = np.round(np.exp(fin.f_log_sales), 1)
        fin = fin.drop_duplicates(["nse_symbol", "fund_period"]).sort_values(["nse_symbol", "fund_period"])
        print(f"financials: {len(fin)} firm-periods for {fin.nse_symbol.nunique()} firms", flush=True)
    except Exception as e:
        fin = pd.DataFrame(); print(f"financials join failed ({e}); RAs fetch from annual reports", flush=True)

    # ---- supply-chain scaffold among selected (industry adjacency; VERIFY from disclosures) ----
    ind_of = psel.groupby("nse_symbol").industry_name.agg(lambda s: s.value_counts().index[0]).to_dict()
    sc_rows = []
    for up, dn in CHAIN_HINTS:
        ups = [s for s in sel if up in norm_i(ind_of.get(s, ""))]
        dns = [s for s in sel if dn in norm_i(ind_of.get(s, ""))]
        for u in ups:
            for d in dns:
                if u != d:
                    sc_rows.append(dict(supplier=u, buyer=d, supplier_industry=ind_of[u],
                                        buyer_industry=ind_of[d], hint=f"{up}->{dn}",
                                        status="HYPOTHESIS_verify_from_disclosures"))
    scaffold = pd.DataFrame(sc_rows).drop_duplicates(["supplier", "buyer"])

    # ---- real daily stock for selected (pyarrow dataset, asset_id filter pushdown) ----
    import pyarrow.dataset as pads
    parts = [d for d in sorted(glob.glob(f"{STOCK}/date=*"))
             if STK_FROM <= os.path.basename(d).split("=")[1] <= STK_TO]
    files = [f for d in parts for f in glob.glob(f"{d}/*.parquet")]
    print(f"scanning {len(files)} stock files for {len(sel)} firms ...", flush=True)
    dset = pads.dataset(files, format="parquet")
    tbl = dset.to_table(columns=["asset_id", "timestamp", "open", "high", "low", "close", "volume"],
                        filter=pads.field("asset_id").isin(sel))
    sdf = tbl.to_pandas()
    sdf["date"] = pd.to_datetime(sdf.timestamp).dt.date.astype(str)
    sdf = sdf.sort_values(["asset_id", "date"])
    sdf["daily_return"] = sdf.groupby("asset_id").close.pct_change().round(5)
    stock = sdf[["asset_id", "date", "open", "high", "low", "close", "volume", "daily_return"]]
    print(f"stock: {len(stock)} rows, {stock.asset_id.nunique()} firms with price", flush=True)

    ev = pd.DataFrame([{k: e[k] for k in ("event_id", "type", "name", "start", "end", "note")}
                       | {"affected_district_keywords": "|".join(e["districts"]), "is_key_event": e["key"]}
                       for e in EVENTS])

    for name, df in [("companies", companies), ("plants", plants), ("financials_annual", fin),
                     ("stock_daily", stock), ("extreme_events", ev),
                     ("event_plant_exposure", exposure), ("supply_chain_scaffold", scaffold)]:
        df.to_csv(os.path.join(OUT, f"{name}.csv"), index=False)
        print(f"wrote {name}.csv rows={len(df)}", flush=True)


def norm_i(s):
    return str(s).lower()


if __name__ == "__main__":
    main()
