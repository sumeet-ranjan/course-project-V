"""G7 R4: propagation at the downstream node measured with Tata Consumer's salt numbers by quarter, Q1-Q4 FY25.

Source: research/realign/tcpl_salt_kpis.csv (company presentations, press releases and call transcripts; only rows whose
quote passed src/42). Implied price/mix = salt revenue growth - salt volume growth (percentage points; an approximation
that also carries mix, e.g. value-added salts growing 26-35%). The single retail price increase (Rs 2 on a Rs 28 pack,
about 7%, after a two-year gap) was announced in the Q2 call of 18 Oct 2024 and reached the market in October (Q3).
Output: outputs/deliverables/stepC_gj_tcpl_salt.csv
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd, numpy as np
from common import ROOT, OUT
RE = ROOT + "/research/realign/"; DEL = OUT + "deliverables/"
qc = pd.read_csv(RE + "quote_check_realign.csv"); ok = set(qc[(qc.file == "tcpl_salt_kpis.csv") & (qc.status == "verified")].row)
K = pd.read_csv(RE + "tcpl_salt_kpis.csv", dtype=str).fillna(""); K = K[K.index.isin(ok)]
full_year = K.unit.str.contains("full year", case=False) | K.notes.str.contains("full year|full-year|FY25 full", case=False)
def num(q, metric, fy=False):
    x = K[(K.quarter == q) & (K.metric == metric) & (full_year == fy)]
    v = pd.to_numeric(x.value.str.extract(r"(-?\d+(?:\.\d+)?)")[0], errors="coerce").dropna()
    return (float(v.iloc[0]), x.document_title.iloc[0]) if len(v) else (np.nan, "")
def text(q, metric):
    x = K[(K.quarter == q) & (K.metric == metric)]
    return " | ".join(dict.fromkeys(x.quote)) if len(x) else ""
PRICE = {"Q1 FY25": "none", "Q2 FY25": "announced: Rs 2 on a Rs 28 pack (about 7%), in the market from October 2024",
         "Q3 FY25": "in effect: the same increase ('a 7% price increase after 2 years')", "Q4 FY25": "no new increase ('taken price increase slightly head of the curve')"}
MITH = {"Q1 FY25": "before the storm", "Q2 FY25": "yes: 'Mithapur recorded its highest ever rain since 1929'; the cost had not yet reached Tata Consumer in the September quarter",
        "Q3 FY25": "no mention", "Q4 FY25": "no mention"}
rows = []
for q in ("Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25", "FY25"):
    qq, fy = (("Q4 FY25", True) if q == "FY25" else (q, False))
    rv, rs = num(qq, "salt_revenue_growth", fy); vv, vs = num(qq, "salt_volume_growth", fy)
    rows.append(dict(period=q, salt_revenue_growth_pct=rv, salt_volume_growth_pct=vv, implied_price_mix_pp=(rv - vv) if pd.notna(rv) and pd.notna(vv) else np.nan,
                     retail_price_action=PRICE.get(q, ""), market_share=("" if q == "FY25" else text(q, "salt_market_share")), margin_statement=("" if q == "FY25" else text(q, "salt_margin")),
                     mithapur_mentioned=MITH.get(q, ""), note=("salt revenue growth for Q2 is in the Q2 investor presentation, which could not be retrieved (NSE 403; company copy empty)" if q == "Q2 FY25" else
                                                           "full year, from the Q4 FY25 presentation" if q == "FY25" else ""),
                     sources="; ".join(dict.fromkeys([s for s in (rs, vs) if s]))))
T = pd.DataFrame(rows); T.to_csv(DEL + "stepC_gj_tcpl_salt.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 70); print(T.drop(columns=["sources"]).to_string(index=False))
