"""Shared loaders + cleaned inputs for the climate / asset-exposure project."""
import os, numpy as np, pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D, EXT, OUT = ROOT + "/data/", ROOT + "/external/", ROOT + "/outputs/"
TAB, FIG = OUT + "tables/", OUT + "figs/"

# --- events. Pack events + recurrences named in the pack. Dates VERIFIED against CAQM/PIB orders
# and press (see research/verified_event_dates.csv). 'start' = date the shock became public;
# the engine uses the first trading day on/after it.
#  * GRAP-IV 2024: order issued Sun 17 Nov, effective 8am Mon 18 Nov -> first trading day 18 Nov.
#    Re-imposed late evening Mon 16 Dec -> first trading day 17 Dec. (Revoked 5 Dec and 24 Dec.)
#  * Only the 2024 schedule bans ALL construction; in 2022/2023 Stage IV halted linear public
#    projects only -> 2022/2023 are a weaker treatment for real-estate firms.
#    ROUND 3 NOTE (dates below unchanged): the press releases show the ban on building construction
#    is a Stage III measure in all three years; Stage IV only adds linear public projects. The
#    Stage III order dates are tested separately in 24_grap_stage3_event_study.py (README 5.15).
#  * Gujarat 2023: Sardar Sarovar release began Sat 16 Sep; Bharuch/Ankleshwar flooded 17-18 Sep.
EVENTS = pd.DataFrame([
    ("E_NCR_GRAP_2024", "NCR", "2024-11-05", "pack",  "GRAP 2024 (pack date, 5 Nov - wrong)"),
    ("E_NCR_GRAP4_2024", "NCR", "2024-11-18", "verified", "GRAP-IV 2024, 1st (18 Nov)"),
    ("E_NCR_GRAP4_2024B", "NCR", "2024-12-17", "verified", "GRAP-IV 2024, 2nd (17 Dec)"),
    ("E_NCR_GRAP4_2023", "NCR", "2023-11-05", "verified", "GRAP-IV 2023 (5 Nov)"),
    ("E_NCR_GRAP4_2022", "NCR", "2022-11-03", "verified", "GRAP-IV 2022 (3 Nov)"),
    ("E_GJ_FLOOD_2024", "GJ",  "2024-08-25", "pack",  "Gujarat flood 2024 (Vadodara)"),
    ("E_GJ_FLOOD_2023", "GJ",  "2023-09-16", "verified", "Gujarat flood 2023 (Narmada/Bharuch)"),
    ("E_HP_FLOOD_2023", "HP",  "2023-07-08", "pack",  "Himachal flood 2023"),
    ("E_CHE_FLOOD_2023", "CHE", "2023-12-04", "pack",  "Chennai Michaung 2023"),
], columns=["event_id", "zone", "start", "src", "label"])
EVENTS["start"] = pd.to_datetime(EVENTS.start)

# --- corrected district footprints (exact names as they appear in plants.csv) ----------------
ZONES = {
    "NCR": ["Baghpat", "East Delhi", "Faridabad", "Gautam Buddha Nagar", "Ghaziabad", "Gurgaon",
            "Jhajjar", "Meerut", "NCT of Delhi", "NCT of Delhi Districts", "New Delhi", "North Delhi",
            "North East Delhi", "North West Delhi", "Sonipat", "South Delhi", "South West Delhi",
            "West Delhi", "Central Delhi", "Shahdara", "South East Delhi"],
    "GJ": ["Vadodara", "Bharuch", "Anand", "Kheda", "Panchmahal", "Panch Mahals", "Navsari", "Tapi", "Dang"],
    # pack's substring match also swept in Guna, Junagadh, Virudhunagar, Yamunanagar,
    # Bilaspur (Chhattisgarh), Hamirpur (UP), Arunachal Pradesh -> removed here
    "HP": ["Solan", "Sirmaur", "Shimla", "Kullu", "Una", "Bilaspur  HP", "Hamirpur  HP", "Mandi"],
    "CHE": ["Chennai", "Kancheepuram", "Chengalpattu", "Tiruvallur", "Thiruvallur", "Villupuram"],
}

def companies(): return pd.read_csv(D + "companies.csv")
def plants(): return pd.read_csv(D + "plants.csv")

def stock():
    s = pd.read_csv(D + "stock_daily.csv", parse_dates=["date"]).sort_values(["asset_id", "date"])
    # BUG IN PACK: every date is stamped one calendar day early (IST midnight -> UTC), so trading
    # days appear as Sun-Thu. Verified: Adani/Hindenburg, 4-Jun-2024 election crash, Saturday
    # budget sessions and NIFTY same-day correlation all line up only after +1 day.
    # (RAJESHEXPO alone is stamped correctly, so the shift is applied only to firms whose "trading
    # days" fall on Sundays.)
    sun = s.groupby("asset_id").date.transform(lambda d: (d.dt.dayofweek == 6).mean())
    s.loc[sun > 0.05, "date"] += pd.Timedelta(days=1)
    s = s.drop_duplicates(["asset_id", "date"], keep="first")   # 2020-06-23 is duplicated for all firms
    s["ret"] = s.daily_return
    # corporate-action artefacts: unadjusted jumps (e.g. NMDC 2022-10-26 +86% on NMDC-Steel demerger)
    s.loc[s.ret.abs() > 0.40, "ret"] = np.nan
    return s

def returns_wide():
    return stock().pivot(index="date", columns="asset_id", values="ret")

def indices():
    i = pd.read_csv(EXT + "indices_daily.csv", parse_dates=["date"])
    w = i.pivot_table(index="date", columns="index", values="close").sort_index()
    return w.pct_change(fill_method=None)

def exposure():
    """firm x zone exposure with corrected footprints. cost share, plant-count share."""
    p = plants()
    tot = p.groupby("nse_symbol").agg(total_cost=("project_cost_cr", "sum"), n_plants=("lat", "size"))
    rows = []
    for z, ds in ZONES.items():
        h = p[p.dist_name.isin(ds)].groupby("nse_symbol").agg(
            exp_cost=("project_cost_cr", "sum"), exp_plants=("lat", "size"))
        h["zone"] = z; rows.append(h.reset_index())
    e = pd.concat(rows).merge(tot, on="nse_symbol")
    e["share_cost"] = e.exp_cost / e.total_cost.replace(0, np.nan)
    e["share_plants"] = e.exp_plants / e.n_plants
    return e

def sector(ind):
    i = str(ind).lower()
    for k, v in [("housing", "Realty/Construction"), ("cement", "Cement"), ("steel", "Steel/Metals"),
                 ("iron", "Steel/Metals"), ("alumin", "Steel/Metals"), ("mineral", "Steel/Metals"),
                 ("chemical", "Chemicals"), ("dyes", "Chemicals"), ("pesticide", "Chemicals"),
                 ("fertil", "Chemicals"), ("tyre", "Auto/Tyres"), ("vehicle", "Auto/Tyres"),
                 ("electricity", "Power"), ("gas", "Oil&Gas"), ("refinery", "Oil&Gas"), ("storage", "Oil&Gas"),
                 ("health", "Healthcare/Pharma"), ("drug", "Healthcare/Pharma")]:
        if k in i: return v
    return "Other"
