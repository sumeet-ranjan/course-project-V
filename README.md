# Climate shocks and supply-chain propagation in India

**Research question (from the assignment):** when a localized, documented extreme event damages the
physical plants of a listed firm, does the shock propagate along the supply chain to firms that were
never in the disaster zone? Two deep-dives: **E_NCR_GRAP_2024** (Delhi-NCR construction ban) and
**E_GJ_FLOOD_2024** (Vadodara floods).

**Scope.** Since 22 Nov 2026, `docs_from_pack/INSTRUCTIONS.md` and `docs_from_pack/README.md` are the
only definition of scope, method and deliverables. Where any other file in this folder disagrees with
them, the assignment wins.
- `GAP_MAP.md`: what exists and what is missing.
- `NEXT_STEPS.md`: the plan, with the decision points (◆) that are the user's calls.
- `HANDOVER.md`: environment setup, data traps and permissions.

The work of earlier rounds (hazard panels, satellite proxies, pricing) is kept but archived. It is
not part of the deliverables (see the end of this file).

## Deliverables (§6 of the instructions)

| # | Deliverable | File (in `outputs/deliverables/`) | Status, 23 Nov 2026 |
|---|---|---|---|
| 1 | Traced-pathway diagram + evidence table per node, NCR | `pathway_NCR.png/.svg`, `evidence_NCR.csv` | **revised at the checkpoint-4 review (23 Nov 2026)**: G3–G5 applied; results days vs call days; Ahluwalia's own NCR exposure; NBCC branch closed; lag figure `fig_lag_paths.png` |
| 1 | The same, Gujarat | `pathway_GJ.png/.svg`, `evidence_GJ.csv` | **revised (checkpoint 4)**: G7 applied; Tata Chemicals' price evidence; Tata Consumer Q2 salt; magnitude line; Archean not attributed |
| 2 | Verified supply-chain links file, replacing the scaffold | `verified_links.csv` (built by `src/40_links_file.py`) | G1, G4 and G7 applied (128 rows). Each row carries the external, footprint and trade flags. Contractor links: Ahluwalia ← DLF verified and material; B.L. Kashyap ← DLF verified, site hit not documented; B.L. Kashyap ← Anant Raj held; J. Kumar ← NBCC low dose. Tata Chemicals → Tata Consumer verified and material (G7). Cement/steel rows are not verified, with a materiality bound |
| 3(i) | Direct event study / DiD | `table1_direct.csv`, `table1_direct_firms.csv`, `table1_returns_25nov2024.csv`, `table1_did.csv` (read with `table1_notes.md`) | done (Step 1, 23 Nov 2026), on the G2 firm sets |
| 3(ii) | Propagation dose-response | `table2_dose_response.csv`, `table2_dose_response_fit.csv`, `table2_notes.md` | **revised (checkpoint 4)** (`src/58`): NCR 8 contractors (3 linked, 5 zero dose), dose shown beside each contractor's own NCR order-book share (not separable with 8 firms), exact permutation tests; Gujarat one link (no slope); cement market level (two-firm variant run, not interpreted) |
| 3(iii) | Placebos | `table3_placebo.csv`, `table3_placebo_firms.csv`, `table3_notes.md` (firm lists in `placebo_firms.csv`) | **revised (checkpoint 4)**: means and medians; Gujarat list approved with changes (Reliance Power dropped, Tata Steel flagged, re-screened against Tata Chemicals and Archean) |
| 4 | Memo, 5 pages at most as set | `memo.md`, `memo.pdf` (A4, 4 pages incl. figure and tables; built by `src/61_build_memo.sh`), figure `fig_memo_pathways.png` (`src/60`) | **revised (checkpoint 4)**, with the manual-trace section |
| — | Hit-firm registers (scope change, 23 Nov 2026) | `hit_register_NCR.csv`, `hit_register_GJ.csv` | NCR 45 rows, Gujarat 40 rows; G7 grades in column `grade` |

