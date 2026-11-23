"""Optical check for standing water at the Chennai plants, Nov-Dec 2023 (Step 1b).

Sentinel-1 radar did not pass over Chennai between 30 Nov 2023 and 17 Jan 2024 (README 5.8), so the
only satellite views of surface water are optical, which cloud blocks. Sources (public, Microsoft
Planetary Computer, read as cloud-optimised GeoTIFF windows):
  * Sentinel-2 L2A: scene classification SCL (water = 6; cloud 8/9, cirrus 10, cloud shadow 3 and
    no-data 0/1 are "obscured") and MNDWI = (B03 - B11) / (B03 + B11) on clear pixels;
  * Landsat 7/8/9 Collection-2 L2: QA_PIXEL bits (clear = bit 6, water = bit 7; cloud bits 1-4).
For every plant in the Chennai zone and every scene: share of the 500 m circle that is clear, and the
share of the clear part that is water (SCL water or MNDWI > 0 for Sentinel-2; QA water for Landsat).
A plant has "new water" on an event scene if its clear water share is at least 10 points above its
own pre-event level (median of clear pre-event scenes) with at least 30% of the circle clear.
Outputs: external/optical_chennai_plant_scenes.csv, outputs/tables/optical_chennai_*.csv
"""
import os, sys, json, urllib.request, warnings
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd, rasterio, pyproj
from rasterio.windows import from_bounds
from common import *
warnings.filterwarnings("ignore")
os.environ.setdefault("GDAL_HTTP_MAX_RETRY", "4"); os.environ.setdefault("GDAL_HTTP_RETRY_DELAY", "2")
os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR"); os.environ.setdefault("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".tif")
API = "https://planetarycomputer.microsoft.com/api"
SUB = {"Chennai city": (12.90, 13.20, 80.15, 80.30), "Manali-Ennore": (13.14, 13.30, 80.24, 80.36),
       "Sriperumbudur-Oragadam": (12.78, 13.02, 79.78, 80.05), "Gummidipoondi": (13.35, 13.45, 80.05, 80.15)}
EVENT0, EVENT1 = pd.Timestamp("2023-12-04"), pd.Timestamp("2023-12-12")

def search(coll, bbox, d0, d1):
    body = {"collections": [coll], "bbox": bbox, "datetime": f"{d0}T00:00:00Z/{d1}T23:59:59Z", "limit": 200}
    req = urllib.request.Request(API + "/stac/v1/search", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=120))["features"]

def token(coll): return json.load(urllib.request.urlopen(f"{API}/sas/v1/token/{coll}", timeout=60))["token"]

P = plants().reset_index().rename(columns={"index": "plant_id"})
Z = P[P.dist_name.isin(ZONES["CHE"])].copy()
Z["sub"] = "other zone"
for nm, (a0, a1, b0, b1) in SUB.items(): Z.loc[Z.lat.between(a0, a1) & Z.lon.between(b0, b1), "sub"] = nm
bbox = [Z.lon.min() - .02, Z.lat.min() - .02, Z.lon.max() + .02, Z.lat.max() + .02]
rows = []

def windows(src, lon, lat, rad=500):
    tr = pyproj.Transformer.from_crs("EPSG:4326", src.crs, always_xy=True); x, y = tr.transform(lon, lat)
    w = from_bounds(x - rad, y - rad, x + rad, y + rad, src.transform).round_offsets().round_lengths()
    a = src.read(1, window=w, boundless=True, fill_value=0)
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    cx, cy = (a.shape[1] - 1) / 2, (a.shape[0] - 1) / 2; px = abs(src.transform.a)
    return a, (np.hypot((xx - cx) * px, (yy - cy) * px) <= rad)

