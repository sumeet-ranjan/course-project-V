"""Night-time lights at the plants: did they go dark after each event, and for how long?

Input: external/ntl_plant_daily.csv.gz (from 14_ntl_extract.py).
A plant-night is "clean" if >= 5 of its 9 pixels have a high-quality retrieval AND >= 80% of the
~10 km block around it is clear (cloud-edge retrievals read low). A plant is "lit" if its baseline
radiance is >= 5 nW/cm2/sr. `ratio` = tonight / the same pixels' own normal (1 = normal).

Groups for each event (same satellite tiles, same nights):
  zone = plants in the corrected district footprint (common.ZONES)
  far  = plants more than FAR_KM from the zone centre (for Chennai also excluding the Andhra coast,
         where Michaung made landfall): the same-night benchmark
Per plant: ratio on its first clean night in the early window; dark = ratio_first < DARK (0.6);
dim = 1 - ratio_first / far-control median that night, clipped to [0, 1].
What a reading means: outdoor and street lighting at about 01:50 local time over ~1.4 km. Dark =
the site AND its surroundings had no power that night. It is not a production measure.
Outputs: outputs/tables/ntl_*.csv, outputs/figs/06_ntl_subareas.png, 07_ntl_plant_maps.png
"""
import numpy as np, pandas as pd
from es_lib import *

DARK = 0.6
EV = {  # event -> (zone, centre lat, lon, far km, early window, label)
    "E_CHE_FLOOD_2023": ("CHE", 13.0, 80.2, 250, (0, 4), "Chennai, Cyclone Michaung (rain 3-4 Dec 2023)"),
    "E_GJ_FLOOD_2024":  ("GJ",  22.0, 73.0, 300, (0, 6), "Gujarat flood (rain 25-28 Aug 2024)"),
    "E_GJ_FLOOD_2023":  ("GJ",  22.0, 73.0, 300, (0, 6), "Gujarat, Narmada flood (17-18 Sep 2023)"),
}
SUB = {  # named sub-areas inside the zones (lat0, lat1, lon0, lon1)
    "CHE": {"Chennai city": (12.90, 13.20, 80.15, 80.30), "Manali-Ennore": (13.14, 13.30, 80.24, 80.36),
            "Sriperumbudur-Oragadam": (12.78, 13.02, 79.78, 80.05)},
    "GJ": {"Vadodara": (22.20, 22.45, 73.05, 73.30), "Bharuch-Ankleshwar-Jhagadia": (21.55, 21.80, 72.90, 73.20),
           "Dahej-Vilayat": (21.60, 21.92, 72.45, 72.75)},
}
ZBOX = {"CHE": (12.0, 13.7, 79.3, 80.5), "GJ": (20.3, 23.2, 72.3, 74.6)}   # plausible coordinate box for each zone
def km(lat, lon, la0, lo0):
    p = np.pi / 180
    a = np.sin((lat - la0) * p / 2) ** 2 + np.cos(lat * p) * np.cos(la0 * p) * np.sin((lon - lo0) * p / 2) ** 2
    return 2 * 6371 * np.arcsin(np.sqrt(a))

P = plants().reset_index().rename(columns={"index": "plant_id"})
P["plant_share"] = P.project_cost_cr / P.groupby("nse_symbol").project_cost_cr.transform("sum").replace(0, np.nan)
D = pd.read_csv(EXT + "ntl_plant_daily.csv.gz", parse_dates=["night_ist"]).merge(
    P[["plant_id", "lat", "lon", "dist_name", "industry_name", "plant_share"]], on="plant_id")
