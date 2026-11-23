"""Electricity demand by state around each event (Grid-India daily Power Supply Position reports).

Source: the daily "Energy Met" by state from Grid-India (formerly POSOCO) PSP report table C, as
compiled by Robbie Andrew (CICERO): https://robbieandrew.github.io/india/data/POSOCO_data.csv
(grid-india.in itself does not answer from this environment). Units: GWh per day (= million units).
For each event day the baseline is the same weekday's average over the previous two weeks, so the
Sunday dip is not mistaken for an event. Neighbouring states not hit by the event are shown as a
control. Caveat: state energy covers homes and farms as well as factories, and rain itself lowers
demand (less cooling and pumping), so a dip is an upper bound on lost industrial load.
Outputs: outputs/tables/power_state_event.csv, power_state_summary.csv, figs/10_power_demand.png
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from es_lib import *
raw = pd.read_csv(EXT + "power_raw/POSOCO_data.csv")
raw["date"] = pd.to_datetime(raw.yyyymmdd.astype(str)); raw = raw.set_index("date")
E = raw[[c for c in raw.columns if c.endswith(": EnergyMet")]].rename(columns=lambda c: c.split(":")[0])
CASES = {  # event -> (label, hit state, control states, first affected day, last day shown)
    "E_CHE_FLOOD_2023": ("Chennai, Cyclone Michaung", "Tamil Nadu", ["Karnataka", "Kerala"], "2023-12-03", 14),
    "E_GJ_FLOOD_2024":  ("Gujarat flood, Aug 2024", "Gujarat", ["Maharashtra", "Rajasthan"], "2024-08-25", 14),
    "E_GJ_FLOOD_2023":  ("Gujarat, Narmada flood, Sep 2023", "Gujarat", ["Maharashtra", "Rajasthan"], "2023-09-16", 14),
}
rows, summ = [], []
for ev, (label, st, ctrl, d0, n) in CASES.items():
    d0 = pd.Timestamp(d0)
    for s in [st] + ctrl:
        x = E[s]
        pre = x.loc[d0 - pd.Timedelta(days=14):d0 - pd.Timedelta(days=1)]
        wd = pre.groupby(pre.index.dayofweek).mean()
        for k in range(-14, n + 1):
            day = d0 + pd.Timedelta(days=k)
            if day not in x.index or pd.isna(x[day]): continue
            b = wd.get(day.dayofweek, pre.mean())
            rows.append(dict(event_id=ev, state=s, role="hit" if s == st else "control", date=day.date(), rel_day=k,
                             energy_met_gwh=x[day], baseline_gwh=b, deviation_pct=100 * (x[day] / b - 1)))
    r = pd.DataFrame([q for q in rows if q["event_id"] == ev])
    h = r[(r.role == "hit") & (r.rel_day >= 0)].set_index("rel_day"); c = r[(r.role == "control") & (r.rel_day >= 0)].groupby("rel_day").deviation_pct.mean()
    adj = h.deviation_pct - c                                   # hit state minus control states
    low = h.deviation_pct.idxmin()
    back = next((k for k in h.index if k > low and h.deviation_pct[k] > -3), np.nan)
    short = (h.baseline_gwh - h.energy_met_gwh).loc[:back - 1 if back == back else h.index.max()].clip(lower=0).sum()
    summ.append(dict(event_id=ev, label=label, state=st, normal_gwh_per_day=h.baseline_gwh.mean(), lowest_day=str(h.date[low]),
                     lowest_deviation_pct=h.deviation_pct[low], control_deviation_same_day_pct=c[low], lowest_minus_control_pct=adj[low],
                     days_below_minus3pct=int((h.deviation_pct.loc[:back - 1 if back == back else h.index.max()] < -3).sum()),
                     first_day_back_within_3pct=str(h.date[back]) if back == back else "not within window",
                     shortfall_gwh=short, shortfall_in_days_of_normal_use=short / h.baseline_gwh.mean(),
                     pre_event_sd_pct=r[(r.role == "hit") & (r.rel_day < 0)].deviation_pct.std()))
d = pd.DataFrame(rows); d.round(2).to_csv(TAB + "power_state_event.csv", index=False)
s = pd.DataFrame(summ); s.round(2).to_csv(TAB + "power_state_summary.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(s.round(2).T.to_string())
for ev in CASES:
    print("\n", ev); print(d[(d.event_id == ev) & d.rel_day.between(-3, 10)].pivot(index="date", columns="state", values="deviation_pct").round(1).to_string())

fig, axs = plt.subplots(1, 3, figsize=(15, 4.6), sharey=True)
for ax, (ev, (label, st, ctrl, d0, n)) in zip(axs, CASES.items()):
    x = d[d.event_id == ev]
    ax.axhline(0, color="#c9c8c2", lw=.9); ax.axvline(0, color=MUTED, lw=.8, ls=":")
    for stt, col in zip([st] + ctrl, [ORANGE, BLUE, AQUA]):
        g = x[x.state == stt]
        ax.plot(g.rel_day, g.deviation_pct, color=col, lw=2 if stt == st else 1.4, label=f"{stt}" + (" (hit)" if stt == st else " (control)"))
    ax.set_title(label, loc="left"); ax.set_xlabel(f"Days from {pd.Timestamp(d0):%d %b %Y}"); ax.legend(fontsize=8, loc="lower right")
axs[0].set_ylabel("Daily electricity supplied vs same weekday\nin the previous two weeks, %")
fig.suptitle("State electricity use around each event (Grid-India daily reports)", x=0.01, ha="left", fontweight="bold")
fig.tight_layout(); fig.savefig(FIG + "10_power_demand.png", dpi=200)
