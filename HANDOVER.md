# Handover: climate shocks and supply-chain propagation

Read this file first for **environment setup, data traps and permissions**. Scope, method and deliverables come only
from the assignment (`docs_from_pack/INSTRUCTIONS.md`, `docs_from_pack/README.md`); then read `GAP_MAP.md` and
`NEXT_STEPS.md` (the approved plan). `README.md` is the front page.
This folder is self-contained: there is no git repository to pull from. Work inside this folder.

## 1. What the project is
The assignment asks whether a localized, documented extreme event that damages a listed firm's plants
propagates along the supply chain to firms outside the disaster zone. It asks for a node-by-node traced
pathway for two key events: the Delhi-NCR construction ban (GRAP, Nov 2024) and the Vadodara floods
(Aug 2024). `docs_from_pack/INSTRUCTIONS.md` and `docs_from_pack/README.md` are the only definition
of scope, method and deliverables (user, 22 Nov 2026). The starting dataset is the research pack
(`data/`): 81 firms, 3,907 plants with coordinates, daily prices 2020–2025 for 61 firms, and four named events.

## 2. Where things stand (23 Nov 2026)
- **Realigned on 22 Nov 2026.** Earlier rounds answered "can direct physical exposure be priced". Most
  of their effort went to Chennai, pricing, hazard panels and satellite proxies, none of which is a
  deliverable. That work is kept but archived: `archive/README_rounds1-4.md`, and
  `archive/HANDOVER_round4.md` for the earlier status text.
- **`GAP_MAP.md`** maps each deliverable, and steps A–E for both events, against what exists.
  **`NEXT_STEPS.md`** is the plan the user approved on 23 Nov 2026. It follows the order of the
  instructions' §7 and has decision gates (◆) that are the user's calls.
- **Done:**
  - Decision G1: the 32 legacy link rows are classified in `outputs/deliverables/verified_links.csv` (`src/40_links_file.py`).
  - The scaffold result and the earlier link-test result are withdrawn.
  - README is rewritten to the assignment's scope.
- **G2 and G3 decided (23 Nov 2026):** firm sets in `research/realign/g2_decision.csv`; reasons in
  `research/realign/G2_G3_recommendation.md`. The January 2025 Stage III orders were added to the record.
- **Step 1 done (checkpoint 1):** `outputs/deliverables/table1_*` (`src/43`, a rerun of `src/es_lib.py`),
  placebo lists in `placebo_firms.csv`.
- **Step B for NBCC and DLF done (checkpoint 2):**
  - No cement or steel firm-to-firm link was found.
  - Three contractor links were documented (Ahluwalia and B.L. Kashyap ← DLF; J. Kumar ← NBCC).
  - Decision G4 went to the user (`research/realign/G4_recommendation.md`); decided on 23 Nov 2026 (next item).
  - The user asked for a zip of the folder at each checkpoint.
- **G4 applied and the scope widened (23 Nov 2026):**
  - Contractor links: Ahluwalia ← DLF material; B.L. Kashyap ← DLF site hit not documented; J. Kumar ← NBCC low dose.
  - The cement/steel firm hop is not verified (a materiality bound is added).
  - Cement is tested as a market-level test; DLF's two malls are Summit Plaza and Midtown Plaza.
  - The user added rules: trade classes; no NCR weight dated after Dec 2024; external and footprint flags on every firm.
  - Hit-firm registers for both events, including firms outside the pack (`outputs/deliverables/hit_register_*.csv`).
- **NCR Steps C–D done:** `src/49` (node CARs and quarterly numbers), `src/50` (cement market test), `src/51` (registers), `src/47` (evidence table). **G5 decided and applied (23 Nov 2026).**
- **Gujarat Step A outside the pack done:** Tata Chemicals, Archean, Adani Ports and GE T&D; the Tata Chemicals → Tata Consumer chain (`src/52`, `src/53`). **G7 decided and applied (23 Nov 2026).**
- **Checkpoint 4 (23 Nov 2026): all four deliverables drafted.**
  - G5/G7 corrections: `src/55` (contractor windows net of unlinked contractors; disclosure days), `src/56` (rain episodes; Archean vs specialty peers), `src/57` (Tata Consumer salt by quarter); evidence in `research/realign/g5_timing_docs.csv`, `g7_docs.csv`, `news_checks.csv`, `tcpl_salt_kpis.csv`.
  - Step E: `src/58` (dose-response and placebo tables), `src/59` (pathway diagrams, lag figure); memo draft `outputs/deliverables/memo.md`.
  - The final causal claim (§5) is the user's: the memo grades the evidence and leaves the verdict to the user.
