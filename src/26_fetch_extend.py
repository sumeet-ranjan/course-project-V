"""Extend the inputs to November 2026 for an out-of-sample test (Step 6, existing 61 firms).

1. Daily prices for the 61 traded firms from the Yahoo Finance chart API (SYMBOL.NS), Jan 2024 to
   today, adjusted close. The overlap with the pack (Jan 2024 to Dec 2025, after the one-day date
   fix in common.stock()) is used to check that the two sources agree; returns from 1 Jan 2026 on
   are appended to the pack's returns.          -> external/prices_yahoo_2024_2026.csv
2. The same indices as 00_fetch_external.py, Jan 2024 to today.  -> external/indices_daily_2026.csv
3. Daily rainfall (NASA POWER, PRECTOTCORR) at the 478 plant-district centroids for 2026.
   NOTE: POWER serves MERRA-2 up to 30 Sep 2026 and the near-real-time GEOS-IT model from 1 Oct 2026
   (API header "sources"); analyses use rainfall only to 30 Sep 2026 so the source stays MERRA-2.
                                                 -> external/rain_daily_2026.csv.gz
Re-runnable; per-district rainfall files are cached in external/rain_raw_2026/ (not zipped).
"""
import os, sys, json, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
import pandas as pd, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
RR = EXT + "rain_raw_2026/"; os.makedirs(RR, exist_ok=True)
P1 = int(pd.Timestamp("2024-01-01").timestamp()); P2 = int(pd.Timestamp.now().normalize().timestamp())
END = (pd.Timestamp.now().normalize() - pd.Timedelta(days=1)).strftime("%Y%m%d")

def get(url, tries=4):
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=120).read()
        except Exception as e:
            err = e; time.sleep(3 * (i + 1))
    raise err

def chart(tk):
    u = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(tk)}?period1={P1}&period2={P2}&interval=1d&events=div%2Csplit"
    r = json.loads(get(u))["chart"]["result"][0]
    ts = pd.to_datetime(r["timestamp"], unit="s") + pd.Timedelta(hours=5, minutes=30)
    q = r["indicators"]["quote"][0]; adj = r["indicators"].get("adjclose", [{}])[0].get("adjclose", q["close"])
    return pd.DataFrame({"date": ts.normalize(), "close": q["close"], "adjclose": adj, "volume": q["volume"]}).dropna(subset=["close"])

def prices():
    syms = sorted(stock().asset_id.unique()); out, log = [], []
    for s in syms:
        got = None
        for tk in (f"{s}.NS", f"{s}.BO"):
            try:
                d = chart(tk); d["asset_id"] = s; d["ticker"] = tk; got = d; break
            except Exception as e:
                log.append((s, tk, str(e)[:80]))
        if got is not None: out.append(got)
        time.sleep(0.4)
    p = pd.concat(out); p.to_csv(EXT + "prices_yahoo_2024_2026.csv", index=False)
    print("prices:", p.asset_id.nunique(), "of", len(syms), "firms;", p.date.min().date(), "to", p.date.max().date())
    for l in log: print("   failed", l)

IDX = {"NIFTY50": "^NSEI", "NIFTY500": "^CRSLDX", "REALTY": "^CNXREALTY", "METAL": "^CNXMETAL", "ENERGY": "^CNXENERGY",
       "INFRA": "^CNXINFRA", "PHARMA": "^CNXPHARMA", "AUTO": "^CNXAUTO", "FMCG": "^CNXFMCG"}
def indices():
    out = []
    for name, tk in IDX.items():
        try:
            d = chart(tk)[["date", "close"]]; d["index"] = name; out.append(d)
        except Exception as e:
            print("index failed", name, e)
    pd.concat(out).to_csv(EXT + "indices_daily_2026.csv", index=False); print("indices:", [d["index"].iloc[0] for d in out])

def rain_one(row):
    key, lat, lon = row; fn = f"{RR}{key}.csv"
    if os.path.exists(fn): return
    u = ("https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR&community=AG"
         f"&longitude={lon:.3f}&latitude={lat:.3f}&start=20260101&end={END}&format=JSON")
    try:
        d = json.loads(get(u))["properties"]["parameter"]["PRECTOTCORR"]
        pd.Series(d, name="mm").rename_axis("date").to_csv(fn)
    except Exception as e:
        print("rain failed", key, str(e)[:80])

def rain():
    c = pd.read_csv(EXT + "district_centroids.csv")
    with ThreadPoolExecutor(5) as ex:
        list(ex.map(rain_one, c[["key", "lat", "lon"]].itertuples(index=False, name=None)))
    fr = []
    for k, dn in zip(c.key, c.dist_name):
        fn = f"{RR}{k}.csv"
        if os.path.exists(fn):
            d = pd.read_csv(fn); d["dist_name"] = dn; fr.append(d)
    r = pd.concat(fr); r = r[r.mm > -900]
    r["date"] = pd.to_datetime(r.date.astype(str), format="%Y%m%d")
    r.to_csv(EXT + "rain_daily_2026.csv.gz", index=False)
    print("rain 2026:", r.dist_name.nunique(), "districts;", r.date.min().date(), "to", r.date.max().date())

if __name__ == "__main__":
    a = sys.argv[1:] or ["prices", "idx", "rain"]
    if "prices" in a: prices()
    if "idx" in a: indices()
    if "rain" in a: rain()
