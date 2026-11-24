"""Step E: traced-pathway diagrams (deliverable 1) and the lag figure (INSTRUCTIONS §4, lag structure).

Diagrams follow the instruction's layout: event -> exposed plant(s) -> hit firm (evidence, dates) -> verified link
(dependence) -> upstream/downstream firm (CAR, delta-financials, evidence, lag). Every number is taken from the
deliverable tables (evidence_NCR.csv, evidence_GJ.csv, verified_links.csv, stepC_*, cement_market_test.csv,
gj_archean_vs_peers.csv, stepC_gj_tcpl_salt.csv) as decided at G1-G7. Line styles carry the verdict, and every box says
it in words: solid blue = documented and accepted; dashed grey = link verified but effect not confirmed; red cross with
the words "chain breaks here" = no verified link or no company statement.
Lag figure: CAR paths by trading weeks since the event for the hit firms and the traced node, with the comparison group.
Outputs: outputs/deliverables/pathway_NCR.png/.svg, pathway_GJ.png/.svg, fig_lag_paths.png
"""
import os, sys, textwrap; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import es_lib as E
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from common import EXT, OUT
DEL = OUT + "deliverables/"
INK, MUTED, GREY, SURF, BLUE, ORANGE, AQUA, RED = "#0b0b0b", "#52514e", "#8a8984", "#fcfcfb", "#2a78d6", "#eb6834", "#1baf7a", "#d03b3b"
FILL = {"event": "#f0efec", "plant": "#f6f5f2", "doc": "#ffffff", "weak": "#ffffff", "break": "#ffffff", "note": "#f6f5f2"}
EDGE = {"event": INK, "plant": GREY, "doc": BLUE, "weak": GREY, "break": RED, "note": GREY}
def box(ax, x, y, w, h, title, body, kind="doc", fs=7.4, wrap=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.25,rounding_size=0.8", fc=FILL[kind], ec=EDGE[kind],
                                lw=1.6 if kind in ("doc", "event") else 1.1, ls="--" if kind in ("weak",) else "-"))
    n = wrap or max(18, int(w * 3.25))
    txt = "\n".join(textwrap.fill(p, n) for p in body.split("\n")) if body else ""
    ax.text(x + 0.7, y + h - 0.6, title, fontsize=fs + 1.2, fontweight="bold", va="top", ha="left", color=INK)
    ax.text(x + 0.7, y + h - 0.6 - 2.0, txt, fontsize=fs, va="top", ha="left", color=INK, linespacing=1.22)
def arrow(ax, p1, p2, kind="doc", label="", lx=0, ly=0.8, fs=7.2, rad=0.0):
    col = {"doc": BLUE, "weak": GREY, "break": RED, "plain": INK}[kind]
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=12, lw=1.8 if kind == "doc" else 1.3, color=col,
                                 ls="--" if kind in ("weak", "break") else "-", connectionstyle=f"arc3,rad={rad}"))
    if label:
        ax.text((p1[0] + p2[0]) / 2 + lx, (p1[1] + p2[1]) / 2 + ly, label, fontsize=fs, ha="center", va="bottom", color=INK,
                bbox=dict(fc=SURF, ec="none", pad=0.6))
    if kind == "break":
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        ax.text(mx, my, "✕", fontsize=13, color=RED, ha="center", va="center", fontweight="bold")
def frame(title, sub):
    fig = plt.figure(figsize=(18, 10.5)); ax = fig.add_axes([0.01, 0.01, 0.98, 0.9]); ax.set_xlim(0, 100); ax.set_ylim(0, 58); ax.axis("off")
    fig.text(0.012, 0.965, title, fontsize=15, fontweight="bold", color=INK, va="top"); fig.text(0.012, 0.93, sub, fontsize=9.5, color=MUTED, va="top")
    for x, h in ((1, "EVENT"), (17.5, "EXPOSED PLANTS"), (31, "HIT FIRM (evidence, dates)"), (52.5, "VERIFIED LINK (dependence)"), (69.5, "UPSTREAM / DOWNSTREAM FIRM (CAR, Δ financials, evidence, lag)")):
        ax.text(x, 57.2, h, fontsize=8.6, fontweight="bold", color=MUTED, va="top")
    ax.plot([0.5, 99.5], [55.3, 55.3], color="#e2e1dc", lw=1)
    return fig, ax
