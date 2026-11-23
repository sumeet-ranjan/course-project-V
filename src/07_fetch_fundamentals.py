"""Fetch public quarterly + annual financials, balance sheet, cash flow and market cap for every
firm with price data, from the public screener.in company pages (consolidated; standalone
fallback). Output (long format, Rs crore):
  external/fin_quarterly.csv   firm, period_end, item, value      (13 quarters, Sep-2023 ->)
  external/fin_annual.csv      firm, fy_end, statement, item, value (12 years)
  external/market_cap.csv      firm, market_cap_cr, price, shares_cr, basis"""
import io, os, re, sys, time, urllib.request
import pandas as pd
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
ALIAS = {}
def page(sym, cons=True):
    u = f"https://www.screener.in/company/{sym}/" + ("consolidated/" if cons else "")
    return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=40).read().decode()
def num(x):
    x = str(x).replace(",", "").replace("%", "").strip()
    try: return float(x)
    except ValueError: return None
def table(s, sec):
    t = s.find("section", id=sec)
    t = t.find("table") if t else None
    if t is None: return None
    d = pd.read_html(io.StringIO(str(t)))[0]
    d = d.rename(columns={d.columns[0]: "item"}); d["item"] = d.item.str.replace("+", "", regex=False).str.strip()
    return d
firms = sorted(returns_wide().columns); Q, A, M, log = [], [], [], []
for f in firms:
    got = None
    for cons in (True, False):
        try:
            s = BeautifulSoup(page(ALIAS.get(f, f), cons), "lxml"); q = table(s, "quarters")
            if q is not None and q.shape[1] > 3 and q.iloc[0, 1:].notna().sum() > 2: got = (s, q, "consolidated" if cons else "standalone"); break
        except Exception as e:
            err = str(e)
        time.sleep(1.2)
    if not got: log.append((f, "FAILED")); print(f, "FAILED"); continue
    s, q, basis = got; log.append((f, basis))
    for c in q.columns[1:]:
        for it, v in zip(q.item, q[c]):
            if num(v) is not None: Q.append((f, c, it, num(v), basis))
    for sec in ("profit-loss", "balance-sheet", "cash-flow"):
        d = table(s, sec)
        if d is None: continue
        for c in d.columns[1:]:
            for it, v in zip(d.item, d[c]):
                if num(v) is not None: A.append((f, c, sec, it[:60], num(v), basis))
    r = {li.find("span", class_="name").get_text(strip=True): num(li.find("span", class_="number").get_text(strip=True)) for li in s.select("#top-ratios li")}
    mc, px = r.get("Market Cap"), r.get("Current Price")
    M.append((f, mc, px, mc / px if mc and px else None, r.get("Book Value"), r.get("Face Value"), basis))
    print(f, basis, len(q.columns) - 1, mc); time.sleep(1.5)
q = pd.DataFrame(Q, columns=["firm", "period", "item", "value", "basis"]); q["period_end"] = pd.to_datetime(q.period, format="%b %Y", errors="coerce") + pd.offsets.MonthEnd(0)
q.to_csv(EXT + "fin_quarterly.csv", index=False)
pd.DataFrame(A, columns=["firm", "period", "statement", "item", "value", "basis"]).to_csv(EXT + "fin_annual.csv", index=False)
pd.DataFrame(M, columns=["firm", "market_cap_cr", "price", "shares_cr", "book_value_ps", "face_value", "basis"]).to_csv(EXT + "market_cap.csv", index=False)
pd.DataFrame(log, columns=["firm", "status"]).to_csv(EXT + "fin_fetch_log.csv", index=False)
