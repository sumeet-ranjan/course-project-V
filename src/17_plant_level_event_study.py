"""Rerun of the event study with plant-level hits instead of district footprints.

Question: does the stock reaction scale with assets that were actually dark (night lights) or
actually under water (Sentinel-1 radar), rather than with assets merely located in the district?

Exposure measures per firm and event (all are shares of the firm's total plant cost):
  share_zone     plants in the affected districts (the measure used in 03_event_study.py)
  share_dark     zone plants whose first clean night-light reading was < 60% of normal
  share_dim      zone plants weighted by how far they dimmed against far-away plants that night
  share_notdark  share_zone - share_dark (in the zone, observed or not, but not shown dark)
  share_flood500 zone plants with radar-detected new water within 500 m (Gujarat 2024 only)
Same engine and same inference as 03: market-model abnormal returns vs NIFTY 500 and 1,000 placebo
dates with the SAME exposure vector. Outputs: outputs/tables/plant_level_event_study.csv,
plant_level_exposure.csv, figs/09_plant_level_dose_response.png
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from es_lib import *
PL = placebo_t0s()
EVS = {"E_CHE_FLOOD_2023": "Chennai, Cyclone Michaung (Dec 2023)", "E_GJ_FLOOD_2024": "Gujarat flood (Aug 2024)"}
fi = pd.read_csv(TAB + "ntl_firm_event.csv")
ex = fi[["event_id", "nse_symbol", "share_zone", "share_observed", "share_dark", "share_dim"]].copy()
ex["share_notdark"] = ex.share_zone - ex.share_dark
if os.path.exists(TAB + "flood_firm_event.csv"):
    fl = pd.read_csv(TAB + "flood_firm_event.csv")
    ex = ex.merge(fl[["event_id", "nse_symbol", "share_flood500", "share_flood_observed"]], on=["event_id", "nse_symbol"], how="left")
ex.round(4).to_csv(TAB + "plant_level_exposure.csv", index=False)
MEAS = [m for m in ["share_zone", "share_dark", "share_dim", "share_notdark", "share_flood500"] if m in ex.columns]

def vec(ev, m, firms):
    return ex[ex.event_id == ev].set_index("nse_symbol")[m].reindex(firms).fillna(0.0)

def stat(ar, x, zone_x, w):
    c = car(ar, *w).dropna(); xv = x.reindex(c.index); zv = zone_x.reindex(c.index)
    hi, none = c[xv >= 0.10], c[zv == 0]
    slope = np.polyfit(xv.values, c.values, 1)[0] if xv.std() > 0 else np.nan
    return hi.mean() - none.mean(), slope, len(hi), hi.mean(), none.mean()

def horse(ar, xd, xn, w):
    """CAR = a + b_dark * share_dark + b_notdark * share_notdark."""
    c = car(ar, *w).dropna()
    X = np.column_stack([np.ones(len(c)), xd.reindex(c.index).values, xn.reindex(c.index).values])
    b = np.linalg.lstsq(X, c.values, rcond=None)[0]
    return b[1], b[2]

rows = []
for ev, label in EVS.items():
    t0 = t0_of(EVENTS.set_index("event_id").start[ev]); ar = ar_matrix(t0)
    plac = [a for a in (ar_matrix(int(p)) for p in PL) if a is not None]
    for m in MEAS:
        if ex[(ex.event_id == ev)][m].fillna(0).sum() == 0: continue
        for w in WINDOWS:
            d, s, n, ch, cn = stat(ar, vec(ev, m, ar.columns), vec(ev, "share_zone", ar.columns), w)
            pb = np.array([stat(a, vec(ev, m, a.columns), vec(ev, "share_zone", a.columns), w)[:2] for a in plac])
            rows.append(dict(event_id=ev, label=label, measure=m, window=f"[{w[0]},{w[1]}]", n_firms_ge10pct=n, car_exposed=ch, car_unexposed=cn,
                diff=d, p_diff=np.mean(np.abs(pb[:, 0] - np.nanmean(pb[:, 0])) >= abs(d - np.nanmean(pb[:, 0]))) if n else np.nan,
                slope=s, p_slope=np.mean(np.abs(pb[:, 1] - np.nanmean(pb[:, 1])) >= abs(s - np.nanmean(pb[:, 1])))))
    for w in WINDOWS:   # horse race: dark assets vs other zone assets
        bd, bn = horse(ar, vec(ev, "share_dark", ar.columns), vec(ev, "share_notdark", ar.columns), w)
        pb = np.array([horse(a, vec(ev, "share_dark", a.columns), vec(ev, "share_notdark", a.columns), w) for a in plac])
        rows.append(dict(event_id=ev, label=label, measure="horse race: b_dark | b_notdark", window=f"[{w[0]},{w[1]}]",
            slope=bd, p_slope=np.mean(np.abs(pb[:, 0] - pb[:, 0].mean()) >= abs(bd - pb[:, 0].mean())),
            diff=bn, p_diff=np.mean(np.abs(pb[:, 1] - pb[:, 1].mean()) >= abs(bn - pb[:, 1].mean())),
            car_exposed=bd - bn, car_unexposed=np.mean(np.abs((pb[:, 0] - pb[:, 1]) - (pb[:, 0] - pb[:, 1]).mean()) >= abs((bd - bn) - (pb[:, 0] - pb[:, 1]).mean()))))
res = pd.DataFrame(rows); res.round(4).to_csv(TAB + "plant_level_event_study.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print("=== exposure measure by measure (diff = firms with >=10% on that measure minus firms with no zone assets) ===")
print(res[~res.measure.str.startswith("horse")][["label", "measure", "window", "n_firms_ge10pct", "car_exposed", "car_unexposed", "diff", "p_diff", "slope", "p_slope"]].round(3).to_string(index=False))
h = res[res.measure.str.startswith("horse")].rename(columns={"slope": "b_dark", "p_slope": "p_b_dark", "diff": "b_notdark", "p_diff": "p_b_notdark",
                                                             "car_exposed": "b_dark_minus_b_notdark", "car_unexposed": "p_difference"})
print("\n=== horse race: CAR = a + b_dark*share_dark + b_notdark*share_notdark (per 100% of assets) ===")
print(h[["label", "window", "b_dark", "p_b_dark", "b_notdark", "p_b_notdark", "b_dark_minus_b_notdark", "p_difference"]].round(3).to_string(index=False))

# ---- figure: 5-day abnormal return against each firm's zone share, marking how much of it was dark
cars = pd.read_csv(TAB + "event_study_firm_cars.csv")
fig, axs = plt.subplots(1, 2, figsize=(13, 5.2), sharey=True)
for ax, (ev, label) in zip(axs, EVS.items()):
    c = cars[cars.event_id == ev].merge(ex[ex.event_id == ev], on="nse_symbol", how="left").fillna({"share_zone": 0, "share_dark": 0})
    c = c[c.share_zone >= 0.10]
    ax.axhline(0, color="#c9c8c2", lw=.9)
    none = cars[(cars.event_id == ev) & (cars.share_cost == 0)].car_0_5.mean() * 100
    ax.axhline(none, color=MUTED, lw=.8, ls=":"); ax.text(104, none + .25, "mean of firms with no zone assets", fontsize=7.5, color=MUTED, ha="right")
    obs = c.share_observed.fillna(0) >= 0.5 * c.share_zone; dk = c.share_dark >= 0.10
    for msk, col, mk, lab in ((dk, ORANGE, "s", "≥10% of assets dark"), (obs & ~dk, BLUE, "o", "sites observed, not dark"),
                              (~obs & ~dk, "#a3a29b", "o", "sites mostly unobserved (cloud)")):
        g = c[msk]
        ax.scatter(g.share_zone * 100, g.car_0_5 * 100, s=58, color=col if col != "#a3a29b" else "none", edgecolors=SURF if col != "#a3a29b" else col,
                   marker=mk, lw=1, label=f"{lab} ({len(g)})", zorder=3)
        for r in g.itertuples(): ax.annotate(r.nse_symbol, (r.share_zone * 100, r.car_0_5 * 100), xytext=(5, 4), textcoords="offset points", fontsize=7, color=MUTED)
    ax.set_title(label, loc="left"); ax.set_xlabel("Share of plant cost in the affected districts, %"); ax.set_xlim(5, 105); ax.legend(fontsize=8, loc="lower left")
axs[0].set_ylabel("Abnormal return, event day to day 5, %")
fig.suptitle("Stock reaction of zone-exposed firms, split by whether their sites went dark", x=0.01, ha="left", fontweight="bold")
fig.tight_layout(); fig.savefig(FIG + "09_plant_level_dose_response.png", dpi=200)
