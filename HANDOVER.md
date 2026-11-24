# Handover: climate shocks and supply-chain propagation in India

**Dated 24 Nov 2026. Final state.** This file is a self-contained briefing for a reader, human or AI agent, who receives
only this folder. It describes where the work stands, not how it got there. The history is in `archive/` (the previous
handover is `archive/HANDOVER_realign_2026-11-23.md`).

**Final counts:**
- **Links file:** 128 rows (4 verified links).
- **Quotes:** 976 evidence rows checked against the saved originals, 812 verified, 0 not found.
- **Cement plants:** 217 rows, of which 205 grey-cement plants of 24 makers enter the test; 22 lie within 300 km of
  Delhi.
- **Hit-firm registers:** 45 rows (NCR) and 40 (Gujarat).
- **Memo:** 5 A4 pages.

---

## 1. What this is

**The assignment.** `docs_from_pack/INSTRUCTIONS.md` is the only definition of scope (with `docs_from_pack/README.md`).
Where any other file disagrees, the assignment wins. A task that does not serve one of its four deliverables is not
done.

**Research question.** When a localized, documented extreme event damages the physical plants of a listed firm, does the
shock propagate along the supply chain to firms that were never in the disaster zone, and can the pathway be traced in
real data? There are two deep-dives:
- **E_NCR_GRAP_2024:** the Delhi-NCR construction ban under GRAP Stage III/IV, Nov–Dec 2024.
- **E_GJ_FLOOD_2024:** the pack's "Gujarat floods — Vadodara/central Gujarat", which was in fact the deep depression that
  became Cyclonic Storm Asna on the Saurashtra and Kutch coast, Aug 2024.

**Hypotheses (brief §1):**
- **H1, direct:** firms with a plant in the event district respond negatively against matched controls.
- **H2, forward:** buyers of a hit supplier, outside the zone, respond with a lag, scaled by input dependence.
- **H3, backward:** suppliers to a hit firm lose offtake, with a smaller, lagged response scaled by revenue dependence.
- **H4, dose-response and placebo:** effects grow with exposure × severity × dependence, and unlinked, unexposed firms
  show nothing.

**The four deliverables (brief §6):**
1. A traced-pathway diagram per event, with an evidence table per node.
2. The verified links file, replacing the scaffold.
3. Results tables: (i) direct, (ii) dose-response, (iii) placebos.
4. A 3–5 page memo, including what the manual trace caught that an automated pipeline would miss.

**Who decides what (brief §5).**
- **The author** (the student who owns this project) decides which links are real and material, which mechanism the
  evidence supports, what counts as a confound, and the final causal claim.
- **The agent** collects, computes and drafts. It puts each decision to the author as a recommendation with its
  evidence, and dependent work waits.

All past decisions are logged in §8.

## 2. Read order: the five files to open first

1. `HANDOVER.md` (this file).
2. `docs_from_pack/INSTRUCTIONS.md`: the brief.
3. `outputs/deliverables/memo.md` (or `memo.pdf`): the findings as the author submits them. Its Conclusion is left to
   the author.
4. `README.md`: the project page, the deliverables index and the list of pack errors.
5. `outputs/deliverables/table2_notes.md`: the longest methods note (dose-response, and the cement test's specification,
   amendments and results). Then read `table1_notes.md` and `table3_notes.md`.

## 3. Findings in ten lines

