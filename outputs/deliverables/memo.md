# Climate shocks and supply-chain propagation in India: two traced pathways

*Memo, draft of 23 Nov 2026. Decisions G1–G7 applied.*

**Supporting files:** the evidence tables, diagrams, links file and results tables are in `outputs/deliverables/`.
Every quote used here was checked by script (`src/42`) against the saved text of the original document.

## 1. Question and approach

When a localized, documented extreme event damages firms, does the damage travel along supply chains to firms outside
the event zone? We traced two events by hand, one firm and one document at a time.

**Steps (INSTRUCTIONS §2):**
- **A.** Confirm the hit firm from its own documents.
- **B.** Verify firm-to-firm links and their dependence weights.
- **C.** Measure each node: CARs, plus the next quarter's numbers.
- **D.** Find the disclosure that names the channel, and rule out confounds.
- **E.** Draw the pathway.

**Methods:**
- **Prices:** market-model event studies (NIFTY 500; estimation window [−250, −30]). Inference uses placebo event days:
  each statistic is compared with the same statistic on 1,000 random days.
- **Financials:** quarterly numbers from company filings and screener.in.
- **Scale:** the traced pathways rest on fewer than ten firms each. The p-values have little power, and they are
  reported as such.

## 2. What we found

### 2.1 NCR, winter 2024: the construction ban (GRAP Stage III/IV)

**The shock.**
- CAQM's GRAP orders stopped construction and demolition in Delhi-NCR: Stage III from 15 Nov 2024, Stage IV from
  08:00 on 18 Nov.
- Restrictions were re-imposed late on 16 Dec (first trading day 17 Dec). Stage III returned for four spells in
  January–February 2025, with Stage IV again on 15–16 Jan (PIB releases).
- Event day 0 is 18 Nov 2024.

**Hit firms (confirmed from their own documents, G3).**
- **NBCC** (34 NCR sites, 94% of its plant cost). Amrapali and 70% of its GPRA redevelopment were "severely hitted by
  the NGT". Project-management growth was 1.2%, against "8% to 10%" otherwise.
- **DLF** (48 NCR sites, 42%). "the 2 malls in the Delhi NCR were a little delayed because of the GRAP and the stoppage
  of construction".
- Neither firm's share price responded:
  - Against eight developers with no NCR project, the confirmed builders' CAR difference is +0.4 pp over (−1,+5)
    (p = 0.91).
  - DLF's construction cash outflow rose in the ban quarter, from Rs 521 cr to Rs 591 cr.
  - Three builders that were exposed but are not confirmed by their own documents fell 10.7 pp more than the controls
    (one-sided p = 0.05). They then rebounded by 10.6 pp over (+6,+20).

**Links.**
- NBCC states that it buys no construction materials itself; its contractors do. No document on either side links any
  cement or steel firm to DLF or NBCC.
- DLF's FY24 construction outflow of Rs 1,642 cr is at most 0.7–14% of any listed supplier's revenue.
- **The cement/steel hop of the assignment's suggested chain therefore breaks at the firm level.**
- Three contractor links were verified and were live during the ban:
  - **Ahluwalia ← DLF:** DLF is 3.4–10% of Ahluwalia's sales (Arbour; Downtown Phase-2, Rs 1,094.67 cr, awarded
    11 Oct 2024).
  - **B.L. Kashyap ← DLF:** 35–44% of its sales.
  - **J. Kumar ← NBCC:** 1.6–3.4%.
- These contractors' own NCR sites were under the same ban, so they are **within-zone** nodes, not out-of-zone suppliers.

**The documented node: Ahluwalia Contracts (G5).** Its own calls trace the mechanism:
- "GRAP-IV is in place … going to impact this quarter" (18 Nov 2024).
- Clients, DLF among them, paid for idle labour; the ban "got lifted around the 3rd or the 4th of February".
- FY25 growth was guided down to "8.5%-9%" from about 10% (12 Feb 2025).
- Later: "we lost approximately two to three months, two months in Q3 and nearly a month in Q4 of FY '25"
  (2 Jun 2025).

Its numbers agree:
- Q3 FY25 turnover −7.3% YoY; Q4 +4.5% YoY.
- FY25 +6.3% (Rs 4,098.62 cr against Rs 3,855.29 cr), below the guidance.

**The price evidence is weaker than the documents:**
- On its two disclosure days, Ahluwalia fell more than the five unlinked contractors: −4.7% on 18 Nov (p = 0.04) and
  −6.3% over 12–13 Feb (p = 0.05).
