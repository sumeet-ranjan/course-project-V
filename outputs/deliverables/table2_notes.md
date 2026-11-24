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

### Results (final run, 24 Nov 2026)

Built by `src/62_cement_geo.py` (plants, geocodes, road distances) and `src/63_cement_delivery_test.py`. Files:
`cement_plants_geo.csv` (one row per plant), `table2_cement_makers.csv` (doses, flags, outcomes per maker),
`table2_cement_fit.csv` (every regression), and Panel C of `table2_dose_response.csv` (the main rows).

**Does any conclusion change after the final fixes? No.**
- The cement test is still a null in every window, sample and dose, with every p ≥ 0.23.
- Neither test could detect the largest loss the ban could cause.
- What changed: the signs are now mixed instead of mostly positive around 18 Nov. The (−1,+1) coefficient turns
  negative with Mangalam in, and returns to +0.01 without it.

**Fixes in the final run (all decided by the author before it was run).**
- **Mangalam is not a single-site company.** Its Aligarh grinding unit was added.
  - Mangalam's FY2024-25 annual report says: "The Company has manufacturing plants in Morak (Rajasthan) and Aligarh
    (Uttar Pradesh)". This is the company's copy: the NSE copy returned no file, and the FY2023-24 report is a scan with
    no text.
  - IBM's Table 1 gives the unit 0.75 MTPA.
  - Its count dose is 0.50 (1 of 2 plants, at 145 km), against 0.19 by capacity.
- **Nuvoco added (10 plants).** Its annual report could not be read: the NSE copy refused, the BSE listing returned 403
  and the company page renders only in JavaScript. Its decks list no plants. The list rests on its own documents:
  - the Q3 FY25 call: "the Bhiwani grinding unit"; "the Chittor and the Nimbol facility";
  - the Q3 FY25 deck: capacity build-up, with "Haryana expansion (2024)" of 1.2 MTPA and a 25.0 MTPA total;
  - the decks' plant awards: Arasmeta, Sonadih, Risda, Jojobera, Panagarh and a "Bihar Cement Plant";
  - the Q3 press release: Nimbol;
  - IBM for Mejia.

  A possible Odisha unit is not documented and is left out. Bhiwani lies 118 km from Delhi. The doses are 0.10 by
  count and 0.05 by capacity.
- **One row for the Ambuja group.** Ambuja's consolidated row holds ACC's plants and volumes. ACC is therefore no longer
  a separate observation, and Rajpura is not counted twice. ACC stays in `table2_cement_makers.csv`, marked
  `in_tests = no`.
- **Capacity-weighted dose (robustness):** capacity within 300 km ÷ the maker's total capacity in Nov 2024
  (`research/realign/cement_capacity.csv`, 49 plant capacities and 9 totals).
  - Plant capacities: IBM, *Indian Minerals Yearbook 2022*, Cement, Table 1 (2020-21). Company documents for plants
    built or enlarged later: Shree Nawalgarh 3.5, Udaipur Cement Works 4.70, Nuvoco Bhiwani 1.2 and Nimbol 2.3, and JK
    Cement's own plant page.
  - Totals: company statements for Nov–Dec 2024. UltraTech's is 151.35 MTPA, the Q3 FY25 total less India Cements.
  - Three northern plants have no documented capacity and count as zero: UltraTech's Sadhraur (Rajpura, within
    300 km) and Balara (Pali), and Ambuja's Marwar Mundwa. UltraTech's capacity share near Delhi is therefore a
    lower bound.
  - IBM's 2020-21 figures miss later expansions.
- **Without Mangalam:** reported for the two main doses, because Mangalam's count dose (0.50) is the largest and its Q2
  results fell in the first windows.

**Data obtained.**
- **Plants:** 205 grey-cement plants of 24 listed makers, each from an annual report, BRSR, deck, call, exchange
  filing or IBM.
  - 22 lie within 300 km of Delhi by road. Two are integrated units (UltraTech Kotputli 170 km; Shree Nawalgarh
    255 km); the rest are grinding units.
  - White-cement units and India Cements' plants are left out. India Cements became an UltraTech subsidiary only on
    24 Dec 2024.
  - Geocodes: two plants fell back to their district centroid (flagged); Nuvoco's Bihar plant is placed at its state
    (no place given); UltraTech's Sarkipar has no road distance.