## Decisions taken by the user
- **22 Nov 2026, realignment:**
  - **NCR hit firms** are the builders under the construction ban; the chain to trace runs to their cement and steel suppliers.
  - **Maruti** is a within-zone comparison, promoted to a traced branch only if a disclosed GRAP effect is found.
  - **Torrent Power** is not a clean placebo, because it is a Petronet customer.
  - **The scaffold result** is removed from the findings.
  - **Original documents only:** nothing enters a deliverable until the original document has been read.
- **23 Nov 2026:**
  - The plan in `NEXT_STEPS.md` is approved.
  - **G1:** the legacy links are classified as follows.
    - *Rejected:* Aarti–UPL (the joint venture starts supplying only in Q1 FY 2026-27).
    - *Held:* Petronet → GAIL, IOC, BPCL and Torrent (no Dahej shock found).
    - *Removed from the NCR test:* the links built on IGL, RVNL and Maruti.
    - *Out of scope:* the Chennai and other off-chain rows.
    - *Candidates:* Gujarat Alkalies → NALCO, pending Step A; Shree Cement's North market share, as a possible fallback weight.

- **23 Nov 2026, G2 and G3** (details in `research/realign/G2_G3_recommendation.md` and `g2_decision.csv`):
  - **G3:** NBCC and DLF are the confirmed NCR hit firms. Anant Raj, Parsvnath and Unitech are exposed, not confirmed. NBCC's "1.5 months" is read as the 15 Nov–27 Dec 2024 span.
  - **G2, NCR:**
    - Confirmed and unconfirmed builders are reported separately.
    - The main benchmark is all eligible developer controls, equal-weighted; the nearest two by size is the robustness check.
    - NBCC is also measured against a PSU benchmark (Nifty PSE), with a window ending 22 Nov.
    - IGL, Adani Enterprises, Adani Green, Adani Power and Torrent are dropped. ACC is flagged as contaminated for Step C.
  - **G2, Gujarat:**
    - Both footprints are reported. The Vadodara footprint is defined by sites, and Step A starts from GSFC and Gujarat Alkalies.
    - DCW is excluded.
    - Controls are matched by sub-industry first and size second. All ten firms are kept, and the five without a size match are not described as size-matched.
    - The user will check the five unverified controls by hand.
  - **Record:** the January 2025 Stage III orders are added to `research/proxy/official_hazard_records.csv`.

- **23 Nov 2026, G4 and the scope change:**
  - **R1:** the cement/steel firm-level hop is not verified. A materiality bound is added: DLF's FY24 construction outflow of Rs 1,642 cr against each supplier's FY24 revenue.
  - **R2:** all contractors are within-zone upstream nodes.
    - Ahluwalia ← DLF is verified and material, with the Downtown Phase-2 contract live from 11 Oct 2024.
    - B.L. Kashyap ← DLF is verified, but no hit at its site is documented. B.L. Kashyap ← Anant Raj is held.
    - J. Kumar ← NBCC is a low-dose row.
    - Unlinked contractors are kept as comparison rows.
  - **R3:** cement is tested as a separate market-level test, not a firm link.
  - **R4:** DLF's two delayed malls are Summit Plaza (Gurugram) and Midtown Plaza (Delhi). Their contractor is not identified; Tata Projects is documented only for the ONE Midtown towers.
  - **Rules:**
    - Suppliers are classified by trade. Civil, structural and ready-mix work is banned under Stage III; fit-out trades are contrasts.
    - No weight dated after Dec 2024 is used for NCR.
    - "ACC India Pvt Ltd" is not ACC Ltd.
    - Every firm is flagged external and in_pack_footprint.
  - **Scope change:** hit-firm registers for both events, including firms outside the pack.