- **Checkpoint-4 review (23 Nov 2026) applied:** revised tables 2-3 (+ `table2_notes.md`, `table3_notes.md`, `table3_placebo_firms.csv`), evidence tables, diagrams, G5/G7 records, memo (`memo.pdf`, 4 A4 pages; limit 5 as set, tables and figures included). New evidence: `research/realign/contractor_ncr_orderbook.csv`, `nbcc_contractors.csv`, `gj_placebo_rescreen.csv`, more rows in `news_checks.csv` and `tcpl_salt_kpis.csv`.
- **Run order after any change:** `42` first if any evidence CSV changed (the cement scripts read only verified rows); `45` (placebo lists; reads `gj_placebo_rescreen.csv`); `49 → 55` (NCR); `62 → 63` (cement plants, then the delivery test: about 5 minutes; the geocodes are cached); `47` (NCR evidence, reads 55 and 63); `52 → 56 → 57 → 53` (Gujarat); `54 → 40` (links); `50`, `51`; `58` (set `SKIP_PLACEBO=1` to refit table 2 without recomputing table 3); `59`, `60`; `61_build_memo.sh` last (check the page count). Then `42` to re-check every quote.
- **The permission check blocked one command:** a direct download of an exchange PDF with a browser-like
  header (23 Nov 2026). It was not retried. Sub-agents are told to use only the page reader and to record
  refusals instead of working around them.

## 3. What has been done, and how

**Scope note (22 Nov 2026):**
- Rows for scripts `04`, `06`, `08`, `09` and `13`–`33` describe archived work, not deliverables.
- `05` and `10` are superseded; their results are withdrawn.
- Still used: `common.py`, `es_lib.py`, `00`, `03`, `07`, `11`, `12` and `18`.
- Deliverable scripts start at `40`: `src/40_links_file.py` builds the links file.

