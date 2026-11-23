"""Night lights for the most severe rain episodes (plant-level hits for the hazard panel, Step 1b).

Cheaper design than 14_ntl_extract.py, so that ~65 episode-weeks fit in one run:
  * daily VNP46A2 tiles only for the first 11 nights after each episode start (nights 0..10);
  * baseline = the same pixels in NASA's ANNUAL cloud-free composite (VNP46A4, "AllAngle_Composite_
    Snow_Free") of the previous calendar year, so no pre-event daily tiles are needed;
  * same-night normalisation: each night, every plant's ratio (tonight / annual baseline) is divided
    by the median ratio of CONTROL plants in the same tile(s) that night. Controls are lit plants
    more than 200 km from any hit plant, in districts with no extreme-rain episode within 10 days.
    This removes tile-wide effects (moon, atmosphere, season, the annual-composite level).
  * a plant-night counts only if >= 5 of its 9 pixels have a high-quality retrieval and >= 80% of the
    surrounding ~10 km is clear (as in 14_...); a plant is lit if its baseline is >= 5 nW/cm2/sr.
  * "dark" = first clean night (nights 0-7) below 0.6 of the control-normalised baseline; the false
    -alarm rate is measured on the controls on the same nights.
Episodes: every week with a firm-episode where >= 10% of a traded firm's plant cost sat in an
extreme-rain district (27_out_of_sample.py's episode list, Nov 2020 - Sep 2026). The Chennai Dec 2023
and Gujarat Aug 2024 weeks are included to validate this design against the full method of 14/15.
Raw tiles are deleted after each episode. Stage 1 caches one file per week in external/ntl_ep_cache/.
Outputs: external/ntl_episode_plant_nights.csv.gz, outputs/tables/ntl_episode_*.csv, figs/13_ntl_episodes.png
Usage: python3 src/25_ntl_episodes.py [fetch] [analyse]
"""
import os, sys, re, json, glob, shutil, subprocess, urllib.request, urllib.parse, warnings, datetime as dt
from concurrent.futures import ThreadPoolExecutor
import numpy as np, pandas as pd, h5py
from scipy.ndimage import uniform_filter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
warnings.filterwarnings("ignore", category=RuntimeWarning)
RAW, ANN, CACHE = EXT + "ntl_ep_raw/daily/", EXT + "ntl_ep_raw/annual/", EXT + "ntl_ep_cache/"
for d_ in (RAW, ANN, CACHE): os.makedirs(d_, exist_ok=True)
G = "HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/"
NIGHTS = range(0, 11); MIN_SHARE = 0.10

def km(lat, lon, la0, lo0):
    p = np.pi / 180
    a = np.sin((lat - la0) * p / 2) ** 2 + np.cos(lat * p) * np.cos(la0 * p) * np.sin((lon - lo0) * p / 2) ** 2
    return 2 * 6371 * np.arcsin(np.sqrt(a))

def tile_of(lat, lon): return f"h{int(np.floor((lon + 180) / 10)):02d}v{int(np.floor((90 - lat) / 10)):02d}"

_CMR = {}
def cmr(short, tile, t0, t1):
    """Granule URLs by acquisition key (YYYYDDD). Queries by the tile's centre point (fast) rather than a
    file-name wildcard (slow), and caches one query per product, tile and year."""
    h, v = int(tile[1:3]), int(tile[4:6]); lon, lat = -180 + 10 * h + 5, 90 - 10 * v - 5
    out = {}
    for yr in range(pd.Timestamp(t0).year, pd.Timestamp(t1).year + 1):
        key = (short, tile, yr)
        if key not in _CMR:
            q = {"short_name": short, "version": "2", "temporal": f"{yr}-01-01T00:00:00Z,{yr}-12-31T23:59:59Z", "point": f"{lon},{lat}", "page_size": "2000"}
            for attempt in range(5):
                try:
                    d = json.load(urllib.request.urlopen("https://cmr.earthdata.nasa.gov/search/granules.json?" + urllib.parse.urlencode(q), timeout=120)); break
                except Exception:
                    if attempt == 4: raise
                    subprocess.run(["sleep", str(10 * (attempt + 1))])
            got = {}
            for e in d["feed"]["entry"]:
                for l in e["links"]:
                    hr = l["href"]
                    if hr.startswith("https://data.laadsdaac") and hr.endswith(".h5") and f".{tile}." in hr:
                        got[re.search(r"\.A(\d{7})\.", hr).group(1)] = hr
            _CMR[key] = got
        out.update(_CMR[key])
    return out

