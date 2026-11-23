"""Memo figure: the two traced pathways as one compact schematic, sized for an A4 page (the full diagrams with evidence
are pathway_NCR.png and pathway_GJ.png). Numbers come from the deliverable tables as decided at G1-G7 and the
checkpoint-4 review. Output: outputs/deliverables/fig_memo_pathways.png
"""
import os, sys, textwrap; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from common import OUT
DEL = OUT + "deliverables/"
INK, MUTED, GREY, BLUE, RED = "#0b0b0b", "#52514e", "#8a8984", "#2a78d6", "#d03b3b"
TS = pd.read_csv(DEL + "stepC_gj_tcpl_salt.csv").set_index("period")
CT = pd.read_csv(DEL + "cement_market_test.csv"); cm = CT[CT.spec.str.startswith("main") & (CT.window == "(-1,5)") & (CT.event == "18 Nov 2024")].iloc[0]
fig = plt.figure(figsize=(7.2, 5.3)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 65); ax.axis("off")
def box(x, y, w, h, title, body, kind="doc"):
    ec = {"doc": BLUE, "weak": GREY, "break": RED, "event": INK}[kind]
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.25,rounding_size=0.8", fc="#f0efec" if kind == "event" else "white", ec=ec, lw=1.1, ls="--" if kind == "weak" else "-"))
    ax.text(x + 0.8, y + h - 0.8, title, fontsize=7.0, fontweight="bold", va="top", color=INK)
    ax.text(x + 0.8, y + h - 3.3, textwrap.fill(body, int(w * 1.42)), fontsize=6.2, va="top", color=INK, linespacing=1.2)
def arrow(p1, p2, kind="doc"):
    col = {"doc": BLUE, "weak": GREY, "break": RED}[kind]
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=7, lw=1.2, color=col, ls="--" if kind != "doc" else "-"))
    if kind == "break": ax.text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, "✕", fontsize=8, color=RED, ha="center", va="center", fontweight="bold")
pc = lambda v: "0%" if round(v) == 0 else f"{v:+.0f}%"
vol = ", ".join(pc(TS.loc[q, "salt_volume_growth_pct"]) for q in ("Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25"))
pm = ", ".join(f"{TS.loc[q, 'implied_price_mix_pp']:+.0f}" for q in ("Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25"))
# A. NCR
ax.text(1, 64.3, "A. NCR, winter 2024: transmission inside the zone", fontsize=7.8, fontweight="bold", va="top", color=INK)
box(1, 45, 17, 15.5, "GRAP Stage III/IV", "Construction stopped in Delhi-NCR from 15 and 18 Nov 2024; re-imposed 16 Dec; Stage III again in Jan 2025.", "event")
box(21.5, 45, 20, 15.5, "Builders: NBCC, DLF", "Hit confirmed in their own words (GPRA, Amrapali; two malls delayed). No price effect.")
box(45.5, 45, 27, 15.5, "Contractor at NCR sites: Ahluwalia", "Link: DLF is 3.4-10% of its sales. 33% of its own order book is in NCR: directly exposed. Lost 'two months in Q3 and nearly a month in Q4'; FY25 +6.3% vs 8.5-9% guided. Call days: no significant price move.")
box(76, 45, 23, 15.5, "Other contractors", "B.L. Kashyap (DLF, 35-44% of sales): hit not documented. J. Kumar (NBCC, 1.6-3.4%): no effect.", "weak")
box(21.5, 35, 20, 7.5, "NBCC's contractors", "In NBCC's filings; unlisted: no price or quarterly data.", "weak")
box(45.5, 36, 27, 6.5, "Out of the zone: cement and steel", f"No firm-level link. Market test {100*cm.gap_north_minus_none:+.1f} pp (p {cm.p_two_sided:.2f}): not detected.", "break")
arrow((18.3, 52.5), (21.3, 52.5)); arrow((41.8, 52.5), (45.3, 52.5)); arrow((72.8, 52.5), (75.8, 52.5), "weak")
arrow((31.5, 44.8), (31.5, 42.7), "weak"); arrow((41.8, 46.5), (45.3, 40.5), "break")
# B. Gujarat
ax.text(1, 32.3, "B. Gujarat, Aug 2024: the one out-of-zone link", fontsize=7.8, fontweight="bold", va="top", color=INK)
box(1, 12.5, 17, 16, "Storm Asna", "Deep depression over Saurashtra and Kutch, 25-30 Aug 2024; Cyclonic Storm 'Asna' (IMD). All hit firms are outside the pack.", "event")
box(21.5, 12.5, 20, 16, "Tata Chemicals, Mithapur", "About 10 days lost; 40,000 t salt and 30,000 t soda ash; about Rs 40 cr cost. Share price: no visible response.")
box(45.5, 12.5, 27, 16, "Tata Consumer (buyer)", "Link: Tata Chemicals is 18-24% of its material inputs. The cost arrived a quarter later ('had to buy brine'). One Tata Salt increase, Rs 2 on Rs 28 (about 7%), from Oct 2024; margin held; partly a catch-up after two years.")
box(76, 12.5, 23, 16, "Shelf price, by quarter", f"Salt price/mix {pm} pp (Q1-Q4 FY25); volume {vol}: cost, not shortage. The 7% is worth at least Rs 110 cr a year.")
box(1, 1.8, 17, 7.7, "Pack chemical belt", "Sites dark; no statement: breaks at Step A.", "break")
box(21.5, 2.5, 20, 7, "Archean, Kutch", "Rs 40.18 cr salt stock lost; price fall not attributed.", "weak")
arrow((18.3, 20.5), (21.3, 20.5)); arrow((41.8, 20.5), (45.3, 20.5)); arrow((72.8, 20.5), (75.8, 20.5))
arrow((9.5, 12.3), (9.5, 9.7), "break"); arrow((18.3, 13.5), (21.3, 8.5), "weak")
fig.savefig(DEL + "fig_memo_pathways.png", dpi=220); print("wrote fig_memo_pathways.png")