| Stage | Script | Output |
|---|---|---|
| Shared loaders, corrected exposure footprints, verified event dates | `src/common.py`, `src/es_lib.py` | — |
| External data: NIFTY indices (Yahoo chart API), rainfall for 478 districts (NASA POWER) | `src/00_fetch_external.py` | `external/indices_daily.csv`, `external/rain_daily.csv.gz` |
| Direct event study, placebo-date inference | `src/03_event_study.py` | `outputs/tables/event_study_*.csv`, `figs/01_*` |
| Rainfall hazard panel (all extreme episodes) | `src/04_hazard_panel.py` | `outputs/tables/rain_*.csv`, `figs/02_*`, `03_*` |
| Propagation on the pack's industry scaffold | `src/05_propagation.py` | `propagation_scaffold.csv` |
| Pricing: loss-per-event, hazard scorecard, concentration | `src/06_pricing.py` | `pricing_*.csv`, `figs/04_*` |
| Financials and market cap (screener.in public pages) | `src/07_fetch_fundamentals.py` | `external/fin_quarterly.csv`, `fin_annual.csv`, `market_cap.csv` |
| River discharge (Open-Meteo flood API), modelled PM2.5 | `src/08_fetch_river_aqi.py` | `external/river_daily.csv.gz`, `pm25_daily_cams.csv` |
| River episodes, fundamentals panel, rupee losses | `src/09_fundamentals_river_rupees.py` | `river_*.csv`, `fundamentals_*.csv`, `rupee_*.csv`, `figs/05_*` |
| Propagation on verified links | `src/10_verified_links.py` | `propagation_verified_links.csv` |
| NSE announcements for the open cases (via page reader) | `src/11_fetch_announcements.py` | `research/nse_announcements*`, |
| Earnings-call transcripts and keyword search (via page reader) | `src/12_fetch_transcripts.py` | `research/transcripts/`, `transcript_keyword_hits.csv` |
| Web verification and supply-link research (done by sub-agents with web search) | — | `research/verified_*.csv`, `research/disclosures_*.csv` |
| Disclosure verdicts per case | — | `research/step1_disclosure_findings.csv` |
| **Round 3.** Night-light tiles (NASA Black Marble VNP46A2; Earthdata login) | `src/13_fetch_ntl.py` | `external/ntl_raw/` (6 GB, not in the zip) |
| Night lights at every plant, pixel-matched ratio to normal | `src/14_ntl_extract.py` | `external/ntl_plant_daily.csv.gz`, `ntl_area_daily.csv` |
| Dark sites, cluster series, firm shares | `src/15_ntl_analysis.py` | `outputs/tables/ntl_*.csv`, `figs/06_*`, `07_*` |
| Radar flood extent at the plants (Copernicus GFM) | `src/16_flood_gfm.py` | `external/flood_gfm_plant_pass.csv`, `outputs/tables/flood_*.csv`, `figs/08_*` |
| Event study with plant-level exposure | `src/17_plant_level_event_study.py` | `plant_level_event_study.csv`, `plant_level_exposure.csv`, `figs/09_*` |
| Re-check of sub-agent quotes against their pages | `src/18_verify_quotes.py` | `research/proxy/quote_check.csv` |
| State electricity use around the events | `src/19_power_demand.py` | `power_state_*.csv`, `figs/10_*` |
| Nitrogen dioxide over the clusters (Sentinel-5P) | `src/20_no2.py` | `external/no2_box_daily.csv`, `no2_box_event.csv`, `figs/11_*` |
| Interruption-cost bound against the price move | `src/21_interruption_pricing.py` | `pricing_interruption_bound.csv` |
| One evidence table in the template layout | `src/22_compile_proxy_evidence.py` | `research/proxy_evidence.csv` |
| Sector-adjusted check of the Chennai price drop | `src/23_chennai_sector_check.py` | `chennai_sector_check.csv`, `external/indices_extra.csv` |
| Delhi event study on the Stage III (construction-ban) order dates | `src/24_grap_stage3_event_study.py` | `grap_stage3_event_study.csv` |
| **Round 4.** Prices (Yahoo, validated against the pack), indices and NASA POWER rain to Nov 2026 | `src/26_fetch_extend.py` | `external/prices_yahoo_2024_2026.csv`, `indices_daily_2026.csv`, `rain_daily_2026.csv.gz` |
| Out-of-sample test: fit Nov 2020–Dec 2024, test Jan 2025–Sep 2026 | `src/27_out_of_sample.py` | `oos_*.csv`, `figs/12_*` |
| Night lights for 66 severe episode-weeks (annual-composite baseline, same-night controls; Earthdata login) | `src/25_ntl_episodes.py` | `external/ntl_ep_cache/`, `ntl_episode_plant_nights.csv.gz`, `ntl_episode_*.csv`, `figs/13_*` |
| Expected annual outage loss and the firm risk card | `src/28_expected_interruption_loss.py` | `pricing_expected_interruption_loss.csv`, `deliverable_firm_risk_card.csv`, `figs/16_*` |
| Delhi daily AQI as a continuous treatment | `src/29_delhi_aqi_panel.py` | `delhi_aqi_*.csv`, `figs/14_*` |
| Optical water check at Chennai plants (Sentinel-2, Landsat) | `src/30_chennai_optical.py` | `external/optical_chennai_plant_scenes.csv`, `optical_chennai_*.csv` |
| Rainfall triggers on the official IMD 0.25° grid | `src/31_imd_hazard.py` | `external/rain_imd_daily.csv.gz`, `imd_*.csv`, `figs/15_*` |
| State GST collections test, with placebo | `src/32_flows_round3.py` | `flows_gst_state_test.csv` |
| Chennai plants on the NRSC RISAT-1A flood map of 7 Dec 2023 (GeoPDF, georeferenced from its embedded corners) | `src/33_nrsc_chennai_flood.py` | `nrsc_chennai_plants.csv`, `figs/17_*` |
| Sub-agent research (source link and quote per row; quotes re-checked by `src/18`) | — | `research/proxy/flow_data_round3.csv`, `damage_disclosures.csv`, `research/transcripts_round3.csv`, `manual_collection/REQUESTS_verification.csv` |
| Official orders, Delhi daily air quality 2022–2023, river levels (sub-agent, quotes re-checked) | — | `research/proxy/official_hazard_records.csv`, `delhi_aqi_daily.csv` |
| Third-party record, flows, flood-map products, official records (sub-agents, web search) | — | `research/proxy/*.csv` |