def legend(ax, y=0.6):
    ax.plot([1, 4], [y + 0.6, y + 0.6], color=BLUE, lw=1.8); ax.text(4.5, y + 0.6, "documented and accepted (company's own words + numbers)", fontsize=7.6, va="center", color=INK)
    ax.plot([30, 33], [y + 0.6, y + 0.6], color=GREY, lw=1.3, ls="--"); ax.text(33.5, y + 0.6, "verified, but effect not confirmed or immaterial", fontsize=7.6, va="center", color=INK)
    ax.text(53, y + 0.6, "✕", color=RED, fontsize=11, va="center", fontweight="bold"); ax.text(54.5, y + 0.6, "chain breaks here (no verified link / no company statement)", fontsize=7.6, va="center", color=INK)
    ax.text(82, y + 0.6, "CARs: market model vs NIFTY 500; p from placebo days", fontsize=7.2, va="center", color=MUTED)
def save(fig, name):
    fig.savefig(DEL + name + ".png", dpi=170); fig.savefig(DEL + name + ".svg"); plt.close(fig); print("wrote", name)
# ------------------------------- NCR -------------------------------
NC = pd.read_csv(DEL + "stepC_ncr_node_cars.csv"); NET = pd.read_csv(DEL + "stepC_ncr_contractor_net.csv"); CT = pd.read_csv(DEL + "cement_market_test.csv")
def c(sym, ev, w):
    x = NC[(NC.nse_symbol == sym) & (NC.event.str.startswith(ev)) & (NC.window == w)].iloc[0]; return f"{100*x.car:+.1f}% (p {x.p_two_sided:.2f})"
def n(sym, ev, w):
    x = NET[(NET.nse_symbol == sym) & (NET.event.str.startswith(ev)) & (NET.window == w)].iloc[0]; return f"{100*x.net_of_unlinked:+.1f}% (p {x.p_net_two_sided:.2f})"
cm = CT[(CT.spec.str.startswith("main")) & (CT.window == "(-1,5)") & (CT.event == "18 Nov 2024")].iloc[0]
fig, ax = frame("NCR, winter 2024: construction ban (GRAP Stage III/IV) → builders → contractors at NCR sites",
                "Traced pathway (Step E). Decisions G1-G5 and the checkpoint-4 and checkpoint-5 reviews applied, 23 Nov 2026. Transmission inside the zone: builder to contractor at NCR sites, both under the ban. Out of the zone: not detected.")
box(ax, 0.8, 14, 14.2, 38, "GRAP orders (CAQM)",
    "Stage III 15 Nov 2024; Stage IV from 18 Nov 08:00: construction and demolition stopped in Delhi-NCR.\n"
    "Re-imposed 16-17 Dec; Stage III again 3-5, 9-12, 15-17 Jan and 29 Jan - 3 Feb 2025 (PIB releases).\n"
    "Event day 0 = 18 Nov 2024; second episode day 0 = 17 Dec 2024.", kind="event")
box(ax, 17.5, 39, 12, 10, "NBCC: 34 NCR sites", "94% of its plant cost in NCR districts (pack data)", kind="plant")
box(ax, 17.5, 20, 12, 10, "DLF: 48 NCR sites", "42% of its plant cost in NCR districts (pack data)", kind="plant")
arrow(ax, (15.3, 40), (17.3, 44), "plain"); arrow(ax, (15.3, 28), (17.3, 25), "plain")
box(ax, 31, 36, 19.5, 16, "NBCC (confirmed, G3)",
    "Q3 FY25 call (Feb 2025): Amrapali and 70% of GPRA \"severely hitted by the NGT\"; project-management growth 1.2% against \"8% to 10%\"; ban of \"1.5 months\".\n"
    f"CAR to 22 Nov {c('NBCC','18 Nov','(-1,3)')}; consolidated Q3 sales +15.9% YoY.")
box(ax, 31, 15, 19.5, 18, "DLF (confirmed, G3)",
    "Q3 FY25 call (27 Jan 2025): \"the 2 malls in the Delhi NCR were a little delayed because of the GRAP and the stoppage of construction\" (Summit Plaza, Midtown Plaza).\n"
    f"CAR (-1,+5) {c('DLF','18 Nov','(-1,5)')}. Construction outflow Rs 521 cr (Q2) → Rs 591 cr (Q3): cash spend did not fall.")