plant_rows, sub_rows, cov_rows = [], [], []
for ev, (zone, la0, lo0, far_km, early, label) in EV.items():
    d = D[D.event_id == ev].copy()
    d["group"] = np.where(d.dist_name.isin(ZONES[zone]), "zone", np.where(km(d.lat, d.lon, la0, lo0) > far_km, "far", "ring"))
    if zone == "CHE":
        d.loc[(d.group == "far") & d.lat.between(13.5, 17.5) & (d.lon > 79.0), "group"] = "ring"
    d["sub"] = "other"
    for nm, (a0, a1, b0, b1) in SUB[zone].items():
        d.loc[(d.group == "zone") & d.lat.between(a0, a1) & d.lon.between(b0, b1), "sub"] = nm
    # a few zone plants carry coordinates far outside their stated district (e.g. Petronet's largest
    # "Bharuch" entry sits across the Gulf of Khambhat): their reading is not the plant's, so drop them
    la_a, la_b, lo_a, lo_b = ZBOX[zone]
    bad = (d.group == "zone") & ~(d.lat.between(la_a, la_b) & d.lon.between(lo_a, lo_b))
    d.loc[bad, "base"] = np.nan
    lit = d[d.base >= 5]
    ok = lit[(lit.n_valid >= 5) & (lit.clear_10km >= 0.8) & lit.ratio.notna()].copy()
    far = ok[ok.group == "far"].groupby("rel_day").ratio.agg(["median", "size"])
    ok["far_med"] = ok.rel_day.map(far["median"].where(far["size"] >= 10))
    # coverage of the zone by night: how many lit zone plants had a clean reading
    nz = lit[lit.group == "zone"].plant_id.nunique()
    for rd in range(-30, 31):
        g = ok[(ok.group == "zone") & (ok.rel_day == rd)]
        cov_rows.append(dict(event_id=ev, rel_day=rd, zone_lit_plants=nz, clean_readings=len(g), coverage=len(g) / nz,
                             zone_median=g.ratio.median() if len(g) >= 10 else np.nan,
                             far_median=far["median"].get(rd, np.nan) if far["size"].get(rd, 0) >= 10 else np.nan))
    # sub-area x night medians (only nights when >= 60% of the sub-area's lit plants are clean)
    for nm in SUB[zone]:
        n_sub = lit[lit["sub"] == nm].plant_id.nunique()
        for rd, g in ok[ok["sub"] == nm].groupby("rel_day"):
            if len(g) / n_sub >= 0.6:
                sub_rows.append(dict(event_id=ev, sub_area=nm, rel_day=rd, night_ist=g.night_ist.iloc[0].date(), lit_plants=n_sub,
                                     clean_readings=len(g), median_ratio=g.ratio.median(), share_below_0_6=(g.ratio < DARK).mean(),
                                     far_median=g.far_med.iloc[0]))
    # per plant
    e = ok[ok.rel_day.between(*early)].sort_values("rel_day")
    late = ok[ok.rel_day.between(8, 14)]
    for pid, g in d[d.group == "zone"].groupby("plant_id"):
        r0 = g.iloc[0]; ge = e[e.plant_id == pid]; gl = late[late.plant_id == pid]
        first = ge.iloc[0] if len(ge) else None
        plant_rows.append(dict(event_id=ev, plant_id=pid, nse_symbol=r0.nse_symbol, sub_area=r0["sub"], dist_name=r0.dist_name,
            lat=r0.lat, lon=r0.lon, industry=r0.industry_name, plant_share=r0.plant_share, base_radiance=r0.base,
            lit=bool(r0.base >= 5), observed=first is not None,
            first_clean_night=first.night_ist.date() if first is not None else None,
            first_clean_rel_day=first.rel_day if first is not None else np.nan,
            ratio_first=first.ratio if first is not None else np.nan,
            dim=float(np.clip(1 - first.ratio / first.far_med, 0, 1)) if first is not None and np.isfinite(first.far_med) else np.nan,
            dark=bool(first.ratio < DARK) if first is not None else np.nan,
            ratio_min_early=ge.ratio.min() if len(ge) else np.nan, clean_nights_early=len(ge),
            ratio_days_8_14=gl.ratio.median() if len(gl) else np.nan,
            first_night_back_above_0_8=(ok[(ok.plant_id == pid) & (ok.rel_day >= 0) & (ok.ratio >= 0.8)].rel_day.min()
                                        if first is not None and first.ratio < DARK else np.nan)))