- Neither day is clean:
  - 18 Nov is also the ban's day 0 and the first day to price Ahluwalia's own Q2 results.
  - On 12 Feb, B.L. Kashyap also fell 3.9% with no filing of its own.
- Ahluwalia's large later falls survive netting: −31.9% net over (+21,+60), p = 0.04; −17.5% net over the second
  episode's (+6,+20), p = 0.07. **But those windows contain no Ahluwalia disclosure** (its Q3 results came after the
  close on 11 Feb, the day (+21,+60) ends). Their cause is not identified, and they are not counted as evidence.
- **Lag:** Q3–Q4 FY25, i.e. November 2024 to February 2025.

**The other nodes:**
- **B.L. Kashyap:** no mention of the ban and no price effect. Its Q3 sales fell 25% YoY, but Q2 had already fallen 18%,
  so it is not confirmed.
- **J. Kumar:** low dose, no effect, as expected.
- **NBCC's upstream branch is open:** no contractor was identified on Amrapali or GPRA.

**Out-of-zone propagation: not detected.**
- In a coarse market-level test, cement makers with northern capacity did no worse than makers with none: +2.5 pp over
  (−1,+5), p = 0.34, the wrong sign for a hit.
- UltraTech is the only supplier that names the curbs, as one of three reasons for North infrastructure degrowth. In
  the same quarter its housing and commercial segments grew.

**Register:** of the 45 rows in the NCR register, six firms attribute an effect to the ban: NBCC, DLF, Ahluwalia,
Ashiana (area constructed −13.64% QoQ), Godrej Properties (billing moved from Q3 to Q4) and UltraTech (in part).

### 2.2 Gujarat, August 2024: Cyclonic Storm Asna

**The shock.**
- The pack lists this event as the "Vadodara floods". IMD's records show a deep depression over Saurashtra and Kutch,
  25–30 Aug 2024, which "INTENSIFIED INTO A CYCLONIC STORM 'ASNA'" (Tropical Cyclone Advisory No. 1, 30 Aug).
- Rain over 25–31 Aug: Jamnagar 525 mm, Porbandar 502 mm, Kachchh 360 mm.
- An earlier episode, 18–24 Jul, brought 288 mm, 610 mm and 86 mm respectively.

**The pack's own chemical belt breaks at Step A.**
- Night lights show Vadodara plant sites of GSFC and Gujarat Alkalies dark on 30 Aug.
- But no pack firm's Q2 FY25 call or exchange filing attributes any effect to the flood.
- Their direct test has the wrong sign: +5.5 pp against sub-industry controls over (−1,+5), p = 0.05. Part of this is
  the controls themselves falling 4.7% (p = 0.10).

**All four hit firms are external to the pack's 81 firms** (G7). Three of them are outside the pack's listed districts.
- **Tata Chemicals, Mithapur (material):** operations hit "for almost 10 days"; 30,000 t of soda ash and 40,000 t of
  salt lost; Rs 11 cr one-off in profit after tax (deck), about Rs 40 cr of cost (call). The company dates the rains to
  "July and August", so the loss cannot be split between the two episodes.
- **Archean, Kutch (material):** "Asna cyclone impact resulting in loss of Industrial salt stock of Rs. 40.18 Crs
  (4.72 Lakhs MT)".
- **Adani Ports (confirmed, immaterial):** "4 days equivalent" lost at Mundra and Tuna; August cargo still +5% YoY.
- **GE T&D India, Vadodara (confirmed, immaterial):** production disruption, no damage; sales +59% in the quarter.

**Archean's price is not read as a response to the storm.**
- It fell 15.8% over (−1,+5): −11.7% net of specialty-chemical peers (one-sided p = 0.04).
- The fall is spread over the week after a +7.5% jump on 22 Aug. No company news was found for 21 Aug–24 Sep.
- At about Rs 1,560 cr (Rs 1,160 cr net of peers), it is roughly 30–40 times the booked loss.

**The forward chain (H2): Tata Chemicals → Tata Consumer (edible salt). Verified and material.**
- **The link, documented on both sides:**
  - Tata Chemicals: Tata Consumer "continues to be a single customer" for edible salt.
  - Tata Consumer: "more than 85% of the salt we offer in the market is sourced from Tata Chemicals".
  - FY24 weights: Tata Chemicals is 18–24% of Tata Consumer's material input cost; Tata Consumer is 10–36% of Tata
    Chemicals' sales.
- **The mechanism is a cost pass-through, not a shortage.** In Tata Consumer's own words, Mithapur "had to buy brine
  which is the cost". The cost reached Tata Consumer a quarter later: "September quarter the cost has not come in
  through us".