arrow(ax, (29.7, 44), (30.8, 44), "doc"); arrow(ax, (29.7, 25), (30.8, 25), "doc")
# links + nodes
box(ax, 69.5, 44.5, 30, 8.5, "J. Kumar Infraprojects (no effect)", f"No mention of the ban. CAR (-1,+5) {c('JKIL','18 Nov','(-1,5)')}; Q3 sales +22% YoY. Low dose, as expected.", kind="weak")
arrow(ax, (50.7, 47), (69.3, 48.5), "weak", "NBCC = 1.6-3.4% of J. Kumar's sales\n(verified, not material)", ly=0.5)
box(ax, 69.5, 36, 30, 7, "NBCC's upstream branch: closed", "GPRA contractors in NBCC's filings (Varindera Constructions; Shapoorji Pallonji & Co. Pvt; Girdhari Lal Constructions Pvt) and Gaursons (Amrapali, trade press) were unlisted in Nov 2024: no price or filed quarterly data.", kind="note")
arrow(ax, (50.7, 40), (69.3, 39.5), "weak", "contractors on GPRA / Amrapali: unlisted", ly=0.4)
box(ax, 69.5, 17.5, 30, 17, "Ahluwalia Contracts (documented; directly exposed)",
    "Calls: \"GRAP-IV is in place … going to impact this quarter\" (18 Nov 2024); FY25 growth \"8.5%-9%\" against about 10% (12 Feb 2025); lost \"two months in Q3 and nearly a month in Q4 of FY '25\" (2 Jun 2025).\n"
    "Own exposure: 33.3% of its order book in NCR (31 Dec 2024). Δ: Q3 turnover -7.3% YoY; Q4 +4.5% YoY; FY25 +6.3%, below the guidance.\n"
    f"Price, net of unlinked contractors: 18 Nov (ban day 0 and Q2 results day; not separable) {n('AHLUCONT','18 Nov','(0,0)')}; call days (ban statements) 19 Nov {n('AHLUCONT','18 Nov','(1,1)')}, 13 Feb {n('AHLUCONT','12 Feb','(1,1)')}: not distinguishable from zero. Late falls hold no disclosure: not attributed.\n"
    "Lag: Q3-Q4 FY25 (Nov 2024 - Feb 2025).")
arrow(ax, (50.7, 27), (69.3, 27), "doc", "DLF = 3.4-10% of Ahluwalia's sales\n(Arbour; Downtown Ph-2 Rs 1,094.67 cr, 11 Oct 2024)", ly=0.5)
box(ax, 69.5, 9.5, 30, 6.8, "B.L. Kashyap (not confirmed)", f"No filing 12 Nov-30 Dec: on the ban's day 0 it fell {n('BLKASHYAP','18 Nov','(0,0)')} net, like Ahluwalia. (-1,+5) {n('BLKASHYAP','18 Nov','(-1,5)')}. Q3 sales -25% YoY, but Q2 already -18%.", kind="weak")
arrow(ax, (50.7, 19), (69.3, 13), "weak", "DLF = 35-44% of B.L. Kashyap's sales\n(verified; site hit not documented)", ly=-3.6)
box(ax, 31, 3.2, 19.5, 9, "Cement / steel suppliers (firm level)", "No document on either side links any supplier to DLF or NBCC. DLF's FY24 construction outflow (Rs 1,642 cr) is at most 0.7-14% of any listed supplier's revenue.", kind="break")
arrow(ax, (40, 14.8), (40, 12.5), "break")
ax.text(41.2, 13.6, "chain breaks here", fontsize=7.6, color=INK, va="center")
# checkpoint 5: cement makers that deliver to NCR replace the market-level test (kept in table2_notes.md as the comparison)
CFIT = pd.read_csv(DEL + "table2_cement_fit.csv"); CMK = pd.read_csv(DEL + "table2_cement_makers.csv").set_index("maker")
cf_ = lambda o, smp="all; ACC and Ambuja excluded": CFIT[(CFIT.outcome == o) & (CFIT["sample"] == smp) & (CFIT.dose == "near300_n") & (CFIT.control == "north_rest_n")].iloc[0]
c5, c17, v3, v2 = cf_("CAR 18 Nov 2024 (-1,5)"), cf_("CAR 17 Dec 2024 (-1,5)"), cf_("vol_yoy_q3fy25", "all"), cf_("vol_yoy_q2fy25 (pre-ban check)", "all")
box(ax, 54, 2.3, 45.5, 6.6, "Cement makers that deliver to NCR (not a firm link; null)",
    f"Dose: share of a maker's plants within 300 km of Delhi by road (Shree {CMK.loc['SHREECEM','near300_n']:.2f}, UltraTech {CMK.loc['ULTRACEMCO','near300_n']:.2f}, "
    f"JK Cement {CMK.loc['JKCEMENT','near300_n']:.2f}, JK Lakshmi {CMK.loc['JKLAKSHMI','near300_n']:.2f}). Coefficient {c5.coef:+.2f} over (-1,+5) (p {c5.p_two_sided:.2f}), "
    f"{c17.coef:+.2f} for 17 Dec (p {c17.p_two_sided:.2f}); Q3 volume {v3.coef:+.2f} (p {v3.p_two_sided:.2f}), as before the ban (Q2 {v2.coef:+.2f}). "
    "Not detected; the largest possible loss is below what the tests can detect. UltraTech names the curbs as one of three reasons for North infrastructure degrowth.", kind="note", wrap=150)
