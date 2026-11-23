# Next steps: plan built from GAP_MAP.md, in the order of INSTRUCTIONS §7

**Status, 23 Nov 2026:**
- Done: plan approved; Step 0 (correcting the record); decision G1 accepted and applied (`outputs/deliverables/verified_links.csv`).
- NCR Step A evidence collected and quote-checked (`research/realign/ncr_stepA_evidence.csv`).
- G2 and G3 decided by the user on 23 Nov 2026 (see README, "Decisions").
- January 2025 Stage III orders added to the record.
- **Step 1 done (checkpoint 1):** `outputs/deliverables/table1_*`, placebo lists in `placebo_firms.csv`.
- **Step B for NBCC and DLF done (checkpoint 2):**
  - Evidence: `research/realign/stepB_*.csv`.
  - Links: `src/46_stepB_links.py`, rows N001–N084 of `outputs/deliverables/verified_links.csv`.
  - G4 decided by the user on 23 Nov 2026 and applied.
- **NCR Steps C–D done (checkpoint 3); G5 decided by the user on 23 Nov 2026 and applied** (`research/realign/G5_recommendation.md`, rewritten as the decided record).
- **Gujarat Step A outside the pack and the Tata chain done; G7 decided by the user on 23 Nov 2026 and applied** (`research/realign/G7_recommendation.md`).
- **Checkpoint 4 (23 Nov 2026): G5/G7 corrections, Step E, dose-response, placebos and the memo draft.**
  - G5: release times and window dates verified (`research/realign/g5_timing_docs.csv`); Ahluwalia's disclosure days and every window net of the unlinked contractors with placebo p (`src/55`, `stepC_ncr_contractor_net.csv`, `stepC_ncr_disclosure_days.csv`); Q4 YoY and FY25 from the company's Q4 call; cement variant dropped (`news_checks.csv`).
  - G7: hit firms graded; rain episodes (`src/56`, `gj_rain_episodes.csv`); Archean vs specialty peers and news; one retail price increase (₹2 on ₹28, about 7%); 85% item closed; Tata Consumer salt by quarter (`src/57`, `stepC_gj_tcpl_salt.csv`); Tata Chemicals' 10 Oct and 21 Oct moves sourced.
  - Step E: `pathway_NCR`, `pathway_GJ`, `fig_lag_paths` (`src/59`); `table2_dose_response*`, `table3_placebo.csv` (`src/58`); `memo.md` (draft).
- **Open, for the user:** (1) review the memo draft and the two diagrams; (2) the final causal claim (§5) is yours: the memo states the evidence grading, not a verdict; (3) the Gujarat placebo list is still provisional; (4) Signature Global's Q3 FY25 transcript (your manual download) goes into the NCR register when it arrives.
- **Open, documents not obtained:** Tata Consumer's Q2 FY25 investor deck (Q2 salt revenue growth; NSE 403, company copy empty); GE T&D's 27 Aug 2024 notice; the contractors on NBCC's Amrapali and GPRA projects; a documented site hit at B.L. Kashyap.

**Scope:** `docs_from_pack/INSTRUCTIONS.md` and `docs_from_pack/README.md` only. `HANDOVER.md` still
holds for environment setup, data traps and permissions. The previous to-do list is kept in
`archive/NEXT_STEPS_round4.md`.

**Rules for every step**
- A task is done only if it serves one of the four deliverables in §6.
- Nothing enters a deliverable until its original document has been read. Each evidence row carries
  the URL, document, page, a verbatim quote, and `read_mode = original`.
- Which links are real, which mechanism holds, what is a confound, and the final causal claim are your
  calls (§5). Each gate (◆) goes to you as a recommendation with its evidence; work that depends on it waits.
- A null is a result. If a chain breaks, the diagram shows where.
- Deliverables go in `outputs/deliverables/`.

## 0. Correct the record (no new analysis)
- 0.1 Remove the scaffold result from README's findings: bottom-line item 5, §3 "Propagation", and the pass-through row in §4. Mark `05_propagation.py` and `propagation_scaffold.csv` as superseded.
- 0.2 Withdraw the link-test result (README 5.5, `propagation_verified_links.csv`). Its NCR hit firms were wrong, and its Petronet and Aarti–UPL links do not qualify.
- 0.3 Restructure the links file. Add columns `status` (verified / held / rejected + reason), `live_from`, `live_to` and `read_mode`, plus two weights, each with a low–high bracket and its basis:
  - `w_buyer_input_cost` (supplier's share of the buyer's input cost; forward test, H2)
  - `w_supplier_sales` (buyer's share of the supplier's sales; backward test, H3)
  - **◆G1:** your call on each existing row.
- 0.4 README and HANDOVER: state the assignment as the scope. Move off-scope sections under "archived, not a deliverable".
- 0.5 MANUAL_DATA_REQUESTS: keep only the items that serve a deliverable: M3, M12, M11, M1b, M1c, M1d. Drop the rest.