def fetch(url, dest_dir, jar):
    fn = dest_dir + os.path.basename(url); part = fn + f".part{os.getpid()}"
    if os.path.exists(fn) and os.path.getsize(fn) > 1_000_000: return fn
    for attempt in range(4):
        r = subprocess.run(["curl", "-sS", "-L", "--netrc-optional", "-m", "900", "-c", jar, "-b", jar, "-o", part, "-w", "%{http_code}", url],
                           capture_output=True, text=True)
        if r.stdout.strip() == "200" and os.path.exists(part):
            with open(part, "rb") as f:
                if f.read(8) == b"\x89HDF\r\n\x1a\n": os.replace(part, fn); return fn
        subprocess.run(["sleep", str(5 * (attempt + 1))])
    return None

def episodes():
    es = pd.read_csv(TAB + "oos_firm_episode_cars.csv", parse_dates=["start"])
    ep = pd.read_csv(TAB + "oos_district_episodes.csv", parse_dates=["start"]); ep["wk"] = ep.start.dt.to_period("W").astype(str)
    sel = es[es.share >= MIN_SHARE].groupby("wk").agg(sev=("sev", "max"), n=("share", "size")).sort_values("sev", ascending=False)
    return es, ep, sel

def stage1(only=None):
    es, ep, sel = episodes()
    if only: sel = sel[sel.index.isin(only)]
    P = plants().reset_index().rename(columns={"index": "plant_id"})
    cen = P.groupby("dist_name")[["lat", "lon"]].median()
    P["coord_ok"] = km(P.lat, P.lon, P.dist_name.map(cen.lat), P.dist_name.map(cen.lon)) <= 100
    P["tile"] = [tile_of(a, b) for a, b in zip(P.lat, P.lon)]
    top = 90 - 10 * P.tile.str[4:6].astype(int); left = -180 + 10 * P.tile.str[1:3].astype(int)
    P["r"] = np.clip(np.floor((top - P.lat) * 240).astype(int), 0, 2399); P["c"] = np.clip(np.floor((P.lon - left) * 240).astype(int), 0, 2399)
    OFF = np.array([(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1)])
    for wk, row in sel.iterrows():
        out_fn = CACHE + wk.replace("/", "_") + ".csv.gz"
        if os.path.exists(out_fn): continue
        try:                                   # one worker per week (several workers can run in parallel)
            os.close(os.open(out_fn + ".lock", os.O_CREAT | os.O_EXCL))
        except FileExistsError:
            continue
        raw = RAW + f"{os.getpid()}/"; os.makedirs(raw, exist_ok=True)
        e = ep[ep.wk == wk]; start = e.start.min().normalize(); hit_d = set(e.dist_name)
        near = set(ep[(ep.start - start).abs().dt.days <= 10].dist_name)
        hit = P[P.dist_name.isin(hit_d) & P.coord_ok]
        if hit.empty: continue
        tiles = sorted(hit.tile.unique())
        cand = P[P.tile.isin(tiles) & ~P.dist_name.isin(near) & P.coord_ok].copy()
        dmin = np.min([km(cand.lat.values, cand.lon.values, a, b) for a, b in zip(hit.lat.values, hit.lon.values)], axis=0) if len(cand) else []
        ctrl = cand[np.asarray(dmin) > 200]
        Q = pd.concat([hit.assign(role="hit"), ctrl.assign(role="control")])
        rows = []
        for t in tiles:
            q = Q[Q.tile == t]
            yr = start.year - 1
            ann = cmr("VNP46A4", t, f"{yr}-06-01", f"{yr}-06-02")
            a_url = ann.get(f"{yr}001")
            a_fn = fetch(a_url, ANN, ANN + f".jar{os.getpid()}.txt") if a_url else None
            if a_fn is None: print(wk, t, "no annual composite"); continue
            with h5py.File(a_fn, "r") as f: base = f[G + "AllAngle_Composite_Snow_Free"][()]
            base = np.where(base > -900, base, np.nan)
            d0, d1 = (start - pd.Timedelta(days=1)).date(), (start + pd.Timedelta(days=max(NIGHTS) - 1)).date()
            daily = cmr("VNP46A2", t, d0, d1)
            urls = []
            for k in NIGHTS:
                fd = (start + pd.Timedelta(days=k - 1)).date(); key = f"{fd.year}{fd.timetuple().tm_yday:03d}"
                if key in daily: urls.append((k, daily[key]))
            with ThreadPoolExecutor(6) as ex:
                files = dict(zip([k for k, _ in urls], ex.map(lambda ku: fetch(ku[1], raw, raw + f".jar{ku[0]}.txt"), urls)))
            rr = np.clip(q.r.values[:, None] + OFF[None, :, 0], 0, 2399); cc = np.clip(q.c.values[:, None] + OFF[None, :, 1], 0, 2399)
            B = base[rr, cc]; bmean = np.nanmean(B, axis=1)
            for k, fn in files.items():
                if fn is None: continue
                with h5py.File(fn, "r") as f:
                    g = f[G]; ntl = g["DNB_BRDF-Corrected_NTL"][()]; mq = g["Mandatory_Quality_Flag"][()]; cm = g["QF_Cloud_Mask"][()]
                good = (ntl > -900) & (mq == 0); land = ((cm >> 1) & 7) != 3
                clr = uniform_filter(good.astype(np.float32), 21, mode="nearest") / np.maximum(uniform_filter(land.astype(np.float32), 21, mode="nearest"), 1e-3)
                X = np.where(good[rr, cc], ntl[rr, cc], np.nan); ok = np.isfinite(X) & np.isfinite(B) & (B > 0)
                num = np.where(ok, X, 0).sum(1); den = np.where(ok, B, 0).sum(1)
                for i in range(len(q)):
                    rows.append((wk, start.date(), q.plant_id.values[i], q.nse_symbol.values[i], q.role.values[i], t, k, int(np.isfinite(X[i]).sum()),
                                 float(np.clip(clr[q.r.values[i], q.c.values[i]], 0, 1)), num[i] / den[i] if den[i] > 0 else np.nan, bmean[i]))
                os.remove(fn)
        d = pd.DataFrame(rows, columns=["wk", "start", "plant_id", "nse_symbol", "role", "tile", "night", "n_valid", "clear_10km", "ratio_raw", "base_annual"])
        d.round(4).to_csv(out_fn, index=False); os.remove(out_fn + ".lock"); shutil.rmtree(raw, ignore_errors=True)
        print(wk, "start", start.date(), "| tiles", tiles, "| hit plants", len(hit), "controls", len(ctrl), "| rows", len(d), flush=True)