legend(ax)
save(fig, "pathway_NCR")
# ------------------------------- Gujarat -------------------------------
pc = lambda v: "0%" if round(v) == 0 else f"{v:+.0f}%"
GN = pd.read_csv(DEL + "stepC_gj_node_cars.csv"); AP = pd.read_csv(DEL + "gj_archean_vs_peers.csv"); TS = pd.read_csv(DEL + "stepC_gj_tcpl_salt.csv").set_index("period")
g = lambda s, w: (lambda x: f"{100*x.car:+.1f}% (p {x.p_two_sided:.2f})")(GN[(GN.nse_symbol == s) & (GN.window == w)].iloc[0])
a3 = AP[(AP.window == "(-1,5)")].iloc[0]
fig, ax = frame("Gujarat, Aug 2024: deep depression → Cyclonic Storm Asna → Tata Chemicals (Mithapur) → Tata Consumer (Tata Salt)",
                "Traced pathway (Step E). Decisions G1-G7 and the checkpoint-4 and checkpoint-5 reviews applied, 23 Nov 2026. All four hit firms are external to the pack's 81 firms; the one out-of-zone link is a cost passed into the retail price.")
box(ax, 0.8, 14, 14.2, 38, "Storm system: Asna",
    "Deep depression over Saurashtra & Kutch, 25-30 Aug 2024; \"INTENSIFIED INTO A CYCLONIC STORM 'ASNA'\" (IMD advisory No. 1, 30 Aug).\n"
    "Rain 25-31 Aug: Jamnagar 525 mm, Porbandar 502 mm, Kachchh 360 mm. An earlier episode, 18-24 Jul: 288, 610 and 86 mm (NASA POWER).\n"
    "Event day 0 = 26 Aug 2024.", kind="event", wrap=40)
box(ax, 17.5, 41, 12, 11, "Pack chemical belt (Vadodara)", "GSFC and Gujarat Alkalies sites dark on 30 Aug (night lights); Bodal: no usable reading.", kind="plant")
box(ax, 17.5, 22, 12, 13.5, "Sites outside the pack's districts", "Mithapur (Devbhumi Dwarka); Hajipir (Kutch); Mundra and Tuna ports (Kutch).", kind="plant")
box(ax, 17.5, 13.5, 12, 6.5, "Vadodara (in footprint)", "GE T&D India plant.", kind="plant")
arrow(ax, (15.3, 44), (17.3, 46), "plain"); arrow(ax, (15.3, 29), (17.3, 29), "plain"); arrow(ax, (15.3, 18), (17.3, 17), "plain")
box(ax, 31, 44, 19.5, 8.5, "No pack firm attributes an effect", "Q2 FY25 calls and NSE filings 25 Aug - 30 Sep 2024 read for 10 firms: no statement. The pack's chain breaks here, at Step A.", kind="break")
arrow(ax, (29.7, 47), (30.8, 47), "break")
box(ax, 31, 25.5, 19.5, 17, "Tata Chemicals, Mithapur (material hit)",
    "Call: operations hit \"for almost 10 days\"; 30,000 t soda ash and 40,000 t salt lost; Rs 11 cr one-off in PAT (deck), about Rs 40 cr cost (call). Press release: \"heavy rains in July and August\": loss not separable between the two episodes.\n"
    "Price: 26-30 Aug -0.1% abnormal; results day 18 Oct +1.1% (daily s.d. 2.3%): the shock is not visible in the share price. 10 Oct (+4.3%) and 21 Oct (+10.4%) unrelated.")
