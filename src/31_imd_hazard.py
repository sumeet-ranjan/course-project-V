"""Step 3: rebuild the rainfall triggers with the official IMD gridded rainfall instead of NASA POWER.

Source: India Meteorological Department, Pune - daily gridded rainfall 0.25 x 0.25 degree (gauge
based), yearly binary files (135 x 129 grid from 6.5N 66.5E, float32 mm, -999 = no data), downloaded
from https://www.imdpune.gov.in/cmpg/Griddata/Rainfall_25_Bin.html (POST rain=<year> to rainfall.php).
NASA POWER (used so far) is a reanalysis on a ~0.5 x 0.625 degree grid; IMD is interpolated from
rain gauges at 0.25 degree, so it is the official and finer series.
Exactly the same rules as 04_hazard_panel.py: each district's series at the IMD cell nearest its
plant centroid (nearest cell with data if the centroid falls on a coastal no-data cell); 3-day
totals; 5-year return level from the 2000-2019 annual maxima; episodes from Nov 2020 when the 3-day
total exceeds it, more than 30 days apart; firm-episodes and same-date unexposed benchmark as in 04.
Outputs: external/rain_imd_daily.csv.gz, outputs/tables/imd_*.csv, figs/15_imd_vs_nasa.png
Usage: python3 src/31_imd_hazard.py
"""
import os, sys, glob; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from es_lib import *
import statsmodels.formula.api as smf
RAW = EXT + "imd_raw/"
LAT = 6.5 + 0.25 * np.arange(129); LON = 66.5 + 0.25 * np.arange(135)
cen = pd.read_csv(EXT + "district_centroids.csv")

def series():
    fn = EXT + "rain_imd_daily.csv.gz"
    if os.path.exists(fn): return pd.read_csv(fn, parse_dates=["date"])
    files = sorted(glob.glob(RAW + "ind*_rfp25.grd")); out = []
    cells = None
    for f in files:
        yr = int(os.path.basename(f)[3:7])
        a = np.fromfile(f, dtype="<f4"); nd = a.size // (129 * 135); a = a.reshape(nd, 129, 135)
        if cells is None:                                         # nearest cell with data for each district
            valid = (a > -900).mean(axis=0) > 0.9
            jj, ii = np.nonzero(valid); cells = []
            for la, lo in zip(cen.lat, cen.lon):
                k = np.argmin((LAT[jj] - la) ** 2 + (LON[ii] - lo) ** 2); cells.append((jj[k], ii[k], np.hypot(LAT[jj[k]] - la, LON[ii[k]] - lo)))
        dates = pd.date_range(f"{yr}-01-01", periods=nd)
        for (j, i, dist), dn in zip(cells, cen.dist_name):
            out.append(pd.DataFrame({"date": dates, "dist_name": dn, "mm": a[:, j, i]}))
        print(yr, nd, "days", flush=True)
    r = pd.concat(out); r = r[r.mm > -900]
    r.to_csv(fn, index=False)
    far = sum(1 for c in cells if c[2] > 0.18); print("districts whose nearest IMD cell is > 0.18 degree away:", far)
    return r

rain = series().sort_values(["dist_name", "date"])
END = rain.date.max()
rain["r3"] = rain.groupby("dist_name").mm.transform(lambda s: s.rolling(3, min_periods=1).sum())
base = rain[rain.date.dt.year <= 2019]
amax = base.groupby(["dist_name", base.date.dt.year]).r3.max().unstack()
thr = pd.DataFrame({"rl5": amax.quantile(0.8, axis=1), "rl2": amax.quantile(0.5, axis=1)})
rain = rain.merge(thr, left_on="dist_name", right_index=True); rain["sev"] = rain.r3 / rain.rl5

