"""Flows from official monthly statistics (research/proxy/flow_data_round3.csv, collected by a sub-agent
with a source link and quote per number; quotes re-checked by 18_verify_quotes.py).

GST collected in a state in month M mostly reflects supplies made in month M-1 (monthly returns are
filed by the 20th of the next month). So:
  Chennai, Dec 2023      -> Tamil Nadu collections of Jan 2024
  Gujarat, Aug 2024      -> Gujarat collections of Sep 2024 (and Sep 2023 flood -> Oct 2023)
  Delhi ban, Nov-Dec 2024 -> Delhi, Haryana, Uttar Pradesh collections of Dec 2024 and Jan 2025
Test: the hit state's share of the seven states' combined collections in the event month, against
the average of the month before and the month after; the same calculation one year later (or
earlier) removes the seasonal pattern (difference-in-differences on shares, levels only, so the
months without a published year-earlier figure can be used).
Output: outputs/tables/flows_gst_state_test.csv
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from common import *
d = pd.read_csv(ROOT + "/research/proxy/flow_data_round3.csv", dtype=str).fillna("")
g = d[d.dataset == "gst_state"].copy()
g["month"] = pd.to_datetime(g.period_label_in_source.str.replace("*", "", regex=False), format="%b-%y")
g["value"] = pd.to_numeric(g.value.str.replace(",", ""), errors="coerce")
# also use the year-earlier column of each release as a value for that earlier month when it is not reported on its own
g["cmp_month"] = pd.to_datetime(g.comparison_period.str.replace("*", "", regex=False), format="%b-%y", errors="coerce")
g["cmp"] = pd.to_numeric(g.comparison_value.str.replace(",", ""), errors="coerce")
prior = g.dropna(subset=["cmp_month", "cmp"]); prior = pd.DataFrame({"region": prior.region.values, "month": prior.cmp_month.values, "value": prior.cmp.values})
v = pd.concat([g[["region", "month", "value"]], prior], ignore_index=True)
v = v.dropna().drop_duplicates(["region", "month"], keep="first").pivot(index="month", columns="region", values="value").sort_index()
share = v.div(v.sum(axis=1), axis=0)

def did(state, m, ref_shift):
    m = pd.Timestamp(m); r = m + pd.DateOffset(months=ref_shift)
    def bump(t):
        a, b = t - pd.DateOffset(months=1), t + pd.DateOffset(months=1)
        if not all(x in share.index for x in (a, t, b)) or share[[state]].loc[[a, t, b]].isna().any().any(): return np.nan
        return share.at[t, state] - (share.at[a, state] + share.at[b, state]) / 2
    e, c = bump(m), bump(r)
    return e, c, e - c if np.isfinite(e) and np.isfinite(c) else np.nan, share.at[m, state] if m in share.index else np.nan
rows = []
for lab, st, m, shift in (("Chennai Dec 2023", "Tamil Nadu", "2024-01-01", 12), ("Gujarat Aug 2024", "Gujarat", "2024-09-01", -12),
                          ("Gujarat Sep 2023", "Gujarat", "2023-10-01", 12), ("Delhi ban Nov 2024", "Delhi", "2024-12-01", -12),
                          ("Delhi ban Nov 2024", "Haryana", "2024-12-01", -12), ("Delhi ban Nov 2024", "Uttar Pradesh", "2024-12-01", -12),
                          ("Delhi ban Dec 2024", "Delhi", "2025-01-01", -12), ("Delhi ban Dec 2024", "Haryana", "2025-01-01", -12),
                          ("Delhi ban Dec 2024", "Uttar Pradesh", "2025-01-01", -12)):
    e, c, dd, sh = did(st, m, shift)
    rows.append(dict(event=lab, state=st, collection_month=pd.Timestamp(m).strftime("%b %Y"), comparison_year_month=(pd.Timestamp(m) + pd.DateOffset(months=shift)).strftime("%b %Y"),
                     state_share_of_7=sh, bump_event_pp=100 * e, bump_comparison_pp=100 * c, difference_pp=100 * dd,
                     difference_pct_of_state=100 * dd / sh if np.isfinite(dd) and sh else np.nan))
o = pd.DataFrame(rows); o.round(3).to_csv(TAB + "flows_gst_state_test.csv", index=False)
pd.set_option("display.width", 250)
print("months available:", [x.strftime("%b-%y") for x in v.index]); print(o.round(3).to_string(index=False))
yo = g[g.growth_pct != ""].assign(gr=lambda x: pd.to_numeric(x.growth_pct, errors="coerce")).pivot_table(index="month", columns="region", values="gr")
print("\nyear-on-year growth (%) as published:"); print(yo.round(0).to_string())

# ---- placebo: the same statistic for every state and month where it can be computed
pl = []
for st in share.columns:
    for m in share.index:
        for shift in (12, -12):
            e, c, dd, sh = did(st, m, shift)
            if np.isfinite(dd): pl.append(dict(state=st, month=m, shift=shift, difference_pp=100 * dd, pct=100 * dd / sh))
pl = pd.DataFrame(pl).drop_duplicates(["state", "month"])
o["placebo_share_with_larger_abs_pct"] = [np.mean(pl.pct.abs() >= abs(x)) if np.isfinite(x) else np.nan for x in o.difference_pct_of_state]
o["placebo_n"] = len(pl)
o.round(3).to_csv(TAB + "flows_gst_state_test.csv", index=False)
print("\nplacebo distribution over", len(pl), "state-months: sd of difference (% of state) =", round(pl.pct.std(), 2),
      "| 90th pct of |difference| =", round(pl.pct.abs().quantile(.9), 2))
print(o[["event", "state", "collection_month", "difference_pct_of_state", "placebo_share_with_larger_abs_pct"]].round(3).to_string(index=False))