| # | Finding | Hypothesis | Strength |
|---|---|---|---|
| 1 | NCR: NBCC and DLF (pack firms) state the hit in their own words (GPRA and Amrapali; two malls delayed). Neither stock responded: +0.4 pp against developers with no NCR project, p = 0.91. | H1 | hit documented; no price effect |
| 2 | NCR: the ban passed from builder to contractor at NCR sites. Ahluwalia (external; DLF is 3.4–10% of its sales; 33.3% of its order book is in NCR, so it is also directly exposed) lost "two months in Q3 and nearly a month in Q4". FY25 grew +6.3% against 8.5–9% guided. | H3 (inside the zone) | documented; price evidence weak |
| 3 | NCR, Ahluwalia's price: 18 Nov mixes ban day 0 with its Q2 results (own −2.8%, p = 0.16; net of comparison −4.7%, p = 0.04). The call days that price its ban statements are not distinguishable from zero. Later large falls hold no disclosure and are not attributed. | — | weak |
| 4 | NCR, other nodes: B.L. Kashyap's hit is not documented; J. Kumar shows no effect (low dose); NBCC's GPRA contractors were unlisted, so that branch is closed. | H3 | — |
| 5 | NCR, out of the zone: no firm-level cement or steel link exists. The cement delivery test (share of a maker's plants within 300 km of Delhi) is null in every window and specification (p ≥ 0.23), and cannot detect the ban's largest possible loss. Steel stops at the materiality bound. | H3 | not detected (low power) |
| 6 | NCR dose-response over 8 contractors: no slope (exact permutation p = 0.67–1.00). | H4 | null, n = 8 |
| 7 | Gujarat: the pack's Vadodara chemical belt breaks at the first step. Sites went dark, no firm says anything, and the stocks beat their controls (+5.5 pp, p = 0.05). | H1 | breaks |
| 8 | Gujarat hit firms, all external. Material: Tata Chemicals at Mithapur (about 10 days; about Rs 40 cr) and Archean in Kutch (Rs 40.18 cr of salt stock). Confirmed but immaterial: Adani Ports, GE T&D. No share-price signal at Tata Chemicals; Archean's fall is not attributed. | H1 (outside the pack) | documented |
| 9 | Gujarat link, Tata Chemicals → Tata Consumer (edible salt; 18–24% of Tata Consumer's material inputs). The cost is stated by both firms and was passed into one Tata Salt increase of about 7% (Oct 2024), with margin held. A storm-quarter volume stall at both firms is unexplained and consistent with lost supply. | H2 | documented; partly a catch-up; no price effect at either firm |
| 10 | Placebos are null (NCR 24 firms; Gujarat list without Reliance Power). Overall, transmission is documented inside the NCR zone and along one Gujarat link; out-of-zone propagation is not detected. The final causal claim is the author's. | H4 | — |

## 4. Deliverables index (`outputs/deliverables/`)

Row counts are data rows (header excluded). "Built by" is the script that writes the file. `src/64` then rewrites the
label columns in plain words.

| File | What it holds | Built by | Size |
|---|---|---|---|
| `pathway_NCR.png`, `pathway_NCR.svg` | Deliverable 1, NCR diagram | `src/59` | 1 figure |
| `pathway_GJ.png`, `pathway_GJ.svg` | Deliverable 1, Gujarat diagram | `src/59` | 1 figure |
| `fig_lag_paths.png` | Lag at each hop, both events | `src/59` | 1 figure |
| `evidence_NCR.csv` | Evidence per node, NCR (date, source, quote, CARs, Δfinancials, lag, status) | `src/47` | 132 rows |
| `evidence_GJ.csv` | Evidence per node, Gujarat | `src/53` | 97 rows |
| `verified_links.csv` | Deliverable 2: links with status, weights (brackets and basis), sources, external and in_pack_footprint flags | `src/40` (inputs `src/46`, `src/54`) | 128 rows |
| `table1_direct.csv` | Deliverable 3(i): direct event study by event, group, window (with zero-alpha columns) | `src/43` | 92 rows |
| `table1_direct_firms.csv` | Firm-level CARs behind table 1 | `src/43` | 60 rows |
| `table1_did.csv` | Quarterly DiD (descriptive) | `src/43` | 8 rows |
| `table1_returns_25nov2024.csv` | Returns around 25 Nov 2024 (Stage IV news) | `src/43` | 16 rows |
| `table1_notes.md` | How to read table 1 | hand-written | 56 lines |
| `table2_dose_response.csv` | Deliverable 3(ii): panels A (NCR contractors), B (Gujarat link), C (cement delivery test), C2 (old market test) | `src/58` | 76 rows |
| `table2_dose_response_fit.csv` | Slopes and exact permutation p for panel A | `src/58` | 45 rows |
| `table2_cement_makers.csv` | Cement makers: doses (count, 150 km, capacity), flags, CARs, quarterly outcomes | `src/63` | 24 rows |
| `table2_cement_fit.csv` | Every cement regression (sample × dose × outcome) with placebo or permutation p | `src/63` | 106 rows |
| `cement_plants_geo.csv` | Every cement plant with geocode, road and straight distance to Delhi | `src/62` | 217 rows |
| `table2_notes.md` | How to read table 2, incl. the cement test's specification (written before the run), amendments, results and earlier runs | hand-written | 356 lines |
| `table3_placebo.csv` | Deliverable 3(iii): placebo groups, mean and median CARs, placebo-date p | `src/58` | 30 rows |
| `table3_placebo_firms.csv` | Firm-level placebo CARs with flags | `src/58` | 294 rows |
| `placebo_firms.csv` | Placebo and control lists, with reasons for every exclusion | `src/45` | 122 rows |
| `table3_notes.md` | How to read table 3 | hand-written | 53 lines |
| `memo.md`, `memo.pdf`, `memo.html` | Deliverable 4, the memo (PDF 5 A4 pages; Conclusion left to the author) | hand-written; `src/61_build_memo.sh` | 225 lines; 5 pages |
| `fig_memo_pathways.png` | The memo's figure | `src/60` | 1 figure |
| `hit_register_NCR.csv`, `hit_register_GJ.csv` | Every firm screened as a possible hit firm, with status and grade | `src/51` | 45, 40 rows |
| `stepC_ncr_node_cars.csv`, `stepC_ncr_quarterly.csv` | NCR node CARs and quarterly numbers | `src/49` | 78, 30 rows |
| `stepC_ncr_contractor_net.csv`, `stepC_ncr_disclosure_days.csv`, `stepC_ncr_unlinked_flags.csv` | Contractor windows net of the comparison group (with and without takeover targets, zero-alpha), disclosure days, comparison flags | `src/55` | 36, 4, 2 rows |
| `stepC_gj_node_cars.csv`, `stepC_gj_quarterly.csv`, `stepC_gj_results_days.csv`, `results_days_extra.csv` | Gujarat node CARs, quarterly numbers, results days | `src/52` | 18, 24, 7, 1 rows |
| `stepC_gj_tcpl_salt.csv`, `stepC_gj_salt_magnitude.csv` | Salt by quarter (Tata Consumer and Tata Chemicals); storm cost against the price increase | `src/57` | 5, 4 rows |
| `gj_rain_episodes.csv`, `gj_rain_7day_max.csv`, `gj_archean_vs_peers.csv`, `gj_archean_daily_ar.csv`, `gj_tatachem_price.csv` | Rain episodes, Archean against peers and by day, Tata Chemicals' price | `src/56` | 6, 78, 8, 13, 11 rows |
| `cement_market_test.csv`, `cement_market_test_doses.csv`, `cement_market_test_firms.csv` | The earlier market-level cement test (kept as the comparison) | `src/50` | 12, 10, 60 rows |

## 5. Folder map and run order

| Folder or file | What it is |
|---|---|
| `docs_from_pack/` | The pack's brief (`INSTRUCTIONS.md`), `README.md`, `DATA_DICTIONARY.md` and the sample builder `build_real_sample.py` |
| `data/` | The pack's data, 7 CSVs. Always read through `src/common.py`, which fixes its errors (§6). |
| `external/` | Fetched datasets (§6) |
| `research/realign/` | This work's evidence: 41 CSVs (quote, source, `saved_text` per row); `docs/` with 518 saved document texts; the decision records `G2_G3_recommendation.md`, `G4_recommendation.md`, `G5_recommendation.md`, `G7_recommendation.md`; the frozen cement-test specification `cement_test_spec_20261123*.md`; the quote check `quote_check_realign.csv` |
| `research/transcripts/` | 27 earnings-call transcripts read for the hit-firm screens |
| `research/*.csv`, `research/nse_announcements/`, `research/proxy/` | Earlier rounds' evidence. A few files are still read, e.g. `verified_links_all.csv` by `src/40` and `transcript_keyword_hits.csv` by `src/51`. |
| `src/` | Scripts (below) |
| `outputs/deliverables/` | The deliverables (§4). `outputs/tables/` and `outputs/figs/` are earlier rounds' outputs, archived. |
| `archive/` | Earlier handovers, READMEs, plans and request lists |
| `manual_collection/` | Templates and request lists for data collected by hand (earlier rounds) |
| `GAP_MAP.md`, `NEXT_STEPS.md`, `MANUAL_DATA_REQUESTS.md` | The plan and its record |

**Live scripts.**
- `src/40`–`src/64`, `src/common.py` (data loading and the pack fixes), `src/es_lib.py` (event-study engine),
  `src/memo_style.css` and `src/memo_to_pdf.js` (memo build).
- `src/41`, `src/44` and `src/48` are one-off helpers of the gates (candidates, matching, round-2 fetches). Their outputs
  are saved in `research/realign/`.

**Archived scripts: do not extend.**
- `src/00`–`src/33` belong to earlier rounds (hazard panels, night lights, flood maps, pricing).
- Some produced inputs that are still used: `00` (indices, rainfall, district centroids), `07` (screener.in financials),
  `11`–`12` (announcements, transcripts) and `26` (price extension).
- `src/03` reproduces the earlier layout only.

**Rebuild (from the folder root).**

1. **Re-check quotes:** `python3 src/42_check_quotes_realign.py`, first whenever an evidence CSV changed. Later scripts
   use only rows that pass.
2. **Placebo and control lists:** `python3 src/45_g2_decision.py`.
3. **Table 1:** `python3 src/43_direct_event_study.py`. It fetches missing peer financials from screener.in.
4. **Links:** `python3 src/46_stepB_links.py`, then `python3 src/54_gj_links.py`, then `python3 src/40_links_file.py`.
5. **NCR nodes:** `python3 src/49_stepC_ncr.py`, then `python3 src/55_g5_contractor_net.py`.
6. **Cement:**
   - `python3 src/50_cement_market_test.py` (the old market test);
   - `python3 src/62_cement_geo.py` (geocodes come from `external/cement_geo_cache.csv`; only new places need the
     network);
   - `python3 src/63_cement_delivery_test.py` (about 5–8 minutes).
7. **NCR evidence:** `python3 src/47_evidence_tables.py`.
8. **Gujarat:** `src/52_stepC_gj.py`, then `src/56_g7_corrections.py`, `src/57_tcpl_salt_table.py` and
   `src/53_evidence_gj.py`.
9. **Registers:** `python3 src/51_registers.py`.
10. **Tables 2 and 3:** `python3 src/58_tables_dose_placebo.py`. `SKIP_PLACEBO=1` refits table 2 only.
11. **Diagrams:** `python3 src/59_pathway_diagrams.py`, then `python3 src/60_memo_figure.py`.
12. **Plain words:** `python3 src/64_plain_labels.py`. It is the last data step and rewrites the label columns of the
    deliverable CSVs.
13. **Memo PDF:** `bash src/61_build_memo.sh`. Check the printed page count: at most 5.
14. **Final check:** `python3 src/42_check_quotes_realign.py`. Expect 0 "NOT FOUND".

## 6. Data

**The pack** (`data/`) holds:
- `companies.csv`: 81 firms, with industry, plant counts and role;
- `plants.csv`: plants with district, coordinates and project cost;
- `financials_annual.csv`;
- `stock_daily.csv`: 2020–2025;
- `extreme_events.csv`;
- `event_plant_exposure.csv`;
- `supply_chain_scaffold.csv`: industry-based link guesses.

**Known errors in the pack.** These are fixed in `src/common.py` unless stated otherwise. **Do not undo them.**

| Error | Effect if ignored | Fix |
|---|---|---|
| Stock dates are one day early for 60 of 61 firms (RAJESHEXPO alone is right) | every window off by a day | shifted +1 day |
| "Himachal" exposure by substring ("una", "bilaspur", "hamirpur") also catches Guna, Junagadh, Virudhunagar, Yamunanagar, Bilaspur (Chhattisgarh), Hamirpur (UP), Arunachal Pradesh | 47 of 83 "Himachal" plant rows are in other states | exact district lists |
| Keywords "tiruvallur" and "panchmahal" miss "Thiruvallur" and "Panch Mahals" | Chennai and Gujarat exposure understated | added |
| GRAP dated 5 Nov 2024; Stage III was ordered on the evening of 14 Nov, in force 08:00 15 Nov (a market holiday); Stage IV from 18 Nov | window two weeks early | verified dates from CAQM; day 0 = 18 Nov 2024 |
| 20 of 81 firms have no prices | — | sample of 61 for returns |
| `financials_annual.csv` is one quarter; `revenue_proxy_cr` is in rupees; capex empty | no fundamentals test | quarterly statements from screener.in (`external/fin_quarterly.csv`) |
| NMDC +86% on 26 Oct 2022 (demerger, unadjusted); 23 Jun 2020 duplicated for every firm | outliers in estimation windows | removed |
| 25% of plants have zero project cost; some "districts" are state names | cost shares only relative | used as shares, never as rupee levels |
| `plants.csv` holds project records and at least one misplaced plant; not a list of cement plants | wrong cement doses | not used for cement: plants rebuilt from company documents (`research/realign/cement_plants_A–E.csv`) |
| The scaffold's links are industry guesses | false links | replaced by `verified_links.csv`; no cement/steel → builder link is verified at firm level |

**External datasets.** The date is the file date in `external/`; the source and script are given.

| File | Source | Script | Date |
|---|---|---|---|
| `indices_daily.csv`, `indices_extra.csv`, `indices_daily_2026.csv` | Yahoo Finance chart API (NIFTY 500 and sector indices) | `src/00`, `src/26` | 16–18 Nov 2026 |
| `indices_psu_infra.csv` | Yahoo Finance (Nifty PSE, Infra, Realty; tickers such as ^CNXPSE), fetched for the G2 benchmarks; no script writes it; read by `src/43`, `src/49` | — | 23 Nov 2026 |
| `prices_yahoo_2024_2026.csv` | Yahoo Finance (pack firms to Nov 2026, validated against the pack) | `src/26` | 18 Nov 2026 |
| `prices_peers.csv` | Yahoo Finance (firms outside the pack: contractors, cement makers, developers, placebo firms) | `src/41`, extended by `src/48` | 23 Nov 2026 |
| `fin_quarterly.csv`, `fin_annual.csv`, `market_cap.csv` | screener.in public pages | `src/07` | 16 Nov 2026 |
| `fin_quarterly_peers.csv`, `fin_annual_peers.csv`, `market_cap_peers.csv` | screener.in public pages | fetched on demand by `src/43`, `src/49`, `src/52`; `src/48`; `src/41` | 23 Nov 2026 |
| `shares_register.csv` | share counts for register firms without a screener.in market cap; read by `src/51` | — | 23 Nov 2026 |
| `rain_daily.csv.gz`, `rain_daily_2026.csv.gz` | NASA POWER (district points) | `src/00`, `src/26` | 16 and 18 Nov 2026 |
| `rain_imd_daily.csv.gz` | IMD 0.25° gridded rainfall | `src/31` | 18 Nov 2026 |
| `district_centroids.csv` | median plant coordinates per district in the pack's `plants.csv` | `src/00` | 16 Nov 2026 |
| `cement_geo_cache.csv` | OpenStreetMap Nominatim geocodes and OSRM public-router road distances | `src/62` | 23–24 Nov 2026 |
| `river_daily.csv.gz`, `pm25_daily_cams.csv` | Open-Meteo flood API; CAMS PM2.5 via Open-Meteo (earlier rounds) | `src/08` | 16 Nov 2026 |
| `ntl_*`, `flood_gfm_plant_pass.csv`, `no2_box_daily.csv`, `optical_chennai_plant_scenes.csv` | NASA Black Marble (Earthdata login), Copernicus GFM, Sentinel-5P, Sentinel-2/Landsat (earlier rounds; archived) | `src/13`–`src/30` | 17–18 Nov 2026 |
| IBM *Indian Minerals Yearbook 2022*, Cement (Table 1, plant capacities 2020-21) | Indian Bureau of Mines, `https://ibm.gov.in/writereaddata/files/1697613517652f86cd47a4fCement_2022.pdf` (copy supplied by the author) | text saved as `research/realign/docs/ibm__IMYB2022_cement.txt` | 24 Nov 2026 |

**Saved texts of documents read.**
- **Location and naming:** every document used as evidence is saved as text in `research/realign/docs/`, named
  `<prefix>__<SYMBOL>__<document>.txt`. Each evidence row names it in `saved_text`, and `src/42` checks its quote against
  it.
- **Prefixes, by the task that read the document:**
  - `cementA`–`cementE`, `cemcap`: cement plants, capacities and KPIs;
  - `events`: NSE announcement lists and filings, Oct–Dec 2024;
  - `makes`: NBCC makes, the CCI order, ready-mix pages;
  - `stepB_supplier`, `stepB_contractor`, `stepB_builder`: link screening;
  - `ncrA`, `ncr2`, `grap`, `maruti`: NCR hit-firm evidence;
  - `nbccctr`, `ordbook`: NBCC's contractors and contractors' order books;
  - `tatachain`, `tcplsalt`, `tcsalt`: the Tata chain;
  - `gjhit`, `gjplacebo`, `devctl`, `chemctl`: Gujarat hit firms, placebo screens, controls;
  - `news`: news checks; `ibm`: the IBM yearbook.
- **Older texts:** transcripts from earlier rounds are in `research/transcripts/` (e.g. `delhi_2024_NBCC_Feb2025.txt`).
- **Failed fetches:** a saved text that is an error page (403 or "Access Denied") is kept as the record of a failed
  fetch. Its rows are never verified.

## 7. Method

**Event study** (`src/es_lib.py`).
- **Model:** market model against NIFTY 500, estimated on trading days [−250, −30] before day 0. AR = R − (α + βM).
- **CARs:** sums of ARs over the window. A CAR needs prices on 70% of the window's days.
- **Inference:** the same statistic is computed on 1,000 random event days (about 800 for firms whose prices start in
  Jun–Aug 2021). The two-sided p is the share of placebo statistics at least as large in absolute value.
- **Event days:** NCR day 0 = 18 Nov 2024, second episode 17 Dec 2024; Gujarat day 0 = 26 Aug 2024.
- **Windows:** (−1,+3), (−1,+5), (+6,+20), (+21,+60), and single days (0,0) and (1,1) for results and call days.
- **Release times** come from exchange filing timestamps: an after-close release is priced the next trading day.
- **Zero-alpha CAR:** the same AR with α set to 0 and β kept (`ar_matrix(..., zero_alpha=True)`), reported beside the
  market-model CAR for (+6,+20) and (+21,+60). Long windows otherwise carry the estimation-window drift (Unitech's alpha
  term is −17.7 of its −23.5 pp).
- **Net of comparison:** a contractor's CAR minus the equal-weighted mean CAR of the five unlinked comparison contractors
  (NCC, PSP Projects, Cemindia (formerly ITD Cementation), L&T, Capacit'e), with the same placebo inference.
  - It is also reported without the two takeover targets, PSP (Adani Infra, 19 Nov 2024) and Cemindia (Renew Exim DMCC,
    25 Oct 2024).
  - It is reported on the zero-alpha basis too (`src/55`).
- **DiD:** quarterly, descriptive only (`table1_did.csv`).

**Firm sets and the files that define them.**
- **Hit firms:** `hit_register_NCR.csv`, `hit_register_GJ.csv`.
  - NCR confirmed: NBCC and DLF. Anant Raj, Parsvnath and Unitech are exposed, not confirmed.
  - Gujarat: Tata Chemicals and Archean (material); Adani Ports and GE T&D (immaterial).
- **Exposed sets and matched controls:** `research/realign/g2_decision.csv` (from `g2_exposed_sets.csv` and
  `g2_control_candidates.csv`). Controls are matched by sub-industry, then size.
- **Placebo firms:** `placebo_firms.csv`. NCR has 24 unexposed, unlinked firms; Gujarat has 12, after Reliance Power
  was dropped for SEBI's order of 22 Aug 2024. Tata Steel is flagged as a Tata group firm.
- **Comparison contractors:** the list `COMP` in `src/55`; flags in `stepC_ncr_unlinked_flags.csv`.
- **Cement makers:** `table2_cement_makers.csv`, with plants from `research/realign/cement_plants_A–E.csv`.
  - One row per group: Ambuja includes ACC, Sanghi and Penna.
  - The Ambuja group's denominator is 43 units (`cement_unit_counts.csv`).
  - Capacities come from `cement_capacity.csv`.

**Flags.**
- **`external`:** "yes" if the firm is not among the pack's 81 firms (`data/companies.csv`).
- **`in_pack_footprint`:** "yes" or "no" for pack firms, by the pack's exposure map with the fixes. External firms are
  "not established" unless a document places a site.
- Both are set in `src/40` and carried into the evidence tables and registers.

**Dependence weights** (`verified_links.csv`).
- **`w_supplier_sales`:** the buyer's share of the supplier's sales, used for contractors. Brackets are built from order
  books and contract run-rates, not reported sales shares:
  - Ahluwalia ← DLF 3.4–10%: low = the Arbour run-rate annualised ÷ FY24 income; high = DLF's share of the unexecuted
    order book at 31 Dec 2024;
  - B.L. Kashyap ← DLF 34.6–43.5%;
  - J. Kumar ← NBCC 1.6–3.4%.
- **`w_buyer_input_cost`:** the supplier's share of the buyer's input cost. Tata Chemicals is 18.2–24.0% of Tata
  Consumer's material cost (FY24).
- **Each `*_basis` column states how its bracket was built.**
- **Table 2's dose** = the bracket midpoint × the builder's NCR plant-cost share (DLF 0.42, NBCC 0.94).
- **No weight dated after Dec 2024 is used for NCR.**

**Cement delivery test.**
- **Specification:** in `table2_notes.md`, written before the run, with two amendments made before the run. Frozen
  copies with SHA-256 hashes are `research/realign/cement_test_spec_20261123.md` and `..._amended.md`.
- **Dose:** the share of a maker's plants within 300 km (and 150 km) of Delhi by OSRM road distance, with the share of its
  other northern plants as a control. A capacity-weighted version is the robustness check.
- **Outcomes and inference:** CARs with placebo-date p; Q3 FY25 volume and realisation YoY with permutation p, and Q2 as
  the pre-ban check.

## 8. Decision log

The deliverables carry no decision codes. This table explains them. G1–G9 are the decision gates of the plan
(`NEXT_STEPS.md`). The reviews are the author's review rounds. All dates are 2026.

| Code | Date | What the author decided | What it changed | Recorded in |
|---|---|---|---|---|
| G1 | 23 Nov | Legacy links: Aarti–UPL rejected (JV supplies only from FY 2026-27); Petronet → GAIL/IOC/BPCL/Torrent held (no Dahej shock); IGL, RVNL and Maruti links removed from the NCR test; Chennai rows out of scope; Gujarat Alkalies → NALCO and Shree's North market share as candidates | link statuses | `verified_links.csv`; README "Decisions" |
| G2 | 23 Nov | Exposed sets and controls. NCR: confirmed and unconfirmed builders reported apart; benchmark = all eligible developer controls; NBCC also against Nifty PSE; IGL, Adani firms and Torrent dropped; ACC flagged. Gujarat: both footprints, Vadodara defined by sites; DCW excluded; controls by sub-industry, then size | table 1 groups; placebo and control lists | `research/realign/G2_G3_recommendation.md`, `g2_decision.csv` |
| G3 | 23 Nov | NBCC and DLF are the confirmed NCR hit firms; Anant Raj, Parsvnath and Unitech exposed, not confirmed; NBCC's "1.5 months" read as 15 Nov–27 Dec 2024 | hit-firm set | same, registers |
| G4 | 23 Nov | R1: cement/steel firm-level hop not verified, materiality bound added. R2: contractors are within-zone upstream nodes (Ahluwalia ← DLF verified and material; B.L. Kashyap ← DLF verified, hit not documented; B.L. Kashyap ← Anant Raj held; J. Kumar ← NBCC low dose; unlinked contractors as comparison). R3: cement as a separate market test. R4: DLF's two delayed malls identified. Rules: trade classes; no NCR weight after Dec 2024; "ACC India Pvt Ltd" ≠ ACC Ltd; external and in_pack_footprint flags; hit-firm registers | links, NCR evidence, registers | `research/realign/G4_recommendation.md`; README |
| G5 | 23 Nov | NCR mechanism (ban → builders' sites → Ahluwalia) accepted on documents and quarterly numbers; price claim corrected (late windows hold no disclosure; disclosure days net of comparison); out-of-zone "not detected"; small/mid-cap sell-off and Q4 seasonality added as confounds | NCR diagram, evidence, memo | `research/realign/G5_recommendation.md` |
| G6 | — | Maruti branch, to be promoted only if a GRAP effect was found. Its screen found none, so it was not promoted | — | `hit_register_NCR.csv` |
| G7 | 23 Nov | Gujarat hit firms graded (material: Tata Chemicals, Archean; immaterial: Adani Ports, GE T&D); both rain episodes shown; Archean checked against peers and news | Gujarat registers and evidence | `research/realign/G7_recommendation.md` |
| G8 | 23 Nov (with G7) | Tata Chemicals → Tata Consumer verified and material | link G001 | `verified_links.csv`; G7 record |
| G9 | 23 Nov (with G7) | Gujarat mechanism: a cost pass-through ending in one ~7% retail increase, measured by salt revenue, volume and price by quarter; Tata Chemicals' 10 and 21 Oct moves unrelated | Gujarat diagram, salt table | G7 record; `stepC_gj_tcpl_salt.csv` |
| Review 1 (checkpoint 4) | 23 Nov | Three corrections (one Tata Salt increase; 12 Feb = results, 13 Feb = guidance cut; Adani's +5% is August cargo); results days vs call days; Gujarat placebo list without Reliance Power, medians, Tata Steel flagged, re-screen; Tata Chemicals' price and Tata Consumer's Q2 salt; Archean not attributed; dose beside own NCR exposure; NBCC's contractors (unlisted, branch closed) | tables 2–3, evidence, memo | README; G5 and G7 records |
| Review 2 (checkpoint 5) | 23 Nov | Cement delivery test replaces the market test as the main cement result; Gujarat mechanism reworded with Tata Chemicals' volumes; 18 Nov labelled not separable, B.L. Kashyap beside it; takeover targets flagged, every net figure with and without them; zero-alpha CARs; steel stops at the bound; Gujarat re-screen left partial | table 2, evidence, diagrams, memo | `table2_notes.md`; README; G5 record |
| Close-out | 24 Nov | Plant-count dose accepted as the main version; narrowed takeover flag accepted, both versions kept; Ambuja/ACC denominators and no lead-distance dose accepted. Fixes: Mangalam's Aligarh unit, Nuvoco's plants, capacity-weighted robustness, one row for the Ambuja group (conclusion unchanged: null). Memo final in the author's voice; plain words in deliverables; Signature Global read | all deliverables | this file; `table2_notes.md` |

## 9. Glossary

**Firm symbols (NSE):**
- **NCR:** NBCC, DLF (pack); AHLUCONT = Ahluwalia Contracts (India); BLKASHYAP = B.L. Kashyap and Sons; JKIL = J. Kumar
  Infraprojects; NCC; PSPPROJECT = PSP Projects; CEMPRO = Cemindia Projects (formerly ITD Cementation); LT = Larsen &
  Toubro; CAPACITE = Capacit'e Infraprojects; ANANTRAJ, PARSVNATH, UNITECH (pack); SIGNATURE = Signatureglobal (India).
- **Cement:** ULTRACEMCO = UltraTech; SHREECEM = Shree Cement (both pack); ACC (pack); AMBUJACEM = Ambuja Cements;
  JKCEMENT = JK Cement; JKLAKSHMI = JK Lakshmi (with UDAICEMENT = Udaipur Cement Works); MANGLMCEM = Mangalam Cement;
  NUVOCO = Nuvoco Vistas; BIRLACORPN = Birla Corporation; DALBHARAT = Dalmia Bharat; HEIDELBERG = Heidelberg Cement
  India; INDIACEM = India Cements; ORIENTCEM, STARCEMENT, PRSMJOHNSN = Prism Johnson, RAMCOCEM, SAGCEM, KCP, NCLIND,
  DECCANCE, SAURASHCEM, SHREDIGCEM, BVCL, KESORAMIND.
- **Gujarat:** TATACHEM = Tata Chemicals; TATACONSUM = Tata Consumer Products; ACI = Archean Chemical Industries;
  ADANIPORTS; GVT&D = GE Vernova T&D India; GSFC, GUJALKALI (pack belt).
- **Placebo flags:** RPOWER = Reliance Power; TATASTEEL.

**Terms:**
- **GRAP:** Graded Response Action Plan for Delhi-NCR air quality.
- **CAQM:** Commission for Air Quality Management, which issues the GRAP orders.
- **Stage III/IV:** GRAP stages. Stage III bans construction and demolition, including ready-mix plants and the loading
  and unloading of cement. Stage IV adds further curbs.
- **"NGT ban":** how companies refer to the GRAP order. NGT is the National Green Tribunal, not the issuer. One transcript
  spells GRAP "graph".
- **Pack:** the starter package (`data/`, `docs_from_pack/`), with 81 firms.
- **Scaffold:** `supply_chain_scaffold.csv`, the pack's industry-based link guesses.
- **External:** not among the pack's 81 firms.
- **Hit firm:** a firm whose own documents confirm the event hit its operations. "Confirmed" and "exposed" are G3's
  terms.
- **Steps A–E** (brief §2): A, confirm the shock at the source; B, build the real chain; C, measure each node; D, confirm
  the mechanism; E, draw the pathway.
- **AR / CAR:** abnormal return and cumulative abnormal return. **Zero-alpha CAR**: see §7. **Net of comparison**: see
  §7.
- **Placebo-date p:** the p-value from the same statistic on random event days.
- **Within the zone:** both firms under the same ban (builder and contractor at NCR sites).
- **Dose:** link weight × exposure.
- **`near300_n`:** share of a maker's plants within 300 km of Delhi by road. **`north_rest_n`:** its plants in northern
  states beyond 300 km. **`_cap`:** the capacity-weighted versions.
- **Lead distance:** a maker's average road distance to customers.
- **GPRA:** General Pool Residential Accommodation (NBCC's Delhi redevelopment). **RMC:** ready-mixed concrete.
- **BRSR:** Business Responsibility and Sustainability Report. **IBM:** Indian Bureau of Mines. **MTPA:** million tonnes
  a year.
- **OSRM, Nominatim:** OpenStreetMap routing and geocoding services.
- **Asna:** the cyclonic storm of 30 Aug 2024. **Mithapur:** Tata Chemicals' site. **Kachchh:** Kutch.

## 10. Gaps: documents not obtained, and why

Do not repeat these attempts unless the route changes. A human with a browser can fetch most of them by hand.

| Document | What was tried | Why it failed |
|---|---|---|
| NBCC's approved makes (cement, ready-mix, rebar) for the packages live in Nov 2024 | NBCC public tender pages; NBCC general conditions (GCC 2019, 2022, 2026) | works tenders sit on the e-procurement portal (CPPP) behind a CAPTCHA, not attempted; the public site lists corporate tenders only; the GCC names no brand |
| Cement makers' ready-mix plants in NCR | UltraTech RMC locator; ACC and Nuvoco pages | the locator is dynamic (no plant list in the text); the other pages show no NCR plants |
| Nuvoco's annual report (plant list) | NSE copy via the page reader (403); plain request (empty reply); BSE annual-report API (403); company page | the company page renders only in JavaScript; the decks list no plants. The list was built from Nuvoco's call, decks, press release and IBM |
| Mangalam's FY2023-24 report; its 2016 filing on the Aligarh unit | NSE copy (403); company copy; BSE API (403) | the company's FY24 copy is an image-only scan; the FY2024-25 company copy (OCR) was used; no 2016 filing read, so the Sept 2016 start date is unverified |
| JK Cement's Q2/Q3 FY25 decks, Q2 transcript, BRSR FY25, annual report | NSE copies via the page reader | 403; no quarterly volume |
| Per-plant capacity of UltraTech, Shree, Ambuja and ACC | annual reports, decks, BRSR | not published. IBM 2020-21 was used; UltraTech's Sadhraur (Rajpura) and Balara (Pali) and Ambuja's Marwar Mundwa have no documented capacity |
| Dalmia's "Acquisition" filing of 24 Oct 2024 | NSE attachment | 403; left unclassified |
| JK Lakshmi's Q2 FY25 results date | NSE announcement list | fetch failed |
| Shree's Q3 FY25 call | NSE announcement lists, 15 Jan–31 Mar 2025 | no call was held (only results, a press release and investor meetings) |
| Own annual reports of Jindal Steel & Power, Jindal Stainless, Lodha, NBCC, SAIL, NMDC (Gujarat placebo re-screen) | sub-agent | the author stopped the re-screen; NMDC's report did not load. Left partial by the author's decision |
| A primary source for Gaursons on Amrapali | searches | trade press only |
| Own NCR order-book shares of J. Kumar, NCC, PSP, Cemindia, L&T, Capacit'e | decks and calls | not disclosed; three decks refused (403). Only Ahluwalia (33.3%) and B.L. Kashyap (Haryana, Delhi) disclose |
| GE T&D's 27 Aug 2024 notice | NSE | not found; its 6 Sep 2024 filing, which cites it, was read |
| Signature Global's Q3 FY25 transcript | company link (404) | obtained as the author's copy of the exchange filing and read (no mention of the ban) |
| Hosts that do not answer from the cloud | cpcb.nic.in, grid-india.in, ffs.india-water.gov.in, web.archive.org and others (earlier rounds) | the remote site drops the connection |

## 11. Rules that still apply

- **Original documents only.** Nothing enters a deliverable until the original document has been read. Page summaries
  and search snippets are not enough.
- **Every quote must pass `src/42`** against the saved text. Rows that fail are not used.
- **No weight dated after Dec 2024** is used for an NCR link.
- **No paywalled pages.**
- **No CAPTCHA or access workarounds:** no browser-imitating headers, no database-style queries, no retries designed to
  get past a refusal. Record the gap instead.
- **Nulls are reported.** A broken chain is shown where it breaks. Report confounds and failed fetches as well as
  positive results.
- **Verify anything you would otherwise state from memory**, and say plainly when something is unverified.
- **Decisions are the author's** (§1): put links, mechanisms, confounds and the final claim to the author as
  recommendations with evidence.
- **Permissions the author gave** (re-confirm once in a new session):
  - reading public pages through the free page reader (`https://r.jina.ai/<URL>`) is fine, including sites that refuse
    automated clients;
  - mechanical lookups may go to sub-agents on a smaller model, but every fact they return needs a source link and a
    quote, and they must save the text of each document read;
  - logins and keys are given only through the secure credential form, never in chat. The NASA Earthdata login, needed
    only for night-light tiles in earlier rounds, is held that way.
- **Privacy:** the author's name, email and other personal details are never sent to an outside service. The geocoding
  user agent carries no personal data.
- **Save progress as you go** (`README.md`, `NEXT_STEPS.md`, this file).
- **Zip without the raw folders:** `external/rain_raw`, `external/river_raw`, `__pycache__`, `external/ntl_raw`,
  `external/no2_raw`, `external/flood_maps_raw/gfm`, `research/proxy/_page_cache`, `external/ntl_ep_raw`,
  `external/imd_raw`, `external/rain_raw_2026` (and `external/power_raw/*.zip` if present).

## 12. Environment

- **Python 3.13.18:** pandas 3.0.5, numpy 2.5.3, matplotlib 3.11.2, pypdf 6.17.0. `requirements.txt` adds scipy,
  statsmodels, yfinance, lxml, beautifulsoup4, h5py, rasterio and pyproj (the last three for earlier rounds). Install
  with `pip install -r requirements.txt`, plus `pip install pypdf` for the page count.
- **Memo build:** pandoc 3.1.3 (HTML with embedded figure), then Node 22 with Playwright and Chromium
  (`src/memo_to_pdf.js`, A4). The style is `src/memo_style.css`, and `src/61_build_memo.sh` prints the page count.
- **Offline:** every deliverable script runs from the saved CSVs, except `src/43`, `src/49` and `src/52` when a peer's quarterly financials are missing, and `src/62` for places not yet in the geocode cache.
- **Network needed for:**
  - `src/43`, which fetches missing peer financials from screener.in;
  - `src/62`, for new places only (Nominatim and OSRM, about 1 request a second, a research user agent);
  - any new document fetch (exchange archives, company sites, the page reader);
  - price or index updates (Yahoo Finance).

## 13. Open items, next steps, and what not to do

**Open items:**
1. **The memo's Conclusion** (§7 of `memo.md`): the author will write it, about 100 words. There is room inside the
   five pages. Rebuild with `bash src/61_build_memo.sh` and confirm 5 pages.
2. **The final causal claim:** the author's.

**Sensible next steps, only if the author asks:**
- **Fetch by hand:** NBCC's approved makes for Sarojini Nagar Package IV-B and other GPRA packages (CAPTCHA portal); add
  them to `research/realign/nbcc_makes_cci_rmc.csv` with quotes; then decide whether the steel bound can become a test.
- **Missing capacities:** the three northern plants without one (UltraTech Sadhraur and Balara, Ambuja Marwar Mundwa),
  from company announcements, to tighten the capacity-weighted dose.
- **Missing documents:** Nuvoco's FY24 annual report (plant list) and JK Cement's quarterly volumes, from the company or
  exchange by hand.
- **Gujarat placebo re-screen:** the six annual reports, if the author reopens it.

**What not to do:**
- Do not undo the fixes in `src/common.py`: the one-day date shift, the corrected district footprints, the verified
  event dates.
- Do not extend the archived scripts (`src/00`–`src/33`) or bring back the scaffold result or the withdrawn earlier
  link tests.
- Do not use the pack's `plants.csv` for cement doses, or any weight dated after Dec 2024 for NCR.
- Do not add analysis that serves no deliverable.
- Do not bypass a 403 or a CAPTCHA, and do not fetch paywalled pages.
- Do not put decision codes back into the deliverables. Run `src/64` after any rebuild.
- Do not draft the memo's Conclusion or the final claim: they are the author's.
