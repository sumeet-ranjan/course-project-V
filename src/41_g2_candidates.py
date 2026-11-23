"""Evidence for decision G2 (exposed sets and matched controls) — collects data only, decides nothing.

1. Exposed sets on the corrected footprints (common.exposure), traded firms only; for Gujarat 2024 also the
   share of plant cost in Vadodara district alone (the documented flood footprint).
2. Candidate matched controls (listed peers outside the sample): daily prices from the Yahoo chart API
   (adjusted close, Jun 2021 - Dec 2025) and market cap / share count from the public screener.in page.
   Plant and project locations come from the sub-agent tables in research/realign/ (checked separately).
3. Size at the event: shares x close on the last trading day before the event (14 Nov 2024; 23 Aug 2024).
   Share counts are today's, so sizes are approximate.
Outputs: external/prices_peers.csv, external/market_cap_peers.csv,
         research/realign/g2_exposed_sets.csv, research/realign/g2_control_candidates.csv
"""
import os, sys, json, time, urllib.request, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd, numpy as np
from bs4 import BeautifulSoup
from common import *
RE = ROOT + "/research/realign/"
NCR_PEERS = {"BRIGADE": "Brigade Enterprises", "SOBHA": "Sobha", "PRESTIGE": "Prestige Estates", "OBEROIRLTY": "Oberoi Realty",
             "GODREJPROP": "Godrej Properties", "KOLTEPATIL": "Kolte-Patil", "SUNTECK": "Sunteck Realty", "PURVA": "Puravankara",
             "MAHLIFE": "Mahindra Lifespace", "ARVSMART": "Arvind SmartSpaces", "AJMERA": "Ajmera Realty", "RUSTOMJEE": "Keystone Realtors",
             "SHRIRAMPPS": "Shriram Properties", "PHOENIXLTD": "Phoenix Mills"}
GJ_PEERS = {"CHAMBLFERT": "Chambal Fertilisers", "COROMANDEL": "Coromandel International", "RCF": "Rashtriya Chemicals & Fertilizers",
            "NFL": "National Fertilizers", "PARADEEP": "Paradeep Phosphates", "DEEPAKFERT": "Deepak Fertilisers", "TATACHEM": "Tata Chemicals",
            "VINATIORGA": "Vinati Organics", "BALAMINES": "Balaji Amines", "FINEORG": "Fine Organic", "CLEAN": "Clean Science",
            "SUDARSCHEM": "Sudarshan Chemical", "CHEMPLASTS": "Chemplast Sanmar", "GALAXYSURF": "Galaxy Surfactants", "NOCIL": "NOCIL", "DCW": "DCW"}
P1, P2 = int(pd.Timestamp("2021-06-01").timestamp()), int(pd.Timestamp("2025-12-31").timestamp())
UA = {"User-Agent": "Mozilla/5.0"}
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read().decode()
def chart(tk):
    u = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(tk)}?period1={P1}&period2={P2}&interval=1d&events=div%2Csplit"
    r = json.loads(get(u))["chart"]["result"][0]
    ts = pd.to_datetime(r["timestamp"], unit="s") + pd.Timedelta(hours=5, minutes=30)
    q = r["indicators"]["quote"][0]; adj = r["indicators"].get("adjclose", [{}])[0].get("adjclose", q["close"])
    return pd.DataFrame({"date": ts.normalize(), "close": q["close"], "adjclose": adj, "volume": q["volume"]}).dropna(subset=["close"])
def screener(sym):
    for cons in (True, False):
        try:
            s = BeautifulSoup(get(f"https://www.screener.in/company/{sym}/" + ("consolidated/" if cons else "")), "lxml")
            r = {li.find("span", class_="name").get_text(strip=True): li.find("span", class_="number").get_text(strip=True) for li in s.select("#top-ratios li")}
            mc, px = (float(str(r.get(k, "")).replace(",", "") or "nan") for k in ("Market Cap", "Current Price"))
            if mc == mc: return mc, px, "consolidated" if cons else "standalone"
        except Exception as e: err = e
        time.sleep(1.5)
    return np.nan, np.nan, "failed"
if "fetch" in sys.argv[1:] or not os.path.exists(EXT + "prices_peers.csv"):
    out, mcs = [], []
    for sym, nm in {**NCR_PEERS, **GJ_PEERS}.items():
        try: d = chart(sym + ".NS"); d["asset_id"] = sym; out.append(d)
        except Exception as e: print("price failed", sym, str(e)[:80])
        mc, px, basis = screener(sym); mcs.append((sym, nm, mc, px, mc / px if px == px and px else np.nan, basis))
        print(sym, len(out[-1]) if out and out[-1].asset_id.iat[0] == sym else 0, mc); time.sleep(1.2)
    pd.concat(out).to_csv(EXT + "prices_peers.csv", index=False)
    pd.DataFrame(mcs, columns=["firm", "company", "market_cap_cr", "price", "shares_cr", "basis"]).to_csv(EXT + "market_cap_peers.csv", index=False)