box(ax, 31, 13.5, 19.5, 10.8, "Archean, Kutch (material hit)",
    f"\"Asna cyclone impact resulting in loss of Industrial salt stock of Rs. 40.18 Crs (4.72 Lakhs MT)\". CAR (-1,+5) {100*a3.car_aci:+.1f}%, {100*a3.net_of_peers:+.1f}% net of specialty peers; 30-40x the booked loss. Not attributed.")
box(ax, 31, 3.2, 19.5, 9, "Confirmed, immaterial", "Adani Ports: \"4 days equivalent\" at Mundra and Tuna; August cargo still +5% YoY. GE T&D India: \"Production disruption\", no damage; quarter's sales +59%.", kind="weak")
arrow(ax, (29.7, 30), (30.8, 32), "doc"); arrow(ax, (29.7, 25), (30.8, 19), "doc"); arrow(ax, (29.7, 23), (30.8, 10.5), "weak"); arrow(ax, (29.7, 15), (30.8, 8), "weak")
box(ax, 69.5, 25.5, 30, 27, "Tata Consumer Products (downstream buyer; cost passed into the shelf price)",
    "Q2 call (18 Oct 2024): \"Mithapur recorded its highest ever rain since 1929\"; Mithapur \"had to buy brine which is the cost\"; \"September quarter the cost has not come in through us\".\n"
    "Last step, the shelf price: one increase, \"INR2 on a INR28 base, which is roughly around 7%\", effective October 2024. Margin held: \"it has put us back exactly where it should be in salt\". Partly a catch-up: it comes \"after a two-year hiatus\".\n"
    f"Δ salt (company): implied price/mix {TS.loc['Q1 FY25','implied_price_mix_pp']:+.0f}, {TS.loc['Q2 FY25','implied_price_mix_pp']:+.0f}, {TS.loc['Q3 FY25','implied_price_mix_pp']:+.0f}, {TS.loc['Q4 FY25','implied_price_mix_pp']:+.0f} pp (Q1-Q4) beside volume {', '.join(pc(TS.loc[q,'salt_volume_growth_pct']) for q in ('Q1 FY25','Q2 FY25','Q3 FY25','Q4 FY25'))}: cost stated by both firms; the Q2 volume stall (Tata Chemicals' India salt 322 kt vs 338 kt) is unexplained and consistent with lost supply. A 7% increase is worth at least Rs 110 cr a year, against a whole storm cost of about Rs 40 cr.\n"
    f"Price: CAR (-1,+5) {g('TATACONSUM','(-1,5)')}; results day 21 Oct -6.7% is tea-driven by the company's account, not attributable to salt.\n"
    "Lag: one quarter (cost and price change in Q3 FY25, Oct-Dec 2024).")
arrow(ax, (50.7, 34), (69.3, 34), "doc", "Edible salt. Tata Chemicals = 18-24% of Tata Consumer's\nmaterial input cost; Tata Consumer = 10-36% of its sales;\n\"single customer\" (TCL AR); \"more than 85%\" of TCPL's salt", ly=0.6)
box(ax, 69.5, 15, 30, 7.5, "Consumers (Tata Salt)", "Pay about 7% more per pack from October 2024. Salt volume was flat in Q2 and +1% in Q3 (no reason given by the company), then +5% in Q4.", kind="note")
arrow(ax, (84.5, 25.3), (84.5, 22.7), "doc")
legend(ax)
save(fig, "pathway_GJ")
# ------------------------------- lag figure -------------------------------
pp = pd.read_csv(EXT + "prices_peers.csv", parse_dates=["date"])
peer = pp.pivot_table(index="date", columns="asset_id", values="adjclose").sort_index().pct_change(fill_method=None)
add = peer.reindex(E.R.index); E.R = pd.concat([E.R, add[[c for c in add.columns if c not in E.R.columns]]], axis=1)
fig, axs = plt.subplots(1, 2, figsize=(13, 4.8), sharey=False)
def path(day, fs, post):
    ar = E.ar_matrix(E.t0_of(day), pre=1, post=post); return ar[fs].cumsum()
