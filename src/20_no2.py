"""Nitrogen dioxide over the industrial clusters (Sentinel-5P TROPOMI), around each event.

NO2 comes from combustion (boilers, furnaces, traffic, power plants), so a fall over an industrial
cluster that then recovers is a sign of activity stopping and restarting. Limits: pixels are about
5.5 x 3.5 km, cloudy pixels are unusable (the same cloud that hides the night lights), and wind
moves the plume from day to day, so single days are noisy.

Source: Microsoft Planetary Computer copy of the Copernicus Sentinel-5P Level-2 NO2 product
(collection sentinel-5p-l2-netcdf, public, no login). The near-real-time 5-minute granules are
used because the full-orbit files are ~580 MB each. (NASA GES DISC also hosts it, but that archive
needs the "NASA GESDISC DATA ARCHIVE" application approved on the user's Earthdata account.)
Per box and day: mean tropospheric NO2 column of pixels with qa_value >= 0.75 (the product's
recommended filter, which also removes cloudy scenes), and the number of such pixels.
Outputs: external/no2_box_daily.csv, outputs/tables/no2_box_event.csv, figs/11_no2.png
"""
import os, sys, json, subprocess, urllib.request, numpy as np, pandas as pd, h5py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
RAW = EXT + "no2_raw/"; os.makedirs(RAW, exist_ok=True)
CASES = {  # event -> (start, boxes {name: (lat0, lat1, lon0, lon1, role)})
    "E_CHE_FLOOD_2023": ("2023-12-04", {"Chennai city + Manali-Ennore": (12.90, 13.30, 80.10, 80.36, "hit"),
                                         "Sriperumbudur-Oragadam": (12.78, 13.02, 79.78, 80.05, "hit"),
                                         "Bengaluru": (12.85, 13.10, 77.45, 77.75, "control")}),
    "E_GJ_FLOOD_2024": ("2024-08-25", {"Vadodara": (22.20, 22.45, 73.05, 73.30, "hit"), "Bharuch-Ankleshwar-Jhagadia": (21.55, 21.80, 72.90, 73.20, "hit"),
                                        "Dahej-Vilayat": (21.60, 21.92, 72.45, 72.75, "hit"), "Indore": (22.60, 22.82, 75.75, 75.98, "control")}),
    "E_GJ_FLOOD_2023": ("2023-09-16", {"Vadodara": (22.20, 22.45, 73.05, 73.30, "hit"), "Bharuch-Ankleshwar-Jhagadia": (21.55, 21.80, 72.90, 73.20, "hit"),
                                        "Dahej-Vilayat": (21.60, 21.92, 72.45, 72.75, "hit"), "Indore": (22.60, 22.82, 75.75, 75.98, "control")}),
}
PRE, POST = 14, 12

def stac(bbox, d0, d1):
    body = {"collections": ["sentinel-5p-l2-netcdf"], "bbox": bbox, "datetime": f"{d0}T00:00:00Z/{d1}T23:59:59Z", "limit": 500,
            "query": {"s5p:product_name": {"eq": "no2"}, "s5p:processing_mode": {"eq": "NRTI"}}}
    req = urllib.request.Request("https://planetarycomputer.microsoft.com/api/stac/v1/search", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=180))["features"]

def token():
    return json.load(urllib.request.urlopen("https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-5p-l2-netcdf", timeout=60))["token"]

def fetch():
    rows, tok = [], token()
    for ev, (start, boxes) in CASES.items():
        s = pd.Timestamp(start); d0, d1 = (s - pd.Timedelta(days=PRE)).date(), (s + pd.Timedelta(days=POST)).date()
        la = [b[0] for b in boxes.values()] + [b[1] for b in boxes.values()]; lo = [b[2] for b in boxes.values()] + [b[3] for b in boxes.values()]
        items = sorted(stac([min(lo), min(la), max(lo), max(la)], d0, d1), key=lambda f: f["properties"]["datetime"])
        print(ev, len(items), "granules", flush=True)
        for it in items:
            href = it["assets"]["no2"]["href"]; fn = RAW + os.path.basename(href)
            r = subprocess.run(["curl", "-sS", "-L", "-m", "900", "--retry", "2", "-o", fn, "-w", "%{http_code}", href + "?" + tok], capture_output=True, text=True)
            if r.stdout.strip() != "200":
                tok = token(); print("  fail", r.stdout.strip(), os.path.basename(href)); continue
            try:
                with h5py.File(fn, "r") as f:
                    p = f["PRODUCT"]; lat = p["latitude"][0]; lon = p["longitude"][0]
                    v = p["nitrogendioxide_tropospheric_column"][0].astype(float); q = p["qa_value"]
                    qa = q[0].astype(float) * float(np.ravel(q.attrs.get("scale_factor", 1))[0])
                    fill = float(np.ravel(p["nitrogendioxide_tropospheric_column"].attrs.get("_FillValue", 9.97e36))[0])
                v[(v == fill) | (v > 1e30)] = np.nan
                for name, (a0, a1, b0, b1, role) in boxes.items():
                    m = (lat >= a0) & (lat <= a1) & (lon >= b0) & (lon <= b1)
                    if m.sum() == 0: continue
                    g = m & (qa >= 0.75) & np.isfinite(v)
                    rows.append(dict(event_id=ev, box=name, role=role, time_utc=it["properties"]["datetime"][:19], pixels_in_box=int(m.sum()),
                                     good_pixels=int(g.sum()), no2_umol_m2=float(np.nanmean(v[g]) * 1e6) if g.sum() else np.nan,
                                     mean_qa=float(qa[m].mean()), granule=os.path.basename(href)))
            except Exception as e:
                print("  read error", os.path.basename(href), str(e)[:80])
            os.remove(fn)
        pd.DataFrame(rows).to_csv(EXT + "no2_box_daily.csv", index=False)
    return pd.DataFrame(rows)

