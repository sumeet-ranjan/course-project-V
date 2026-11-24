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