- **Ambuja and ACC units** come from the "Site Location" lists in their FY2023-24 annual reports
  (`research/realign/cement_plants_D.csv`). The group's denominator is its own count of 43 units at 30 Sep 2024
  (`cement_unit_counts.csv`).
- **Quarterly figures:** volume for 8 makers in both Q3s and 7 in both Q2s; realisation for 4.
  - JK Cement's decks returned 403. Mangalam publishes no volume.
  - Nuvoco prints no Q3 FY24 volume. Shree published no Q3 FY25 realisation.
- **Lead distance:** reported for Q3 FY25 by three makers only (UltraTech 377 km, Ambuja 285 km, JK Lakshmi 381 km), so
  the lead-distance dose cannot be estimated (accepted by the author).

**Doses** (`table2_cement_makers.csv`)

| Maker | Within 300 km (count) | Within 150 km | Northern plants beyond 300 km | Within 300 km (capacity) | Plants within 300 km |
|---|---|---|---|---|---|
| Mangalam | 0.50 (1 of 2) | 0.50 | 0.50 | 0.19 | Aligarh 145 km |
| Shree | 0.29 (5 of 17) | 0.18 | 0.24 | 0.22 | Khushkhera 78, Sikandrabad 90, Panipat 106, Laksar 191, Nawalgarh 255 |
| UltraTech | 0.17 (9 of 53) | 0.09 | 0.17 | 0.09 (lower bound) | Dadri 43, Sikandrabad 65, Jharli 87, Israna 116, Aligarh 141, Kotputli 170, Roorkee 200, Neem Ka Thana 200, Rajpura 244 |
| JK Cement | 0.17 (2 of 12) | 0.17 | 0.33 | 0.15 | Jharli 100, Aligarh 145 |
| JK Lakshmi (with Udaipur Cement Works) | 0.14 (1 of 7) | 0.14 | 0.29 | 0.08 | Jhamri 65 |
| Nuvoco | 0.10 (1 of 10) | 0.10 | 0.20 | 0.05 | Bhiwani 118 |
| Ambuja group (ACC, Sanghi, Penna) | 0.07 (3 of 43) | 0.02 | 0.26 | 0.045 | Dadri 43, Roorkee 200, Rajpura 244 (ACC) |

All other makers have no plant within 300 km. Ambuja's Ropar plant lies just outside, at 310 km.

**Takeover-related makers.** A maker is flagged if it was a party to a deal in a cement business (open offer, stake
purchase or acquisition of control) in 1 Oct–31 Dec 2024:
- Ambuja: Orient Cement, 22 Oct.
- Orient: Ambuja's open offer.
- UltraTech: India Cements (CCI approval 20 Dec, control 24 Dec); Kesoram's cement business (NCLT sanction 26 Nov); a
  Star Cement stake (27 Dec).
- India Cements: the target.
- Star Cement: UltraTech's stake purchase; a report of an Adani bid, clarified on 4 Dec.
- Kesoram: the transfer of its cement business (it has no prices).

The narrowed flag was accepted by the author. Both versions are kept:
- **Narrowed flag (main):** the "without takeover-related" column below.
- **Broad flag:** every merger or stake filing in the events file, including captive-power stakes (Birla,
  Heidelberg), internal amalgamations (Shree, JK Cement), promoter transfers (Mangalam), a share sale (Ramco) and a
  rights issue in a subsidiary (Prism).
  - It leaves 7 makers, only two with plants near Delhi (JK Lakshmi, Nuvoco).
  - Coefficients: +0.056 over (−1,+1) (p = 0.23); +0.076 over (−1,+5) (p = 0.26); +0.075 over (+6,+20)
    (p = 0.50); 17 Dec −0.038 (p = 0.57) and −0.080 (p = 0.46).
  - In the first run, before Nuvoco was added, it left one exposed maker and could not be estimated.