if "summary" not in sys.argv:          # "summary" re-uses the saved per-plant table instead of reading the imagery again
    # ---------------- Sentinel-2 ----------------
    tok = token("sentinel-2-l2a")
    items = search("sentinel-2-l2a", bbox, "2023-11-01", "2023-12-31")
    items = sorted(items, key=lambda f: f["id"])                       # keep the latest processing per tile and date
    best = {}
    for it in items:
        k = (it["properties"].get("s2:mgrs_tile"), it["properties"]["datetime"][:10]); best[k] = it
    print("Sentinel-2 scenes:", len(best))
    for (tile, day), it in sorted(best.items(), key=lambda kv: kv[0][1]):
        b = it["bbox"]; inside = Z[Z.lon.between(b[0], b[2]) & Z.lat.between(b[1], b[3])]
        if inside.empty: continue
        try:
            scl = rasterio.open(it["assets"]["SCL"]["href"] + "?" + tok); b03 = rasterio.open(it["assets"]["B03"]["href"] + "?" + tok)
            b11 = rasterio.open(it["assets"]["B11"]["href"] + "?" + tok)
        except Exception as e:
            print("  open failed", it["id"], str(e)[:80]); continue
        for r in inside.itertuples():
            try:
                s, m = windows(scl, r.lon, r.lat); g, _ = windows(b03, r.lon, r.lat); sw, _ = windows(b11, r.lon, r.lat)
            except Exception as e:
                continue
            if g.shape != s.shape:                                            # B03 is 10 m; bring it to the 20 m SCL grid
                g = g[: 2 * s.shape[0], : 2 * s.shape[1]].reshape(s.shape[0], 2, s.shape[1], 2).mean(axis=(1, 3)) if g.shape[0] >= 2 * s.shape[0] else np.full(s.shape, np.nan)
            if s[m].size == 0 or (s[m] == 0).all(): continue                  # plant outside the valid part of the scene
            valid = m & (s > 1); obsc = np.isin(s, [3, 8, 9, 10]); clear = valid & ~obsc
            mndwi = (g.astype(float) - sw.astype(float)) / np.maximum(g.astype(float) + sw.astype(float), 1)
            water = clear & ((s == 6) | (mndwi > 0))
            rows.append(dict(sensor="Sentinel-2", scene=it["id"], date=day, plant_id=r.plant_id, nse_symbol=r.nse_symbol, sub_area=r.sub, lat=r.lat, lon=r.lon,
                             valid_frac=valid.sum() / max(1, m.sum()), clear_frac=clear.sum() / max(1, valid.sum()),
                             water_frac_of_clear=water.sum() / clear.sum() if clear.sum() else np.nan,
                             scl_water_frac_of_clear=(clear & (s == 6)).sum() / clear.sum() if clear.sum() else np.nan))
        print(" ", day, tile, "plants", len(inside), flush=True)

    # ---------------- Landsat ----------------
    tok = token("landsat-c2-l2")
    for it in sorted(search("landsat-c2-l2", bbox, "2023-11-01", "2023-12-31"), key=lambda f: f["properties"]["datetime"]):
        day = it["properties"]["datetime"][:10]; b = it["bbox"]; inside = Z[Z.lon.between(b[0], b[2]) & Z.lat.between(b[1], b[3])]
        if inside.empty or "qa_pixel" not in it["assets"]: continue
        try: qa = rasterio.open(it["assets"]["qa_pixel"]["href"] + "?" + tok)
        except Exception as e: print("  open failed", it["id"], str(e)[:80]); continue
        for r in inside.itertuples():
            try: q, m = windows(qa, r.lon, r.lat)
            except Exception: continue
            q = q.astype(np.uint16); valid = m & (q != 1) & (q != 0)
            obsc = ((q >> 1) & 1) | ((q >> 2) & 1) | ((q >> 3) & 1) | ((q >> 4) & 1); clear = valid & (obsc == 0)
            water = clear & (((q >> 7) & 1) == 1)
            if m.sum() == 0 or valid.sum() == 0: continue
            rows.append(dict(sensor=it["properties"].get("platform", "landsat"), scene=it["id"], date=day, plant_id=r.plant_id, nse_symbol=r.nse_symbol, sub_area=r.sub,
                             lat=r.lat, lon=r.lon, valid_frac=valid.sum() / m.sum(), clear_frac=clear.sum() / valid.sum(),
                             water_frac_of_clear=water.sum() / clear.sum() if clear.sum() else np.nan, scl_water_frac_of_clear=np.nan))
        print(" ", day, it["id"][:25], "plants", len(inside), flush=True)