There is no script 01 or 02; the audit and exposure logic live in `common.py`. Scripts 13–24 are Round 3; 25–33 are Round 4.

### Data traps already handled in `src/common.py` — do not undo
- Stock dates in the pack are **one day early** for 60 of 61 firms (RAJESHEXPO is correct). Fixed in `stock()`.
- The pack's Himachal exposure uses substring matching and catches other states. Use `ZONES` / `exposure()`, never `data/event_plant_exposure.csv`.
- `EVENTS` holds verified dates. The pack's GRAP date (5 Nov 2024) is wrong; the order took effect 18 Nov, with a second episode from 17 Dec. These are Stage IV dates. The construction ban itself starts with Stage III (archived README §5.15); the comment block in `common.py` carries a note, the dates were not changed.
- NMDC 2022-10-26 return (+86%) is a demerger artefact; returns above 40% in absolute value are dropped.
- Plant `project_cost_cr` is a relative weight only (25% zeros, units unclear). Use shares, not rupee levels.
- `data/financials_annual.csv` is one quarter only; use `external/fin_quarterly.csv` instead.
- Market cap = current share count × the pack's adjusted price, so historical rupee values are approximate.

### Traps found in Round 3 — also handled, do not undo
- **Night-light file dates are UTC.** The file for day D is the overpass at about 01:50 India time on D+1. `14_ntl_extract.py` shifts by one day (`night_ist`). Checked against the companion product's view time.
- **Night-light quality flags changed in collection 2:** 0 = high quality, 1 = poor (outlier or possible cloud), 255 = none. Older write-ups describe 0/1 as both good. Only 0 is used.
- **Cloud-edge readings are biased low.** A plant-night is kept only if at least 80% of the 10 km around it is clear (`clear_10km`). Without this filter, ordinary nights look like outages.
- **Night-to-night noise is ±10–30%** for a cluster median and single ordinary nights reach 0.69. Never call an outage from one night or one site.
- **A few plant coordinates are far from their stated district** (for example Petronet's largest "Bharuch" entry is across the Gulf of Khambhat; one Unitech "Gautam Buddha Nagar" entry is in Mumbai). `15_…` and `16_…` drop zone plants whose coordinates fall outside the zone box (`ZBOX`). The district-based exposure in `common.py` is unchanged.
- **Radar cannot see water between buildings.** On average 45% of the 500 m around a plant is in the flood product's exclusion mask. "No flood pixel" is not "not flooded" for a built-up site.
- **Sentinel-1 has gaps.** No pass over Chennai from 30 Nov 2023 to 17 Jan 2024. Check the official catalogue before planning radar work; the Planetary Computer mirror also lacks some scenes.
- **Sub-agents sometimes report the page reader as blocked.** It answers 401 "bad IP reputation" when several agents use it at once and recovers after a minute. Run reader-heavy agents one at a time.

### Traps found during the realignment (Nov 2026)
- **Wording:** companies call CAQM's GRAP order the "NGT ban". NBCC's transcript spells GRAP "graph". Keyword screens must include both.
- **"ACC India Pvt Ltd"** (a contractor on DLF Privana South) is the Arabian Construction Company subsidiary, not ACC Ltd. Do not match it to the cement firm.
- **GE Vernova T&D India's symbol `GVT&D`** breaks the NSE announcement API (the "&" splits the URL). Use BSE or company copies.
- **NSE archive PDFs often return 403 through the page reader.** The BSE copy (`AttachHis/<id>.pdf`) or the company site often works. Never work around a refusal.
- **The permission check blocked two requests.** One was a direct download with a browser-like header (the main session). The other was a sub-agent's call to a website's data API. Neither was retried.
- **Dates that differ from first reports:**
  - Tata Chemicals' Q2 FY25 results and deck are dated 17 Oct 2024; its call transcript was filed on 24 Oct.
  - GE T&D's own filing dates its disruption notice 27 Aug 2024; the press reported it on 28 Aug.
  - Ahluwalia's Q2 FY25 call was on 18 Nov 2024, the NCR event day. Its results came out after the close on 14 Nov.
- **Results release times (from the NSE filing names):** Tata Consumer filed its Q2 FY25 results at 16:52 IST on 18 Oct 2024, after the close, so they were priced on 21 Oct. Tata Chemicals filed at 18:01 IST on 17 Oct, so they were priced on 18 Oct.
- **Not found:** the "more than 85% of its salt from Tata Chemicals" statement in Tata Consumer's IAR 2022-23, as read. The link rests instead on Tata Chemicals' FY25 annual report ("single customer") and Tata Consumer's related-party filings.
- **Tata Chemicals' Mithapur cost:** the ₹11 cr one-off is in the deck (the profit impact). The call gives about ₹40–44 cr of total weather impact. Quote both.

### Traps found at G5/G7 (23 Nov 2026) — handled, do not undo
- **Calls after the close.** Ahluwalia's Q3 FY25 call was at 4.00 pm IST on 12 Feb 2025 (notice of 7 Feb), so its guidance cut is priced on 13 Feb; its Q3 results were filed at 16:43 on 11 Feb (priced 12 Feb). Its Q2 call was at 3.00 pm on 18 Nov 2024, 30 minutes before the close. The (+21,+60) window from 18 Nov ends on 11 Feb and holds none of these.
- **The Q3 deck filed at 12:33 on 12 Feb does not mention the ban**: 12 Feb prices the numbers only.
- **One price increase, not two.** Tata Consumer's "INR2" and "7%" are the same increase (₹2 on a ₹28 pack, from October 2024).
- **The "more than 85%" sourcing statement is on Tata Consumer's IAR 2022-23 web page** (`for-better-sourcing.html`, Responsible Sourcing), not in the PDF as read.
- **Adani Ports' "+5%" is its August 2024 cargo**, not a quarterly figure.
- **Placebo days are fewer for firms outside the pack**: Yahoo peer prices start on 1 Jun 2021 (about 800 usable days); Archean listed in Nov 2022 (494).
- **Store CARs at 6 decimals.** At 4 decimals, NBCC's −0.041484 printed as −4.2% in one file and −4.1% in another; `stepC_ncr_node_cars.csv` is now written at 6 decimals.
- **NSE's announcement list for Archean, 22 Aug–5 Sep 2024, is empty**; the wider list (1 Aug–30 Sep) confirms no filing between 21 Aug and 24 Sep. The 20 Aug filing is an immaterial GST penalty.
- **A Benzinga link returned the site's home page**; the 21 Oct 2024 Tata Chemicals move is sourced from Zee Business instead.
- **Sub-agents can die on API overload (529)**; check what they saved before relaunching, and ask them to write their CSV incrementally.

### Traps found at the checkpoint-5 review (23 Nov 2026) — handled, do not undo
- **Alpha leaks into long windows.** A strong estimation-window drift is projected forward as normal return (Unitech's alpha term is −17.7 of its −23.5 pp (+21,+60) CAR). Use `es_lib.ar_matrix(..., zero_alpha=True)` (beta kept) beside the market model for (+6,+20) and (+21,+60): table 1 and both node tables now carry both.
- **Comparison groups can contain takeover targets.** PSP Projects (Adani Infra, 19 Nov 2024) and Cemindia, then ITD Cementation (Renew Exim DMCC, 25 Oct 2024) were targets inside the windows. Every net figure is reported with and without them (`stepC_ncr_unlinked_flags.csv`).
- **A clean day-0 comparison exists:** B.L. Kashyap filed nothing between 11 Nov and 31 Dec 2024.
- **Geocoding rule:** a district-centroid fallback misplaces plants in large districts (Kotputli is 110 km from the Jaipur centroid). The rule was amended before the cement test ran (state check plus 150 km). The specification and its amendment are in `table2_notes.md`, with a frozen copy at `research/realign/cement_test_spec_20261123.md` (sha256 9d8a4867…5e21).
- **Road distances** come from OSM Nominatim and OSRM (public services, about 1 request a second, an identifying research User-Agent, no browser imitation), cached in `external/cement_geo_cache.csv`.
- **NBCC's works tenders (approved makes) are not publicly readable.** They sit on the e-procurement portal behind a CAPTCHA, which was not attempted. The general conditions only refer to a "List of approved makes".
- **The CCI order of 19 Jan 2017 (Ref. Case 05 of 2013)** reads well through Jina from the Indian Kanoon copy (`docs/makes__cci_ik.txt`); the `future.` subdomain does not.
- **Tata Consumer's Q2 call sentence "8% … 1%" does not say volume or revenue.** Cite the deck (slide 24).
- **Ambuja and ACC publish no per-plant capacity** (decks, annual reports, BRSR). Their units come from the "Site Location" lists in the corporate governance sections of their FY2023-24 annual reports (`research/realign/cement_plants_D.csv`). The Ambuja group's denominator is its own unit count at 30 Sep 2024 (43; `cement_unit_counts.csv`). Agent B's placeholder rows (no place) are firm totals, not plants: `src/62` and `src/63` drop them.
- **Takeover flag for cement:** filter on deals in a cement business (open offer, stake purchase, acquisition of control), not on every merger or stake filing. Captive-power stakes, internal amalgamations and promoter transfers are not takeovers. The broad flag left one exposed maker, so the regression was not identified. Both versions are reported; the narrowing came after the first run (stated in `table2_notes.md`).
- **`ols()` in `src/63` returns NaN when fewer than two makers in the sample have a non-zero dose.** Otherwise `lstsq` returns a minimum-norm solution for collinear doses, which looks like a number but means nothing.
- **pandas `iterrows()` rows: use `r["item"]`, not `r.item`** (that is the Series method). It silently wrote method objects into `evidence_NCR.csv`; fixed in `src/47`.
- **Quotes of five characters or fewer are not checkable** (`src/42` needs a fragment longer than 5 characters). Chart labels such as "1.37" need the sentence around them.

### Traps found at the checkpoint-4 review (23 Nov 2026) — handled, do not undo
- **Tata Consumer's Q2 FY25 deck gives no text to the page reader.** A plain download of the BSE PDF (default curl, HTTP 200) converted with `pdftotext -layout` works; saved as `research/realign/docs/tcplsalt__Q2FY25_presentation_bse.txt` with page markers. Printed slide numbers run one behind the PDF page (slide 24 = PDF page 25).
- **Reliance Power was not a clean Gujarat placebo**: SEBI's final order of 22 Aug 2024 against Anil Ambani; −5.0% on each of 23, 26 and 27 Aug.
- **Market-model alpha can manufacture abnormal returns** after a strong estimation-window run-up (Unitech: alpha +0.85% a day; half of its −16.7%). Report medians beside means.
- **Agents may write `saved_text` as a bare file name**; `src/42` then reports "saved text missing". Prefix `research/realign/docs/` (done for `contractor_ncr_orderbook.csv`).
- **Contractors rarely disclose an NCR share of order book**: only Ahluwalia (33.3%); B.L. Kashyap gives Haryana and Delhi; three Q3 decks were refused (403).
- **Pandoc needs a blank line before a list** that follows a paragraph, or the list renders inline. `src/61_build_memo.sh` builds the PDF; check the page count.

### Traps found in Round 4 — handled, do not undo
- **NASA POWER changes its rainfall source on 1 Oct 2026** (MERRA-2 before, the near-real-time GEOS-IT model after; see the API response header "sources"). `src/27` stops rainfall at 30 Sep 2026. Recheck the switch date before extending.
- **NASA's catalogue (CMR) is very slow with file-name wildcards** (about 80 s a query). Query by the tile's centre point and a whole year at once (`cmr()` in `src/25`).
- **Annual night-light composites:** a temporal query that touches 1 Jan also returns the previous year's file; query a mid-year day and pick the file by its `A<year>001` name.
- **IMD grid cells on the coast are "no data"** (-999): each district uses the nearest cell with data (6 districts are more than 0.18° from their cell).
- **IMD's daily value** is the 24 hours ending 08:30 India time, so its peaks can sit a day after NASA's; the 3-day window absorbs this.
- **The Yahoo and pack prices agree** (correlation ≥ 0.99 for 58 of 61 firms) only after the pack's one-day date fix; never use the unshifted pack dates with Yahoo data.
- **A built-in safety check blocks wildcard deletions** in shell commands. Leftover raw tiles from an interrupted run sit in `external/ntl_ep_raw/daily/` (top level), plus partial `.dl2` files in `external/imd_raw/`. They are harmless, excluded from the zip, and can be deleted by hand.

## 4. Environment setup for a new session

1. **Python packages:** `pip install -r requirements.txt`
2. **Smoke test** (no network needed; should print tables and rewrite outputs):
   `python3 src/03_event_study.py`
3. **Network.** The cloud environment used on 17 Nov 2026 has **unrestricted** outbound access, so
   no host is blocked by policy. Hosts that worked: `query1.finance.yahoo.com`, `power.larc.nasa.gov`,
   `flood-api.open-meteo.com`, `air-quality-api.open-meteo.com`, `archive-api.open-meteo.com`,
   `www.screener.in`, `r.jina.ai`, `github.com`, `cmr.earthdata.nasa.gov`, `urs.earthdata.nasa.gov`,
   `data.laadsdaac.earthdatacloud.nasa.gov`, `catalogue.dataspace.copernicus.eu` (search only),
   `stac.eodc.eu`, `data.eodc.eu`, `planetarycomputer.microsoft.com`, `robbieandrew.github.io`,
   `ppac.gov.in`, `pib.gov.in`, `unosat.org`.
   Hosts that do not answer (the remote site drops the connection or the gateway cannot reach it;
   changing network settings will not help): `dosairnowdata.org`, `cpcb.nic.in`,
   `ffs.india-water.gov.in`, `grid-india.in`, `report.grid-india.in`, `vahan.parivahan.gov.in`,
   `bhuvan-app1.nrsc.gov.in`, `ladsweb.modaps.eosdis.nasa.gov`, `landweb.modaps.eosdis.nasa.gov`.
   Some of these are readable through the page reader (item 4). If a future environment is
   restricted and refuses a host by policy, propose adding the exact host and ask the user first.
3b. **NASA Earthdata login.** Saved by the user through the secure credential form as a network
   secret for host `urs.earthdata.nasa.gov` on their Default cloud environment (username and
   password; the proxy adds it, scripts never see it). `curl -L` with a cookie jar is enough;
   see `fetch()` in `src/13_fetch_ntl.py`. Outside the cloud, use `~/.netrc`.
   The NASA atmospheric archive (GES DISC: Sentinel-5P, rainfall) answers "access denied" until the
   user approves the application "NASA GESDISC DATA ARCHIVE" on their Earthdata profile.
3c. **Other Round 4 sources** (all answer from the cloud session): IMD gridded rainfall by POST to
   `https://www.imdpune.gov.in/cmpg/Griddata/rainfall.php` with `rain=<year>` (about 25 MB a year,
   1–3 minutes each); Yahoo Finance chart API for prices; Microsoft Planetary Computer for
   Sentinel-2, Landsat and Sentinel-5P (signed URLs from its token endpoint); EODC for flood maps.
4. **Page reader (how the blocked sites were read).** Many Indian exchange, government and news
   sites refuse automated clients. They are readable through the free Jina reader: fetch
   `https://r.jina.ai/<full target URL>` and take the text after `Markdown Content:`. No key is
   needed; keep to about one request every 5 seconds. See `get()` in `src/11_fetch_announcements.py`.
   - Works: NSE announcement API (`https://www.nseindia.com/api/corporate-announcements?index=equities&symbol=SYMBOL&from_date=DD-MM-YYYY&to_date=DD-MM-YYYY`), BSE company announcement pages, BSE PDF links, caqm.nic.in, pib.gov.in, ppac.gov.in, icra.in PDFs, business-standard.com.
   - Does not work: CPCB bulletin archive, US-embassy air-quality CSVs, river-gauge portal (loads empty), image-only PDFs.
5. **The agent-reach tool** (https://github.com/Panniantong/agent-reach), which the user asked to
   install. The previous session inspected the code, installed it in an isolated virtual
   environment (`python3 -m venv venv && venv/bin/pip install git+https://github.com/Panniantong/agent-reach.git`),
   and did **not** run `agent-reach setup`, because setup writes a skill file into the agent's own
   configuration folders and can install Node and a browser. Its web channel is just the Jina
   reader plus Exa; it also pauses itself for about 100 seconds after any single failure, so the
   scripts here call the Jina reader directly instead. Reinstall it only if you need its other
   channels (YouTube, Reddit, and so on).
6. **Sub-agents.** The user allowed delegating mechanical lookups to sub-agents on a smaller model.
   Require a source link and quote for every row they return; several official pages could only
   be read as summaries, and each research CSV marks which rows those are.
   Since 22 Nov 2026, have them save the text of every document they read (`research/realign/docs/`), and check
   each quote against that text before it is used. Run reader-heavy agents with pauses (see the 401 trap below).

### Permissions the user gave (confirmed again on 17 Nov 2026; re-confirm once in any new session)
- Reading public pages through the reader is fine, including sites that refuse automated access.
- **Do not fetch paywalled articles.**
- Do not paste credentials in chat; ask for keys or logins through the secure credential form.
- Mechanical lookups may go to sub-agents on a smaller model; every fact needs a source link and quote.
A new session should confirm these with the user once, at the start, rather than assume them.
One sub-agent reported that its own attempt to fetch an Internet Archive copy of a dead page was
refused by its permission check; that fetch was not made by anyone.
In Round 4 a sub-agent tried a malformed, database-style query against the Rajya Sabha question
search (rsdoc.nic.in) by mistake; the permission check blocked it, and the agent then used the
site's normal search. web.archive.org does not answer from the cloud session in any case. If the archived copy of the
Indian space agency's Chennai flood map is wanted, ask the user.

## 5. What to do next
Follow `NEXT_STEPS.md`. Work stops at each decision gate (◆) until the user answers. The current gates
are G2 (exposed sets and matched controls) and G3 (which NCR builders count as confirmed hit firms).
Data to download by hand, for deliverables only: `MANUAL_DATA_REQUESTS.md` (M3, M12, M11, M1b, M1c, M1d).
The earlier list is in `archive/MANUAL_DATA_REQUESTS_round4.md`.

## 6. Reporting rules the user has asked for
- **Scope (22 Nov 2026):** the assignment defines scope. A task that does not serve one of the four deliverables (§6) is not done.
- **Decisions are the user's** (instructions §5). The agent collects, computes and drafts. Which links are real, which mechanism holds, what is a confound, and the final causal claim are put to the user as recommendations with evidence; dependent work waits for the answer.
- **A null is an acceptable result.** Show where the chain breaks instead of forcing a pathway.
- **Nothing enters a deliverable until its original document has been read.** Page summaries and search snippets are not enough.
- Verify anything stated from memory, and say plainly when something is unverified.
- Keep the findings honest: report nulls and confounds, not only positive results.
- Save progress as you go: update `README.md`, `NEXT_STEPS.md` and this file, and give the user a
  fresh zip of this folder at the end (exclude `external/rain_raw`, `external/river_raw`, `__pycache__`;
  Round 3 also excludes the re-downloadable raw files `external/ntl_raw` (6 GB), `external/no2_raw`,
  `external/flood_maps_raw/gfm` (0.5 GB) and the page cache `research/proxy/_page_cache`;
  Round 4 also excludes `external/ntl_ep_raw` (annual composites and leftovers), `external/imd_raw`
  (0.7 GB, re-downloadable), `external/rain_raw_2026` and `external/power_raw/*.zip` if present).
