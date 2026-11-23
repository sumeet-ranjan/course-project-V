"""Satellite radar flood extent at the plant coordinates (Copernicus Global Flood Monitoring, GFM).

GFM is the Copernicus Emergency Management Service product that maps flood water on every
Sentinel-1 radar pass (20 m pixels, ensemble of three algorithms). Public, no login:
STAC catalogue https://stac.eodc.eu/api/v1 collection "GFM"; files on data.eodc.eu.
Layers used: ensemble_flood_extent (1 = flood water, i.e. water outside the reference water mask),
exclusion_mask (1 = radar cannot see floods here: dense urban, dense vegetation, shadow, ...),
reference_water_mask (permanent / seasonal water).

For every zone plant and every radar pass: is the plant inside the pass, how much flood water lies
within 250 m / 500 m / 1 km, the distance to the nearest flood pixel, and how much of the 500 m
circle is excluded (blind). A plant is "flood within 500 m" if at least 5 flood pixels (2,000 m2)
lie inside the circle on a pass in the event window.

Radar coverage (checked against the official Copernicus catalogue, see README 5.8):
  Gujarat Aug 2024: pass on 28 Aug 2024 01:02 UTC (06:32 IST), near the river peak.     -> usable
  Gujarat Sep 2023: passes on 15 Sep (before the release) and 27 Sep (9 days after).    -> peak missed
  Chennai Dec 2023: no Sentinel-1 pass between 30 Nov 2023 and 17 Jan 2024.             -> nothing
Outputs: external/flood_gfm_plant_pass.csv, outputs/tables/flood_plant_event.csv,
flood_firm_event.csv, flood_pass_summary.csv, outputs/figs/08_flood_gujarat_2024.png
"""
import os, sys, json, subprocess, urllib.request, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from es_lib import *
import rasterio, pyproj
RAW = EXT + "flood_maps_raw/gfm/"; os.makedirs(RAW, exist_ok=True)
ZBOX = {"GJ": (20.3, 23.2, 72.3, 74.6)}
CASES = {  # event -> (zone, search window, event window for "hit", bbox lon0 lat0 lon1 lat1)
    "E_GJ_FLOOD_2024": ("GJ", "2024-08-10", "2024-09-12", "2024-08-26", "2024-08-31", [72.3, 20.3, 74.6, 23.2]),
    "E_GJ_FLOOD_2023": ("GJ", "2023-09-08", "2023-09-30", "2023-09-16", "2023-09-21", [72.3, 20.3, 74.6, 23.2]),
}
LAYERS = ["ensemble_flood_extent", "exclusion_mask", "reference_water_mask"]

def stac(bbox, d0, d1):
    out, body = [], {"collections": ["GFM"], "bbox": bbox, "datetime": f"{d0}T00:00:00Z/{d1}T23:59:59Z", "limit": 200}
    url = "https://stac.eodc.eu/api/v1/search"
    while url:
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
        j = json.load(urllib.request.urlopen(req, timeout=180)); out += j["features"]
        nxt = [l for l in j.get("links", []) if l.get("rel") == "next"]
        url, body = (nxt[0]["href"], nxt[0].get("body", body)) if nxt else (None, None)
    return out

def get(href):
    fn = RAW + os.path.basename(href)
    if not (os.path.exists(fn) and os.path.getsize(fn) > 1000):
        r = subprocess.run(["curl", "-sS", "-L", "-m", "300", "--retry", "3", "-o", fn, "-w", "%{http_code}", href], capture_output=True, text=True)
        if r.stdout.strip() != "200":
            if os.path.exists(fn): os.remove(fn)
            return None
    return fn