pl = pd.DataFrame(plant_rows); sb = pd.DataFrame(sub_rows); cv = pd.DataFrame(cov_rows)
pl.round(3).to_csv(TAB + "ntl_plant_event.csv", index=False)
sb.round(3).to_csv(TAB + "ntl_subarea_nights.csv", index=False)
cv.round(3).to_csv(TAB + "ntl_zone_coverage_by_night.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)

# ---- event nights against ordinary nights, per sub-area
summ = []
for (ev, nm), g in sb.groupby(["event_id", "sub_area"]):
    early = EV[ev][4]
    en = g[g.rel_day.between(0, 7)]; on = g[(g.rel_day <= -2) | (g.rel_day >= 8)]
    summ.append(dict(event_id=ev, sub_area=nm, lit_plants=g.lit_plants.iloc[0],
        event_nights=" ".join(f"{pd.Timestamp(r.night_ist):%d%b}:{r.median_ratio:.2f}" for r in en.itertuples()) or "none (cloud)",
        lowest_event_night=en.median_ratio.min() if len(en) else np.nan, ordinary_nights=len(on),
        ordinary_min=on.median_ratio.min(), ordinary_p10=on.median_ratio.quantile(.1), ordinary_median=on.median_ratio.median(),
        event_nights_below_all_ordinary=int((en.median_ratio < on.median_ratio.min()).sum()) if len(en) else 0))
summ = pd.DataFrame(summ); summ.round(3).to_csv(TAB + "ntl_subarea_summary.csv", index=False)
print("=== sub-area median light ratio: event nights (rel day 0-7) vs ordinary nights ==="); print(summ.round(2).to_string(index=False))
print("\n=== zone coverage on the first nights after each event (clean readings / lit zone plants) ===")
print(cv[cv.rel_day.between(-1, 12)].pivot(index="rel_day", columns="event_id", values="coverage").round(2).to_string())

# ---- firm level: plant-cost-weighted shares
z = pl.assign(w=pl.plant_share.fillna(0))
fi = z.groupby(["event_id", "nse_symbol"]).apply(lambda t: pd.Series(dict(
    zone_plants=len(t), share_zone=t.w.sum(), share_observed=t.w[t.observed].sum(),
    share_dark=t.w[t.dark == True].sum(), share_dim=(t.w * t.dim.fillna(0)).sum(),   # noqa: E712
    plants_observed=int(t.observed.sum()), plants_dark=int((t.dark == True).sum()),   # noqa: E712
    median_ratio_first=t.ratio_first.median())), include_groups=False).reset_index()
fi["traded"] = fi.nse_symbol.isin(R.columns)
fi.round(4).to_csv(TAB + "ntl_firm_event.csv", index=False)
print("\n=== firms with >= 10% of plant cost in the zone ===")
print(fi[fi.share_zone >= .10].sort_values(["event_id", "share_zone"], ascending=[True, False]).round(3).to_string(index=False))
tot = pl.groupby("event_id").agg(zone_plants=("plant_id", "size"), lit=("lit", "sum"), observed=("observed", "sum"),
                                 dark=("dark", lambda s: (s == True).sum()))   # noqa: E712
tot["dark_share_of_observed"] = tot.dark / tot.observed
print("\n=== zone plants: lit / observed on a clean night in the early window / dark (< 0.6 of normal) ==="); print(tot.round(2).to_string())

# ---- figure 06: sub-area series
fig, axs = plt.subplots(1, 3, figsize=(15.5, 5.6), sharey=True)
COL = [BLUE, ORANGE, AQUA]
for ax, (ev, (zone, la0, lo0, far_km, early, label)) in zip(axs, EV.items()):
    ax.axhline(1, color="#c9c8c2", lw=.9)
    c = cv[cv.event_id == ev].set_index("rel_day").coverage
    blocked = [rd for rd in range(-2, 12) if c.get(rd, 0) < 0.3]
    for rd in blocked: ax.axvspan(rd - .5, rd + .5, color="#eeede8", lw=0)
    ax.axvline(0, color=MUTED, lw=.8, ls=":")
    for col, nm in zip(COL, SUB[zone]):
        g = sb[(sb.event_id == ev) & (sb.sub_area == nm)].sort_values("rel_day")
        seg = (g.rel_day.diff() > 4).cumsum()                     # do not join readings more than 4 nights apart
        for k, (_, h) in enumerate(g.groupby(seg)):
            ax.plot(h.rel_day, h.median_ratio, color=col, lw=1.6, marker="o", ms=5.5, mec=SURF, mew=1.2,
                    label=f"{nm} ({g.lit_plants.iloc[0]} sites)" if k == 0 else None)
    ax.set_title(label, loc="left"); ax.set_xlim(-30.5, 30.5); ax.set_ylim(0.2, 1.6)
    ax.set_xlabel("Days from event start (night of ~01:50 local time)")
    ax.legend(fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=1, title="Median of sites; nights with ≥60% of sites clear", title_fontsize=7)
    ax.text(0.99, 0.97, "grey = cloud, no reading", transform=ax.transAxes, ha="right", va="top", fontsize=7.5, color=MUTED)
axs[0].set_ylabel("Night-time radiance ÷ site's own normal")
fig.suptitle("Night-time lights at plant sites around each event (NASA Black Marble VNP46A2; 1 = normal)", x=0.01, ha="left", fontweight="bold")
fig.tight_layout(); fig.savefig(FIG + "06_ntl_subareas.png", dpi=200); plt.close(fig)

# ---- figure 07: plant maps for the two events with a readable first night
fig, axs = plt.subplots(1, 2, figsize=(13.5, 6.2))
for ax, ev, box in ((axs[0], "E_CHE_FLOOD_2023", (79.62, 80.42, 12.60, 13.48)), (axs[1], "E_GJ_FLOOD_2024", (72.35, 73.65, 21.45, 22.65))):
    g = pl[(pl.event_id == ev) & pl.lon.between(box[0], box[1]) & pl.lat.between(box[2], box[3])]
    un = g[~g.observed]; dk = g[g.dark == True]; nm_ = g[g.dark == False]   # noqa: E712
    ax.scatter(un.lon, un.lat, s=26, facecolors="none", edgecolors="#a3a29b", lw=.9, label=f"No clean reading or unlit ({len(un)})", zorder=2)
    ax.scatter(nm_.lon, nm_.lat, s=34, color=BLUE, edgecolors=SURF, lw=.8, label=f"≥ 60% of normal ({len(nm_)})", zorder=3)
    ax.scatter(dk.lon, dk.lat, s=44, color=ORANGE, marker="s", edgecolors=SURF, lw=.8, label=f"Dark: < 60% of normal ({len(dk)})", zorder=4)
    for nm, (a0, a1, b0, b1) in SUB[EV[ev][0]].items():
        ax.add_patch(plt.Rectangle((b0, a0), b1 - b0, a1 - a0, fill=False, ec="#8b8a84", lw=.8, ls="--", zorder=1))
        ax.text(b0 + .005, a1 + .008, nm, fontsize=7.5, color=MUTED, va="bottom")
    nights = sorted(g.first_clean_night.dropna().unique())
    ax.set_title(f"{EV[ev][5]}\nfirst clean night per site: {nights[0]} to {nights[-1]}", loc="left")
    ax.set_xlim(box[0], box[1]); ax.set_ylim(box[2], box[3]); ax.set_aspect(1 / np.cos(np.deg2rad((box[2] + box[3]) / 2)))
    ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude"); ax.legend(fontsize=8, loc="lower right" if ev == "E_CHE_FLOOD_2023" else "upper left")
fig.suptitle("Which plant sites were dark on the first clear night after the event", x=0.01, ha="left", fontweight="bold")
fig.tight_layout(); fig.savefig(FIG + "07_ntl_plant_maps.png", dpi=200); plt.close(fig)
