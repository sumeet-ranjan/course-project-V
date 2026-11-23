"""Direct-exposure event study (H1 + dose-response + placebo-date inference).
For each event: CAR by exposure group, cross-sectional slope of CAR on asset-exposure share,
and an empirical p-value from 1,000 random placebo dates using the SAME exposure vector
(robust to cross-sectional correlation and to sector tilts in who is exposed)."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from es_lib import *
co = companies().set_index("nse_symbol"); co["sector"] = co.primary_industry.map(sector)
ex = exposure()
PL = placebo_t0s()

def expo_vec(zone, firms):
    s = ex[ex.zone == zone].set_index("nse_symbol").share_cost
    return s.reindex(firms).fillna(0.0)

def stats(ar, x):
    out = {}
    for lo, hi in WINDOWS:
        c = car(ar, lo, hi).dropna(); xv = x.reindex(c.index)
        hi_, none = c[xv >= 0.25], c[xv == 0]
        slope = np.polyfit(xv.values, c.values, 1)[0] if xv.std() > 0 else np.nan
        out[(lo, hi)] = dict(mean_high=hi_.mean(), mean_none=none.mean(), diff=hi_.mean() - none.mean(),
                             slope=slope, n_high=len(hi_), n_none=len(none),
                             frac_neg_high=(hi_ < 0).mean())
    return out

rows, cars, paths = [], [], {}
PLAC = {}
for _, e in EVENTS.iterrows():
    t0 = t0_of(e.start); ar = ar_matrix(t0); x = expo_vec(e.zone, ar.columns)
    st = stats(ar, x)
    if e.zone not in PLAC:   # placebo distribution depends only on the zone's exposure vector
        acc = {w: [] for w in WINDOWS}
        for p in PL:
            a = ar_matrix(int(p))
            if a is None: continue
            s = stats(a, expo_vec(e.zone, a.columns))
            for w in WINDOWS: acc[w].append((s[w]["diff"], s[w]["slope"]))
        PLAC[e.zone] = {w: np.array(v) for w, v in acc.items()}
    for w in WINDOWS:
        pd_, ps = PLAC[e.zone][w][:, 0], PLAC[e.zone][w][:, 1]
        r = st[w]
        rows.append(dict(event_id=e.event_id, label=e.label, src=e.src, t0=DATES[t0].date(), window=f"[{w[0]},{w[1]}]",
            n_high=r["n_high"], n_none=r["n_none"], car_high=r["mean_high"], car_none=r["mean_none"],
            diff=r["diff"], p_diff=np.mean(np.abs(pd_ - np.nanmean(pd_)) >= abs(r["diff"] - np.nanmean(pd_))),
            p_diff_onesided_neg=np.mean(pd_ <= r["diff"]),
            slope=r["slope"], p_slope=np.mean(np.abs(ps - np.nanmean(ps)) >= abs(r["slope"] - np.nanmean(ps))),
            placebo_sd_diff=np.nanstd(pd_), frac_neg_high=r["frac_neg_high"]))
    for f in ar.columns:
        d = dict(event_id=e.event_id, zone=e.zone, nse_symbol=f, share_cost=x[f], sector=co.sector.get(f), role=co.role.get(f))
        for lo, hi in WINDOWS: d[f"car_{lo}_{hi}".replace("-", "m")] = car(ar, lo, hi).get(f)
        cars.append(d)
    cum = ar.loc[-10:40].cumsum(); cum = cum - cum.loc[-1]
    paths[e.event_id] = (cum.loc[:, x >= 0.25].mean(axis=1), cum.loc[:, x == 0].mean(axis=1), e.label, (x >= .25).sum(), (x == 0).sum())

res = pd.DataFrame(rows); res.to_csv(TAB + "event_study_summary.csv", index=False)
cars = pd.DataFrame(cars); cars.to_csv(TAB + "event_study_firm_cars.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(res[["label", "t0", "window", "n_high", "n_none", "car_high", "car_none", "diff", "p_diff", "slope", "p_slope", "frac_neg_high"]].round(4).to_string())

# ---- pooled across the 8 distinct events (drop the pack's mis-dated GRAP-2024) --------------
use = EVENTS[EVENTS.event_id != "E_NCR_GRAP_2024"]
def pooled(t0s):
    o = {w: [] for w in WINDOWS}
    for (_, e), t0 in zip(use.iterrows(), t0s):
        a = ar_matrix(int(t0));
        if a is None: return None
        x = expo_vec(e.zone, a.columns)
        for w in WINDOWS:
            c = car(a, *w).dropna(); o[w].append(pd.DataFrame({"c": c - c.mean(), "x": x.reindex(c.index) - x.reindex(c.index).mean(), "hi": x.reindex(c.index) >= .25, "none": x.reindex(c.index) == 0, "raw": c}))
    r = {}
    for w in WINDOWS:
        d = pd.concat(o[w]); r[w] = ((d.c * d.x).sum() / (d.x ** 2).sum(), d.raw[d.hi].mean() - d.raw[d.none].mean())
    return r
act = pooled([t0_of(s) for s in use.start])
rng = np.random.default_rng(11); pl = []
for _ in range(600):
    r = pooled(rng.choice(PL, len(use)))
    if r: pl.append(r)
prow = []
for w in WINDOWS:
    s = np.array([p[w][0] for p in pl]); d = np.array([p[w][1] for p in pl])
    prow.append(dict(window=f"[{w[0]},{w[1]}]", pooled_slope_event_FE=act[w][0], p_slope=np.mean(np.abs(s - s.mean()) >= abs(act[w][0] - s.mean())),
                     pooled_diff_high_minus_none=act[w][1], p_diff=np.mean(np.abs(d - d.mean()) >= abs(act[w][1] - d.mean())), placebo_sd_diff=d.std()))
pp = pd.DataFrame(prow); pp.to_csv(TAB + "event_study_pooled.csv", index=False); print(pp.round(4).to_string())

# ---- figure: CAR paths ---------------------------------------------------------------------
fig, axs = plt.subplots(3, 3, figsize=(14, 9), sharex=True)
for ax, (k, (h, n, lab, nh, nn)) in zip(axs.ravel(), paths.items()):
    ax.axhline(0, color="#c9c8c2", lw=.8); ax.axvline(0, color=MUTED, lw=.8, ls=":")
    ax.plot(n.index, n * 100, color=BLUE, label=f"No assets in zone (n={nn})")
    ax.plot(h.index, h * 100, color=ORANGE, label=f"≥25% of assets in zone (n={nh})")
    ax.set_title(lab, loc="left"); ax.legend(fontsize=7.5, loc="best")
for ax in axs[2]: ax.set_xlabel("Trading days from event start")
for ax in axs[:, 0]: ax.set_ylabel("Cumulative abnormal return, %")
fig.suptitle("Stock reaction of asset-exposed vs unexposed firms (market-model CAR vs NIFTY 500, rebased at day −1)", x=0.01, ha="left", fontweight="bold")
fig.tight_layout(); fig.savefig(FIG + "01_car_paths.png", dpi=200)