if __name__ == "__main__":
    d = fetch() if "--fetch" in sys.argv or not os.path.exists(EXT + "no2_box_daily.csv") else pd.read_csv(EXT + "no2_box_daily.csv")
    from es_lib import plt, BLUE, ORANGE, AQUA, MUTED, SURF, TAB, FIG
    d["date"] = pd.to_datetime(d.time_utc).dt.normalize()
    # one value per box and day: the granule with most good pixels; usable only if >= half the box is good
    d = d.sort_values("good_pixels").groupby(["event_id", "box", "date"]).tail(1)
    d["usable"] = (d.good_pixels >= 0.5 * d.pixels_in_box) & (d.good_pixels >= 4)
    out = []
    for ev, (start, boxes) in CASES.items():
        s = pd.Timestamp(start); x = d[d.event_id == ev].copy(); x["rel_day"] = (x.date - s).dt.days
        for name in boxes:
            g = x[(x.box == name) & x.usable]
            base = g[g.rel_day <= -2].no2_umol_m2.median()
            for r in x[x.box == name].itertuples():
                out.append(dict(event_id=ev, box=name, role=r.role, date=r.date.date(), rel_day=r.rel_day, usable=r.usable, good_pixels=r.good_pixels,
                                pixels_in_box=r.pixels_in_box, no2_umol_m2=r.no2_umol_m2, baseline_umol_m2=base,
                                ratio=r.no2_umol_m2 / base if r.usable and base == base else np.nan,
                                baseline_days=int((g.rel_day <= -2).sum())))
    o = pd.DataFrame(out).sort_values(["event_id", "box", "rel_day"]); o.round(3).to_csv(TAB + "no2_box_event.csv", index=False)
    pd.set_option("display.width", 250)
    for ev in CASES:
        t = o[(o.event_id == ev)]
        print("\n", ev, "| usable days per box:", t[t.usable].groupby("box").size().to_dict(), "| baseline (umol/m2):", t.groupby("box").baseline_umol_m2.first().round(1).to_dict())
        print(t[t.usable & t.rel_day.between(-6, 12)].pivot(index="rel_day", columns="box", values="ratio").round(2).to_string())
    fig, axs = plt.subplots(1, 3, figsize=(15, 4.8), sharey=True)
    for ax, (ev, (start, boxes)) in zip(axs, CASES.items()):
        ax.axhline(1, color="#c9c8c2", lw=.9); ax.axvline(0, color=MUTED, lw=.8, ls=":")
        for (name, b), col in zip(boxes.items(), [ORANGE, BLUE, AQUA, "#8b8a84"]):
            g = o[(o.event_id == ev) & (o.box == name) & o.usable]
            ax.plot(g.rel_day, g.ratio, color=col if b[4] == "hit" else "#8b8a84", lw=0, marker="o" if b[4] == "hit" else "x", ms=6, mec=SURF if b[4] == "hit" else "#8b8a84",
                    label=f"{name}" + (" (control)" if b[4] != "hit" else ""))
        ax.set_title({"E_CHE_FLOOD_2023": "Chennai, Cyclone Michaung (4 Dec 2023)", "E_GJ_FLOOD_2024": "Gujarat flood (25 Aug 2024)",
                      "E_GJ_FLOOD_2023": "Gujarat, Narmada flood (16 Sep 2023)"}[ev], loc="left"); ax.set_xlabel("Days from event start"); ax.set_ylim(0, 3); ax.legend(fontsize=7.5, loc="upper left")
    axs[0].set_ylabel("Tropospheric NO2 ÷ box's own pre-event median")
    fig.suptitle("Nitrogen dioxide over industrial clusters (Sentinel-5P; only days with at least half the box cloud-free)", x=0.01, ha="left", fontweight="bold")
    fig.tight_layout(); fig.savefig(FIG + "11_no2.png", dpi=200)
