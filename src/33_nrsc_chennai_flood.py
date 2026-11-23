"""Chennai plants against the Indian space agency's radar flood map of 7 Dec 2023 (closes most of M2).

Source: NRSC/ISRO, "Flood / Rain affected areas during Michaung Cyclone in Parts of Tamilnadu State",
map no. 2023/CY/TN/01a/07122023, from RISAT-1A MRS radar of 7 Dec 2023 06:00 IST (pre-flood image
5 Nov 2023). Found through NDEM by a sub-agent; saved as research/proxy/docs/NDEM_TN_Michaung_7Dec2023_map.pdf.
The PDF is a GeoPDF: its main map viewport (BBox in page points [17.281, 765.590, 987.539, 126.687])
carries a /Measure /GEO dictionary with WGS84 corners 12.3011-13.5365 N, 78.9041-80.7798 E (a
latitude/longitude rectangle, so the mapping inside the frame is linear). The page is rendered at
6x (about 35 m per pixel); red pixels are the "Flood / Standing water due to rains" layer.
The map's own disclaimer: it "may include rain water accumulation / flood water in low lying areas /
paddy fields with standing water. No ground verification is done." Radar also misses water between
buildings, so dense urban sites can read dry when they were not.
For each Chennai-zone plant: share of the 250 m / 500 m / 1 km circle that is flood/standing water,
and the distance to the nearest flood pixel. Outputs: outputs/tables/nrsc_chennai_plants.csv,
outputs/figs/17_nrsc_chennai_plants.png
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from common import *
import pypdfium2 as pdfium
SRC = ROOT + "/research/proxy/docs/NDEM_TN_Michaung_7Dec2023_map.pdf"
SCALE = 6.0; PAGE_H = 842.2582
X0, Y0, X1, Y1 = 17.2810, 765.5899, 987.5389, 126.6866          # viewport BBox (left, top, right, bottom), PDF points
LAT_T, LAT_B, LON_L, LON_R = 13.5365, 12.3011, 78.9041, 80.7798
img = np.asarray(pdfium.PdfDocument(SRC)[0].render(scale=SCALE).to_pil().convert("RGB")).astype(int)
H, W, _ = img.shape
def to_px(lat, lon):
    X = X0 + (lon - LON_L) / (LON_R - LON_L) * (X1 - X0); Y = Y0 + (LAT_T - lat) / (LAT_T - LAT_B) * (Y1 - Y0)
    return X * SCALE, (PAGE_H - Y) * SCALE                                    # column, row in the rendered image
r_, g_, b_ = img[..., 0], img[..., 1], img[..., 2]
red = (r_ > 180) & (g_ < 90) & (b_ < 90)
c0, r0 = to_px(LAT_T, LON_L); c1, r1 = to_px(LAT_B, LON_R)
frame = np.zeros_like(red); frame[int(r0) + 3:int(r1) - 3, int(c0) + 3:int(c1) - 3] = True
# legend box inside the frame (bottom right): exclude it
lg = np.zeros_like(red); lg[int(r0 + 0.80 * (r1 - r0)):int(r1), int(c0 + 0.755 * (c1 - c0)):int(c0 + 0.88 * (c1 - c0))] = True
flood = red & frame & ~lg
px_m = (LON_R - LON_L) / (c1 - c0) * 111320 * np.cos(np.deg2rad(12.9))       # metres per pixel (east-west)
py_m = (LAT_T - LAT_B) / (r1 - r0) * 110574
P = plants().reset_index().rename(columns={"index": "plant_id"})
Z = P[P.dist_name.isin(ZONES["CHE"])].copy()
SUB = {"Chennai city": (12.90, 13.20, 80.15, 80.30), "Manali-Ennore": (13.14, 13.30, 80.24, 80.36),
       "Sriperumbudur-Oragadam": (12.78, 13.02, 79.78, 80.05), "Gummidipoondi": (13.35, 13.45, 80.05, 80.15)}
Z["sub_area"] = "other zone"
for nm, (a0, a1, b0, b1) in SUB.items(): Z.loc[Z.lat.between(a0, a1) & Z.lon.between(b0, b1), "sub_area"] = nm
rows = []
yy, xx = np.mgrid[-60:61, -60:61]; dist = np.hypot(xx * px_m, yy * py_m)
for r in Z.itertuples():
    c, rw = to_px(r.lat, r.lon); c, rw = int(round(c)), int(round(rw))
    win = flood[rw - 60:rw + 61, c - 60:c + 61]; fr = frame[rw - 60:rw + 61, c - 60:c + 61] & ~lg[rw - 60:rw + 61, c - 60:c + 61]
    if win.shape != dist.shape: continue
    o = dict(plant_id=r.plant_id, nse_symbol=r.nse_symbol, sub_area=r.sub_area, dist_name=r.dist_name, lat=r.lat, lon=r.lon, industry=r.industry_name)
    for rad in (250, 500, 1000):
        m = (dist <= rad) & fr; o[f"flood_frac_{rad}"] = win[m].mean() if m.any() else np.nan
    o["nearest_flood_m"] = dist[win].min() if win.any() else np.nan
    rows.append(o)
d = pd.DataFrame(rows); d.round(4).to_csv(TAB + "nrsc_chennai_plants.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(f"rendered {W}x{H}; map frame cols {c0:.0f}-{c1:.0f}, rows {r0:.0f}-{r1:.0f}; {px_m:.0f} m x {py_m:.0f} m per pixel; flood pixels {flood.sum():,} ({flood[frame].mean():.1%} of frame)")
s = d.groupby("sub_area").agg(plants=("plant_id", "size"), median_flood_500=("flood_frac_500", "median"), plants_flood500_ge5pct=("flood_frac_500", lambda v: int((v >= .05).sum())),
                              plants_any_within_500=("nearest_flood_m", lambda v: int((v <= 500).sum())), median_nearest_m=("nearest_flood_m", "median"))
print(s.round(3).to_string())
named = d[d.nse_symbol.isin(["APOLLOTYRE", "JKTYRE", "CEATLTD", "MRF", "HINDUNILVR", "INDORAMA", "VASCONEQ", "SRF", "PETRONET", "IOC"])]
print(named[["nse_symbol", "plant_id", "sub_area", "lat", "lon", "industry", "flood_frac_250", "flood_frac_500", "flood_frac_1000", "nearest_flood_m"]].round(3).to_string(index=False))
# overlay figure for a visual check of the georeferencing
from es_lib import plt, BLUE, ORANGE, MUTED
crop = img[int(r0):int(r1), int(c0):int(c1)]
fig, ax = plt.subplots(figsize=(11, 7.6))
ax.imshow(crop.astype(np.uint8), extent=[LON_L, LON_R, LAT_B, LAT_T])
ax.scatter(Z.lon, Z.lat, s=22, facecolors="none", edgecolors=BLUE, lw=1.2, label="Plant sites in the Chennai zone (pack coordinates)")
for nm, (a0, a1, b0, b1) in SUB.items():
    ax.add_patch(plt.Rectangle((b0, a0), b1 - b0, a1 - a0, fill=False, ec="#222222", lw=.8, ls="--")); ax.text(b0, a1 + .01, nm, fontsize=7.5)
ax.set_xlim(79.55, 80.45); ax.set_ylim(12.30, 13.50); ax.set_aspect(1 / np.cos(np.deg2rad(12.9)))
ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude"); ax.grid(False); ax.legend(fontsize=8, loc="lower left")
ax.set_title("Chennai-zone plants on the NRSC RISAT-1A flood map of 7 Dec 2023 (red = flood / standing water)", loc="left")
fig.tight_layout(); fig.savefig(FIG + "17_nrsc_chennai_plants.png", dpi=170)
