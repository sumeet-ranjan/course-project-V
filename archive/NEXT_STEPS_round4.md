# Next steps (to-do list)

**New session? Read `HANDOVER.md` first.**

Status (Round 4, 18 Nov 2026): everything that can be reached from the cloud session has been done
(README sections 5.16–5.25). What remains needs data downloaded by hand; each open item below
carries the ID of its entry in `MANUAL_DATA_REQUESTS.md` / `manual_collection/REQUESTS.csv`.
When files arrive, the item says which script to rerun.

## Step 1. Company disclosures — DONE as far as public filings go (README 5.6, 5.21)
- [x] Chennai: no stoppage notice from any sample firm; no third party reports the tyre plants shut; Maruti and JK Tyre calls say nothing; **Apollo Hospitals' Q3 FY24 call names the cyclone** (two quotes, company PDF). Hindustan Unilever's Chennai entry was dark on 6–7 Dec, but it may be an office address.
- [x] Delhi: DLF and NBCC name a short construction delay; UltraTech mentions slowed construction; no firm quantifies lost days or volumes.
- [x] Gujarat (2023, 2024): no notice, no call mention, no third-party report of a sample plant shut; Petronet's Dahej volumes show no dip.
- [x] Findings compiled in `research/step1_disclosure_findings.csv`, `research/transcripts_round3.csv`, `research/proxy/damage_disclosures.csv`.
- [ ] Gujarat Alkalies, Anant Raj and Shree Cement transcripts, if calls were held (request **M11**; low priority).

## Step 1b. Independent physical proxies — DONE (README 5.7–5.12, 5.17, 5.19)
- [x] Night lights for the three named events (`src/13`–`15`) and for all 66 severe-episode weeks of Nov 2020–Sep 2026 (`src/25`).
- [x] Radar flood maps (Copernicus GFM, `src/16`): Gujarat Aug 2024 only; no Sentinel-1 pass over Chennai in the event window.
- [x] Optical water check at the Chennai plants (`src/30`): tyre plants under cloud on every event scene.
- [x] Nitrogen dioxide (`src/20`): not informative (cloud).
- [x] State electricity (`src/19`), state GST collections (`src/32`), cement/fertiliser indices, rail freight to Feb 2024.
- [x] Event study with plant-level hits: Chennai/Gujarat 2024 (`src/17`) and across 66 episodes (`src/25`): **assets that went dark are priced** (−16% per 100% of plant cost dark over 10 days).
- [x] Chennai flood map from the Indian space agency: found on NDEM (GeoPDF), georeferenced, plants tested (`src/33`, README 5.24): no tyre plant had flood water within 1 km on 7 Dec 2023. The vector layer (request **M2**, now optional) would only refine this.
- [ ] Vehicle registrations by maker and state (**M5**), e-way bills by state (**M6**), rail freight Oct 2024–Mar 2025 (**M7**): add to `src/32` when collected.
- [ ] Optional: the plant-level night-light test on all ~1,000 rain episodes instead of 66 weeks needs Google Earth Engine access (**M13**) or ~200 GB of downloads.
- [ ] Dropped as low value: repair tenders and job postings; customs shipments (**M12**, paid) only if a specific firm's stoppage question stays open.

## Step 2. Accounts test on monthly operating data — WAITING FOR DATA
- [x] Public series checked (README 5.11, 5.20): Maruti production, national cement and fertiliser output, national LNG imports, Petronet quarterly volumes, state GST collections. No firm-level dip found; state GST shows one-month dips of 7–9% after the floods (not significant alone).
- [ ] Monthly plant-level output: tyre makers (**M1a**), GSFC/GNFC/Gujarat Alkalies (**M1b**), northern cement despatches (**M1c**), NCR project progress (**M1d**), tyre-sector rubber use (**M9**). Then rerun `src/09_fundamentals_river_rupees.py` on monthly data: dip in the event month and catch-up after?
- Question it answers: is the dark-asset markdown (README 5.17) matched by output that is really lost?

