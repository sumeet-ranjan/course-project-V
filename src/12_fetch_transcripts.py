"""Earnings-call transcripts for the quarter after each event (links from screener.in, PDFs read
through the Jina reader). Searches for event keywords and saves the surrounding text.
Output: research/transcripts/<case>_<symbol>_<month>.txt, research/transcript_keyword_hits.csv,
        research/transcript_coverage.csv"""
import os, re, sys, time, urllib.request
import pandas as pd
from bs4 import BeautifulSoup
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = ROOT + "/research/transcripts/"; os.makedirs(OUT, exist_ok=True)
CASES = {
 "chennai_2023": (["APOLLOTYRE", "CEATLTD", "JKTYRE", "MRF", "MARUTI", "HINDUNILVR", "APOLLOHOSP"], ["Jan 2024", "Feb 2024"],
                  r"cyclone|michaung|flood|chennai|heavy rain|production loss|plant shut|shutdown|disrupt"),
 "delhi_2024": (["DLF", "ANANTRAJ", "NBCC", "ULTRACEMCO", "SHREECEM", "ACC", "MAXHEALTH"], ["Jan 2025", "Feb 2025"],
                r"grap|pollution|construction ban|ban on construction|air quality|ncr|stoppage|disrupt"),
 "gujarat_2024": (["PETRONET", "GAIL", "GUJALKALI", "GNFC", "GSFC", "AARTIIND", "UPL", "SRF", "DCMSHRIRAM", "BORORENEW"], ["Oct 2024", "Nov 2024"],
                  r"flood|heavy rain|monsoon|vadodara|inundat|water.?logg|shutdown|plant shut|disrupt|force majeure"),
 "gujarat_2023": (["PETRONET", "GUJALKALI", "GNFC", "GSFC", "AARTIIND", "UPL", "SRF", "DCMSHRIRAM"], ["Oct 2023", "Nov 2023"],
                  r"flood|narmada|heavy rain|ankleshwar|bharuch|inundat|shutdown|plant shut|disrupt|force majeure"),
}
def direct(u): return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=40).read().decode()
def jina(u):
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request("https://r.jina.ai/" + u, headers={"User-Agent": "Mozilla/5.0", "X-Timeout": "60"}), timeout=120).read().decode("utf-8", "replace").split("Markdown Content:", 1)[-1]
        except Exception as e: err = e; time.sleep(10 * (i + 1))
    raise err
hits, cov, links = [], [], {}
for case, (syms, months, kw) in CASES.items():
    for s in syms:
        if s not in links:
            try:
                so = BeautifulSoup(direct(f"https://www.screener.in/company/{s}/consolidated/"), "lxml"); c = so.select_one("div.documents.concalls")
                links[s] = [(" ".join(li.get_text(" ", strip=True).split())[:8], next((a.get("href") for a in li.select("a") if "Transcript" in a.get_text()), None)) for li in (c.select("li") if c else [])]
            except Exception as e: links[s] = []
            time.sleep(1.5)
        m = [(mo, u) for mo, u in links[s] if mo in months and u]
        if not m: cov.append(dict(case=case, symbol=s, month="", status="no transcript listed", chars=0, n_hits=0)); print(case, s, "none"); continue
        mo, u = m[0]; fn = f"{OUT}{case}_{s}_{mo.replace(' ', '')}.txt"
        if not os.path.exists(fn):
            try: open(fn, "w").write(jina(u)); time.sleep(5)
            except Exception as e: cov.append(dict(case=case, symbol=s, month=mo, status="fetch failed: " + str(e)[:60], chars=0, n_hits=0)); print(case, s, "FAIL"); continue
        t = re.sub(r"\s+", " ", open(fn).read()); n = 0
        for x in re.finditer(kw, t, re.I):
            n += 1; hits.append(dict(case=case, symbol=s, call_month=mo, keyword=x.group(0).lower(), context=t[max(0, x.start() - 300):x.end() + 300], source_url=u))
        cov.append(dict(case=case, symbol=s, month=mo, status="read" if len(t) > 3000 else "too short (likely unreadable)", chars=len(t), n_hits=n)); print(case, s, mo, len(t), n)
pd.DataFrame(hits).to_csv(ROOT + "/research/transcript_keyword_hits.csv", index=False)
pd.DataFrame(cov).to_csv(ROOT + "/research/transcript_coverage.csv", index=False)
