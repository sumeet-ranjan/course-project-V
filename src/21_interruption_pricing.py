"""Step 5 pricing check: is the share-price move the size of the physical interruption?

For each firm with zone assets in the two events with usable night-light readings, compare
  (a) the market-value change in the 5 trading days after the event, relative to unexposed firms, with
  (b) an UPPER BOUND on operating profit lost to the interruption:
        share of plant cost shown dark  x  days dark / 365  x  the year's operating profit
      where "days dark" runs from the event start to the first clean night back above 80% of normal
      (so cloudy nights count as dark), and no later catch-up of output is allowed; and
  (c) a cruder bound that idles ALL of the firm's zone assets for the length of the state-wide
      electricity dip (3 days in Tamil Nadu, 8 days in Gujarat).
If (a) is many times (b) and (c), the price move cannot be the cost of the stoppage itself.
Market value = current share count x the pack's price (approximate, as in README 5.3).
Output: outputs/tables/pricing_interruption_bound.csv
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from es_lib import *
EVS = {"E_CHE_FLOOD_2023": ("Chennai Dec 2023", "Mar 2024", 3), "E_GJ_FLOOD_2024": ("Gujarat Aug 2024", "Mar 2025", 8)}
pl = pd.read_csv(TAB + "ntl_plant_event.csv"); fi = pd.read_csv(TAB + "ntl_firm_event.csv"); cars = pd.read_csv(TAB + "event_study_firm_cars.csv")
fa = pd.read_csv(EXT + "fin_annual.csv"); fa = fa[fa.statement == "profit-loss"]
mc = pd.read_csv(EXT + "market_cap.csv").set_index("firm")
px = stock().pivot(index="date", columns="asset_id", values="close").reindex(R.index).ffill()
rows = []
for ev, (label, fy, dip_days) in EVS.items():
    t0 = t0_of(EVENTS.set_index("event_id").start[ev])
    c = cars[cars.event_id == ev].set_index("nse_symbol"); none = c.car_0_5[c.share_cost == 0].mean()
    for r in fi[(fi.event_id == ev) & fi.traded & (fi.share_zone >= 0.10)].itertuples():
        f = r.nse_symbol
        if f not in c.index or pd.isna(c.car_0_5[f]): continue
        g = pl[(pl.event_id == ev) & (pl.nse_symbol == f) & (pl.dark == True)]          # noqa: E712
        w = g.plant_share.fillna(0)
        days = float(np.average(g.first_night_back_above_0_8.fillna(30), weights=w)) if w.sum() > 0 else np.nan
        y = fa[(fa.firm == f) & (fa.period == fy)].set_index("item").value
        sales, op = y.get("Sales", np.nan), y.get("Operating Profit", np.nan)
        mcap = mc.shares_cr.get(f, np.nan) * px.iloc[t0 - 1].get(f, np.nan)
        rel = c.car_0_5[f] - none
        lost_dark = r.share_dark * days / 365 * op if days == days else 0.0
        lost_zone = r.share_zone * dip_days / 365 * op
        rows.append(dict(event=label, nse_symbol=f, share_zone=r.share_zone, share_dark=r.share_dark, days_to_80pct_light=days,
                         fy=fy, sales_cr=sales, operating_profit_cr=op, market_cap_before_cr=mcap, car_0_5_vs_unexposed=rel,
                         value_change_cr=rel * mcap, lost_op_profit_bound_dark_cr=lost_dark, lost_op_profit_bound_zone_cr=lost_zone,
                         value_change_over_dark_bound=rel * mcap / -lost_dark if lost_dark > 0 else np.nan,
                         value_change_over_zone_bound=rel * mcap / -lost_zone if lost_zone > 0 else np.nan))
o = pd.DataFrame(rows); o.round(3).to_csv(TAB + "pricing_interruption_bound.csv", index=False)
pd.set_option("display.width", 260); pd.set_option("display.max_columns", 30)
print(o.round(2).to_string(index=False))
for ev, x in o.groupby("event"):
    neg = x[x.value_change_cr < 0]
    print(f"\n{ev}: {len(x)} firms; summed value change {x.value_change_cr.sum():,.0f} cr; summed dark-asset bound {x.lost_op_profit_bound_dark_cr.sum():,.1f} cr; "
          f"summed all-zone-assets bound {x.lost_op_profit_bound_zone_cr.sum():,.1f} cr; ratio to zone bound {x.value_change_cr.sum() / -x.lost_op_profit_bound_zone_cr.sum():.0f}x")
