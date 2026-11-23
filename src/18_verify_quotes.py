"""Independent re-check of the sub-agents' evidence tables: does each quote appear on its source page?

For every row of research/proxy/third_party_*.csv and flow_data.csv that claims read_mode =
original_text, fetch the source URL again (directly; through the Jina reader if the site refuses)
and test whether the quote is on the page. Matching is on normalised text (lower case, letters and
digits only) using the longest of the quote's 8-word shingles, so small spacing differences pass.
Output: research/proxy/quote_check.csv (one row per evidence row: verified / not_matched / unreachable).
PDF and spreadsheet sources are marked not_checked_binary (they need a parser, not a text match).
"""
import os, re, sys, time, csv, urllib.request, pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PX = ROOT + "/research/proxy/"
CACHE = ROOT + "/research/proxy/_page_cache/"; os.makedirs(CACHE, exist_ok=True)
norm = lambda s: re.sub(r"[^a-z0-9ऀ-෿]+", " ", str(s).lower()).strip()

def fetch(u, only=("direct", "reader")):
    fn = CACHE + re.sub(r"[^A-Za-z0-9]+", "_", u)[:150] + ("" if len(only) == 2 else "_" + only[0]) + ".txt"
    if os.path.exists(fn): return open(fn, encoding="utf-8", errors="replace").read()
    txt = ""
    for via in only:
        try:
            url = u if via == "direct" else "https://r.jina.ai/" + u
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)", "X-Timeout": "40", "Accept": "text/html,*/*"})
            raw = urllib.request.urlopen(req, timeout=70).read().decode("utf-8", "replace")
            raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw); raw = re.sub(r"(?s)<[^>]+>", " ", raw)
            raw = raw.replace("&nbsp;", " ").replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", '"').replace("&rsquo;", "'").replace("&lsquo;", "'")
            if len(norm(raw)) > 400: txt = via + "\n" + raw; break
        except Exception as e:
            txt = ""
        time.sleep(6 if via == "reader" else 1)
    open(fn, "w", encoding="utf-8").write(txt)
    return txt

rows = []
FILES = ("third_party_chennai_2023.csv", "third_party_gujarat.csv", "flow_data.csv", "official_hazard_records.csv",
         "flow_data_round3.csv", "damage_disclosures.csv", "government_documents.csv")
for f in FILES:
    if not os.path.exists(PX + f): continue
    d = pd.read_csv(PX + f, dtype=str).fillna("")
    for i, r in d.iterrows():
        u, q, mode = r.get("source_url", ""), r.get("source_quote", r.get("passage", "")), r.get("read_mode", "")
        res = dict(file=f, row=i + 2, source_url=u, read_mode=mode, quote_start=q[:70])
        if mode != "original_text" or not u.startswith("http") or len(norm(q).split()) < 4:
            res["check"] = "not_claimed_original" if mode != "original_text" else "no_quote"
        elif re.search(r"\.(pdf|xlsx?|csv)(\?|$)", u, re.I):
            res["check"] = "not_checked_binary"
        else:
            page = fetch(u); via, _, body = page.partition("\n"); nb = norm(body); w = norm(q).split()
            sh = [" ".join(w[k:k + 8]) for k in range(0, max(1, len(w) - 7))]
            hit = sum(s in nb for s in sh)
            if via == "direct" and hit / len(sh) < 0.5:        # some sites send a shell page to plain clients: try the reader
                page2 = fetch(u, only=("reader",)); v2, _, b2 = page2.partition("\n"); nb2 = norm(b2); h2 = sum(s in nb2 for s in sh)
                if h2 > hit: via, nb, hit = "reader", nb2, h2
            res["via"] = via
            res["check"] = "unreachable" if not nb else ("verified" if hit / len(sh) >= 0.5 else ("partial" if hit else "not_matched"))
            res["share_of_quote_found"] = round(hit / len(sh), 2) if nb else ""
        rows.append(res)
        if len(rows) % 20 == 0: print(len(rows), "rows checked", flush=True)
# transcripts collected in Round 4: check each quote against the saved transcript text (local files)
tf = ROOT + "/research/transcripts_round3.csv"
if os.path.exists(tf):
    d = pd.read_csv(tf, dtype=str).fillna("")
    for i, r in d.iterrows():
        q = r.get("quote", ""); fn = ROOT + "/research/transcripts/" + r.get("transcript_file", "")
        res = dict(file="transcripts_round3.csv", row=i + 2, source_url=r.get("source_url", ""), read_mode="saved_transcript", quote_start=q[:70])
        if len(norm(q).split()) < 4: res["check"] = "no_quote"
        elif not os.path.isfile(fn): res["check"] = "unreachable"
        else:
            nb = norm(open(fn, encoding="utf-8", errors="replace").read()); w = norm(q).split()
            sh = [" ".join(w[k:k + 8]) for k in range(0, max(1, len(w) - 7))]; hit = sum(x in nb for x in sh)
            res["via"] = "local file"; res["check"] = "verified" if hit / len(sh) >= 0.5 else ("partial" if hit else "not_matched"); res["share_of_quote_found"] = round(hit / len(sh), 2)
        rows.append(res)
out = pd.DataFrame(rows)
# table rows quoted as "State | Nov-22 8,551 | Nov-23 10,255 | Growth 20%" (column labels added by the
# collector) cannot match as text: check instead that the state's row on the page carries the same numbers in order
if os.path.exists(PX + "flow_data_round3.csv"):
    fd = pd.read_csv(PX + "flow_data_round3.csv", dtype=str).fillna("")
    for i in out.index[(out.file == "flow_data_round3.csv") & (out.check == "not_matched")]:
        r = fd.loc[int(out.at[i, "row"]) - 2]
        if "|" not in r.source_quote: continue
        t = re.sub(r"\s+", " ", fetch(r.source_url).partition("\n")[2])
        nums = [n.replace(",", "") for n in re.findall(r"\d[\d,]*", r.source_quote.split("|", 1)[1])]
        nums = [n for n in nums if len(n) >= 2 and n not in ("22", "23", "24", "25")]
        for m in re.finditer(re.escape(r.region), t):
            seg = t[m.end(): m.end() + 120].replace(",", ""); pos, good = 0, True
            for n in nums:
                k = seg.find(n, pos)
                if k < 0: good = False; break
                pos = k + len(n)
            if good: out.at[i, "check"] = "verified_table_numbers"; break
out.to_csv(PX + "quote_check.csv", index=False, quoting=csv.QUOTE_MINIMAL)
print(out.groupby(["file", "check"]).size().unstack(fill_value=0).to_string())