## Step 3. Hazard triggers from official data — DONE (README 5.15, 5.18, 5.22)
- [x] Pollution-control orders 2022–2024 read from the government releases; construction ban is a Stage III measure; Stage III dates tested (`src/24`).
- [x] Delhi daily AQI for three winters, used as a continuous treatment (`src/29`): −0.3 pp next-day for NCR builders per 100 AQI points (p = 0.01).
- [x] Rainfall triggers rebuilt on the official IMD 0.25° grid, 2000–2025 (`src/31`): same null for rainfall-defined exposure; IMD and NASA disagree on most individual episodes.
- [x] River levels and dam outflow from press quoting official gauges (README 5.15).
- [ ] Official river-gauge and dam-release series (request **M8**); station-level hourly air quality (**M10**, optional).

## Step 4. Proper propagation test — WAITING FOR DATA
- [ ] Supplier and customer lists with revenue shares for the 61 traded firms (request **M3**), then replace the 11 verified links and run the dose-response regression (reaction vs dependence share) with unlinked same-industry firms as the placebo (`src/10_verified_links.py`).

## Step 5. Pricing model — DONE in its current form (README 5.13, 5.23)
- [x] Interruption bound per event (`src/21`) and expected annual outage loss per firm (`src/28`): ₹232 crore a year (central) to ₹6,185 crore (extreme upper bound) for the 61 firms.
- [x] Market-implied outage markdown from the dark-asset price effect: ₹21,716 crore a year.
- [x] Damage term: insurer provisions and industry insured-loss estimate for Michaung found; no company booked a charge (README 5.21). No firm-level damage figure exists in public filings.
- [x] Deliverable: `outputs/tables/deliverable_firm_risk_card.csv` (exposure map, concentration, hazard frequency, outage loss, market markdown, caveats) for 81 firms.
- [ ] If monthly output (Step 2) shows lost output, add a lost-sales term; if propagation (Step 4) is real, add a supply-chain term.

## Step 6. Out-of-sample test and scale-up — PARTLY DONE (README 5.16)
- [x] Fit on 2020–24, test on Jan 2025–Sep 2026 with the existing 61 firms (`src/26`, `src/27`): the rainfall elasticity does not carry over; concentration → volatility does; hazard maps persist weakly.
- [ ] Plant locations and share counts for a few hundred more firms (request **M4**); prices can then be fetched automatically with `src/26_fetch_extend.py`.

## Automated access (what works from the cloud session)
- [x] Works: NASA cloud archive (night lights; Earthdata login saved as a network secret), NASA CMR (use point queries, not file-name wildcards), Copernicus catalogue (search), EODC flood monitoring, Microsoft Planetary Computer, Yahoo Finance chart API, NASA POWER (MERRA-2 to 30 Sep 2026, near-real-time model after), IMD Pune gridded rainfall (POST form), robbieandrew.github.io (Grid-India daily data), pib.gov.in, ppac.gov.in, caqm.nic.in, sansad.in, gicouncil.in (www), haryanarera.gov.in, the Jina page reader.
- [x] Does not answer (remote end drops the connection; not a policy block): grid-india.in, vahan.parivahan.gov.in, cpcb.nic.in, ffs.india-water.gov.in, indiawris.gov.in, bhuvan / bhuvan-app1.nrsc.gov.in, web.archive.org, fert.gov.in, rubberboard.gov.in, indianrailways.gov.in, gstn.org.in, ewaybillgst.gov.in, up-rera.in, rajyasabha.nic.in, ladsweb/landweb.modaps.eosdis.nasa.gov, dosairnowdata.org.
- [ ] NASA GES DISC (Sentinel-5P, rainfall) needs the "NASA GESDISC DATA ARCHIVE" application approved on the user's Earthdata profile (optional; a public mirror was used).

## Known limits to keep in mind
- 61 traded firms; the dark-asset result rests on 19 firm-episodes with ≥ 5% of plant cost dark.
- Plant cost shares are unaudited relative weights.
- Market cap uses current share counts, so historical rupee values are approximate.
- Some verification rows rest on page summaries, not original text (flagged row by row in `research/`).