- **The last step is the shelf price.** There was one increase on Tata Salt, "INR2 on a INR28 base, which is roughly
  around 7%", in the market from October 2024. Margin held: "it has put us back exactly where it should be in salt".
- **By quarter:**
  - Implied salt price/mix (revenue growth minus volume growth): +1 pp in Q1 FY25, +6 pp in Q3, +8 pp in Q4.
  - Volume growth: +8%, +1%, +1%, +5%.
  - Market share kept rising.
- **Lag:** one quarter.
- **Not attributable to salt:**
  - Tata Consumer's −6.7% on its results day (21 Oct) is tea-driven by its own account.
  - Tata Chemicals' +4.3% on 10 Oct (after Ratan Tata's death) and +10.4% on 21 Oct (reports that the RBI had
    rejected Tata Sons' appeal for exemption from mandatory listing) are unrelated.

## 3. How strong is it

**Strength of each claim.**

| Claim | Evidence | Strength |
|---|---|---|
| NCR: ban → builders → Ahluwalia (within zone) | firms' own statements at every node; contractor revenue, guidance and the lost months; two mixed disclosure days | **documented**; price evidence weak |
| NCR: propagation to out-of-zone suppliers | no firm link; market-level test +2.5 pp (p = 0.34) | **not detected** (low power) |
| Gujarat: Tata Chemicals → Tata Consumer → retail price | both sides document the link and weights; buyer describes cost, lag, price and margin; salt price/mix by quarter | **documented**; no measurable price effect at the buyer |
| Gujarat: the pack's chemical belt | dark sites, no statement; wrong-sign test | **breaks at Step A** |

**Results tables.**
- **(i) Direct event study / DiD** (`table1_*`): no negative response at the confirmed NCR builders, and a wrong-sign
  response for the Gujarat pack belt. The DiD on quarterly outcomes is descriptive only (2–10 exposed firms, nothing
  significant).
- **(ii) Dose-response** (`table2_*`).
  - **NCR:** eight contractors, three linked and five at zero dose. Dose = the builder's share of the contractor's
    sales × the builder's NCR exposure. Exact permutation tests show no relation between dose and any CAR
    (p = 0.67–1.00).
  - The one "significant" slope, Q3 sales growth (p = 0.05), is matched by the same slope on the quarter *before* the
    ban (p = 0.05). It reflects B.L. Kashyap's earlier decline. On the change in growth it vanishes (p = 0.79), and
    without B.L. Kashyap nothing remains.
  - **Gujarat:** one verified forward link, so there is no slope to estimate.
  - Sector, size and own exposure cannot be controlled with n = 8.
- **(iii) Placebos** (`table3_placebo.csv`): unexposed, unlinked firms and the control groups return nulls.
  - The 24 NCR placebo firms: mean CAR −1.3% to +2.3%, p = 0.30–0.83. Between none and three of the 24 are
    individually significant in each window, against about one expected.
  - In Gujarat, the provisional placebo firms (−4.9%, p = 0.12) and the controls (−4.7%, p = 0.10) fell together over
    (−1,+5). That common move in late August is a caution for any peer-adjusted reading of that week, Archean's
    included.

**Confounds carried, not resolved:**
- Ahluwalia's own results on the ban's day 0.
- The January ban recurrences inside (+21,+60).
- The small- and mid-cap sell-off of Jan–Feb 2025.
- Q4 seasonality.
- The Maharashtra election in the NCR control window.
- Farmers' agitation and the RRTS completion, alongside the curbs, in UltraTech's North row.
- Tea costs at Tata Consumer.
- Two years of general cost inflation inside the 7% salt price increase.
- Soda-ash prices and imports, GHCL's maintenance and Tata Chemicals' new capacity, all in the same quarter.

## 4. What the manual trace caught that an automated pipeline would have missed or got wrong

This is the main output. Each item is a place where a pipeline driven by the pack's scaffold, keywords and filing dates
would have produced a confident and wrong answer.

1. **It would have studied the wrong firms in Gujarat.**
   - The pack's footprint points at the Vadodara chemical belt. Those firms went dark on the satellite but said nothing,
     and their stocks beat their controls.
   - The firms the storm actually hit (Tata Chemicals at Mithapur, Archean in Kutch, Adani's Kutch ports) are not in the
     pack, and none of their sites is in its listed districts.
   - The event itself is mislabelled: it was the deep depression that became Cyclonic Storm Asna, not a Vadodara flood.
   - A pipeline keyed on the pack's districts and firm list tests a non-event and misses the pathway.
2. **It would have "found" or tested a cement/steel → construction link that does not exist.**
   - The scaffold guesses links from industry codes. No document on either side links any cement or steel firm to the
     hit builders, and NBCC buys no materials itself.
   - The real chain runs through contractors whose own sites were under the ban, so the effect stays within the zone.
   - The earlier "verified links" result was withdrawn for related errors. It counted Petronet links without a confirmed
     source shock and the Aarti–UPL joint venture before it supplied anything. In Step B, a Capacit'e–NBCC contract
     was rejected because it was not live on the event date.
3. **Keyword screening misses the shock's own name.** Companies call CAQM's GRAP order "the NGT ban", and NBCC's
   transcript spells GRAP "graph". A search for "GRAP" misses both.
4. **Entity matching creates false links.** "ACC India Pvt Ltd", a contractor on DLF's Privana South, is the Arabian
   Construction Company's subsidiary, not ACC Ltd the cement maker. A name matcher draws a cement link to DLF that
   does not exist.
5. **Event timing from filing dates is wrong.**
   - Transcripts are filed days after the calls (Tata Chemicals' on 24 Oct, for results released at 18:01 on 17 Oct).
   - Results are released after the close: Tata Consumer at 16:52 on 18 Oct, so it is priced on 21 Oct; Ahluwalia at
     16:43 on 11 Feb.
   - Calls run after the close: Ahluwalia at 4.00 pm on 12 Feb, so the guidance cut is priced on 13 Feb.
   - Our own first reading made this error, and the review caught it. We had placed Ahluwalia's guidance cut inside a
     window that ends on 11 Feb.
6. **Price moves near the event that have nothing to do with it.**
   - Tata Consumer's −6.7% on 21 Oct is tea.
   - Tata Chemicals' +10.4% the same day followed reports that the RBI had rejected Tata Sons' listing exemption; its
     +4.3% on 10 Oct followed Ratan Tata's death.
   - ACC and Ambuja fell on the Adani indictment (21 Nov). IGL had its own gas-allocation cut on day 0. A PSU rally
     on 25 Nov lifted NBCC.
   - Archean's fall is 30–40 times its booked loss.
   - A pipeline that reads every abnormal return as a shock response would report all of these as propagation.
7. **Magnitude checks overturn plausible stories.**
   - DLF's construction spend rose in the ban quarter.
   - B.L. Kashyap's revenue fall began before the ban, and it alone produces the only "significant" dose-response slope.
     The pre-ban placebo outcome exposes that.
   - Tata Chemicals' Rs 11 cr and Rs 40 cr are different concepts: a one-off in profit after tax, and the total weather
     cost.
8. **Extracted numbers get double-counted.** Tata Consumer's "₹2" and "7%" are the same price increase (₹2 on a ₹28
   pack), not two increases. Our own first draft had it as two.
9. **The weight's direction and liveness matter.**
   - The forward test needs the supplier's share of the *buyer's input cost* (18–24%), not the buyer's share of the
     supplier's sales (10–36%).
   - The NCR weights had to predate the event, and the contracts had to be live on the event date (Ahluwalia's
     Downtown Phase-2 contract was awarded on 11 Oct 2024).
10. **Attribution across overlapping shocks.** Tata Chemicals' loss covers two rain episodes, July and August. An
    event-window pipeline would assign all of it to the August storm.
11. **Documents and summaries disagree.**
    - The "more than 85%" sourcing statement is not in Tata Consumer's annual-report PDF as read. It is on the report's
      web page.
    - Several facts first seen in search snippets or page summaries turned out different or unsupported once the
      original was read: the Tata Chemicals results date and a mall wrongly identified as one of the two delayed. One
      of our own quotes had a city name modernised ("Gurugram" for the transcript's "Gurgaon"); the quote check caught it.
    - Some documents refuse automated access (NSE 403s, an empty company PDF). These were recorded as gaps, not filled
      by guesswork.

## 5. Open items

- **NBCC's upstream branch:** the contractors on Amrapali and GPRA are not identified.
- **B.L. Kashyap:** a site hit is not documented.
- **Ahluwalia's late falls:** the cause is not identified.
- **Missing documents:**
  - Signature Global's Q3 FY25 transcript (the user is downloading it by hand).
  - Tata Consumer's Q2 FY25 deck (its salt revenue growth for Q2).
  - GE T&D's original 27 Aug notice.
- **Provisional:** the Gujarat placebo list.
- **Power:** with three NCR links and one Gujarat link, the dose-response cannot be estimated with any power. The result
  is a documented within-zone pathway, a documented cost pass-through, and nulls everywhere the chain breaks.
