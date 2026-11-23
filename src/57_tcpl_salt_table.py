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
    x = x.assign(_pri=~x.document_title.str.contains("Investor Presentation", case=False)).sort_values("_pri", kind="stable")   # the deck's figures first (checkpoint-4 review)
    v = pd.to_numeric(x.value.str.extract(r"(-?\d+(?:\.\d+)?)")[0], errors="coerce").dropna()
    return (float(v.iloc[0]), x.document_title.iloc[0]) if len(v) else (np.nan, "")
def text(q, metric):
    x = K[(K.quarter == q) & (K.metric == metric)]
    return " | ".join(dict.fromkeys(x.quote)) if len(x) else ""
PRICE = {"Q1 FY25": "none", "Q2 FY25": "announced: Rs 2 on a Rs 28 pack (about 7%), effective October 2024 ('Price increase announced in Tata Salt to combat the input cost increase')",
         "Q3 FY25": "in effect: the same increase ('a 7% price increase after 2 years')", "Q4 FY25": "no new increase ('taken price increase slightly head of the curve')"}
MITH = {"Q1 FY25": "before the storm", "Q2 FY25": "yes: 'Mithapur recorded its highest ever rain since 1929'; the cost had not yet reached Tata Consumer in the September quarter",
        "Q3 FY25": "no mention", "Q4 FY25": "no mention"}
rows = []
for q in ("Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25", "FY25"):
    qq, fy = (("Q4 FY25", True) if q == "FY25" else (q, False))
    rv, rs = num(qq, "salt_revenue_growth", fy); vv, vs = num(qq, "salt_volume_growth", fy)
    rows.append(dict(period=q, salt_revenue_growth_pct=rv, salt_volume_growth_pct=vv, implied_price_mix_pp=(rv - vv) if pd.notna(rv) and pd.notna(vv) else np.nan,
                     retail_price_action=PRICE.get(q, ""), market_share=("" if q == "FY25" else text(q, "salt_market_share")), margin_statement=("" if q == "FY25" else text(q, "salt_margin")),
                     mithapur_mentioned=MITH.get(q, ""), note=("deck slide 24: 'Salt revenue grew 2% with flat volumes'; the Q2 call gives salt volume +1%" if q == "Q2 FY25" else
                                                           "full year, from the Q4 FY25 presentation" if q == "FY25" else ""),
                     sources="; ".join(dict.fromkeys([s for s in (rs, vs) if s]))))
T = pd.DataFrame(rows); T.to_csv(DEL + "stepC_gj_tcpl_salt.csv", index=False)
# magnitude (checkpoint-4 review): the storm cost against the value of the 7% increase
PURCH = 758.46 + 818.18   # Tata Consumer's FY24 purchases from Tata Chemicals, Rs cr (related-party filings, verified_links.csv G001)
M = pd.DataFrame([
    dict(item="Tata Chemicals' total weather cost (Q2 FY25 call)", value_cr=40.0, basis="'around Rs.40 crore, of which Rs.25 crore was on account of unstable operation, the increased cost, and Rs.15 crore of the insurance claim' (research/realign/docs/tatachain__TATACHEM__Q2FY25_call.txt)"),
    dict(item="part of it passed to Tata Consumer", value_cr=np.nan, basis="not given in any document read (Tata Chemicals Q2/Q3 calls, AR FY2024-25; Tata Consumer Q2/Q3 calls, decks)"),
    dict(item="value of a 7% increase, at least (7% x FY24 purchases from Tata Chemicals)", value_cr=round(0.07 * PURCH, 1), basis=f"0.07 x Rs {PURCH:,.2f} cr a year; a lower bound, since the increase applies to Tata Salt's retail value, which exceeds the purchase cost"),
    dict(item="ratio: annual value of the increase / whole storm cost", value_cr=round(0.07 * PURCH / 40.0, 1), basis="the increase is worth about 2.8 times the storm's whole cost to Tata Chemicals in its first year: consistent with the company's own statement that it also recovers two years without an inflation increase")])
M.to_csv(DEL + "stepC_gj_salt_magnitude.csv", index=False); print(M.to_string(index=False))
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 70); print(T.drop(columns=["sources"]).to_string(index=False))