def stage2():
    import statsmodels.formula.api as smf
    from es_lib import plt, BLUE, ORANGE, AQUA, MUTED, SURF
    es, ep, sel = episodes()
    d = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(CACHE + "*.csv.gz"))], ignore_index=True)
    d["clean"] = (d.n_valid >= 5) & (d.clear_10km >= 0.8) & (d.base_annual >= 5) & d.ratio_raw.notna()
    cm = d[d.clean & (d.role == "control")].groupby(["wk", "night"]).ratio_raw.agg(["median", "size"])
    d = d.join(cm, on=["wk", "night"]); d["rel"] = np.where(d["size"] >= 15, d.ratio_raw / d["median"], np.nan)
    d.drop(columns=["median", "size"]).round(4).to_csv(EXT + "ntl_episode_plant_nights.csv.gz", index=False)
    u = d[d.clean & d.rel.notna()]
    P = plants().reset_index().rename(columns={"index": "plant_id"})
    P["plant_share"] = P.project_cost_cr / P.groupby("nse_symbol").project_cost_cr.transform("sum").replace(0, np.nan)
    hp = d[d.role == "hit"].groupby(["wk", "plant_id"]).agg(nse_symbol=("nse_symbol", "first"), base=("base_annual", "first")).reset_index()
    first = u[(u.role == "hit") & (u.night <= 7)].sort_values("night").groupby(["wk", "plant_id"]).first().reset_index()
    hp = hp.merge(first[["wk", "plant_id", "night", "rel"]].rename(columns={"night": "first_night", "rel": "rel_first"}), on=["wk", "plant_id"], how="left")
    hp["lit"] = hp.base >= 5; hp["observed"] = hp.rel_first.notna(); hp["dark"] = np.where(hp.observed, hp.rel_first < 0.6, np.nan)
    def back(r):
        if r.dark != 1: return np.nan
        z = u[(u.wk == r.wk) & (u.plant_id == r.plant_id) & (u.night > r.first_night) & (u.rel >= 0.8)]
        return z.night.min() if len(z) else np.nan
    hp["night_back_08"] = hp.apply(back, axis=1)
    hp = hp.merge(P[["plant_id", "dist_name", "lat", "lon", "industry_name", "plant_share"]], on="plant_id")
    hp.round(4).to_csv(TAB + "ntl_episode_plants.csv", index=False)
    # false-alarm rate on controls, on the same nights as the hit plants' first clean night
    fa = u[u.role == "control"].assign(low=lambda x: x.rel < 0.6).groupby(["wk", "night"]).low.mean()
    hp["fa_rate"] = [fa.get((w, n), np.nan) for w, n in zip(hp.wk, hp.first_night)]
    W = hp.groupby("wk").agg(hit_plants=("plant_id", "size"), lit=("lit", "sum"), observed=("observed", "sum"), dark=("dark", lambda s: (s == 1).sum()),
                             median_first_night=("first_night", "median"), median_rel_first=("rel_first", "median"), control_false_alarm=("fa_rate", "mean"),
                             median_night_back=("night_back_08", "median")).reset_index()
    W["dark_share_observed"] = W.dark / W.observed.replace(0, np.nan); W["excess_dark_share"] = W.dark_share_observed - W.control_false_alarm
    W = W.merge(sel.reset_index()[["wk", "sev"]], on="wk", how="left").merge(ep.groupby("wk").start.min().rename("start"), on="wk")
    W = W.sort_values("start"); W.round(3).to_csv(TAB + "ntl_episode_summary.csv", index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
    print("=== per episode-week (hit plants = plants in districts with an extreme-rain episode) ===")
    print(W[["wk", "start", "sev", "hit_plants", "lit", "observed", "median_first_night", "dark", "dark_share_observed", "control_false_alarm", "excess_dark_share", "median_night_back"]].round(2).to_string(index=False))
    tot = dict(weeks=len(W), weeks_with_10plus_observed=int((W.observed >= 10).sum()), hit_plants=int(W.hit_plants.sum()), lit=int(W.lit.sum()),
               observed=int(W.observed.sum()), dark=int(W.dark.sum()), p_dark_given_observed=W.dark.sum() / W.observed.sum(),
               control_false_alarm=float(u[u.role == "control"].assign(low=lambda x: x.rel < 0.6).low.mean()))
    print("\ntotals:", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in tot.items()})
    # severity buckets
    hp2 = hp.merge(W[["wk", "sev"]], on="wk")
    sb = hp2[hp2.observed].groupby(pd.cut(hp2[hp2.observed].sev, [1, 1.25, 1.5, 2, 5])).agg(observed=("plant_id", "size"), p_dark=("dark", "mean"),
                                                                                         median_night_back=("night_back_08", "median"), weeks=("wk", "nunique")).reset_index()
    sb["sev"] = sb.sev.astype(str); sb.round(3).to_csv(TAB + "ntl_episode_severity.csv", index=False); print("\n=== by severity (3-day rain / 5-yr level) ==="); print(sb.round(3).to_string(index=False))
    # validation against the full method (Chennai Dec 2023, Gujarat Aug 2024)
    full = pd.read_csv(TAB + "ntl_plant_event.csv")
    vmap = {"2023-12-04/2023-12-10": "E_CHE_FLOOD_2023", "2024-08-26/2024-09-01": "E_GJ_FLOOD_2024"}
    for wk, ev in vmap.items():
        a = hp[(hp.wk == wk) & hp.observed][["plant_id", "dark", "rel_first", "first_night"]]
        b = full[(full.event_id == ev) & full.observed][["plant_id", "dark", "ratio_first"]]
        m = a.merge(b, on="plant_id", suffixes=("_new", "_full"))
        if len(m): print(f"\nvalidation {ev}: {len(m)} plants in both; agreement on dark {np.mean(m.dark_new.astype(bool) == m.dark_full.astype(bool)):.0%}; "
                         f"dark share new {m.dark_new.mean():.0%} vs full {m.dark_full.astype(float).mean():.0%}; rank corr {m.rel_first.corr(m.ratio_first, method='spearman'):.2f}")
    # firm-episode horse race
    proc = set(W.wk)
    fe = es[es.wk.isin(proc) & (es.share >= 0.02)].copy()
    hpw = hp.assign(w=hp.plant_share.fillna(0))
    agg = hpw.groupby(["wk", "nse_symbol"]).apply(lambda t: pd.Series(dict(share_dark=t.w[t.dark == 1].sum(), share_obs=t.w[t.observed].sum())), include_groups=False).reset_index()
    fe = fe.merge(agg, on=["wk", "nse_symbol"], how="left").fillna({"share_dark": 0, "share_obs": 0})
    fe["share_notdark"] = fe.share - fe.share_dark
    fe.round(4).to_csv(TAB + "ntl_episode_firm_cars.csv", index=False)
    H = []
    for lab, s in (("all firm-episodes", fe), ("hit assets mostly observed", fe[fe.share_obs >= 0.5 * fe.share])):
        for h in (5, 10, 20, 40):
            dep = f"adj_0_{h}"
            if dep not in s.columns: continue
            x = s.dropna(subset=[dep])
            if len(x) < 15: continue
            m = smf.ols(f"{dep} ~ share_dark + share_notdark", x).fit(cov_type="cluster", cov_kwds={"groups": x.wk.astype("category").cat.codes})
            t = m.t_test("share_dark - share_notdark = 0")
            H.append(dict(sample=lab, window=f"[0,{h}]", n=len(x), weeks=x.wk.nunique(), firm_eps_with_dark=int((x.share_dark > 0).sum()),
                          b_dark=m.params["share_dark"], p_dark=m.pvalues["share_dark"], b_notdark=m.params["share_notdark"], p_notdark=m.pvalues["share_notdark"],
                          diff=float(np.squeeze(t.effect)), p_diff=float(np.squeeze(t.pvalue))))
    H = pd.DataFrame(H); H.round(4).to_csv(TAB + "ntl_episode_horse_race.csv", index=False)
    print("\n=== horse race across episodes: CAR minus same-date unexposed = a + b_dark*share_dark + b_notdark*share_notdark ===")
    print(H.round(3).to_string(index=False))
    # figure
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.8))
    ax = axs[0]; w = W[W.observed >= 10].copy()
    ax.scatter(w.sev, w.dark_share_observed * 100, s=12 + w.observed / 3, color=BLUE, edgecolor=SURF, zorder=3, label="dark share of observed hit plants")
    ax.scatter(w.sev, w.control_false_alarm * 100, s=18, marker="x", color="#8b8a84", zorder=2, label="same nights, control plants (false alarms)")
    for r in w[w.dark_share_observed >= 0.3].itertuples(): ax.annotate(str(r.start.date()), (r.sev, r.dark_share_observed * 100), xytext=(4, 3), textcoords="offset points", fontsize=7, color=MUTED)
    ax.set_xlabel("Episode severity: peak 3-day rain ÷ district's 5-year level"); ax.set_ylabel("Plants below 60% of normal light, %")
    ax.set_title(f"A. How often do sites in extreme-rain districts go dark? ({len(w)} weeks with ≥10 sites seen)", loc="left"); ax.legend(fontsize=7.5)
    ax = axs[1]
    groups = ((fe.share_dark >= 0.05, ORANGE, "≥5% of plant cost dark"), ((fe.share_dark < 0.05) & (fe.share_obs >= 0.5 * fe.share), BLUE, "sites observed, not dark"),
              ((fe.share_dark < 0.05) & (fe.share_obs < 0.5 * fe.share), "#a3a29b", "sites mostly unobserved"))
    hz = [h for h in (5, 10, 20, 40) if f"adj_0_{h}" in fe.columns]
    for k, (msk, col, lab) in enumerate(groups):
        mu, lo, hi_ = [], [], []
        for h in hz:
            x = fe[msk].dropna(subset=[f"adj_0_{h}"])
            m = smf.ols(f"adj_0_{h} ~ 1", x).fit(cov_type="cluster", cov_kwds={"groups": x.wk.astype("category").cat.codes})
            mu.append(100 * m.params.iloc[0]); lo.append(100 * (m.params.iloc[0] - 1.96 * m.bse.iloc[0])); hi_.append(100 * (m.params.iloc[0] + 1.96 * m.bse.iloc[0]))
        xs = np.arange(len(hz)) + (k - 1) * 0.12
        ax.vlines(xs, lo, hi_, color=col, lw=1.4, alpha=.8); ax.plot(xs, mu, color=col, marker="o", ms=6, lw=1.6, label=f"{lab} (n={int(msk.sum())})")
    ax.axhline(0, color="#c9c8c2", lw=.8); ax.set_xticks(range(len(hz))); ax.set_xticklabels([f"0–{h}" for h in hz])
    ax.set_xlabel("Trading days after the episode"); ax.set_ylabel("CAR minus same-date unexposed firms, % (mean, 95% CI by week)")
    ax.set_title("B. Stock reaction by whether the firm's sites went dark", loc="left"); ax.legend(fontsize=7.5, loc="lower left")
    fig.suptitle("Night lights after the most severe rain episodes, Nov 2020–Sep 2026 (NASA Black Marble, first 7 nights)", x=0.01, ha="left", fontweight="bold")
    fig.tight_layout(); fig.savefig(FIG + "13_ntl_episodes.png", dpi=200)

if __name__ == "__main__":
    a = sys.argv[1:] or ["fetch", "analyse"]
    wk = [x for x in a if "/" in x]
    if "fetch" in a: stage1(wk or None)
    if "analyse" in a: stage2()