# ---- validation on the named events, IMD next to NASA
nasa = pd.read_csv(EXT + "rain_daily.csv.gz", parse_dates=["date"]).sort_values(["dist_name", "date"])
nasa["r3"] = nasa.groupby("dist_name").mm.transform(lambda s: s.rolling(3, min_periods=1).sum())
nb = nasa[nasa.date.dt.year <= 2019]; nam = nb.groupby(["dist_name", nb.date.dt.year]).r3.max().unstack()
nasa = nasa.merge(nam.quantile(0.8, axis=1).rename("rl5"), left_on="dist_name", right_index=True); nasa["sev"] = nasa.r3 / nasa.rl5
val = []
for ev, dists, a, b in [("Gujarat flood 2024", ["Vadodara", "Bharuch", "Anand", "Kheda"], "2024-08-24", "2024-09-05"),
                        ("Gujarat flood 2023", ["Bharuch", "Vadodara", "Narmada"], "2023-09-15", "2023-09-22"),
                        ("Himachal flood 2023", ["Solan", "Shimla", "Kullu", "Una", "Sirmaur"], "2023-07-07", "2023-07-25"),
                        ("Chennai Michaung 2023", ["Chennai", "Kancheepuram", "Thiruvallur"], "2023-12-02", "2023-12-12")]:
    for d in dists:
        x = rain[(rain.dist_name == d) & rain.date.between(a, b)]; y = nasa[(nasa.dist_name == d) & nasa.date.between(a, b)]
        if len(x) == 0: continue
        px, py = x.loc[x.r3.idxmax()], y.loc[y.r3.idxmax()] if len(y) else None
        val.append(dict(event=ev, district=d, imd_peak_date=px.date.date(), imd_peak_3day_mm=px.r3, imd_5yr_level_mm=px.rl5, imd_ratio=px.sev,
                        nasa_peak_date=py.date.date() if py is not None else None, nasa_peak_3day_mm=py.r3 if py is not None else np.nan,
                        nasa_ratio=py.sev if py is not None else np.nan))
val = pd.DataFrame(val); val.round(2).to_csv(TAB + "imd_validation_named_events.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print("IMD rainfall to", END.date()); print("=== named events: peak 3-day rain, IMD vs NASA POWER ==="); print(val.round(2).to_string(index=False))

# ---- episodes, IMD, and agreement with NASA
def episodes(df, start="2020-11-01", end=None):
    r = df[(df.date >= start) & (df.sev >= 1)]
    if end is not None: r = r[r.date <= end]
    r = r.copy(); r["gap"] = r.groupby("dist_name").date.diff().dt.days.fillna(999); r["ep"] = (r.gap > 30).groupby(r.dist_name).cumsum()
    return r.groupby(["dist_name", "ep"]).agg(start=("date", "min"), peak_sev=("sev", "max"), peak_mm=("r3", "max")).reset_index()
ep = episodes(rain, end=END); epn = episodes(nasa, end=END)
ep.to_csv(TAB + "imd_extreme_episodes_by_district.csv", index=False)
def matched(a, b, tol=3):
    m = a.merge(b[["dist_name", "start"]], on="dist_name", how="left", suffixes=("", "_o"))
    m["hit"] = (m.start - m.start_o).abs().dt.days <= tol
    return m.groupby(["dist_name", "start"]).hit.any()
agree = dict(imd_episodes=len(ep), nasa_episodes=len(epn), imd_matched_by_nasa_within_3d=matched(ep, epn).mean(), nasa_matched_by_imd_within_3d=matched(epn, ep).mean(),
             district_count_spearman=pd.concat([ep.groupby("dist_name").size().rename("imd"), epn.groupby("dist_name").size().rename("nasa")], axis=1).fillna(0).corr(method="spearman").iloc[0, 1])
print("\n=== IMD vs NASA extreme-rain episodes, Nov 2020 - end ==="); print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in agree.items()})

# ---- firm-episodes and event study with IMD triggers
p = plants(); tot = p.groupby("nse_symbol").project_cost_cr.sum()
pe = p.merge(ep, on="dist_name"); pe["wk"] = pe.start.dt.to_period("W")
fe = pe.groupby(["nse_symbol", "wk"]).agg(start=("start", "min"), hit_cost=("project_cost_cr", "sum"), n_plants_hit=("lat", "size"),
        sev=("peak_sev", "max"), districts=("dist_name", lambda s: "|".join(sorted(set(s))[:5]))).reset_index()
fe["share"] = fe.hit_cost / fe.nse_symbol.map(tot); fe = fe[fe.nse_symbol.isin(R.columns)]
def firm_cars(firm, date):
    ar = ar_matrix(t0_of(date), pre=1, post=25)
    if ar is None or firm not in ar: return None
    hit = set(fe.nse_symbol[(fe.start - pd.Timestamp(date)).abs().dt.days <= 10]); un = [c for c in ar.columns if c not in hit]
    o = {f"car_0_{h}": ar[firm].loc[0:h].sum() for h in (5, 10, 20)}
    o.update({f"adj_0_{h}": ar[firm].loc[0:h].sum() - ar[un].loc[0:h].sum().mean() for h in (5, 10, 20)}); return o
rows = []
for _, x in fe[fe.share >= 0.02].iterrows():
    c = firm_cars(x.nse_symbol, x.start)
    if c: rows.append({**x.drop("wk").to_dict(), **c})
