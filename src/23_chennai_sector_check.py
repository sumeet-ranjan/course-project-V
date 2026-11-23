"""Confound check for the Chennai price drop: was the week of 4 Dec 2023 a sector rotation?

4 Dec 2023 was also the first trading day after four state-election results, and the market rose
3.6% in the next five days, led by energy and power. The Chennai-exposed firms are tyre makers,
a hospital chain, a consumer-goods firm and builders: sectors that lagged that rally. The placebo
dates in 03_event_study.py control for sector tilts on average, not for a one-off sector shock on
the event date itself. This script compares each exposed firm with its own sector index over the
same days (market-model abnormal return of the index, same engine).
Adds NIFTY FMCG (Yahoo Finance) to the sector indices already in external/indices_daily.csv.
Output: outputs/tables/chennai_sector_check.csv
"""
import os, sys, json, urllib.request, urllib.parse; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from es_lib import *
fn = EXT + "indices_extra.csv"
if not os.path.exists(fn):
    u = "https://query1.finance.yahoo.com/v8/finance/chart/" + urllib.parse.quote("^CNXFMCG") + "?period1=1640995200&period2=1719792000&interval=1d"
    r = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read())["chart"]["result"][0]
    d = pd.DataFrame({"date": (pd.to_datetime(r["timestamp"], unit="s") + pd.Timedelta(hours=5, minutes=30)).normalize(),
                      "close": r["indicators"]["quote"][0]["close"]}).dropna(); d["index"] = "FMCG"; d.to_csv(fn, index=False)
ix = indices()
fm = pd.read_csv(fn, parse_dates=["date"]).set_index("date").close.pct_change(fill_method=None)
ix["FMCG"] = fm.reindex(ix.index)
t0 = t0_of("2023-12-04")
def idx_car(name, lo, hi):
    y = ix[name].reindex(DATES); a, b = t0 + EST[0], t0 + EST[1]
    yy, m = y.iloc[a:b], MKT.iloc[a:b]; ok = yy.notna() & m.notna()
    beta = np.cov(yy[ok], m[ok])[0, 1] / m[ok].var(); alpha = yy[ok].mean() - beta * m[ok].mean()
    return (y.iloc[t0 + lo:t0 + hi + 1] - (alpha + beta * MKT.iloc[t0 + lo:t0 + hi + 1])).sum()
SECT = {"APOLLOTYRE": "AUTO", "JKTYRE": "AUTO", "CEATLTD": "AUTO", "APOLLOHOSP": "PHARMA", "HINDUNILVR": "FMCG", "VASCONEQ": "REALTY", "INDORAMA": None}
c = pd.read_csv(TAB + "event_study_firm_cars.csv"); c = c[c.event_id == "E_CHE_FLOOD_2023"].set_index("nse_symbol")
nt = pd.read_csv(TAB + "ntl_firm_event.csv"); nt = nt[nt.event_id == "E_CHE_FLOOD_2023"].set_index("nse_symbol")
none5, none10 = c.car_0_5[c.share_cost == 0].mean(), c.car_0_10[c.share_cost == 0].mean()
rows = []
for f, s in SECT.items():
    i5, i10 = (idx_car(s, 0, 5), idx_car(s, 0, 10)) if s else (np.nan, np.nan)
    rows.append(dict(nse_symbol=f, share_zone=c.share_cost[f], share_dark=nt.share_dark.get(f, np.nan), sector_index=s or "none available",
                     car_0_5=c.car_0_5[f], sector_index_car_0_5=i5, car_0_5_minus_sector=c.car_0_5[f] - i5,
                     car_0_10=c.car_0_10[f], sector_index_car_0_10=i10, car_0_10_minus_sector=c.car_0_10[f] - i10))
o = pd.DataFrame(rows); o.round(4).to_csv(TAB + "chennai_sector_check.csv", index=False)
pd.set_option("display.width", 250)
print("market, raw return days 0-5:", round(MKT.iloc[t0:t0 + 6].sum(), 3), "| unexposed firms' mean CAR(0,5):", round(none5, 3))
print({k: round(idx_car(k, 0, 5), 3) for k in ["AUTO", "PHARMA", "REALTY", "FMCG", "ENERGY", "INFRA", "METAL"]})
print(o.round(3).to_string(index=False))
m = o.dropna(subset=["car_0_5_minus_sector"])
print(f"\nsix firms with a sector index: mean CAR(0,5) {m.car_0_5.mean():.3f}; mean after subtracting the sector index {m.car_0_5_minus_sector.mean():.3f}; "
      f"10 days: {m.car_0_10.mean():.3f} -> {m.car_0_10_minus_sector.mean():.3f}")
