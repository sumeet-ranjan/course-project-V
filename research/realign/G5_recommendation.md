# Decision G5: NCR mechanism and confounds. Recommendation and evidence (23 Nov 2026)

**The question:** along the traced NCR pathway, which mechanism does the evidence support, and what are the confounds?

**Where the evidence is** (every quote checked against the saved original by `src/42`):
- `outputs/deliverables/evidence_NCR.csv` (per node)
- `hit_register_NCR.csv` (all firms screened)
- `stepC_ncr_node_cars.csv` and `stepC_ncr_quarterly.csv` (node responses)
- `cement_market_test*.csv` (market-level branch)
- `verified_links.csv` (links, with G4 applied)

**How to read the CARs:** market model; p-values come from each firm's own CAR on 1,000 random days. Windows
start at 18 Nov 2024 unless marked 17 Dec, the start of the second ban episode.

## What each node shows

| Node | Own statement (original document) | Price response | Quarterly change | Reading |
|---|---|---|---|---|
| **DLF** (hit firm) | "the 2 malls in the Delhi NCR were a little delayed because of the GRAP and the stoppage of construction" (27 Jan 2025). The two malls are Summit Plaza and Midtown Plaza (G4 R4) | +5.2% to 22 Nov (p = 0.10); +5.8% over (−1,+5) (p = 0.12); −6.4% over the second episode's (+6,+20) (p = 0.23) | Q3 sales +0.5% YoY. **Construction outflow rose from Rs 521 cr (Q2) to Rs 591 cr (Q3)** | Delay confirmed by the firm and small. DLF's construction cash spend did not fall in the ban quarter. No price effect. |
| **NBCC** (hit firm) | Amrapali and 70% of GPRA "severely hitted by the NGT"; project-management growth 1.2% against "8% to 10%" otherwise; a ban of "1.5 months" (15 Nov–27 Dec) | −4.1% to 22 Nov (p = 0.36); −1.5% over (−1,+5) (p = 0.77); +1.3% against the PSU index | Consolidated Q3 sales +15.9% YoY | Hit confirmed by the firm, and quantified on one segment (about 7–9 pp of growth). No price effect. The upstream branch stays open: no contractor identified on Amrapali or GPRA. |
| **Ahluwalia** ← DLF (contractor, material, within zone) | Nov 2024: "GRAP-IV is in place … I've kept the margin guidance muted". Feb 2025: FY25 growth "8.5%-9%" against about 10% guided; labour cost up "on account of NGT"; clients (DLF named) paid idle labour; "January also has been badly hit"; restart "on 3rd or 4th of February" (the last Stage III revocation was 3 Feb). The planned Arbour ramp to Rs 25 cr a month was delayed | −11.9% to 22 Nov (p = 0.03). Its own Q2 results came out after the close on 14 Nov and its call was on 18 Nov. −7.8% over (−1,+5) (p = 0.19). **−19.5% over the second episode's (+6,+20) (p = 0.02); −33.4% over (+21,+60) (p = 0.02)**, a window that holds its Q3 guidance cut | Q3 sales −7.2% YoY, −5.8% QoQ; margin 9% (−2 pp YoY); Q4 +27.7% QoQ (catch-up) | **The mechanism is documented end to end at this node**: ban → stopped civil work on DLF and other NCR sites → lower revenue and higher idle-labour cost → guidance cut → price falls in the windows that carry those disclosures. Builders absorbed part of the cost by paying idle labour. |
| **B.L. Kashyap** ← DLF (verified link; site hit not documented) | No mention in its Q3 FY25 presentation | No effect (+0.1% over (−1,+5); +1.2% over the second episode's (+6,+20)) | Q3 sales −25.3% YoY, but already −18.3% in Q2; margin 2.6% | Not confirmed at this node; the decline predates the ban. |
| **J. Kumar** ← NBCC (not material) | No mention | No effect (+3.0% over (−1,+5)) | Q3 sales +22% YoY | Low dose (2–3% of its sales). No effect, as expected. |
| **Unlinked contractors** (NCC, PSP, ITD/Cemindia, L&T, Capacit'e) | No mention | About zero on average (−0.0% over (−1,+5); +3.1% over (+6,+20)) | Q3 sales from −10.6% (PSP) to +22.7% (Capacit'e) YoY | Comparison group. ITD and Capacit'e have NCR presence. |
| **Cement/steel, firm level** | No document links any cement or steel firm to NBCC or DLF | — | — | **The chain breaks here** (G4 R1). DLF's FY24 construction outflow is at most 0.7%–14% of any listed supplier's FY24 revenue; NBCC buys no materials itself. |
| **Cement, market level** (not a firm link) | UltraTech, North row: housing grew, commercial grew; "Infrastructure segment registered degrowth on account of pollution control measures taken in Delhi and surrounding regions, projects on hold due to farmers agitation in Punjab and completion of major projects like RRTS" | Makers with northern capacity minus makers with none: +2.5 pp over (−1,+5) (p = 0.34). Against documented zeros only: +10.6 pp (p = 0.005). Both the wrong sign | — | No measurable market-level propagation. One supplier names the curbs, as one of three reasons, for one segment. |

**Other firms attributing an effect** (`hit_register_NCR.csv`):
- **Ashiana Housing (external):** "QoQ decline by 13.64% due to imposition of GRAP related restrictions in Delhi-NCR", in area constructed.
- **Godrej Properties (external):** "because of NGT ban … some of the billing milestones had moved from quarter 3 to quarter 4".

The other 25 firms screened say nothing. Signature Global, Max Estates and Unitech could not be read.

## Confounds, and how each is handled

| Confound | Affects | Handling | Status |
|---|---|---|---|
| IGL's own gas-allocation cut (18 Nov) | the old direct test | IGL excluded everywhere | closed |
| Adani indictment (21 Nov) | ACC, Ambuja, Adani firms | out of all controls, placebos and the cement test; ACC flagged for Step C | closed |
| PSU rally (25 Nov) | NBCC | window ending 22 Nov; PSU benchmark; controls' 25 Nov returns shown (rally broad: PSU index +2.5%, developers +1.5% to +5%) | controlled |
| Ahluwalia's own Q2 results (14 Nov, after close) and call (18 Nov) | Ahluwalia (−1,+5) | cannot be separated: the call itself carried the GRAP guidance. Read the move as a response to the firm's own disclosure of the ban's effect; the second-episode window and the quarterly numbers are shown alongside | open (by construction) |
| The ban recurred: Stage III on 3–5, 9–12, 15–17 Jan and 29 Jan–3 Feb 2025 | all (+21,+60) windows | recorded from the PIB releases. Ahluwalia says January was hit | noted: (+21,+60) is not a clean post-event window |
| Maharashtra assembly election (polling 20 Nov, a market holiday; results 23 Nov) | developer controls (5 of 8 are Mumbai/Pune-focused) | not separated; controls' 25 Nov returns are mixed (Lodha −1.4% to Puravankara +5.0%) | possible; not established |
| Farmers' agitation in Punjab; RRTS completion | cement market level | UltraTech names both alongside the curbs | cannot be separated |
| B.L. Kashyap's falling revenue before the ban | B.L. Kashyap node | Q2 already −18% YoY | explains its quarter better than the ban does |
| "NGT ban" wording | text screening | companies call CAQM's GRAP order the "NGT ban"; NBCC's transcript spells GRAP "graph" | a manual-trace point: an automated GRAP keyword search misses both |

## Recommendation (your call)

**R1. Accept the mechanism for the within-zone chain.** Ban → builders' sites (DLF, NBCC) → contractor
(Ahluwalia). It is documented by each firm's own statements and by Ahluwalia's revenue, cost and guidance, and
priced at the contractor in the windows that carry its disclosures. Record that the effect is within the zone: the
contractor's sites were themselves under the ban.

**R2. Reject propagation to out-of-zone suppliers.**
- No firm-level cement or steel link exists.
- The market-level test is null, or the wrong sign.
- The only supplier statement assigns the curbs one of three causes for one segment, while housing and commercial grew.

**R3. Keep NBCC's upstream branch open** (no contractor identified on Amrapali or GPRA). **Record B.L. Kashyap as a
verified but unconfirmed node.**

**R4. Treat the hit firms' own price responses as nil.** DLF +5.8%, NBCC −1.5% over (−1,+5). The mechanism
shows in their statements, and in DLF's case not even in its cash spend.

**R5. Carry the open confounds into the memo.** These are the Ahluwalia timing, the January recurrences and the
Maharashtra election. None reverses R1 or R2.
