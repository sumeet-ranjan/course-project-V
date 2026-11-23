"""Check every quote in research/realign/*.csv against the saved text of its document.

A row is usable in a deliverable only if read_mode is an original document and its quote is found in the
saved text (case-insensitive, whitespace, quote marks and dashes normalised; a quote with "..." is checked
fragment by fragment). Rows without a quote (e.g. documented "no mention") are listed as such.
Output: research/realign/quote_check_realign.csv
"""
import os, re, sys, glob; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from common import ROOT
def norm(t):
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")
    t = re.sub(r"[*#>_|]", " ", t)
    return re.sub(r"\s+", " ", t).strip().lower()
rows = []
for f in sorted(glob.glob(ROOT + "/research/realign/*.csv")):
    if f.endswith("quote_check_realign.csv"): continue
    d = pd.read_csv(f, dtype=str).fillna("")
    if not {"quote", "saved_text"} <= set(d.columns): continue
    for i, r in d.iterrows():
        q, st = r.quote.strip(), r.saved_text.strip()
        path = st if st.startswith("/") else os.path.join(ROOT, st)
        if not q: status = "no quote"
        elif not st or not os.path.exists(path): status = "saved text missing"
        else:
            t = norm(open(path, encoding="utf-8", errors="ignore").read())
            if len(t) < 1500 and ("403" in t or "access denied" in t or "not found" in t): status = "saved text is an error page"
            else:
                frags = [norm(x) for x in re.split(r"\.\.\.|…|\[\.\.\.\]|\s\|\s", q) if len(norm(x)) > 5]
                status = "verified" if frags and all(x in t for x in frags) else "NOT FOUND"
        rows.append(dict(file=os.path.basename(f), row=i, key=r.get("nse_symbol", ""), read_mode=r.get("read_mode", ""), status=status, quote=q[:160]))
o = pd.DataFrame(rows); o.to_csv(ROOT + "/research/realign/quote_check_realign.csv", index=False)
print(o.groupby(["file", "status"]).size().to_string())
bad = o[o.status == "NOT FOUND"]
if len(bad): print("\nNOT FOUND:\n" + bad.to_string(index=False))