P = plants().reset_index().rename(columns={"index": "plant_id"})
P["plant_share"] = P.project_cost_cr / P.groupby("nse_symbol").project_cost_cr.transform("sum").replace(0, np.nan)
yy, xx = np.mgrid[-50:51, -50:51]; DIST = np.hypot(yy, xx) * 20.0      # metres from the plant pixel
rows, passes = [], []
for ev, (zone, s0, s1, e0, e1, bbox) in CASES.items():
    la_a, la_b, lo_a, lo_b = ZBOX[zone]
    q = P[P.dist_name.isin(ZONES[zone]) & P.lat.between(la_a, la_b) & P.lon.between(lo_a, lo_b)].copy()
    items = sorted(stac(bbox, s0, s1), key=lambda f: f["properties"]["datetime"])
    print(ev, len(items), "GFM items;", len(q), "zone plants", flush=True)
    for it in items:
        pr = it["properties"]; when = pd.Timestamp(pr["datetime"]).tz_localize(None)
        files = {k: get(it["assets"][k]["href"]) for k in LAYERS if k in it["assets"]}
        if not files.get("ensemble_flood_extent"): print("  missing", it["id"]); continue
        with rasterio.open(files["ensemble_flood_extent"]) as src:
            tr = pyproj.Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
            X, Y = tr.transform(q.lon.values, q.lat.values)
            fl = src.read(1); T = src.transform; H, W = fl.shape
        ex = rasterio.open(files["exclusion_mask"]).read(1) if files.get("exclusion_mask") else None
        rw = rasterio.open(files["reference_water_mask"]).read(1) if files.get("reference_water_mask") else None
        cols = np.floor((X - T.c) / T.a).astype(int); rws = np.floor((Y - T.f) / T.e).astype(int)
        n_in = 0
        for (pid, sym, sh), c, r in zip(q[["plant_id", "nse_symbol", "plant_share"]].itertuples(index=False), cols, rws):
            if not (50 <= c < W - 50 and 50 <= r < H - 50): continue
            w = fl[r - 50:r + 51, c - 50:c + 51]
            if w[50, 50] == 255: continue                                   # outside this radar pass
            n_in += 1; valid = w != 255; f = (w == 1)
            d = dict(event_id=ev, plant_id=pid, nse_symbol=sym, pass_utc=when, tile=pr.get("Equi7Tile"), on_flood_pixel=int(w[50, 50] == 1))
            for rad in (250, 500, 1000):
                m = (DIST <= rad) & valid
                d[f"flood_px_{rad}"] = int(f[m].sum()); d[f"flood_frac_{rad}"] = f[m].mean() if m.sum() else np.nan
            d["nearest_flood_m"] = DIST[f].min() if f.any() else np.nan
            m5 = DIST <= 500
            d["excluded_frac_500"] = float((ex[r - 50:r + 51, c - 50:c + 51][m5] == 1).mean()) if ex is not None else np.nan
            d["refwater_frac_500"] = float((rw[r - 50:r + 51, c - 50:c + 51][m5] == 1).mean()) if rw is not None else np.nan
            rows.append(d)
        passes.append(dict(event_id=ev, pass_utc=when, tile=pr.get("Equi7Tile"), item=it["id"], zone_plants_inside=n_in,
                           flooded_pixels_in_tile=pr.get("flooded_pixels"), in_event_window=e0 <= str(when.date()) <= e1))
