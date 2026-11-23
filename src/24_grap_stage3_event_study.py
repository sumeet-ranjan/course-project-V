"""Step 3 rerun for Delhi: the construction ban starts with GRAP Stage III, not Stage IV.

Read directly from the government press releases (pib.gov.in; research/proxy/official_hazard_records.csv):
  * Stage III (29 Oct 2022, 2 Nov 2023): "Enforce strict ban on construction and demolition
    activities in the entire NCR, except for the following categories of projects" (railways, metro,
    airports, defence, hospitals, linear public projects, ...).
  * Stage IV (3 Nov 2022, 5 Nov 2023): adds "Ban C&D activities in linear public projects such as
    highways, roads, flyovers, over bridges, power transmission, pipelines".
  * 2024 (revised schedule): Stage III bans listed dust-generating categories (earthwork, piling,
    demolition, road works ...) across the NCR; Stage IV extends this to linear public projects.
So for builders the treatment date is the Stage III order. src/common.py is left unchanged (its
dates are the verified Stage IV dates); this script adds the Stage III dates beside them.
`start` is the first calendar day on which the order could be traded on (orders posted after the
market close are dated the next day). In 2024 the Stage III dates lead to the same first trading
days as the Stage IV dates already in common.py (15 Nov 2024 was not a trading day).
Output: outputs/tables/grap_stage3_event_study.csv
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from es_lib import *
EV3 = [  # (id, order posted, start used, label)
    ("GRAP3_2022A", "Sat 29 Oct 2022 5:37 PM", "2022-10-30", "Stage III, 29 Oct 2022 (to 14 Nov)"),
    ("GRAP3_2022B", "Sun 4 Dec 2022",          "2022-12-04", "Stage III, 4 Dec 2022 (to 7 Dec)"),
    ("GRAP3_2023",  "Thu 2 Nov 2023 8:12 PM",  "2023-11-03", "Stage III, 2 Nov 2023 (to 28 Nov)"),
    ("GRAP3_2024J", "Sun 14 Jan 2024",         "2024-01-14", "Stage III, 14 Jan 2024 (to 18 Jan)"),
    ("GRAP3_2024A", "Thu 14 Nov 2024 7:14 PM", "2024-11-15", "Stage III, 14 Nov 2024 (to 5 Dec)"),
    ("GRAP3_2024B", "Mon 16 Dec 2024 evening", "2024-12-17", "Stage III, 16 Dec 2024 (to 27 Dec)"),
]
co = companies().set_index("nse_symbol"); co["sector"] = co.primary_industry.map(sector)
ex = exposure(); x_all = ex[ex.zone == "NCR"].set_index("nse_symbol").share_cost
PL = placebo_t0s()

def stat(ar, w, realty_only):
    c = car(ar, *w).dropna(); xv = x_all.reindex(c.index).fillna(0.0)
    if realty_only: keep = co.sector.reindex(c.index) == "Realty/Construction"; c, xv = c[keep], xv[keep]
    hi, none = c[xv >= 0.25], c[xv == 0]
    return hi.mean() - none.mean(), len(hi), len(none), hi.mean(), none.mean()

plac = [a for a in (ar_matrix(int(p)) for p in PL) if a is not None]
rows = []
for eid, posted, start, label in EV3:
    t0 = t0_of(start); ar = ar_matrix(t0)
    for realty in (False, True):
        for w in [(-1, 1), (0, 5), (0, 10), (0, 20)]:
            d, nh, nn, ch, cn = stat(ar, w, realty)
            pb = np.array([stat(a, w, realty)[0] for a in plac]); pb = pb[np.isfinite(pb)]
            rows.append(dict(event=eid, label=label, order_posted=posted, first_trading_day=DATES[t0].date(), sample="real estate and construction only" if realty else "all sectors",
                             window=f"[{w[0]},{w[1]}]", n_ncr=nh, n_other=nn, car_ncr=ch, car_other=cn, diff=d,
                             p_diff=np.mean(np.abs(pb - pb.mean()) >= abs(d - pb.mean())) if nh and nn else np.nan))
o = pd.DataFrame(rows); o.round(4).to_csv(TAB + "grap_stage3_event_study.csv", index=False)
pd.set_option("display.width", 250)
print("trading days around 15 Nov 2024:", [str(d.date()) for d in DATES[(DATES >= "2024-11-13") & (DATES <= "2024-11-19")]])
for s in ("all sectors", "real estate and construction only"):
    print("\n===", s); print(o[(o["sample"] == s) & o.window.isin(["[0,5]", "[0,10]"])][["label", "first_trading_day", "window", "n_ncr", "n_other", "car_ncr", "car_other", "diff", "p_diff"]].round(3).to_string(index=False))
m = o[(o["sample"] == "real estate and construction only") & (o.window == "[0,5]")]
print("\nreal estate, days 0-5, mean difference across the six Stage III orders:", round(m["diff"].mean(), 4), "| negative in", int((m["diff"] < 0).sum()), "of", len(m))