- **23 Nov 2026, G5 (NCR) and G7 (Gujarat):**
  - **G5:** the within-zone mechanism (ban → builders' sites → Ahluwalia) is accepted on documents and quarterly numbers; the price claim was corrected (the late windows hold no Ahluwalia disclosure; disclosure days reported net of unlinked contractors); out-of-zone propagation "not detected"; the cement test's +2.5 pp is the result and its two-firm variant is dropped; two confounds added (small- and mid-cap sell-off of Jan–Feb 2025; Q4 seasonality).
  - **G7:** hit firms graded (material: Tata Chemicals, Archean; confirmed but immaterial: Adani Ports, GE T&D); both rain episodes shown; Archean's price fall checked against peers and news; the Tata chain accepted as a cost pass-through ending in one ~7% retail price increase; propagation measured with salt revenue, volume and price by quarter; Tata Chemicals' 10 Oct and 21 Oct moves flagged as unrelated.
- **23 Nov 2026, checkpoint-4 review:** the three corrections accepted (one Tata Salt increase; 12 Feb = Q3 results, 13 Feb = guidance cut; Adani's +5% is August cargo), as were "not detected", the cement +2.5 pp and the four Gujarat grades. Changes: 18 Nov treated like February (results day vs call day); Gujarat placebo list approved with changes (Reliance Power dropped for SEBI's order of 22 Aug 2024, medians, Tata Steel flagged, re-screen); Tata Chemicals' price evidence stated; Tata Consumer Q2 salt added (+2% revenue, flat volume) with a magnitude line; Archean "not attributed"; the cement two-firm variant kept as one note; dose shown beside own NCR exposure; memo framed as transmission inside the zone (NCR) and the one out-of-zone link (Gujarat); GE T&D's 6 Sep filing read; NBCC's contractors unlisted (branch closed).

## Findings so far (within scope)
- **Step 1, H1 direct effect** (`outputs/deliverables/table1_*`; p-values from 1,000 placebo days):
  - **NCR, 18 Nov 2024:**
    - *Confirmed builders (NBCC, DLF):* no effect against the developer controls. +0.4 pp over (−1,+5), p = 0.91; the nearest-two check gives −1.3 pp, p = 0.79.
    - *NBCC alone:* −3.2 pp against the controls (p = 0.56) and +1.3 pp against the Nifty PSE index (p = 0.77). Over the window to 22 Nov: −4.4 pp (p = 0.32) and −2.0 pp (p = 0.65).
    - *Unconfirmed builders:* fall more, −10.7 pp over (−1,+5) (two-sided p = 0.12, one-sided 0.05), then rebound +10.6 pp over (+6,+20).
    - *Within-zone firms* (Maruti, hospitals and others): −2.2% (p = 0.43).
    - *The 17 Dec re-imposition and the pooled Stage III starts of 2022–2024:* nothing.
  - **Gujarat, 26 Aug 2024:**
    - No negative effect on either footprint. At impact (−1,+5) the exposed chemical firms beat their sub-industry pools (+5.5 pp, p = 0.05, the wrong sign).
    - The positive late window (+21,+60) is driven by firm-specific moves (Kiri +64%, DCM Shriram +34%, Zuari +29%) that have not been checked.
  - **Quarterly DiD:** nothing distinguishable from zero.
- **Earlier layout of the direct test (superseded by Step 1, kept for reference):** exposed firms with ≥ 25% of plant cost in the zone against all unexposed sample firms (`outputs/tables/event_study_summary.csv`).
  - NCR, 18 Nov 2024: −4.0 pp over [−1,+1] (p = 0.017), mostly IGL's fall on its own gas-allocation cut.
  - Gujarat: −1.7 pp over [0,+20] (p = 0.77).
- **Disclosures, Step A material:**
  - *NCR:* two builders name the ban in their own calls (G3).
    - DLF (27 Jan 2025): "2 malls in the Delhi NCR were a little delayed because of the GRAP and the stoppage of construction".
    - NBCC (13 Feb 2025):
      - "our major projects are Amrapali and 70% GPRA so these two projects this year severely hitted by the NGT … Otherwise, 8% to 10% minimum increase will be there" (project-management growth was 1.2%). The CMD names the green tribunal ("NGT"), not GRAP.
      - "the third quarter is mostly impacted by the graph [sic] in Delhi and NCR area".
      - "last 1.5 months, there was a ban on construction in Delhi and NCR", read as 15 Nov–27 Dec.
    - No builder filed a stoppage notice with the exchange.
  - *Gujarat:* no sample firm has a disclosed or reported plant stoppage so far.
- **Step B, NCR (decision G4 pending, `research/realign/G4_recommendation.md`):**
  - No cement or steel firm-to-firm link to NBCC or DLF exists in either side's documents. NBCC states it buys no construction materials itself; its contractors do.
  - Three contractor links were documented and were running during the ban:
    - Ahluwalia Contracts ← DLF: 3–10% of Ahluwalia's sales.
    - B.L. Kashyap ← DLF: 35–44% of its sales.
    - J. Kumar ← NBCC: 2–3% of its sales.
  - The contractors' own NCR sites were under the same ban, so they are within-zone nodes.
  - UltraTech is the only cement or steel firm whose Q3 FY25 documents mention the Delhi pollution curbs (as one cause of infrastructure degrowth).
- **NCR Steps C–D (decision G5 taken 23 Nov 2026, `research/realign/G5_recommendation.md`):**
  - **Hit firms:** NBCC and DLF state the hit, but show no price effect (−1.5% and +5.8% over (−1,+5)). DLF's construction outflow rose in the ban quarter (Rs 521 cr to Rs 591 cr).
  - **Ahluwalia (DLF's contractor, within zone): the mechanism is documented by the firm's statements and numbers** (accepted at G5 on documents and quarterly numbers).
    - Its statements: margin guidance muted for GRAP-IV (Nov 2024); FY25 growth guided down to "8.5%-9%" (12 Feb 2025); idle labour paid by clients including DLF; restart on 3–4 Feb; "we lost approximately two to three months, two months in Q3 and nearly a month in Q4 of FY '25" (Q4 call, 2 Jun 2025).
    - Its numbers (company's own): Q3 FY25 turnover −7.3% YoY; Q4 FY25 +4.5% YoY; FY25 +6.3% (Rs 4,098.62 cr against Rs 3,855.29 cr), below the 8.5–9% guided.
    - Its price, net of the unlinked contractors (`stepC_ncr_contractor_net.csv`): results days 18 Nov 2024 −4.7% (p = 0.04; Q2 results, down 2.78% by 10:32 on the profit fall; also the ban's day 0) and 12 Feb 2025 −4.0% (p = 0.08); call days, which price its ban statements, 19 Nov −1.3% (p = 0.55) and 13 Feb −2.2% (p = 0.28): no significant move. The large later falls contain no Ahluwalia disclosure and are not attributed.
    - Its own exposure: 33.3% of its order book is in Delhi NCR (31 Dec 2024), so it is directly exposed: transmission inside the zone, builder to contractor at NCR sites.
  - **B.L. Kashyap and J. Kumar:** no effect.
  - **Cement:** no firm-level link (the chain breaks here). The market-level test, a coarse labelled test with little power, gives +2.5 pp over (−1,+5) (p = 0.34): propagation **not detected**. The variant against two documented zero-capacity makers was dropped (it rested on Star Cement and Prism Johnson; no cause for Star's fall was found). UltraTech says only North infrastructure fell, for three reasons, while housing and commercial grew.
  - **Register:** six firms attribute an effect to the ban (NBCC, DLF, Ahluwalia, Ashiana, Godrej Properties, UltraTech in part). Signature Global's Q3 transcript is to be downloaded by hand by the user.
  - **NBCC's upstream branch: closed.** Its GPRA contractors (Varindera Constructions, Shapoorji Pallonji & Co. Pvt, Girdhari Lal Constructions Pvt; from NBCC's filings) and Gaursons on Amrapali (trade press) were unlisted in Nov 2024: no price or filed quarterly data (`research/realign/nbcc_contractors.csv`).
- **Gujarat (decision G7 taken 23 Nov 2026, `research/realign/G7_recommendation.md`):**
  - **The Gujarat hit firms are all external to the pack**, graded at G7:
    - *Material:* Tata Chemicals (Mithapur: about 10 days; 30,000 t soda ash and 40,000 t salt) and Archean (Kutch: Rs 40.18 cr of salt stock lost to "Asna cyclone").
    - *Confirmed, immaterial:* Adani Ports (Mundra and Tuna, "4 days equivalent"; August cargo still +5% YoY) and GE T&D India (Vadodara, production disruption, no damage; sales +59%).
  - **The storm system was Asna:** the deep depression of 25–30 Aug 2024 over Saurashtra and Kutch that became Cyclonic Storm "Asna" (IMD Tropical Cyclone Advisory No. 1, 30 Aug 2024). Mithapur and Kutch are outside the pack's listed districts.
  - **Two rain episodes** (NASA POWER): 18–24 Jul and 25–31 Aug 2024 (Jamnagar 288 vs 525 mm, Porbandar 610 vs 502 mm, Kachchh 86 vs 360 mm). Tata Chemicals dates its loss to "July and August", so it cannot be split between them; Archean's loss is the late-August storm alone.
  - **Archean's −15.8% price fall** is −11.7% net of specialty-chemical peers (one-sided p = 0.04); it fell 1.0–2.6% a day as Kachchh took 61–98 mm (26–29 Aug), then 4.8% on 2 Sep in 1 mm of rain, after a +7.5% jump on 22 Aug; no company news found. At about Rs 1,560 cr it is 30–40 times the Rs 40 cr booked loss. **Not attributed.**
  - **Tata Chemicals' share price shows nothing:** −0.1% abnormal over 26–30 Aug, +1.1% on its results day (daily s.d. 2.3%): the shock is documented in statements and tonnes, not in the price.
  - **The pack's chemical belt** is kept as its own branch. Its Vadodara sites went dark on 30 Aug, but no pack firm attributes an effect: the chain breaks at Step A.
  - **Forward chain (H2), Tata Chemicals → Tata Consumer (edible salt): verified and material, a cost pass-through, not a shortage.**
    - Both sides document the link: Tata Chemicals calls Tata Consumer the "single customer" for edible salt; Tata Consumer sources "more than 85% of the salt we offer in the market" from Tata Chemicals. FY24 weights: 18–24% of Tata Consumer's material inputs, 10–36% of Tata Chemicals' sales.
    - Mithapur had to buy brine; the cost reached Tata Consumer a quarter later; Tata Consumer raised the price of Tata Salt **once**, by ₹2 on a ₹28 pack (about 7%), from October 2024; margin held.
    - Measured by quarter (`stepC_gj_tcpl_salt.csv`): implied salt price/mix +1, +2, +6, +8 pp (Q1–Q4 FY25) beside volume +8%, 0%, +1%, +5%: cost, not shortage. Magnitude (`stepC_gj_salt_magnitude.csv`): the increase is worth at least Rs 110 cr a year against a whole storm cost of about Rs 40 cr: partly a catch-up after two years without an increase.
    - Results-day returns are not attributed to salt: Tata Consumer −6.7% on 21 Oct 2024 (tea-driven by its own account); Tata Chemicals +1.1% on 18 Oct. Its +4.3% on 10 Oct (after Ratan Tata's death) and +10.4% on 21 Oct (RBI ruling on Tata Sons' listing) are unrelated.
- **H2–H4, propagation (Step E, `table2_*`, `table3_placebo.csv`):**
  - **Dose-response, NCR (backward, H3):** dose = builder's share of the contractor's sales × builder's NCR exposure, across 8 contractors (3 linked, 5 at zero dose). No relation with any CAR (exact permutation p = 0.67–1.00). The one "significant" slope, Q3 sales growth (p = 0.05), is matched by the same slope on the pre-ban quarter (p = 0.05): it is B.L. Kashyap's earlier decline, and it vanishes on the change in growth (p = 0.79) or without B.L. Kashyap. **Result: null, with n = 8.**
  - **Gujarat (forward, H2):** one verified link; propagation shows as a cost pass-through into the retail price, not as a price or volume shock at the buyer.
  - **Placebos:** unexposed, unlinked firms and the G2 controls return nulls (NCR placebo firms: mean CAR −1.3% to +2.3%, p = 0.30–0.83). Gujarat placebo list approved with changes: Reliance Power dropped (−20.7% after SEBI's order of 22 Aug 2024 against Anil Ambani); without it mean −3.6% (p = 0.21), median −2.1%; half of Unitech's −16.7% is a market-model artefact; Tata Steel flagged. The Gujarat controls fell together in the storm week (−4.7%, all six firms; cause not identified).
  - Two earlier results remain **withdrawn**: the scaffold test (unverified industry-level guesses) and the earlier "verified links" test (archived README §5.5: wrong NCR hit firms, Petronet links without a confirmed source shock, the Aarti–UPL joint venture before it supplied).

## Problems found in the pack (handled in `src/common.py`; do not undo)

| Issue | Effect if ignored | Handling |
|---|---|---|
| **Stock dates are one day early** for 60 of 61 firms (trading days appear Sunday–Thursday; RAJESHEXPO alone is right) | Every event window is off by a day | Shifted +1 day |
| **Himachal exposure is wrong.** Substring matching on "una", "bilaspur", "hamirpur" also catches Guna, Junagadh, Virudhunagar, Yamunanagar, Bilaspur (Chhattisgarh), Hamirpur (UP), Arunachal Pradesh | 47 of 83 "Himachal" plant rows are in other states | Exact district lists |
| Keywords "tiruvallur" and "panchmahal" never match the data's "Thiruvallur" and "Panch Mahals" | Chennai and Gujarat exposure understated | Added |
| GRAP event date in the pack is 5 Nov 2024; Stage III was ordered on the evening of 14 Nov (in force 08:00, 15 Nov, a market holiday) and Stage IV from 18 Nov | Wrong window, two weeks early | Verified dates from CAQM's own releases; first trading day 18 Nov 2024 |
| 20 of 81 firms have no prices (merged or delisted) | Sample is 61 firms | Dropped from return tests |
| Financials are one quarter for 64 firms; `revenue_proxy_cr` is in rupees, not crore; capex is empty | No before/after test on fundamentals | Quarterly statements fetched from screener.in (`external/fin_quarterly.csv`) |
| NMDC +86% on 26 Oct 2022 (demerger, unadjusted); 23 Jun 2020 duplicated for every firm | Outliers in estimation windows | Removed |
| 25% of plants have zero project cost; some "districts" are state names | Cost shares are relative weights only | Used as shares, never as rupee levels |

## Method of the direct event study (engine in `src/es_lib.py`)
- **Model:** market model against NIFTY 500, estimation window [−250, −30] trading days.
- **Inference:** abnormal returns are compared with the same statistic on 1,000 random placebo dates, which allows for same-day correlation across firms.
- **Exposure:** plant cost in the event districts ÷ firm's total plant cost, on the corrected footprints.
- **Reproduce the earlier layout:** `python3 src/03_event_study.py`. The new deliverable scripts are numbered from `src/40_…`.

## Folder map
- `data/`, `docs_from_pack/`: the pack and the assignment.
- `src/`:
  - `40_…` onward build the deliverables; `55`–`59` were added on 23 Nov 2026 (G5/G7 corrections: `55` contractor windows net of unlinked contractors and disclosure days, `56` rain episodes and Archean vs peers, `57` Tata Consumer salt by quarter; Step E: `58` dose-response and placebo tables, `59` pathway diagrams and lag figure; checkpoint 4: `60` memo figure, `61_build_memo.sh` memo PDF).
  - `03` (direct event study), `07` (financials), `11`–`12` (announcements, transcripts) and `18` (quote check) are still used.
  - `05` and `10` are superseded.
  - The rest belongs to the archive.
- `research/`: evidence collected so far. `research/realign/` holds the realignment evidence, with the saved text of every document read (`docs/`).
- `outputs/deliverables/`: the deliverables. `outputs/tables`, `outputs/figs`: earlier outputs.
- `archive/`: the earlier README (`README_rounds1-4.md`), handover, to-do list and request list.

## Archived (kept, not extended, not a deliverable)
Archived work:
- rainfall, river and IMD hazard panels
- night lights, radar, optical and NRSC flood maps, nitrogen dioxide
- state electricity and GST flows
- the out-of-sample test
- pricing, expected outage loss and the firm risk card
- the Delhi air-quality panel
- the Chennai and Himachal analysis

Full write-up: `archive/README_rounds1-4.md`. Scripts `04`, `06`, `08`, `09` and `13`–`33` produced it.
