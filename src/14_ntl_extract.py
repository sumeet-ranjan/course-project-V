"""Night-time lights at every plant: turn the raw VNP46A2 tiles (13_fetch_ntl.py) into a small table.

For each event window and each plant inside the downloaded tiles, take the 3 x 3 pixel block
(about 1.4 km x 1.4 km) around the plant coordinate, every night.
  * A pixel counts only if it has a retrieval and Mandatory_Quality_Flag == 0 (high quality,
    main algorithm). Cloudy pixels have no retrieval in the non-gap-filled layer, so cloud = missing.
    (Collection 2 flags, checked in the user guide: 0 high quality, 1 poor (outlier / possible cloud),
    2-5 poor (twilight, eclipse, aurora, glint), 255 no retrieval.)
  * `ntl` = mean radiance of the valid pixels (nW / cm2 / sr).
  * `ratio` = sum of tonight's valid pixels / sum of the SAME pixels' own baseline, where a pixel's
    baseline is its median over nights rel_day <= -2 or >= +15 (needs >= 3 valid baseline nights).
    Matching pixels avoids the composition effect when only part of the block is cloud-free. The
    two-sided baseline is needed for Gujarat Aug 2024, where the monsoon leaves ~3 clear nights before.
  * `ratio_pre` = same with a pre-event-only baseline (rel_day <= -2); sensitivity check.
  * `ratio_any` = as `ratio`, but also accepting flag 1 retrievals (an outage can itself be flagged
    as an "outlier"); sensitivity check.
  * `clear_10km` = share of land pixels with a high-quality retrieval in the ~10 km block around the
    plant. Plant-nights at a cloud edge (low share) read systematically low, so the analysis keeps
    only clear_10km >= 0.8.
Date: the file for UTC day D is the overpass at about 20:20 UTC = about 01:50 IST on D+1
(VNP46A1 UTC_Time over Chennai for file 2023-12-03 reads 20.32 h). `night_ist` = D + 1 day, and
rel_day = night_ist - event start date.
Outputs: external/ntl_plant_daily.csv.gz, external/ntl_area_daily.csv
"""
import os, re, glob, warnings, datetime as dt, numpy as np, pandas as pd, h5py
from scipy.ndimage import uniform_filter
warnings.filterwarnings("ignore", category=RuntimeWarning)
from common import *
RAW = EXT + "ntl_raw/"
G = "HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/"
WINDOWS = {  # event -> (zone, start, tiles)
    "E_CHE_FLOOD_2023": ("CHE", "2023-12-04", ["h25v07", "h26v07"]),
    "E_GJ_FLOOD_2024":  ("GJ",  "2024-08-25", ["h25v06"]),
    "E_GJ_FLOOD_2023":  ("GJ",  "2023-09-16", ["h25v06"]),
}
# urban / industrial boxes used to validate the instrument (lat0, lat1, lon0, lon1)
AREAS = {
    "E_CHE_FLOOD_2023": {"Chennai city": (12.90, 13.20, 80.15, 80.30), "Sriperumbudur-Oragadam belt": (12.80, 13.00, 79.88, 80.02),
                         "Manali-Ennore": (13.14, 13.27, 80.24, 80.34), "Bengaluru (control)": (12.85, 13.10, 77.45, 77.75),
                         "Coimbatore (control)": (10.95, 11.10, 76.90, 77.05)},
    "E_GJ_FLOOD_2024":  {"Vadodara city": (22.24, 22.38, 73.12, 73.26), "Bharuch-Ankleshwar": (21.58, 21.76, 72.95, 73.10),
                         "Dahej industrial": (21.66, 21.76, 72.52, 72.68), "Ahmedabad": (22.95, 23.10, 72.48, 72.68),
                         "Surat": (21.12, 21.26, 72.76, 72.92), "Indore (control)": (22.65, 22.78, 75.80, 75.94),
                         "Jaipur (control)": (26.80, 26.98, 75.70, 75.88)},
}
AREAS["E_GJ_FLOOD_2023"] = AREAS["E_GJ_FLOOD_2024"]

def tile_bounds(t):
    h, v = int(t[1:3]), int(t[4:6])
    return 90 - 10 * v, -180 + 10 * h     # top latitude, left longitude