if "summary" not in sys.argv:
    d = pd.DataFrame(rows); d["date"] = pd.to_datetime(d.date); d.round(4).to_csv(EXT + "optical_chennai_plant_scenes.csv", index=False)
else:
    d = pd.read_csv(EXT + "optical_chennai_plant_scenes.csv", parse_dates=["date"])
d["phase"] = np.where(d.date < EVENT0, "pre", np.where(d.date <= EVENT1, "event", "post"))
ok = d[(d.valid_frac >= 0.5) & (d.clear_frac >= 0.3)]
base = ok[ok.phase == "pre"].groupby(["plant_id", "sensor"])[["water_frac_of_clear", "scl_water_frac_of_clear"]].median()
base.columns = ["pre_water", "pre_scl_water"]
ok = ok.join(base, on=["plant_id", "sensor"]); ok["new_water"] = ok.water_frac_of_clear - ok.pre_water
ok["new_scl_water"] = ok.scl_water_frac_of_clear - ok.pre_scl_water          # stricter: Sentinel-2 scene-classification water only
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
sc = d.groupby(["date", "sensor"]).agg(plants=("plant_id", "nunique"), median_clear=("clear_frac", "median"),
                                       plants_30pct_clear=("clear_frac", lambda v: int((v >= 0.3).sum()))).reset_index()
sc.round(3).to_csv(TAB + "optical_chennai_scenes.csv", index=False)
print("\n=== scenes: how many Chennai-zone plants were visible ==="); print(sc.round(2).to_string(index=False))
ev = ok[ok.phase == "event"].copy()
s = ev.groupby(["date", "sensor", "sub_area"]).agg(plants_clear=("plant_id", "nunique"), median_water_now=("water_frac_of_clear", "median"),
                                                   median_water_pre=("pre_water", "median"), plants_with_new_water=("new_water", lambda v: int((v >= 0.10).sum())),
                                                   plants_new_water_strict=("new_scl_water", lambda v: int((v >= 0.10).sum())),
                                                   with_pre_baseline=("pre_water", lambda v: int(v.notna().sum()))).reset_index()
s.round(3).to_csv(TAB + "optical_chennai_event_subareas.csv", index=False)
print("\n=== event scenes (4-12 Dec 2023), plants with >=30% of the 500 m circle clear ==="); print(s.round(3).to_string(index=False))
named = ev[ev.nse_symbol.isin(["APOLLOTYRE", "JKTYRE", "CEATLTD", "MRF", "HINDUNILVR", "INDORAMA", "VASCONEQ", "APOLLOHOSP", "SRF"])]
named[["date", "sensor", "plant_id", "nse_symbol", "sub_area", "clear_frac", "water_frac_of_clear", "pre_water", "new_water", "new_scl_water"]].round(3).to_csv(TAB + "optical_chennai_named_plants.csv", index=False)
print("\n=== named sample plants on event scenes ==="); print(named[["date", "sensor", "nse_symbol", "sub_area", "clear_frac", "water_frac_of_clear", "pre_water", "new_water"]].round(3).to_string(index=False))

tyre = d[d.nse_symbol.isin(["APOLLOTYRE", "JKTYRE", "CEATLTD"]) & (d.phase == "event")]
vis = tyre.assign(visible=(tyre.valid_frac >= .5) & (tyre.clear_frac >= .3)).groupby(["plant_id", "nse_symbol"]).agg(
    event_scenes=("scene", "nunique"), visible_scenes=("visible", "sum"), water_on_visible=("water_frac_of_clear", lambda v: v.max()))
print("\n=== tyre plants on the event scenes (6-11 Dec) ==="); print(vis.round(3).to_string())
vis.round(3).to_csv(TAB + "optical_chennai_tyre_plants.csv")