es = pd.DataFrame(rows); es["wk"] = es.start.dt.to_period("W").astype(str); es.to_csv(TAB + "imd_firm_episode_cars.csv", index=False)
nes = pd.read_csv(TAB + "rain_firm_episode_cars.csv", parse_dates=["start"]); nes["wk"] = nes.start.dt.to_period("W").astype(str)
S = []
for src, d in (("IMD", es), ("NASA POWER", nes)):
    for lab, m in (("share 2-10%", (d.share < .10)), ("share 10-25%", (d.share >= .10) & (d.share < .25)), ("share >=25%", d.share >= .25),
                   ("share >=25% & severity >=1.5", (d.share >= .25) & (d.sev >= 1.5))):
        x = d[m]
        for h in (5, 10, 20):
            g = x.groupby("wk")[f"adj_0_{h}"].mean()
            S.append(dict(source=src, bucket=lab, window=f"[0,{h}]", n=len(x), weeks=x.wk.nunique(), mean_adj=x[f"adj_0_{h}"].mean(), median_adj=x[f"adj_0_{h}"].median(),
                          t_week_clustered=g.mean() / (g.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan))
    for h in (5, 10, 20):
        mm = smf.ols(f"adj_0_{h} ~ share", d).fit(cov_type="cluster", cov_kwds={"groups": d.wk.astype("category").cat.codes})
        S.append(dict(source=src, bucket="elasticity per 100% of assets", window=f"[0,{h}]", n=int(mm.nobs), weeks=d.wk.nunique(), mean_adj=mm.params["share"],
                      median_adj=np.nan, t_week_clustered=mm.tvalues["share"]))
S = pd.DataFrame(S); S.round(4).to_csv(TAB + "imd_event_study_vs_nasa.csv", index=False)
print("\n=== firm-episode event study: IMD triggers vs NASA POWER triggers (CAR minus same-date unexposed) ===")
print(S.pivot_table(index=["bucket", "window"], columns="source", values=["n", "mean_adj", "t_week_clustered"]).round(3).to_string())

# ---- figure
fig, axs = plt.subplots(1, 4, figsize=(16, 4.4), gridspec_kw={"width_ratios": [1, 1, 1, 1.5]})
for ax, (d_, a, b, lab) in zip(axs[:3], (("Chennai", "2023-11-25", "2023-12-15", "Chennai, Dec 2023"), ("Vadodara", "2024-08-15", "2024-09-05", "Vadodara, Aug 2024"),
                                          ("Bharuch", "2023-09-08", "2023-09-25", "Bharuch, Sep 2023 (dam release)"))):
    x = rain[(rain.dist_name == d_) & rain.date.between(a, b)]; y = nasa[(nasa.dist_name == d_) & nasa.date.between(a, b)]
    ax.plot(x.date, x.sev, color=BLUE, lw=2, label="IMD 0.25° grid"); ax.plot(y.date, y.sev, color="#8b8a84", lw=1.4, ls="--", label="NASA POWER")
    ax.axhline(1, color=ORANGE, lw=1, ls=":"); ax.set_ylim(0, 2.0); ax.tick_params(axis="x", labelrotation=30, labelsize=7)
    ax.set_title(lab, loc="left")
axs[0].set_ylabel("3-day rain ÷ district's 5-year level"); axs[0].legend(fontsize=7.5, loc="upper left")
axs[1].text(0.02, 0.95, "dotted = 5-year level", transform=axs[1].transAxes, fontsize=7.5, color=MUTED, va="top")
ax = axs[3]
for d, col, lab in ((es, BLUE, "IMD triggers"), (nes, "#8b8a84", "NASA POWER triggers")):
    b = pd.cut(d.share, [0.02, .05, .1, .25, .5, 1.01]); g = d.groupby(b, observed=True).agg(x=("share", "mean"), y=("adj_0_10", "mean"))
    ax.plot(g.x * 100, g.y * 100, color=col, marker="o", ms=6, label=f"{lab} (n={len(d)})")
ax.axhline(0, color="#c9c8c2", lw=.8); ax.set_xlabel("Share of plant cost in extreme-rain districts, %"); ax.set_ylabel("CAR days 0–10 minus unexposed, % (bin means)")
ax.set_title("Stock reaction by exposure, Nov 2020–Dec 2025", loc="left"); ax.legend(fontsize=8)
fig.suptitle("Rainfall triggers rebuilt on the official IMD 0.25° grid", x=0.01, ha="left", fontweight="bold")
fig.tight_layout(); fig.savefig(FIG + "15_imd_vs_nasa.png", dpi=200)
