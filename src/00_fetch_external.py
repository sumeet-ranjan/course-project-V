"""Fetch external data the pack does not include:
  1. NIFTY 50 + sector indices (Yahoo Finance chart API)  -> external/indices_daily.csv
  2. Daily rainfall 2000-2025 at every plant district centroid (NASA POWER, PRECTOTCORR,
     ~0.5 deg grid) -> external/rain_daily.parquet-like csv.gz
Re-runnable; skips districts already downloaded."""
import json, os, sys, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
EXT = os.path.join(ROOT, "external"); os.makedirs(EXT + "/rain_raw", exist_ok=True)

def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            return urllib.request.urlopen(req, timeout=90).read()
        except Exception as e:
            time.sleep(3 * (i + 1)); err = e
    raise err

IDX = {"NIFTY50": "^NSEI", "NIFTY500": "^CRSLDX", "REALTY": "^CNXREALTY", "METAL": "^CNXMETAL",
       "ENERGY": "^CNXENERGY", "INFRA": "^CNXINFRA", "PHARMA": "^CNXPHARMA", "AUTO": "^CNXAUTO",
       "COMMODITIES": "^CNXCMDT"}
def indices():
    out = []
    for name, tk in IDX.items():
        try:
            u = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(tk)}?period1=1575158400&period2=1767225600&interval=1d"
            r = json.loads(get(u))["chart"]["result"][0]
            d = pd.DataFrame({"date": pd.to_datetime(r["timestamp"], unit="s").normalize(),
                              "close": r["indicators"]["quote"][0]["close"]}).dropna()
            d["date"] = (pd.to_datetime(r["timestamp"], unit="s") + pd.Timedelta(hours=5, minutes=30)).normalize()[: len(r["timestamp"])][d.index]
            d["index"] = name; out.append(d); print(name, len(d))
        except Exception as e:
            print("FAILED", name, e)
    pd.concat(out).to_csv(EXT + "/indices_daily.csv", index=False)

def rain_one(row):
    key, lat, lon = row
    fn = f"{EXT}/rain_raw/{key}.csv"
    if os.path.exists(fn): return
    u = ("https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR&community=AG"
         f"&longitude={lon:.3f}&latitude={lat:.3f}&start=20000101&end=20251231&format=JSON")
    try:
        d = json.loads(get(u))["properties"]["parameter"]["PRECTOTCORR"]
        pd.Series(d, name="mm").rename_axis("date").to_csv(fn)
    except Exception as e:
        print("FAILED", key, e)

def rain():
    p = pd.read_csv(ROOT + "/data/plants.csv")
    c = p.groupby("dist_name")[["lat", "lon"]].median().reset_index()
    c["key"] = c.dist_name.str.replace(r"[^A-Za-z0-9]+", "_", regex=True)
    c.to_csv(EXT + "/district_centroids.csv", index=False)
    with ThreadPoolExecutor(5) as ex:
        list(ex.map(rain_one, c[["key", "lat", "lon"]].itertuples(index=False, name=None)))
    fr = []
    for k, dn in zip(c.key, c.dist_name):
        fn = f"{EXT}/rain_raw/{k}.csv"
        if os.path.exists(fn):
            d = pd.read_csv(fn); d["dist_name"] = dn; fr.append(d)
    r = pd.concat(fr); r = r[r.mm > -900]
    r["date"] = pd.to_datetime(r.date.astype(str), format="%Y%m%d")
    r.to_csv(EXT + "/rain_daily.csv.gz", index=False)
    print("rain districts", r.dist_name.nunique(), "of", len(c))

if __name__ == "__main__":
    if "idx" in sys.argv or len(sys.argv) == 1: indices()
    if "rain" in sys.argv or len(sys.argv) == 1: rain()
