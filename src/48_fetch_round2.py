"""Round 2 data (23 Nov 2026): daily prices (Yahoo chart API, adjusted close, Jun 2021 - Dec 2025) for the firms
added by decisions G4 and the scope change, merged into external/prices_peers.csv; FY2023-24 revenue (screener.in
public pages) for the cement/steel suppliers outside the sample (materiality bound, R1) into external/fin_annual_peers.csv.
Firms: contractors (G4 R2), cement makers (market-level test, R3), hit-firm register candidates (NCR and Gujarat).
"""
import os, sys, io, json, time, urllib.request, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd, numpy as np
from bs4 import BeautifulSoup
from common import EXT
P1, P2 = int(pd.Timestamp("2021-06-01").timestamp()), int(pd.Timestamp("2025-12-31").timestamp())
UA = {"User-Agent": "Mozilla/5.0"}
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read().decode()
def chart(tk):
    u = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(tk)}?period1={P1}&period2={P2}&interval=1d&events=div%2Csplit"
    r = json.loads(get(u))["chart"]["result"][0]
    ts = pd.to_datetime(r["timestamp"], unit="s") + pd.Timedelta(hours=5, minutes=30)
    q = r["indicators"]["quote"][0]; adj = r["indicators"].get("adjclose", [{}])[0].get("adjclose", q["close"])
    return pd.DataFrame({"date": ts.normalize(), "close": q["close"], "adjclose": adj, "volume": q["volume"]}).dropna(subset=["close"])
CONTRACTORS = ["AHLUCONT", "BLKASHYAP", "JKIL", "NCC", "PSPPROJECT", "CEMPRO", "LT", "CAPACITE"]
CEMENT = ["JKCEMENT", "JKLAKSHMI", "DALBHARAT", "BIRLACORPN", "MANGLMCEM", "NUVOCO", "HEIDELBERG", "PRSMJOHNSN", "RAMCOCEM", "INDIACEM",
          "ORIENTCEM", "SAGCEM", "KCP", "NCLIND", "DECCANCE", "STARCEMENT", "AMBUJACEM", "APLAPOLLO"]
REGISTER = ["ASHIANA", "SIGNATURE", "MAXESTATES", "TATACONSUM", "ACI", "GVT&D", "ADANIPORTS", "GHCL"]
pp = pd.read_csv(EXT + "prices_peers.csv", parse_dates=["date"])
new, fails = [], []
for s in CONTRACTORS + CEMENT + REGISTER:
    if s in set(pp.asset_id): continue
    try: d = chart(s + ".NS"); d["asset_id"] = s; new.append(d); print(s, len(d))
    except Exception as e: fails.append((s, str(e)[:80]))
    time.sleep(0.6)
if new: pp = pd.concat([pp] + new, ignore_index=True); pp.to_csv(EXT + "prices_peers.csv", index=False)
print("price failures:", fails)
# FY2023-24 revenue for suppliers outside the sample (screener.in profit-loss table)
rev = []
for s in ["AMBUJACEM", "JKCEMENT", "JKLAKSHMI", "DALBHARAT", "APLAPOLLO"]:
    for cons in (True, False):
        try:
            so = BeautifulSoup(get(f"https://www.screener.in/company/{s}/" + ("consolidated/" if cons else "")), "lxml")
            t = pd.read_html(io.StringIO(str(so.find("section", id="profit-loss").find("table"))))[0]
            t = t.rename(columns={t.columns[0]: "item"}); t["item"] = t["item"].str.replace("+", "", regex=False).str.strip()
            r = t[t["item"] == "Sales"]
            if len(r) and "Mar 2024" in t.columns:
                rev.append(dict(firm=s, basis="consolidated" if cons else "standalone", sales_fy24_cr=float(str(r["Mar 2024"].iloc[0]).replace(",", "")))); break
        except Exception as e: print(s, cons, str(e)[:60])
        time.sleep(1.5)
pd.DataFrame(rev).to_csv(EXT + "fin_annual_peers.csv", index=False); print(pd.DataFrame(rev).to_string(index=False))