d = pd.DataFrame(rows)
d.round(4).to_csv(EXT + "flood_gfm_plant_pass.csv", index=False)
ps = pd.DataFrame(passes); ps.to_csv(TAB + "flood_pass_summary.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
print(ps.groupby(["event_id", ps.pass_utc.dt.date]).agg(tiles=("tile", "nunique"), plants_inside=("zone_plants_inside", "sum"), in_event_window=("in_event_window", "max")).to_string())

# ---- per plant: event-window passes vs passes before
out = []
for ev, (zone, s0, s1, e0, e1, bbox) in CASES.items():
    x = d[d.event_id == ev].copy(); x["day"] = x.pass_utc.dt.date.astype(str)
    x["phase"] = np.where(x.day < e0, "before", np.where(x.day <= e1, "event", "after"))
    la_a, la_b, lo_a, lo_b = ZBOX[zone]
    for pid, pr in P[P.dist_name.isin(ZONES[zone])].set_index("plant_id").iterrows():
        g = x[x.plant_id == pid]; r = dict(event_id=ev, plant_id=pid, nse_symbol=pr.nse_symbol, dist_name=pr.dist_name, lat=pr.lat, lon=pr.lon,
                                            industry=pr.industry_name, plant_share=pr.plant_share,
                                            coord_ok=bool(la_a <= pr.lat <= la_b and lo_a <= pr.lon <= lo_b))
        for ph in ("before", "event", "after"):
            h = g[g.phase == ph]
            r[f"passes_{ph}"] = h.pass_utc.dt.date.nunique()
            r[f"flood_px_500_{ph}"] = h.flood_px_500.max() if len(h) else np.nan
            r[f"flood_px_1000_{ph}"] = h.flood_px_1000.max() if len(h) else np.nan
            r[f"nearest_flood_m_{ph}"] = h.nearest_flood_m.min() if len(h) else np.nan
        e = g[g.phase == "event"]
        r["observed_event"] = len(e) > 0
        r["event_pass_dates"] = "|".join(sorted(set(e.day)))
        r["on_flood_pixel"] = bool(e.on_flood_pixel.max()) if len(e) else np.nan
        r["flood250"] = bool(e.flood_px_250.max() >= 5) if len(e) else np.nan
        r["flood500"] = bool(e.flood_px_500.max() >= 5) if len(e) else np.nan
        r["flood1000"] = bool(e.flood_px_1000.max() >= 5) if len(e) else np.nan
        r["new_flood500"] = bool(e.flood_px_500.max() >= 5 and not (r["flood_px_500_before"] >= 5)) if len(e) else np.nan
        r["excluded_frac_500"] = e.excluded_frac_500.mean() if len(e) else np.nan
        out.append(r)
fp = pd.DataFrame(out); fp.round(4).to_csv(TAB + "flood_plant_event.csv", index=False)
z = fp.assign(w=fp.plant_share.fillna(0))
ff = z.groupby(["event_id", "nse_symbol"]).apply(lambda t: pd.Series(dict(
    zone_plants=len(t), share_zone=t.w.sum(), plants_observed=int(t.observed_event.sum()), share_flood_observed=t.w[t.observed_event].sum(),
    plants_flood500=int((t.flood500 == True).sum()), share_flood500=t.w[t.flood500 == True].sum(),      # noqa: E712
    plants_flood250=int((t.flood250 == True).sum()), share_flood250=t.w[t.flood250 == True].sum(),      # noqa: E712
    share_flood1000=t.w[t.flood1000 == True].sum(), mean_excluded_500=t.excluded_frac_500.mean())), include_groups=False).reset_index()   # noqa: E712
ff["traded"] = ff.nse_symbol.isin(R.columns)
ff.round(4).to_csv(TAB + "flood_firm_event.csv", index=False)
print("\n=== zone plants against the radar flood layer ===")
print(fp.groupby("event_id").agg(zone_plants=("plant_id", "size"), observed_in_event_window=("observed_event", "sum"),
      on_flood_pixel=("on_flood_pixel", lambda s: (s == True).sum()), flood_within_250m=("flood250", lambda s: (s == True).sum()),   # noqa: E712
      flood_within_500m=("flood500", lambda s: (s == True).sum()), flood_within_1km=("flood1000", lambda s: (s == True).sum()),      # noqa: E712
      mean_blind_share_500m=("excluded_frac_500", "mean")).round(2).to_string())
print("\n=== firms with >= 10% of plant cost in the zone ===")
print(ff[ff.share_zone >= .10].sort_values(["event_id", "share_flood500"], ascending=[True, False]).round(3).to_string(index=False))

# ---- figure 08: the 28 Aug 2024 radar flood layer with the plants (Vadodara - Bharuch - Dahej)
import glob
from rasterio.windows import from_bounds
tr = None; LON0, LON1, LAT0, LAT1 = 72.40, 73.60, 21.50, 22.62
fig, ax = plt.subplots(figsize=(9.6, 9))
for kind, pat, col in (("blind", "ENSEMBLE_EXCLAYER_20240828T0102*", "#e3e2dc"), ("flood", "ENSEMBLE_FLOOD_20240828T0102*", "#1c5cab")):
    for fn in sorted(glob.glob(RAW + pat + ".tif")):
        with rasterio.open(fn) as src:
            if tr is None:
                tr = pyproj.Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
                cx, cy = tr.transform([LON0, LON1, LON0, LON1], [LAT0, LAT0, LAT1, LAT1]); BX = (min(cx), max(cx), min(cy), max(cy))
            b = src.bounds
            if b.right < BX[0] or b.left > BX[1] or b.top < BX[2] or b.bottom > BX[3]: continue
            w = from_bounds(max(BX[0], b.left), max(BX[2], b.bottom), min(BX[1], b.right), min(BX[3], b.top), src.transform).round_offsets().round_lengths()
            a = src.read(1, window=w); wt = src.window_transform(w)
        k = 5; H, W = (a.shape[0] // k) * k, (a.shape[1] // k) * k
        m = (a[:H, :W] == 1).reshape(H // k, k, W // k, k).mean(axis=(1, 3)) >= (0.5 if kind == "blind" else 0.2)   # 100 m cells
        yy_, xx_ = np.nonzero(m)
        ax.scatter((wt.c + (xx_ * k + k / 2) * wt.a) / 1000, (wt.f + (yy_ * k + k / 2) * wt.e) / 1000, s=0.25 if kind == "blind" else 1.2, color=col, marker="s", lw=0, zorder=1 if kind == "blind" else 2, rasterized=True)
g = fp[(fp.event_id == "E_GJ_FLOOD_2024") & fp.coord_ok & fp.observed_event]
X, Y = tr.transform(g.lon.values, g.lat.values); X, Y = np.array(X) / 1000, np.array(Y) / 1000
near = (g.flood1000 == True).values; n500 = (g.flood500 == True).values   # noqa: E712
ax.scatter(X[~near], Y[~near], s=16, facecolors="none", edgecolors="#52514e", lw=.7, zorder=3, label=f"Plant, no flood water within 1 km ({(~near).sum()})")
ax.scatter(X[near & ~n500], Y[near & ~n500], s=38, color=AQUA, edgecolors=SURF, lw=.8, zorder=4, label=f"Flood water within 1 km ({(near & ~n500).sum()})")
ax.scatter(X[n500], Y[n500], s=60, color=ORANGE, marker="s", edgecolors=SURF, lw=.8, zorder=5, label=f"Flood water within 500 m ({n500.sum()})")
ax.scatter([], [], s=30, color="#1c5cab", marker="s", label="Flood water seen by radar, 28 Aug 2024 06:32 IST")
ax.scatter([], [], s=30, color="#e3e2dc", marker="s", label="Radar blind here (built-up, dense vegetation)")
for nm, lo, la in (("Vadodara", 73.18, 22.31), ("Bharuch", 72.99, 21.71), ("Ankleshwar", 73.00, 21.63), ("Dahej", 72.58, 21.71), ("Anand", 72.95, 22.56), ("Halol", 73.47, 22.50)):
    px, py = tr.transform(lo, la); ax.annotate(nm, (px / 1000, py / 1000), xytext=(6, 6), textcoords="offset points", fontsize=8.5, fontweight="bold", color=INK, zorder=6)
ax.set_xlim(BX[0] / 1000, BX[1] / 1000); ax.set_ylim(BX[2] / 1000, BX[3] / 1000); ax.set_aspect("equal"); ax.grid(False)
ax.set_xlabel("km east (Equi7 Asia grid)"); ax.set_ylabel("km north"); ax.legend(fontsize=8, loc="lower left", framealpha=.9, frameon=True, edgecolor="#c9c8c2")
ax.set_title("Gujarat flood, Aug 2024: radar flood extent and plant sites\nCopernicus Global Flood Monitoring, Sentinel-1 pass of 28 Aug 2024", loc="left")
fig.tight_layout(); fig.savefig(FIG + "08_flood_gujarat_2024.png", dpi=170); plt.close(fig)
