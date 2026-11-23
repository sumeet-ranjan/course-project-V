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
| 1 | Traced-pathway diagram + evidence table per node, NCR | `pathway_NCR.*`, `evidence_NCR.csv` | Steps A–B done (G3, G4); Steps C–D done (`stepC_ncr_*`, `cement_market_test*`); decision G5 with the user |
| 1 | The same, Gujarat | `pathway_GJ.*`, `evidence_GJ.csv` | Step A outside the pack done (`gj_hit_firms_docs.csv`); Tata Chemicals → Tata Consumer chain traced; decision G7 with the user |
| 2 | Verified supply-chain links file, replacing the scaffold | `verified_links.csv` (built by `src/40_links_file.py`) | G1 and G4 applied (127 rows). Each row carries the external, footprint and trade flags. Contractor links: Ahluwalia ← DLF verified and material; B.L. Kashyap ← DLF verified, site hit not documented; B.L. Kashyap ← Anant Raj held; J. Kumar ← NBCC low dose. Cement/steel rows are not verified, with a materiality bound |
| 3(i) | Direct event study / DiD | `table1_direct.csv`, `table1_direct_firms.csv`, `table1_returns_25nov2024.csv`, `table1_did.csv` (read with `table1_notes.md`) | first version done (Step 1, 23 Nov 2026), on the G2 firm sets |
| 3(ii) | Propagation dose-response | `table2_dose_response.csv` | not started |
| 3(iii) | Placebos | `table3_placebo.csv` | placebo firm lists drafted (`placebo_firms.csv`, Gujarat list provisional); tests not run |
| 4 | Memo, 3–5 pages | `memo.md` | not started |
| — | Hit-firm registers (scope change, 23 Nov 2026) | `hit_register_NCR.csv`, `hit_register_GJ.csv` | first version: NCR 45 rows, Gujarat 21 rows (Tata Consumer rows pending) |

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
- **NCR Steps C–D (decision G5 pending, `research/realign/G5_recommendation.md`):**
  - **Hit firms:** NBCC and DLF state the hit, but show no price effect (−1.5% and +5.8% over (−1,+5)). DLF's construction outflow rose in the ban quarter (Rs 521 cr to Rs 591 cr).
  - **Ahluwalia (DLF's contractor, within zone):** the mechanism is documented end to end.
    - Its statements: margin guidance muted for GRAP-IV in Nov 2024; FY25 growth cut to 8.5–9%; idle labour paid by clients including DLF; January also hit; restart on 3–4 Feb.
    - Its numbers: Q3 sales −7.2% YoY, then Q4 +28% QoQ.
    - Its price: −19.5% over the second episode's (+6,+20) (p = 0.02) and −33% over (+21,+60) (p = 0.02), the windows that carry its disclosures.
  - **B.L. Kashyap and J. Kumar:** no effect.
  - **Cement:** no firm-level link (the chain breaks here). The market-level test is null or the wrong sign. UltraTech says only North infrastructure fell, for three reasons, while housing and commercial grew.
  - **Register:** six firms attribute an effect to the ban (NBCC, DLF, Ahluwalia, Ashiana, Godrej Properties, UltraTech in part).
- **Gujarat (decision G7 pending, `research/realign/G7_recommendation.md`):**
  - **The Gujarat hit firms are all external to the pack.**
    - Tata Chemicals: Mithapur, about 10 days, 30,000 t soda ash and 40,000 t salt lost.
    - Archean: Kutch, Rs 40.18 cr exceptional loss of 4.72 lakh t salt stock, attributed to Cyclone Asna.
    - Adani Ports: Mundra and Tuna, "4 days equivalent".
    - GE T&D India: Vadodara, production disruption.
  - **Mithapur and Kutch** were hit by the same storm system, outside the pack's listed districts: the deep depression of 25–30 Aug 2024 that became Cyclonic Storm "Asna" (IMD Tropical Cyclone Advisory No. 1, 30 Aug 2024).
  - **The pack's chemical belt** is kept as its own branch. Its Vadodara sites went dark on 30 Aug, but no pack firm attributes an effect: the chain breaks at Step A.
  - **Forward chain (H2), Tata Chemicals → Tata Consumer (edible salt):** documented on both sides.
    - Tata Chemicals: TCPL is the "single customer" for its edible salt.
    - FY24 purchases Rs 1,576.64 cr: 18–24% of Tata Consumer's material inputs, and 10–36% of Tata Chemicals' sales.
    - Tata Consumer's Q2 FY25 call describes a cost pass-through: Mithapur had to buy brine, the cost "flows in into our system", and Tata Salt prices rose by ₹2.
    - Margin held and volumes grew. Q3 brought a 7% price rise, with no margin expansion.
    - The price fell 6.7% on 21 Oct 2024, the first trading day after its results; the company attributes the margin pressure to tea costs.
- **H2–H4, propagation:** no result yet. Two earlier results are **withdrawn**:
  - the scaffold test, which ran on unverified industry-level guesses;
  - the earlier "verified links" test (archived README §5.5), which used the wrong NCR hit firms, counted Petronet links without a confirmed source shock, and counted the Aarti–UPL joint venture, which was not yet supplying.

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
  - `40_…` onward build the deliverables.
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
