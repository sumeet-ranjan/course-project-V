"""Second hazard layer.
 1. River discharge (GloFAS v4 reanalysis via Open-Meteo flood API), 2000-2025, for the districts
    that matter most (event zones + any district holding >=10% of some traded firm's assets).
    A district centroid rarely sits on the main river channel, so we first scan a 5x5 grid
    (+-0.1 deg) for the cell with the highest 2019 mean flow, then pull that cell's history.
 2. Modelled PM2.5 (CAMS global via Open-Meteo air-quality API), Aug-2022 -> 2025, for NCR and
    comparison cities. (Model values understate Delhi peaks; use as a relative index only.)"""
import itertools, json, os, sys, time, urllib.request
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
def g(u, tries=3):
    for i in range(tries):
        try: return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=120).read())
        except Exception as e:
            err = e
            if "429" in str(e): raise
            time.sleep(4 * (i + 1))
    raise err
p = plants(); has = set(returns_wide().columns); p = p[p.nse_symbol.isin(has)]
p["w"] = p.project_cost_cr / p.groupby("nse_symbol").project_cost_cr.transform("sum")
big = p.groupby(["nse_symbol", "dist_name"]).w.sum().reset_index().query("w>=0.10").dist_name.unique()
zone = [d for z in ZONES.values() for d in z if d in set(p.dist_name)]
cen = pd.read_csv(EXT + "district_centroids.csv").set_index("dist_name")
todo = list(dict.fromkeys(zone + sorted(big))); print(len(todo), "districts")
os.makedirs(EXT + "river_raw", exist_ok=True); meta = []
for d in todo:
    fn = EXT + "river_raw/" + cen.key[d] + ".csv"
    if os.path.exists(fn): continue
    la, lo = cen.lat[d], cen.lon[d]
    try:
        pts = list(itertools.product(np.round(la + np.arange(-2, 3) * 0.05, 3), np.round(lo + np.arange(-2, 3) * 0.05, 3)))
        r = g("https://flood-api.open-meteo.com/v1/flood?latitude=" + ",".join(map(str, [a for a, _ in pts])) + "&longitude=" + ",".join(map(str, [b for _, b in pts])) +
              "&daily=river_discharge&start_date=2019-06-01&end_date=2019-10-31")
        best = max(r, key=lambda x: np.nanmean([v if v is not None else np.nan for v in x["daily"]["river_discharge"]]))
        h = g(f"https://flood-api.open-meteo.com/v1/flood?latitude={best['latitude']}&longitude={best['longitude']}&daily=river_discharge&start_date=2000-01-01&end_date=2025-12-31")
        s = pd.DataFrame({"date": h["daily"]["time"], "q": h["daily"]["river_discharge"]}); s["dist_name"] = d
        s["cell_lat"], s["cell_lon"] = best["latitude"], best["longitude"]; s.to_csv(fn, index=False); print(d, best["latitude"], best["longitude"], round(s.q.mean()))
        time.sleep(1)
    except Exception as e:
        print("STOP/FAIL", d, e)
        if "429" in str(e): break
fr = [pd.read_csv(EXT + "river_raw/" + f) for f in os.listdir(EXT + "river_raw")]
if fr: pd.concat(fr).to_csv(EXT + "river_daily.csv.gz", index=False); print("river districts:", len(fr))
CITIES = {"New Delhi": (28.61, 77.21), "Gurgaon": (28.46, 77.03), "Gautam Buddha Nagar": (28.54, 77.39), "Ghaziabad": (28.67, 77.45), "Faridabad": (28.41, 77.31),
          "Sonipat": (28.99, 77.02), "Mumbai": (19.08, 72.88), "Chennai": (13.08, 80.27), "Vadodara": (22.31, 73.18), "Kolkata": (22.57, 88.36), "Bengaluru": (12.97, 77.59)}
aq = []
for c, (la, lo) in CITIES.items():
    try:
        d = g(f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={la}&longitude={lo}&hourly=pm2_5,pm10&start_date=2022-08-05&end_date=2025-12-31")
        x = pd.DataFrame(d["hourly"]); x["time"] = pd.to_datetime(x.time) + pd.Timedelta(hours=5, minutes=30)
        x = x.set_index("time").resample("D").mean().reset_index().rename(columns={"time": "date"}); x["city"] = c; aq.append(x)
    except Exception as e: print("AQ FAIL", c, e)
if aq: pd.concat(aq).to_csv(EXT + "pm25_daily_cams.csv", index=False); print("aq cities", len(aq))
