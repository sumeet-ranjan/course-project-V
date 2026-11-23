# Gap map against the assignment (22 Nov 2026)

Scope: `docs_from_pack/INSTRUCTIONS.md` §2 (steps A–E), §6 (deliverables) and §7 (order of work).
Everything else in this folder is kept but no longer extended. Status codes: **done**, **partial**,
**missing**, **wrong** (must be corrected before use).

## Deliverables (§6)

| Deliverable | What exists | Status | What is missing |
|---|---|---|---|
| 1. Pathway diagram + evidence table per node, both events | Ingredients only: firm CARs, 27 call transcripts, quarterly sales and margins | **missing** | Both diagrams, both evidence tables |
| 2. Verified links file (replaces the scaffold) | `research/verified_links_all.csv`: 32 rows, 11 in-sample pairs | **partial, wrong** | No link on either deep-dive chain. Weights are mostly the supplier's sales share, not the buyer's input-cost share. No read-mode column; quotes not covered by the quote check. Failing rows: Aarti–UPL JV (supply only from Q1 FY27); Petronet → GAIL/IOC/BPCL/Torrent (no Dahej shock found); off-chain IGL, RVNL–NMDC, Adani–NTPC, SAIL–Railways |
| 3(i). Direct event study / DiD | `event_study_summary.csv` and firm CARs for both events; quarterly firm + quarter FE panel; Stage III dates | **partial** | §4 layout: a (−1,+5) window and non-overlapping wider windows (current windows overlap); matched controls (now all unexposed firms); DiD of exposed vs matched controls |
| 3(ii). Propagation dose-response | `propagation_verified_links.csv`: link CARs only, with the wrong NCR hit firms | **missing** | Regression of downstream CAR / Δmargin on dependence × hit severity, with controls |
| 3(iii). Placebos | Placebo-date p-values (direct test); scaffold linked-vs-unlinked test (to be removed) | **partial, wrong** | Placebos on control firms and on unexposed, unlinked firms. Pack controls are compromised: Torrent is a Petronet customer; Adani Green (−18.9%) and Adani Power (−9.1%) fell on 21 Nov 2024 (indictment), inside the NCR window; Essar Oil has no prices. Only MRPL is left clean |
| 4. Memo, 3–5 pages | None (README is a long log, mostly off-scope) | **missing** | The memo. Material for its "manual trace" section is listed at the bottom |

## E_NCR_GRAP_2024: hit firms = NCR builders under the construction ban; chain = their cement and steel suppliers; Maruti = within-zone comparison

| Step | What exists | Status | What is missing |
|---|---|---|---|
| A. Shock at source | Stage III order 14 Nov 2024, in force 08:00 on 15 Nov (market shut; first trading day 18 Nov, the same day as Stage IV); revoked 5 Dec; re-imposed 16 Dec (CAQM/PIB releases). Share of plant cost in NCR: NBCC 94%, Anant Raj 51%, Unitech 50%, Parsvnath 49%, DLF 42%. DLF call, 27 Jan 2025: "2 malls in the Delhi NCR were a little delayed because of the GRAP and the stoppage of construction". NBCC call, Feb 2025: "the third quarter is mostly impacted by the graph in Delhi and NCR area"; "last 1.5 months, there was a ban on construction in Delhi and NCR". No builder filed a notice with the exchange | **partial** | Documents for Anant Raj, Parsvnath and Unitech; stoppage dates per firm; the GRAP schedule was read only from a copy hosted by CREDAI |
| B. Real chain | Scaffold only (every cement and steel firm paired with every builder) | **missing** | Named cement/steel suppliers of the confirmed builders, with the builder's share of each supplier's sales |
| C. Response at each node | Builder CARs; supplier CARs only inside the scaffold test; quarterly sales and operating margin (no inventory, no input cost) | **partial** | Node CARs by week since the order; Q3 FY25 revenue, EBITDA margin, inventory, input cost and guidance from the results filings |
| D. Mechanism | DLF and NBCC name the ban. UltraTech's line about Delhi pollution measures that "slowed construction activities" comes only via trade press; UltraTech and ACC calls do not mention it | **partial** | Breadcrumbs in supplier documents. Confounds: ACC fell 7.3% on 21 Nov 2024 while UltraTech rose 1.7% (ACC's letterhead reads "Adani Corporate House"); cement demand that quarter |
| E. Diagram | None | **missing** | Diagram and evidence table |
| Maruti screen | Maruti (73% of plant cost in NCR) was wrongly used as a hit firm | **wrong** | Screen Maruti's Q3 FY25 call and filings for a disclosed GRAP effect |

## E_GJ_FLOOD_2024: Vadodara, 25 Aug–5 Sep 2024; chain = basic/organic chemicals → specialty chemicals, pharma, agrochemicals

| Step | What exists | Status | What is missing |
|---|---|---|---|
| A. Shock at source | Flood confirmed from original texts: 12.44 in of rain in Vadodara on 26 Aug; Vishwamitri at 37 ft. Rajya Sabha answer: 958 Gujarat units affected statewide (unnamed). Firms with ≥50% of plant cost in the zone: Kiri 100%, Gujarat Alkalies 89%, Bodal 88%, GNFC 87%, SRF 81%, GSFC 79%, Aarti 59%, Petronet 57%, UPL 55%. 169 exchange filings and 9 calls: no flood notice or mention. Only listed plant confirmed disrupted: GE T&D India, Vadodara (not in the sample) | **partial: no sample firm confirmed hit** | Search news and filings firm by firm. If no firm is confirmed, the chain breaks at Step A |
| B. Real chain | Gujarat Alkalies (through its GNAL JV at Dahej) → NALCO: at least 56% of the plant's caustic soda (a supplier-side share). Aarti–UPL: not live. Petronet offtakers: shock unconfirmed | **partial, wrong** | Downstream links from a confirmed hit firm, with the buyer's input-cost share |
| C. Response | Hit-firm CARs; link CARs, including invalid links | **partial** | As for NCR |
| D. Mechanism | Generic monsoon remarks only (GNFC, GAIL) | **missing** | Breadcrumbs and confound checks |
| E. Diagram | None | **missing** | Diagram and evidence table |

**Rests on summaries or snippets (re-read before use):**
- UltraTech's "slowed construction" line (trade press)
- Petronet "no outage" (search snippet)
- every link quote
- Torrent's 2015 capacity booking (news)
- RVNL–NMDC (news)

**Already caught by hand (memo material):**
- the one-day date shift
- keyword errors in the footprints
- the pack's GRAP date is two weeks early, and the construction ban is a Stage III measure
- IGL's own gas-allocation filing
- the NBCC transcript reads "graph", not "GRAP"
- the Torrent control is a Petronet customer
- the Aarti–UPL timing
- ACC is in the Adani group

**Stopped, kept as is:** night lights, flood maps, NO2, electricity, GST flows, rainfall/river hazard panels, out-of-sample test, pricing and risk card, Delhi AQI panel, Chennai and Himachal work.