def file_date(fn):
    m = re.search(r"\.A(\d{4})(\d{3})\.", fn)
    return dt.date(int(m[1]), 1, 1) + dt.timedelta(int(m[2]) - 1)

def load(fn):
    with h5py.File(fn, "r") as f:
        g = f[G]
        ntl = g["DNB_BRDF-Corrected_NTL"][()]; mq = g["Mandatory_Quality_Flag"][()]
        gf = g["Gap_Filled_DNB_BRDF-Corrected_NTL"][()]; lh = g["Latest_High_Quality_Retrieval"][()]
        cm = g["QF_Cloud_Mask"][()]
    return ntl, mq, gf, lh, cm

P = plants().reset_index().rename(columns={"index": "plant_id"})
OFF = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1)]
rows, AREA_OUT = [], []
for ev, (zone, start, tiles) in WINDOWS.items():
    start = pd.Timestamp(start)
    d0, d1 = (start - pd.Timedelta(days=31)).date(), (start + pd.Timedelta(days=30)).date()
    days = [d0 + dt.timedelta(i) for i in range((d1 - d0).days + 1)]
    recs, area_px = [], {}
    for t in tiles:
        top, left = tile_bounds(t)
        q = P[(P.lat < top) & (P.lat >= top - 10) & (P.lon >= left) & (P.lon < left + 10)].copy()
        q["r"] = np.clip(np.floor((top - q.lat) * 240).astype(int), 0, 2399)
        q["c"] = np.clip(np.floor((q.lon - left) * 240).astype(int), 0, 2399)
        n = len(q)
        V = np.full((n, len(days), 9), np.nan, np.float32); A = V.copy()
        GF = np.full((n, len(days)), np.nan, np.float32); LH = GF.copy(); CC = GF.copy(); CL = GF.copy()
        rr = np.clip(q.r.values[:, None] + np.array([o[0] for o in OFF])[None, :], 0, 2399)
        cc = np.clip(q.c.values[:, None] + np.array([o[1] for o in OFF])[None, :], 0, 2399)
        lat_ax = top - (np.arange(2400) + 0.5) / 240; lon_ax = left + (np.arange(2400) + 0.5) / 240
        for j, day in enumerate(days):
            fs = sorted(glob.glob(f"{RAW}VNP46A2.A{day.year}{day.timetuple().tm_yday:03d}.{t}.*.h5"))
            if not fs: continue
            ntl, mq, gf, lh, cm = load(fs[-1])
            x = ntl[rr, cc]; m = mq[rr, cc]
            A[:, j, :] = np.where(x > -900, x, np.nan)
            V[:, j, :] = np.where((x > -900) & (m == 0), x, np.nan)
            g = gf[q.r.values, q.c.values]; GF[:, j] = np.where(g > -900, g, np.nan)
            l = lh[q.r.values, q.c.values].astype(np.float32); LH[:, j] = np.where(l < 255, l, np.nan)
            c = cm[q.r.values, q.c.values]; CC[:, j] = np.where(c < 65535, (c >> 6) & 3, np.nan)
            # share of land pixels with a high-quality retrieval in the 21 x 21 block (~10 km) around the plant:
            # low values mean the plant sits at a cloud edge, where retrievals are biased low
            land = ((cm >> 1) & 7) != 3
            good = uniform_filter(((ntl > -900) & (mq == 0)).astype(np.float32), 21, mode="nearest")
            lnd = uniform_filter(land.astype(np.float32), 21, mode="nearest")
            CL[:, j] = np.clip(good[q.r.values, q.c.values] / np.maximum(lnd[q.r.values, q.c.values], 1e-3), 0, 1)
            for name, (la0, la1, lo0, lo1) in AREAS[ev].items():
                ri = np.where((lat_ax >= la0) & (lat_ax <= la1))[0]; ci = np.where((lon_ax >= lo0) & (lon_ax <= lo1))[0]
                if len(ri) == 0 or len(ci) == 0: continue
                a = ntl[ri.min():ri.max() + 1, ci.min():ci.max() + 1]; b = mq[ri.min():ri.max() + 1, ci.min():ci.max() + 1]
                area_px.setdefault((name, t), {})[j] = np.where((a > -900) & (b == 0), a, np.nan).ravel()
        recs.append((q, V, A, GF, LH, CC, CL))
    night = [pd.Timestamp(d) + pd.Timedelta(days=1) for d in days]
    rel = np.array([(x - start).days for x in night])
    pre = rel <= -2                      # before the event
    two = (rel <= -2) | (rel >= 15)      # before, or at least 15 days after (used as the main baseline)

    def ratio_to_base(X, bmask):
        """X: [plant, night, pixel]. Pixel-matched ratio to each pixel's own median over baseline nights."""
        nb = np.isfinite(X[:, bmask, :]).sum(1)
        base = np.where(nb >= 3, np.nanmedian(X[:, bmask, :], axis=1), np.nan)
        ok = np.isfinite(X) & np.isfinite(base)[:, None, :]
        num = np.where(ok, X, 0).sum(2); den = np.where(ok, base[:, None, :], 0).sum(2)
        return (np.where(den > 0, num / np.where(den > 0, den, 1), np.nan), np.nanmean(base, axis=1),
                np.nanmax(np.where(np.isfinite(base), nb, np.nan), axis=1))

    for q, V, A, GF, LH, CC, CL in recs:
        ratio, base, bn = ratio_to_base(V, two)
        ratio_pre, base_pre, bn_pre = ratio_to_base(V, pre)
        ratio_any, _, _ = ratio_to_base(A, two)
        nval, nval_any, lvl = np.isfinite(V).sum(2), np.isfinite(A).sum(2), np.nanmean(V, axis=2)
        pid, sym = q.plant_id.values, q.nse_symbol.values
        for i in range(len(q)):
            for j in range(len(days)):
                if nval_any[i, j] == 0: continue
                rows.append((ev, pid[i], sym[i], night[j].date(), rel[j], int(nval[i, j]), lvl[i, j], ratio[i, j], ratio_pre[i, j],
                             int(nval_any[i, j]), ratio_any[i, j], GF[i, j], LH[i, j], CL[i, j], base[i], bn[i], base_pre[i], bn_pre[i]))
    # area series: same pixel-matched ratio over all lit pixels of a box (a box may span two tiles)
    for name in AREAS[ev]:
        parts = [v for (nm, t), v in area_px.items() if nm == name]
        if not parts: continue
        cube = np.concatenate([np.stack([p.get(j, np.full(len(next(iter(p.values()))), np.nan)) for j in range(len(days))])
                               for p in parts], axis=1)
        out = {}
        for tag, bmask in (("", two), ("_pre", pre)):
            nb = np.isfinite(cube[bmask]).sum(0)
            base = np.where(nb >= 3, np.nanmedian(cube[bmask], axis=0), np.nan)
            lit = base >= 2.0                                                # lit pixels only
            for k in range(len(days)):
                ok = np.isfinite(cube[k]) & lit
                out.setdefault(k, []).extend([round(ok.sum() / max(1, lit.sum()), 3),
                                              cube[k][ok].sum() / base[ok].sum() if ok.sum() >= 20 else np.nan, int(lit.sum())])
        for k in range(len(days)):
            AREA_OUT.append((ev, name, night[k].date(), rel[k], *out[k]))
    print(ev, "done:", sum(len(r[0]) for r in recs), "plants in tiles", flush=True)

d = pd.DataFrame(rows, columns=["event_id", "plant_id", "nse_symbol", "night_ist", "rel_day", "n_valid", "ntl", "ratio", "ratio_pre",
                                "n_valid_any", "ratio_any", "gapfilled_centre", "days_since_hq", "clear_10km", "base", "base_nights",
                                "base_pre", "base_nights_pre"])
for c in ("ntl", "ratio", "ratio_pre", "ratio_any", "gapfilled_centre", "clear_10km", "base", "base_pre"): d[c] = d[c].astype(float).round(3)
d.to_csv(EXT + "ntl_plant_daily.csv.gz", index=False)
a = pd.DataFrame(AREA_OUT, columns=["event_id", "area", "night_ist", "rel_day", "coverage", "ratio", "n_lit_pixels",
                                    "coverage_pre", "ratio_pre", "n_lit_pixels_pre"])
a["ratio"] = a.ratio.round(3); a["ratio_pre"] = a.ratio_pre.round(3)
a.to_csv(EXT + "ntl_area_daily.csv", index=False)
print(len(d), "plant-night rows;", d.plant_id.nunique(), "plants;", len(a), "area-night rows")
