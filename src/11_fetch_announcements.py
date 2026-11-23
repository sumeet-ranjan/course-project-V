"""Pull NSE corporate announcements for the open cases through the Jina reader (r.jina.ai),
which this environment can reach while nseindia.com itself refuses automated clients.
Output: research/nse_announcements/<case>_<symbol>.json and research/nse_announcements_index.csv"""
import json, os, re, sys, time, urllib.request
import pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = ROOT + "/research/nse_announcements/"
CASES = {
 "chennai_2023": (["APOLLOTYRE", "MRF", "JKTYRE", "CEATLTD", "MARUTI", "HINDUNILVR", "APOLLOHOSP"], "01-12-2023", "20-12-2023"),
 "delhi_2024": (["DLF", "ANANTRAJ", "NBCC", "ULTRACEMCO", "SHREECEM", "ACC", "IGL", "MAXHEALTH"], "15-11-2024", "15-01-2025"),
 "gujarat_2024": (["PETRONET", "GAIL", "IOC", "BPCL", "GUJALKALI", "GNFC", "GSFC", "AARTIIND", "UPL", "SRF", "DCMSHRIRAM", "BORORENEW"], "25-08-2024", "30-09-2024"),
 "gujarat_2023": (["PETRONET", "GUJALKALI", "GNFC", "GSFC", "AARTIIND", "UPL", "SRF", "DCMSHRIRAM", "BODALCHEM", "KIRIINDUS"], "15-09-2023", "15-10-2023"),
}
KW = re.compile(r"cyclone|flood|rain|michaung|grap|pollution|construction ban|shut|disrupt|force majeure|suspen|stoppage|production|operations|natural calamit|inundat|water.?logg|resum", re.I)
def get(u):
    for i in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request("https://r.jina.ai/" + u, headers={"User-Agent": "Mozilla/5.0", "X-Timeout": "40"}), timeout=80)
            return r.read().decode("utf-8", "replace").split("Markdown Content:", 1)[-1].strip()
        except Exception as e:
            err = e; time.sleep(8 * (i + 1))
    raise err
rows = []
for case, (syms, a, b) in CASES.items():
    for s in syms:
        fn = f"{OUT}{case}_{s}.json"
        if not os.path.exists(fn):
            try:
                t = get(f"https://www.nseindia.com/api/corporate-announcements?index=equities&symbol={s}&from_date={a}&to_date={b}")
                j = json.loads(t[t.index("["):t.rindex("]") + 1]); json.dump(j, open(fn, "w"))
            except Exception as e:
                print("FAIL", case, s, str(e)[:80]); time.sleep(5); continue
            time.sleep(5)
        for x in json.load(open(fn)):
            txt = " ".join(str(x.get(k) or "") for k in ("desc", "attchmntText"))
            rows.append(dict(case=case, symbol=s, datetime=x.get("an_dt"), subject=x.get("desc"), text=(x.get("attchmntText") or "")[:400], attachment=x.get("attchmntFile"), keyword_hit=bool(KW.search(txt))))
        print(case, s, sum(1 for r in rows if r["case"] == case and r["symbol"] == s))
d = pd.DataFrame(rows); d.to_csv(ROOT + "/research/nse_announcements_index.csv", index=False)
print(len(d), "announcements;", int(d.keyword_hit.sum()), "keyword hits")