COMP = ["NCC", "PSPPROJECT", "CEMPRO", "LT", "CAPACITE"]
SPEC = ["VINATIORGA", "CLEAN", "SUDARSCHEM"]
panels = [(axs[0], "NCR: builders (hit buyers) and their contractor (supplier)", "2024-11-18", 65,
           [("AHLUCONT", "Ahluwalia (contractor ← DLF)", BLUE), ("DLF", "DLF (hit builder)", ORANGE), ("NBCC", "NBCC (hit builder)", AQUA)], (COMP, "unlinked contractors (mean)"),
           [(20, "17 Dec\nre-imposed"), (60, ""), (61.5, "11 Feb: (+60) ends\n12-13 Feb: Q3\nresults, call")]),
          (axs[1], "Gujarat: hit suppliers and the downstream buyer", "2024-08-26", 60,
           [("TATACONSUM", "Tata Consumer (buyer)", BLUE), ("TATACHEM", "Tata Chemicals (hit supplier)", ORANGE), ("ACI", "Archean (hit)", AQUA)], (SPEC, "specialty peers (mean)"),
           [(32, "10 Oct"), (38.5, "18-21 Oct\nresults"), (5, "2 Sep")])]
for ax, title, day, post, series, (grp, glab), marks in panels:
    P = path(day, [s for s, _, _ in series] + grp, post); x = np.array(P.index) / 5.0
    ax.axhline(0, color="#c9c8c2", lw=1)
    gm = P[grp].mean(axis=1); ax.plot(x, 100 * gm, color=GREY, lw=1.5); ax.text(x[-1] + 0.15, 100 * gm.iloc[-1], glab, fontsize=7.5, color=MUTED, va="center")
    for s, lab, col in series:
        ax.plot(x, 100 * P[s], color=col, lw=2, solid_capstyle="round", label=lab)
        ax.plot([x[-1]], [100 * P[s].iloc[-1]], "o", color=col, ms=6, mec=SURF, mew=2)
        ax.text(x[-1] + 0.15, 100 * P[s].iloc[-1], f"{lab.split(' (')[0]} {100*P[s].iloc[-1]:+.0f}%", fontsize=7.5, color=INK, va="center")
    for d, lab in marks:
        ax.axvline(d / 5, color="#c9c8c2", lw=1); ax.text(d / 5 + 0.08, ax.get_ylim()[1] if False else 0, "", fontsize=7)
    ax.set_title(title, loc="left"); ax.set_xlabel("trading weeks since event (day 0 = " + day + ")"); ax.set_ylabel("cumulative abnormal return, %")
    ax.set_xlim(-0.4, post / 5 + 3.2); ax.legend(loc="lower left", fontsize=7.5)
    lo, hi = ax.get_ylim(); ax.set_ylim(lo, hi + 0.22 * (hi - lo)); lo, hi = ax.get_ylim()
    for d, lab in marks:
        if lab:
            late = d / 5 > post / 5 - 2
            ax.text(d / 5 - 0.12 if late else d / 5 + 0.08, hi - 0.04 * (hi - lo), lab, fontsize=6.8, color=MUTED, va="top", ha="right" if late else "left")
fig.suptitle("Lag structure: CAR by weeks since the event (market model vs NIFTY 500, estimated on days -250 to -30)", x=0.01, ha="left", fontsize=10, fontweight="bold")
fig.text(0.01, 0.012, "NCR: Ahluwalia's late fall holds no disclosure of its own until 12-13 Feb (not attributed).\nGujarat: Tata Consumer's fall comes with its results (21 Oct) and tea costs by the company's own account, not salt; "
         "Tata Chemicals' jumps on 10 Oct and 21 Oct are unrelated (Ratan Tata's death; RBI ruling on Tata Sons' listing).", fontsize=7.2, color=MUTED)
fig.tight_layout(rect=(0, 0.06, 1, 0.95)); fig.savefig(DEL + "fig_lag_paths.png", dpi=170); plt.close(fig); print("wrote fig_lag_paths")