- Dalmia's "Acquisition" filing of 24 Oct 2024 could not be read (403). It is unclassified and kept in.

**Result: no effect detected.** The prediction was a negative coefficient on the near-Delhi share. The table gives
coefficients with the northern-rest control.

| Outcome | Count dose | p | Without takeover-related | Without Mangalam | Capacity-weighted | Makers (with plants near Delhi) |
|---|---|---|---|---|---|---|
| CAR 18 Nov (−1,+1), Ambuja in | −0.064 | 0.36 | −0.066 (p 0.35) | +0.013 (p 0.87) | −0.115 (p 0.34) | 20 (7) |
| CAR 18 Nov (−1,+5) | −0.007 | 0.90 | −0.015 (p 0.88) | +0.123 (p 0.37) | +0.038 (p 0.83) | 19 (6) |
| CAR 18 Nov (+6,+20) | +0.079 | 0.59 | +0.031 (p 0.86) | +0.233 (p 0.23) | +0.243 (p 0.33) | 19 (6) |
| CAR 17 Dec (−1,+5) | +0.032 | 0.70 | +0.090 (p 0.35) | −0.083 (p 0.54) | −0.056 (p 0.72) | 19 (6) |
| CAR 17 Dec (+6,+20) | −0.002 | 0.99 | +0.046 (p 0.75) | −0.169 (p 0.40) | −0.098 (p 0.67) | 19 (6) |
| Q3 FY25 volume, YoY | −0.236 | 0.41 | −0.242 (p 0.40) | (no Mangalam volume) | −0.303 (p 0.47) | 8 (4) |
| Q2 FY25 volume, YoY (pre-ban check) | −0.164 | 0.63 | not identified (4 makers) | (no Mangalam volume) | −0.198 (p 0.68) | 7 (4) |
| Q3 FY25 realisation, YoY | not identified (4 makers) | | | | | 4 (2) |

- **Robustness:** `near300` alone and `near150` give the same picture.
- **Northern-rest control:** its coefficient is between −0.09 and +0.11 in every CAR window and sample (p ≥ 0.21).
- **The near-Delhi makers' own CARs:**
  - (−1,+5): Shree +2.8%, UltraTech +0.4%, JK Cement +2.7%, JK Lakshmi +7.4%, Mangalam −1.4%, Nuvoco +1.2%,
    Ambuja −13.7%. Ambuja's window includes the Adani indictment, so Ambuja is excluded after 19 Nov.
  - (+6,+20): Shree +12.7%, UltraTech +3.7%, JK Cement +9.2%, JK Lakshmi +11.1%, Mangalam +4.3%, Nuvoco +5.3%.
  - Their cause was not checked.
- **Volume:** the negative Q3 coefficient is matched by the pre-ban quarter (Q2 −0.16), so it predates the ban. Shree,
  the highest dose with volume data, grew −7.3% in Q2 and −1.4% in Q3. Every maker with both quarters grew faster in
  Q3 than in Q2.
- **Q3 FY25 statements on NCR:**
  - UltraTech's Q3 deck, North zone: "Infrastructure segment registered degrowth on account of pollution control
    measures taken in Delhi and surrounding regions, projects on hold due to farmers agitation in Punjab and completion
    of major projects like RRTS". Nothing on it in its Q3 call.
  - Shree held no Q3 FY25 call: NSE shows only results, a press release and investor meetings in Singapore.
  - JK Cement's Q3 call mentions Delhi once, about elections ("not any major disruption").
  - Nuvoco's Q3 call names Bhiwani as its base for growing in the North, without any mention of the ban.
  - No mention in the Q3 calls of Ambuja, ACC or JK Lakshmi. Mangalam files no deck or call.

**Size and detectability.**
- **Largest possible Q3 loss** (count share × 30 / 92): Mangalam 16.3% of the quarter's output (it publishes no
  volume), Shree 9.6%, UltraTech 5.5%, JK Cement 5.4%, JK Lakshmi 4.7%, Nuvoco 3.3%, the Ambuja group 2.3%.