# --- exposed sets (pack firms) -------------------------------------------------------------------------
c = companies(); e = exposure(); p = plants(); R = returns_wide(); S = stock()
traded = set(R.columns[R.notna().sum() > 300])
mc = pd.read_csv(EXT + "market_cap.csv").set_index("firm").shares_cr
def size_at(sym, day, px_table):
    x = px_table[(px_table.asset_id == sym) & (px_table.date <= day)]
    return x.close.iloc[-1] if len(x) else np.nan
rows = []
tot = p.groupby("nse_symbol").project_cost_cr.sum()
vad = p[p.dist_name == "Vadodara"].groupby("nse_symbol").project_cost_cr.sum() / tot
bha = p[p.dist_name == "Bharuch"].groupby("nse_symbol").project_cost_cr.sum() / tot
for zone, ev, day in (("NCR", "E_NCR_GRAP_2024 (18 Nov 2024)", "2024-11-14"), ("GJ", "E_GJ_FLOOD_2024 (26 Aug 2024)", "2024-08-23")):
    z = e[(e.zone == zone) & (e.share_cost >= 0.25)].merge(c[["nse_symbol", "company", "primary_industry", "role"]], on="nse_symbol")
    for r in z.itertuples():
        px = size_at(r.nse_symbol, pd.Timestamp(day), S.rename(columns={"close": "close"}))
        rows.append(dict(event=ev, nse_symbol=r.nse_symbol, company=r.company, industry=r.primary_industry, pack_role=r.role,
                         traded=r.nse_symbol in traded, share_zone=round(r.share_cost, 3),
                         share_vadodara=round(vad.get(r.nse_symbol, 0), 3) if zone == "GJ" else "", share_bharuch=round(bha.get(r.nse_symbol, 0), 3) if zone == "GJ" else "",
                         mcap_at_event_cr=round(mc.get(r.nse_symbol, np.nan) * px, 0) if px == px else np.nan))
X = pd.DataFrame(rows).sort_values(["event", "share_zone"], ascending=[True, False]); X.to_csv(RE + "g2_exposed_sets.csv", index=False)
# --- candidate controls ----------------------------------------------------------------------------------
pp = pd.read_csv(EXT + "prices_peers.csv", parse_dates=["date"]); m2 = pd.read_csv(EXT + "market_cap_peers.csv").set_index("firm")
cand = []
for grp, peers, day in (("NCR builders", NCR_PEERS, "2024-11-14"), ("Gujarat chemicals", GJ_PEERS, "2024-08-23")):
    for sym, nm in peers.items():
        px = size_at(sym, pd.Timestamp(day), pp); n = int((pp.asset_id == sym).sum())
        first = pp[pp.asset_id == sym].date.min()
        cand.append(dict(group=grp, nse_symbol=sym, company=nm, price_days=n, first_price=first.date() if pd.notna(first) else "",
                         mcap_at_event_cr=round(m2.shares_cr.get(sym, np.nan) * px, 0) if px == px else np.nan, source="outside sample"))
# in-sample firms with no plant in the zone, same broad industry
ncr0 = set(e[(e.zone == "NCR") & (e.share_cost > 0)].nse_symbol); gj0 = set(e[(e.zone == "GJ") & (e.share_cost > 0)].nse_symbol)
for r in c.itertuples():
    if r.nse_symbol not in traded: continue
    sec = sector(r.primary_industry)
    for grp, sec_ok, zone0, day in (("NCR builders", "Realty/Construction", ncr0, "2024-11-14"), ("Gujarat chemicals", "Chemicals", gj0, "2024-08-23")):
        if sec == sec_ok and r.nse_symbol not in zone0:
            px = size_at(r.nse_symbol, pd.Timestamp(day), S)
            cand.append(dict(group=grp, nse_symbol=r.nse_symbol, company=r.company, price_days=int(R[r.nse_symbol].notna().sum()), first_price="",
                             mcap_at_event_cr=round(mc.get(r.nse_symbol, np.nan) * px, 0) if px == px else np.nan, source=f"in sample ({r.primary_industry}; role {r.role})"))
Y = pd.DataFrame(cand); Y.to_csv(RE + "g2_control_candidates.csv", index=False)
pd.set_option("display.width", 220); pd.set_option("display.max_columns", 20)
print(X.to_string(index=False)); print(Y.to_string(index=False))
