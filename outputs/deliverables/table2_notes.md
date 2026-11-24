# Table 2: propagation dose-response (deliverable 3(ii)). How to read it

Built by `src/58_tables_dose_placebo.py`. Files: `table2_dose_response.csv` (one row per firm or test) and
`table2_dose_response_fit.csv` (slopes and permutation p-values).

**Panel A: NCR, backward (H3): the within-zone contractors of the hit builders.**
- **Firms:** eight contractors.
  - Three are linked: Ahluwalia ← DLF, B.L. Kashyap ← DLF, J. Kumar ← NBCC.
  - Five were screened and found unlinked (NCC, PSP, Cemindia/ITD, L&T, Capacit'e), and enter at zero dose.
- **Dose used:**
  - Dose = the builder's share of the contractor's sales (midpoint of the bracket in `verified_links.csv`) × the
    builder's share of plant cost in NCR districts (DLF 0.42, NBCC 0.94).
  - Ahluwalia: 0.067 × 0.42 = 0.028. B.L. Kashyap: 0.390 × 0.42 = 0.164. J. Kumar: 0.025 × 0.94 = 0.024.
  - The event (GRAP Stage III/IV) is common to all links, so event severity is a constant.
- **Own direct exposure:** each contractor's NCR share of its order book at 31 Dec 2024 sits beside the dose
  (columns `own_ncr_orderbook_share`, `own_ncr_share_low/high`; sources in `research/realign/contractor_ncr_orderbook.csv`).
  - Ahluwalia has 33.3% of its order book in Delhi NCR, so it is **directly exposed**.
  - B.L. Kashyap reports Haryana 45.4% and Delhi 10.1%, but no NCR total.
  - The other six do not disclose an NCR share.
- **With eight firms, the link dose cannot be separated from the contractors' own exposure.** The highest-dose firm
  (B.L. Kashyap) also has the largest Haryana/Delhi book, and the zero-dose firms' NCR shares are unknown.
  Sector and size cannot be controlled either.
- **Fit:** OLS slope of each outcome on the dose, with an exact permutation p-value (all 8! = 40,320 assignments of the
  doses to the firms). Outcomes are the CARs, Q3 FY25 sales growth YoY, the change in operating margin, and two checks:
  - Q2 FY25 sales growth, the quarter before the ban, as a placebo outcome;
  - the change in growth from Q2 to Q3.
- **Result:**
  - No relation between dose and any CAR (p = 0.67–1.00).
  - Without the two takeover targets among the zero-dose firms (PSP: Adani Infra, 19 Nov 2024; Cemindia/ITD: Renew
    Exim DMCC, 25 Oct 2024; n = 6), the CAR slopes are still null (p = 0.47–0.93). The Q3 sales slope (p = 0.03) is
    again matched by the pre-ban quarter (p = 0.04).
  - The Q3 sales slope (p = 0.05) is matched by the same slope on the pre-ban quarter (p = 0.05). It reflects B.L.
    Kashyap's earlier decline. It vanishes on the change in growth (p = 0.79) and without B.L. Kashyap.

**Panel B: Gujarat, forward (H2): Tata Chemicals → Tata Consumer.**
- **One verified link, so there is no slope.**
- **Weight:** Tata Chemicals' share of Tata Consumer's material input cost, FY24, 18.2–24.0%.
- **Supplier's hit:** about 10 days at Mithapur; 40,000 t of salt lost, against 13.48 lakh t of annual salt demand from
  Tata Consumer.
- **Buyer's response:** one retail price increase on Tata Salt, ₹2 on ₹28 (about 7%), from October 2024. Salt price/mix
  ran +1, +2, +6 and +8 pp in Q1–Q4 FY25, beside volume growth of +8%, 0%, +1% and +5% (`stepC_gj_tcpl_salt.csv`).
- **Supplier's volume (checkpoint-5 review):** Tata Chemicals' India salt sales were 326, 322, 354 and 346 kt in
  Q1–Q4 FY25, against 312, 338, 324 and 371 kt a year earlier (+4.5%, −4.7%, +9.3%, −6.7%;
  `research/realign/tatachem_salt_volumes.csv`). In its Q2 call the company said "the numbers are almost same, we were
  behind a bit from our plan". Q4 also fell, with no storm.
- **Mechanism, as worded at the checkpoint-5 review:** cost stated by both firms; the volume stall in the storm quarter
  is unexplained and consistent with lost supply. The Q2 call's "8% ... 1%" sentence does not say volume or revenue; the
  Q2 figures come from the deck, and the call figure is marked unlabelled.
- **Magnitude** (`stepC_gj_salt_magnitude.csv`):
  - No document gives the part of the storm cost passed to Tata Consumer.
  - Tata Chemicals put its whole weather cost at about Rs 40 cr.
  - A 7% increase is worth at least Rs 110.4 cr a year (7% × FY24 purchases of Rs 1,576.64 cr), about 2.8 times that
    cost. This fits the company's statement that the increase also recovers two years without an inflation increase.

**Panel C2 (the comparison; superseded at the checkpoint-5 review): NCR market level, northern capacity share.**
- **Test:** cement makers with northern capacity minus makers with none.
- **Result:** **+2.5 pp over (−1,+5), p = 0.34.** A hit would make the gap negative. It is a coarse test with little
  power: propagation is not detected.
- **Two-firm variant: run, not interpreted.** A variant against the two documented zero-capacity makers only gave
  +10.6 pp over (−1,+5), p = 0.005. It is not interpreted because it rests on two firms. No company news explains Star
  Cement's −9.2%, and Prism Johnson's −5.9% follows its loss-making Q2 results of 13 Nov 2024
  (`research/realign/news_checks.csv`).

---

## Panel C (replaced at the checkpoint-5 review): cement makers that deliver to NCR

### Specification (written 23 Nov 2026, 12:05 UTC, before any of this test was run; not changed after)

**Why this test.**
- Cement is sold close to the plant. Stage III shuts ready-mix batching plants and bans loading and unloading cement
  in NCR.
- "Northern capacity share" (the earlier market-level test) also picks up the northern price cycle, the strongest of
  any region in Q3 FY25.
- This test therefore separates capacity near Delhi from the rest of a maker's northern capacity. The earlier test is
  kept below as the comparison.

**Who delivers: three sources, all original documents.**
1. **Plants:** for every listed cement maker, each plant's place, type (integrated, clinker or grinding), cement
   capacity at Nov 2024, and road distance to Delhi. Sources are annual reports, BRSRs, decks and exchange filings
   (`research/realign/cement_plants_*.csv`). The pack's plants.csv is not used.
   - Capacity: at 30 Sep or 31 Dec 2024 where stated; otherwise 31 Mar 2024 plus documented additions to Nov 2024.
   - Clinker-only units carry no cement capacity.
   - Consolidated subsidiaries are included. Ambuja is reported consolidated (with ACC, Sanghi and Penna) and ACC on
     its own.
2. **Contracts:** the approved makes of cement, ready-mix and reinforcement steel in NBCC's tender documents for
   packages live in Nov 2024, starting with Sarojini Nagar Package IV-B.
3. **Market:** the makers that bid to supply Haryana government buyers, by district, in the CCI order of
   19 Jan 2017 (Ref. Case 05 of 2013), and each maker's ready-mix plants in NCR.

Sources 2 and 3 corroborate who delivers into NCR. They do not enter the regression.

**Road distance.**
- Measured from Delhi (Connaught Place, 28.6315 N, 77.2167 E) to the plant's town, using the OSRM public router on
  OpenStreetMap roads.
- Towns are geocoded with OSM Nominatim and checked against the project's district centroids. Where the geocode is
  more than 60 km from its district centroid, the centroid is used and the plant is flagged.

**Dose.**
- **Main:** `near300` = cement capacity within 300 km of Delhi by road ÷ the maker's total cement capacity
  (Nov 2024). In Q3 FY25 Ambuja reports a lead distance of 285 km and UltraTech 377 km.
- **Alternatives:**
  - `near150`, the same at 150 km;
  - `near_lead`, capacity within the maker's own reported lead distance, where it reports one.
- **Second variable:** `north_rest` = cement capacity in the northern states (Delhi, Haryana, Punjab, Chandigarh,
  Himachal Pradesh, Jammu & Kashmir, Uttarakhand, Rajasthan, Uttar Pradesh) beyond 300 km of Delhi ÷ total capacity.
  It separates the ban from the regional price cycle.

**Outcomes.**
- **CARs** around 18 Nov 2024 (market model against NIFTY 500, estimation window [−250, −30]):
  - (−1,+1), 14–19 Nov, which ends before the Adani indictment of 21 Nov, so ACC and Ambuja are included;
  - (−1,+5) and (+6,+20), without ACC and Ambuja;
  - the 17 Dec 2024 episode, (−1,+5) and (+6,+20), without ACC and Ambuja.
- **Quarterly:** Q3 FY25 sales volume and realisation per tonne, year on year, from company documents. The same
  regressions on Q2 FY25 serve as the pre-ban check.
- **Statements:** any Q3 FY25 statement on NCR (UltraTech's North row; Shree's call if one was held).

**Estimation.**
- Cross-sectional OLS of each outcome on `near300` and `north_rest`, and on `near300` alone. The same is run with
  `near150` and `near_lead`.
- **Inference:**
  - CAR outcomes: a placebo-date p for the `near300` coefficient (the same regression on 1,000 random event days).
  - Quarterly outcomes: a permutation p (10,000 random permutations of `near300` across makers, `north_rest` held
    fixed).
- **Prediction if the ban reached the suppliers:** a negative coefficient on `near300`.
- **Takeover-related makers:** those subject to an open offer, a stake purchase or an acquisition of control
  announced or pending in 1 Oct–31 Dec 2024 are flagged, and every result is reported with and without them.
- **Results announced in the window:** makers whose Q2 FY25 results fall in a CAR window are flagged.

**Size.**
- For each maker, the largest loss the ban could cause in Q3 FY25 is `near300` × D / 92, with D = 30 days under
  Stage III in the quarter. D runs from 15 Nov 08:00 to 5 Dec and from 16 Dec to 27 Dec 2024; it is 29.7–31 days
  depending on the order times.
- The test is said to be able to detect the effect only if this implied loss exceeds twice the outcome's spread under
  the null: the cross-maker s.d. of Q3 volume growth, or the placebo s.d. of the coefficient.

**Confounds to name:**
- northern prices;
- Shree's choice of price over volume;
- mergers and stake purchases announced in Oct–Dec 2024;
- new capacity;
- Q2 results dates.

**Reporting:** the result is reported whatever it is; a null is acceptable.

**Steel:** the approved rebar makes from the same NBCC documents are recorded, with the locations of their mills. If
they are the national mills, there is no local dose: the materiality bound is given and the steel test stops there,
with no regression.

**Amendment (23 Nov 2026, 12:20 UTC, before the test was run).** In a test on three towns, the 60 km geocode rule
misplaced Kotputli: the town is 110 km from the centroid of Jaipur district, so the rule put it 302 km from Delhi by road
instead of about 165 km. The rule is replaced: the geocode is kept if its address lies in the stated state and within
150 km of its district centroid; otherwise the centroid is used and the plant is flagged.

**Amendment 2 (23 Nov 2026, 12:37 UTC, before the test was run).** The plant collection showed that per-plant cement
capacity is not published by the two largest northern makers:
- **UltraTech:** its integrated report lists 24 integrated and 29 grinding units with place, district and state. Its
  decks give capacity by zone only (North 33.3 MTPA at FY24 plus 1.5 added by Dec 2024).
- **Shree:** it gives capacity for only a few plants.
- Several far-off makers also give plant lists without capacities.

A capacity-weighted share therefore cannot be computed from documents for the makers that matter most. The changes:
- **Main dose:** `near300_n` = the share of the maker's cement plants (integrated and grinding units counted alike)
  within 300 km of Delhi by road. Likewise `near150_n`, and `north_rest_n` (plants in the northern states beyond
  300 km).
- **Variant:** the capacity-weighted `near300` is kept for the makers whose every plant has a documented capacity.
- **Bound:** UltraTech's North-zone capacity (34.8 of 151.35 MTPA excluding India Cements, about 0.23) is reported as an
  upper limit on its capacity share.
- **Size:** the largest possible loss uses the count share as its stand-in.
- Everything else in the specification stands.

### Results (run 23 Nov 2026, after the specification and both amendments)

Built by `src/62_cement_geo.py` (plants, geocodes, road distances) and `src/63_cement_delivery_test.py`. Files:
`cement_plants_geo.csv` (one row per plant), `table2_cement_makers.csv` (doses, flags, outcomes per maker),
`table2_cement_fit.csv` (every regression), and Panel C of `table2_dose_response.csv` (the main rows).

**Data obtained.**
- **Plants:** 194 grey-cement plants of 23 listed makers, each from an annual report, BRSR, deck or exchange filing.
  - White-cement units and India Cements' plants are left out. India Cements became an UltraTech subsidiary only on
    24 Dec 2024.
  - 20 plants lie within 300 km of Delhi by road. Two are integrated units (UltraTech Kotputli 170 km; Shree Nawalgarh
    255 km); the other 18 are grinding units.
  - Geocodes: two plants fell back to their district centroid (flagged), and one has no road distance (UltraTech's
    Sarkipar, Chhattisgarh).
- **Ambuja and ACC:** no deck, annual report or BRSR gives their plants' capacities.
  - The site lists in their FY2023-24 annual reports give place and state for 34 units: Ambuja 14 and ACC 20, with
    Asian Concretes' two (`research/realign/cement_plants_D.csv`).
  - The group's denominator is its own count at 30 Sep 2024: 22 integrated and 21 grinding units
    (`cement_unit_counts.csv`). The deck's map "as on 30.09.2024" adds no site in a northern state, apart from
    Penna's Jodhpur clinker line, which was still under construction.
- **Nuvoco is left out.** Its annual report returned 403, and its decks list no plants. They name a 1.2 MTPA Haryana
  unit (2024) without its place.
- **Quarterly figures:** volume for 9 makers in both Q3s and 8 in both Q2s; realisation for 5 makers.
  - JK Cement's decks returned 403. Its transcript gives no volume.
  - Shree published no Q3 FY25 realisation.
  - Ambuja and ACC report net price per bag, not per tonne. Their year-on-year change is used.
- **Lead distance:** reported for Q3 FY25 by only three makers (UltraTech 377 km, Ambuja 285 km, JK Lakshmi 381 km).
  `near_lead` is therefore given per maker but cannot be estimated.

**Doses** (`table2_cement_makers.csv`): share of the maker's plants within 300 km of Delhi by road.

| Maker | Within 300 km | Within 150 km | Northern plants beyond 300 km | Plants within 300 km |
|---|---|---|---|---|
| Shree | 0.29 (5 of 17) | 0.18 | 0.24 | Khushkhera 78 km, Sikandrabad 90, Panipat 106, Laksar 191, Nawalgarh 255 |
| UltraTech | 0.17 (9 of 53) | 0.09 | 0.17 | Dadri 43, Sikandrabad 65, Jharli 87, Israna 116, Aligarh 141, Kotputli 170, Roorkee 200, Neem Ka Thana 200, Rajpura 244 |
| JK Cement | 0.17 (2 of 12) | 0.17 | 0.33 | Jharli 100, Aligarh 145 |
| JK Lakshmi (with Udaipur Cement Works) | 0.14 (1 of 7) | 0.14 | 0.29 | Jhamri 65 |
| Ambuja group (with ACC, Sanghi, Penna) | 0.07 (3 of 43) | 0.02 | 0.26 | Dadri 43, Roorkee 200, Rajpura 244 (ACC) |
| ACC | 0.05 (1 of 20) | 0 | 0.25 | Rajpura 244 |

All other makers have no plant within 300 km. Ambuja's Ropar plant lies just outside, at 310 km.

**Takeover-related makers** (a party to a deal in a cement business: open offer, stake purchase or acquisition of
control, 1 Oct–31 Dec 2024):
- Ambuja: Orient Cement, 22 Oct.
- Orient: Ambuja's open offer.
- UltraTech: India Cements, CCI approval 20 Dec and control 24 Dec; Kesoram's cement business, NCLT sanction
  26 Nov; a Star Cement stake, 27 Dec.
- India Cements, the target.
- Star Cement: UltraTech's stake purchase; a report of an Adani bid, clarified on 4 Dec.
- Kesoram, which has no prices.

*Deviation, stated plainly:* the first run flagged every merger or stake filing in the events file. That flag caught
captive-power stakes (Birla, Heidelberg), internal amalgamations (Shree, JK Cement), promoter transfers (Mangalam), a
share sale (Ramco) and a rights issue in a subsidiary (Prism). It left one exposed maker after 19 Nov (JK Lakshmi), so the
regression was not identified. The flag was narrowed to the deals above after that run was seen. Both are reported:
the broad version is `takeover_flag_broad` and sample "(broad)" in `table2_cement_fit.csv`. Dalmia's "Acquisition"
filing of 24 Oct 2024 could not be read (403); it is unclassified and kept in.

**Result: no effect detected. The prediction was a negative coefficient on `near300`.**

| Outcome | Coefficient on near300 (with northern-rest control) | p | Without takeover-related makers | Makers (with plants near Delhi) |
|---|---|---|---|---|
| CAR 18 Nov (−1,+1), ACC and Ambuja in | +0.056 | 0.52 | +0.056 (p 0.56) | 20 (6) |
| CAR 18 Nov (−1,+5) | +0.179 | 0.19 | +0.150 (p 0.26) | 18 (4) |
| CAR 18 Nov (+6,+20) | +0.234 | 0.26 | +0.287 (p 0.15) | 18 (4) |
| CAR 17 Dec (−1,+5) | −0.137 | 0.32 | −0.051 (p 0.70) | 18 (4) |
| CAR 17 Dec (+6,+20) | −0.192 | 0.37 | −0.179 (p 0.38) | 18 (4) |
| Q3 FY25 volume, YoY | −0.319 | 0.31 | −0.356 (p 0.43) | 9 (5) |
| Q2 FY25 volume, YoY (pre-ban check) | −0.281 | 0.50 | −0.261 (p 0.79) | 8 (5) |
| Q3 FY25 realisation, YoY | +0.010 | 0.97 | not identified | 5 (3) |

- **Signs:** around 18 Nov the coefficients are positive, the wrong sign; around 17 Dec they are negative. None is
  distinguishable from zero. `near300` alone and `near150` give the same picture (p ≥ 0.13 in every window and sample).
- **Northern-rest control:** its coefficient is between −0.04 and +0.07 in every CAR window (p ≥ 0.20).
- **Reading the size:** at +0.179, a maker with Shree's dose (0.29) moved about 5 pp more than a maker with no plant
  near Delhi over (−1,+5), in the wrong direction.
  - The near-Delhi makers' own CARs over (−1,+5) were Shree +2.8%, UltraTech +0.4%, JK Cement +2.7% and JK Lakshmi +7.4%.
  - Over (+6,+20) they were +12.7%, +3.7%, +9.2% and +11.1%. Their cause was not checked.
- **Volume:** the negative Q3 coefficient is matched by the pre-ban quarter (−0.28 in Q2), so it predates the ban.
  - Shree, the highest dose, grew −7.3% in Q2 and −1.4% in Q3.
  - Every maker with both quarters grew faster in Q3 than in Q2.
- **The capacity-weighted variant is not identified:** among the exposed makers only JK Cement documents every
  plant's capacity, as amendment 2 anticipated. UltraTech's North-zone share (about 0.23) remains an upper limit on its
  capacity share.
- **Q3 FY25 statements on NCR:**
  - UltraTech's Q3 deck, North zone: "Infrastructure segment registered degrowth on account of pollution control
    measures taken in Delhi and surrounding regions, projects on hold due to farmers agitation in Punjab and completion
    of major projects like RRTS". Nothing on it in its Q3 call.
  - Shree held no Q3 FY25 call: NSE shows only results, a press release and investor meetings in Singapore. Its Q3
    release mentions NCR only for stubble procurement.
  - JK Cement's Q3 call mentions Delhi once, about elections ("not any major disruption").
  - No mention in the Q3 calls of Ambuja, ACC or JK Lakshmi.

**Size and detectability.**
- **Largest possible Q3 loss** (`near300` × 30 / 92): Shree 9.6% of the quarter's output, UltraTech 5.5%, JK Cement
  5.4%, JK Lakshmi 4.7%, Ambuja 2.3%, ACC 1.6%.
- **Quarterly test:** the cross-maker s.d. of Q3 volume growth is 7.5 pp, so twice the spread is 15 pp. Shree's largest
  possible loss, 9.6%, is below it. A full 30-day stop of all near-Delhi output implies a coefficient of −0.33, against
  twice the permutation s.d. of 0.59. **The volume test could not detect the ban's largest possible effect.**
- **CAR test:** 30 days of lost near-Delhi sales are at most `near300` × 30/365 of a year's sales. Even if every lost
  tonne were lost for good at twice the average margin, and a maker were worth only one year's operating profit, the
  implied coefficient is about −0.16. That is below twice the smallest placebo s.d. of the coefficient (2 × 0.089 = 0.18).
  At higher valuations it is proportionally smaller. **The CAR test could detect only a loss the market expected to
  last or recur, not the ban's direct size.**

**Confounds named in the specification.**
- **Northern prices:** carried by the northern-rest variable, whose coefficient is near zero. Regional prices by maker
  are not published: realisation exists for five makers, as national averages.
- **Shree's choice of price over volume**, in its Q2 FY25 call (11 Nov 2024): "we were very clear that we should try to
  retain and give more importance to price over volumes"; "We adopted very deliberately a strategy of value over
  volume" (`research/realign/cement_kpis_A.csv`). It was stated before the ban and fits Shree's low volume in both
  quarters.
- **Mergers and stake purchases, Oct–Dec 2024:** see the takeover list above. Every result is also reported without
  those makers.
- **New capacity, Apr–Dec 2024:** none documented within 300 km of Delhi.
  - UltraTech added units at Karur, Kukurdih, Jharsuguda, APCW and Arakkonam.
  - Shree added Guntur (2 Apr 2024); JK Cement Prayagraj (Jun 2024); Dalmia Ariyalur and Kadapa.
  - Nuvoco's Haryana unit (2024) is undated and outside the sample.
  - These raise volumes far from Delhi.
- **Q2 results dates:**
  - Mangalam's results (14 Nov, 14:31) fall in (−1,+1) and (−1,+5).
  - Prism's (13 Nov, 12:28) were priced on day −2, but the flag counts them conservatively.
  - Both are zero-dose makers. JK Lakshmi's results date was not obtained (fetch failed).

**Who delivers: the corroborating sources** (not in the regression).
- **Market: the CCI order of 19 Jan 2017** (Ref. Case 05 of 2013; Haryana's 2012 tender for 4 lakh t).
  - Seven makers bid by district. Shree, UltraTech, Jaiprakash, JK Cement, Ambuja and JK Lakshmi bid in about ten
    Haryana districts each, and ACC in three.
  - Lowest-bid wins: Shree 30, Jaiprakash 26, JK Cement 21, JK Lakshmi 16, UltraTech 12, Ambuja 12, ACC 6, Birla 3.
  - The makers that bid are the makers with plants near Delhi in the plant data.
- **Contracts: not obtained.** NBCC's approved makes of cement, ready-mix and rebar for the packages live in Nov 2024
  are in the works-tender documents.
  - Those documents sit on the e-procurement portal, behind a CAPTCHA, and were not attempted.
  - NBCC's public site lists only corporate tenders. Its general conditions refer to a separate list of approved makes
    that names no brand.
- **Ready-mix plants in NCR: not obtained.** UltraTech's plant locator is dynamic; ACC's and Nuvoco's pages show no
  NCR plant locations.

**Steel: stops at the materiality bound, with no regression.** No approved rebar makes could be read, so no mills
were looked up. DLF's FY24 construction outflow (Rs 1,642 cr) is at most 0.7% (Tata Steel), 0.9% (JSW Steel),
1.6% (SAIL), 3.3% (JSPL) and 4.3% (Jindal Stainless) of a steel maker's FY24 revenue.

**Comparison with the old test (Panel C2).** Makers with northern capacity minus makers with none: +2.5 pp over
(−1,+5), p = 0.34, also the wrong sign. The delivery test separates plants near Delhi from the rest of the North, and
the near-Delhi coefficient is also positive (+0.18, p = 0.19). Neither test detects propagation to cement makers.