## 1. Direct event study on the two key events (§7.1) → deliverable 3(i)
- **1.1 ◆G2:** exposed sets and matched controls.
  - My recommendation: exposed = firms with ≥25% of plant cost in the corrected footprint.
  - Matched controls = listed firms in the same industry with no plant in the zone, matched on size. Out-of-sample peers are allowed; their prices come from the existing Yahoo fetcher.
  - Torrent Power is out of the controls. Adani Green and Adani Power come out of the NCR controls if you agree they are confounded.
- 1.2 Event dates:
  - NCR: 18 Nov 2024, the first trading day of Stage III and Stage IV; 17 Dec 2024 for the re-imposition.
  - Gujarat: 26 Aug 2024.
- 1.3 Method: market-model CARs over (−1,+5), (+6,+20) and (+21,+60), which do not overlap. Inference by placebo-date bootstrap, which handles same-day correlation. Pooled GRAP recurrences, clustered by event date, as a robustness check.
- 1.4 Quarterly DiD, exposed vs matched controls, with firm and quarter fixed effects, on revenue growth and EBITDA margin.
- Output: `table1_direct.csv` and a short note.

## 2. NCR, Steps A–B (§7.2) → deliverables 1 and 2
- 2.1 Step A for NBCC and DLF, plus Anant Raj if a document exists:
  - exchange filings (already read: none)
  - Q3 FY25 calls (DLF and NBCC read; Anant Raj missing, M11)
  - original news articles
  - ban dates from the CAQM orders, read on caqm.nic.in if it answers
  - **◆G3:** which builders count as confirmed hit firms.
- 2.2 Step B: find the confirmed builders' named cement and steel suppliers in:
  - annual-report related-party and supplier notes
  - placement documents
  - NBCC procurement awards
  - cement and steel firms' customer disclosures
  - trade and vendor data (M12)
  - The aim is 2–3 real links, weighted by `w_supplier_sales`. If none is disclosed, I will show you the fallback: each supplier's NCR or North-region sales share.
  - **◆G4:** which links are real and material, and whether the fallback counts.

## 3. NCR, Steps C–D, lag and placebo (§7.3) → deliverables 1 and 3(iii)
- 3.1 CAR for each node over the §4 windows, and CAR by week since the order. The lag is read for suppliers vs builders.
- 3.2 Q3 FY25 results filings for each node: revenue, EBITDA margin, inventory, input cost and guidance. Monthly northern cement despatches if you supply M1c.
- 3.3 Step D:
  - Supplier breadcrumbs: UltraTech's own Q3 FY25 release; Shree Cement, ACC and steel-maker documents.
  - Confound checklist: the market, cement-sector demand, the Adani indictment of 21 Nov 2024 (ACC), and the IGL gas cut (IGL is excluded).
  - **◆G5:** mechanism and confounds.
- 3.4 Maruti screen: its Q3 FY25 call and filings, checked for a GRAP effect. **◆G6:** promote it to a branch only if one is found.
- 3.5 Placebo: the same node tests on unexposed, unlinked firms and on the Stage III dates of 2022 and 2023.
- 3.6 Step E: `pathway_NCR` diagram and `evidence_NCR.csv` (date, source, quote, CAR, Δfinancial and lag for each node).

## 4. Gujarat chemicals chain (§7.4) → deliverables 1, 2 and 3
- 4.1 Step A, firm by firm, from original news, filings, calls and parliamentary answers: GSFC, Gujarat Alkalies, GNFC, SRF, Aarti, Kiri and Bodal. Plant production too, if you supply M1b. **◆G7:** the confirmed hit firms, or stop here and record the null.
- 4.2 Step B, only if G7 confirms a firm: downstream buyers weighted by `w_buyer_input_cost`, from raw-material cost notes, customer disclosures and trade data. **◆G8:** which links are real.
- 4.3 Steps C–E as for NCR. **◆G9:** mechanism and confounds. Then the diagram and the evidence table.

## 5. Generalise and write up (§7.5) → deliverables 2, 3(ii), 3(iii) and 4
- 5.1 Final `verified_links.csv`, replacing the scaffold.
- 5.2 Dose-response:
  - Model: downstream CAR (and Δmargin) on dependence × hit severity.
  - Controls: own direct exposure, sector and size.
  - Sample: all verified links. The number of links and the power are reported plainly.
- 5.3 Placebo table: control firms and unexposed, unlinked firms, with the same specifications.
- 5.4 Memo, 3–5 pages: what was found, how strong it is, and what the manual trace caught that an automated pipeline would have missed or got wrong. **◆** Final causal claim: yours.
- 5.5 Update README and HANDOVER, then make a fresh zip.

## Data you may be asked for (only items that serve a deliverable)
- **M3:** supplier and customer links (Step B).
- **M12:** customs shipment records (Step B).
- **M11:** Anant Raj, Gujarat Alkalies and Shree Cement transcripts (Steps A and D).
- **M1b:** Gujarat plant production (Steps A and C).
- **M1c:** northern cement despatches (Step C).
- **M1d:** RERA construction progress (Step A).