- **Quarterly test:** the cross-maker s.d. of Q3 volume growth is 6.4 pp, so twice the spread is 12.8 pp. Shree's
  largest possible loss, 9.6%, is below it. A full 30-day stop of all near-Delhi output implies a coefficient of −0.33,
  against twice the permutation s.d. of 0.52. **The volume test could not detect the ban's largest possible effect.**
- **CAR test:** 30 days of lost near-Delhi sales are at most the count share × 30/365 of a year's sales.
  - Even if every lost tonne were lost for good at twice the average margin, the implied coefficient is
    −0.16 ÷ (firm value in years of operating profit).
  - Twice the placebo s.d. of the coefficient is 0.15 in the main (−1,+1) specification and 0.21 over (−1,+5).
  - So the test could detect the direct loss only if a maker were worth about one year's operating profit. For any
    higher value, it can detect only a loss the market expected to last or recur.

**Confounds named in the specification.**
- **Northern prices:** carried by the northern-rest variable, whose coefficient is near zero. Regional prices by maker
  are not published.
- **Shree's choice of price over volume**, in its Q2 FY25 call (11 Nov 2024): "we were very clear that we should try to
  retain and give more importance to price over volumes"; "We adopted very deliberately a strategy of value over
  volume" (`research/realign/cement_kpis_A.csv`). It was stated before the ban.
- **Mergers and stake purchases, Oct–Dec 2024:** see the takeover list above. Every result is also reported without
  them.
- **New capacity, Apr–Dec 2024:** none documented within 300 km of Delhi apart from Nuvoco's Bhiwani unit (2024, date
  not given).
  - UltraTech added units at Karur, Kukurdih, Jharsuguda, APCW and Arakkonam.
  - Shree added Guntur (2 Apr 2024); JK Cement Prayagraj (Jun 2024); Dalmia Ariyalur and Kadapa.
- **Q2 results dates:**
  - Mangalam's results (14 Nov, 14:31) fall in (−1,+1) and (−1,+5): the without-Mangalam column answers this.
  - Prism's (13 Nov, 12:28) were priced on day −2, but the flag counts them conservatively.
  - JK Lakshmi's results date was not obtained.

**Who delivers: the corroborating sources** (not in the regression).
- **Market: the CCI order of 19 Jan 2017** (Ref. Case 05 of 2013; Haryana's 2012 tender for 4 lakh t).
  - Seven makers bid by district. Shree, UltraTech, Jaiprakash, JK Cement, Ambuja and JK Lakshmi bid in about ten
    Haryana districts each, and ACC in three.
  - Lowest-bid wins: Shree 30, Jaiprakash 26, JK Cement 21, JK Lakshmi 16, UltraTech 12, Ambuja 12, ACC 6, Birla 3.
- **Contracts: not obtained.** NBCC's approved makes for the packages live in Nov 2024 sit in works-tender documents.
  Those are on the e-procurement portal behind a CAPTCHA, which was not attempted. NBCC's general conditions name no
  brand.
- **Ready-mix plants in NCR: not obtained.** UltraTech's plant locator is dynamic, and ACC's and Nuvoco's pages show no
  NCR plant locations.

**Steel: stops at the materiality bound, with no regression.** No approved rebar makes could be read. DLF's FY24
construction outflow (Rs 1,642 cr) is at most 0.7% (Tata Steel), 0.9% (JSW Steel), 1.6% (SAIL), 3.3% (JSPL) and 4.3%
(Jindal Stainless) of a steel maker's FY24 revenue.

**Earlier runs, for the record.**
- **First run (23 Nov 2026):** Mangalam as single-site, Nuvoco missing, ACC and Ambuja both in.
  - Main coefficients: +0.056 over (−1,+1), +0.179 over (−1,+5), +0.234 over (+6,+20); 17 Dec −0.137 and −0.192.
  - Q3 volume −0.319. All p ≥ 0.15.
- **The old market-level test (Panel C2):** makers with northern capacity minus makers with none, +2.5 pp over (−1,+5),
  p = 0.34.

Neither version detects propagation to cement makers.

