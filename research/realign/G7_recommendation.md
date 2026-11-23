# Decision G7: Gujarat hit firms and the Tata Chemicals → Tata Consumer chain (decided 23 Nov 2026; corrections applied)

**The question:** which firms count as confirmed hit firms for the Gujarat event, and does the Tata Chemicals → Tata
Consumer chain hold as a traced forward path (H2)?

**The storm (IMD):**
- National Bulletin No. 24 (29 Aug 2024): "The deep depression over Saurashtra & Kachchh moved slowly southwestwards…"
- Tropical Cyclone Advisory No. 1 (30 Aug 2024): "DEEP DEPRESSION INTENSIFIED INTO A CYCLONIC STORM 'ASNA'".

**All four hit firms are external to the pack's 81 firms.**

## Your decision (23 Nov 2026)
- **R1 accepted, graded:**
  - Tata Chemicals and Archean are **material hits**.
  - Adani Ports and GE T&D are **confirmed but immaterial**: Adani's August cargo still grew 5%; GE T&D's sales rose 59%
    with no damage.
  - Show both rain episodes, and state that Tata Chemicals' loss cannot be split between them. Archean's loss is the
    late-August storm alone.
  - Before reading Archean's −15.8% as a storm response, compare it with specialty-chemical peers and check its news.
- **R2 accepted:** the pack's chemical belt is its own branch and breaks at Step A.
- **R3 accepted:** the chain is a cost pass-through, not a shortage. Add the last step, the retail price of Tata Salt,
  and close the 85% item.
- **R4:** 21 Oct is Tata Consumer's results day, labelled tea-driven and not attributable to salt. Propagation is
  measured with salt revenue, price and volume by quarter. Tata Chemicals is measured on 18 Oct, with 10 Oct and 21 Oct
  flagged as unrelated.
- **R5 accepted,** with those two moves added to the confounds.

## Hit firms, graded (`hit_register_GJ.csv`, column `grade`)

| Firm (site) | Pack footprint? | Grade | Own document | Number |
|---|---|---|---|---|
| **Tata Chemicals** (Mithapur, Devbhumi Dwarka) | no | **material hit** | call (filed 24 Oct 2024): operations hit "for almost 10 days"; press release: "Unprecedented heavy rains in July and August impacted Mithapur operations" | 30,000 t soda ash; 40,000 t salt; Rs 11 cr one-off in profit after tax (deck), about Rs 40 cr cost (call) |
| **Archean Chemical** (Kutch) | no | **material hit** | deck (11 Nov 2024): "Exceptional item is due to Asna cyclone impact resulting in loss of Industrial salt stock of Rs. 40.18 Crs (4.72 Lakhs MT)" | Rs 40.18 cr; 4.72 lakh t |
| **Adani Ports** (Mundra, Tuna) | no | **confirmed, immaterial** | cargo update (2 Sep 2024): "APSEZ handles 36.1 MMT of cargo in Aug’24 (+5% YoY), operations at Mundra and Tuna impacted for 4 days equivalent due to inclement weather" | 4 days equivalent; August cargo +5% YoY |
| **GE T&D India** (Vadodara) | yes | **confirmed, immaterial** | own filing (6 Sep 2024): "There is no damage to the property … except the Production disruption because the labor was unable to reach to the Plant" | no amount; sales +59% YoY in the quarter |

## The two rain episodes (`outputs/deliverables/gj_rain_episodes.csv`; NASA POWER district rainfall, `src/56`)

| District | 18–24 Jul 2024 | 25–31 Aug 2024 |
|---|---|---|
| Jamnagar (pre-2013 district, includes Devbhumi Dwarka and Mithapur) | 288 mm (wettest day 76 mm) | 525 mm (wettest day 196 mm, 27 Aug) |
| Porbandar | 610 mm (wettest day 275 mm, 20 Jul) | 502 mm (wettest day 318 mm, 27 Aug) |
| Kachchh | 86 mm | 360 mm (wettest day 98 mm, 28 Aug) |

- Your figures are reproduced exactly.
- The largest 7-day Jun–Sep totals of 2024 were the highest since 2000 in Jamnagar (534 mm, to 30 Aug) and Porbandar
  (794 mm, to 22 Jul), and the second highest in Kachchh (364 mm, to 30 Aug).
- **Tata Chemicals dates its loss to "July and August".** The Mithapur area took heavy rain in both episodes, so the
  loss **cannot be split between them** from the company's documents.
- **Archean's loss is booked to "Asna cyclone"**, the late-August storm alone. Kachchh had little rain in July.

## Archean's −15.8%: peers and news (`gj_archean_vs_peers.csv`, `gj_archean_daily_ar.csv`, `research/realign/news_checks.csv`)

**CAR over (−1,+5) from 26 Aug (23 Aug–2 Sep 2024):** −15.8% (p = 0.04).

**Against specialty-chemical peers in the same window:**
- **Main peers:** the three G2 specialty controls, each with no Gujarat plant in its own documents (Vinati −1.9%, Clean
  Science −6.1%, Sudarshan −4.2%). Their mean is −4.1%. **Archean net: −11.7%** (two-sided p = 0.11; one-sided 0.04).
- **Wider set:** eight specialty names, five of them with unverified plant locations. Their mean is −3.2%. Archean net:
  −12.6% (p = 0.08).
- Placebo inference uses 494 days, because Archean listed in Nov 2022.

**Timing:**
- The fall is spread across the window: −2.4%, −1.7%, −2.1%, −1.0%, −2.6%, −1.1%, then −4.8% on 2 Sep.
- It follows a **+7.5% abnormal return on 22 Aug**, the day before the window opens.

**News, 21 Aug–24 Sep 2024:**
- No NSE filing in the window.
- The only filing near it (20 Aug) is a GST penalty of Rs 1,10,228, which is immaterial.
- No free article reports a block deal, stake sale, guidance change, bromine-price news or an accident.
- The closest company news predates the window: weak Q1 results on 5 Aug ("declined 10.26%"), and a June 2024 block
  deal seen only as a search snippet.

**Size:**
- The fall is worth about Rs 1,560 cr at the 23 Aug market cap (Rs 9,880 cr), and about Rs 1,160 cr net of peers.
- The booked loss is Rs 40.18 cr, so the price fall is 30–40 times larger.

**Reading:**
- Part of the fall is shared with peers. Part may reverse the 22 Aug jump.
- The rest is far larger than the booked storm loss and has no identified cause.
- **It is not read as a response to the storm loss.** The storm hit is established from the company's own documents,
  not from the price.

## Forward chain (H2): Tata Chemicals → Tata Consumer Products (edible salt)

**The link, from both sides:**
- **Supplier side:** Tata Chemicals' Annual Report FY2024-25: "For edible Salt, Tata Consumer Products Limited (TCPL)
  continues to be a single customer".
- **Buyer side (closes the 85% item):** Tata Consumer IAR 2022-23, Responsible Sourcing section (company web page):
  "In addition, more than 85% of the salt we offer in the market is sourced from Tata Chemicals, which is aligned to
  Tata Group’s sustainability commitments."
- **FY24 weights:** Tata Consumer is 10.2–36% of Tata Chemicals' sales; Tata Chemicals is 18.2–24.0% of Tata Consumer's
  material input cost (`verified_links.csv` row G001).

**The path, step by step:**
1. **Storm → Mithapur:** "highest ever rain since 1929" (Tata Consumer); "almost 10 days" (Tata Chemicals).
2. **Supplier cost:** the salt works could not supply brine, so "we had to buy brine which is the cost" (Tata Consumer
   Q2 call).
3. **Buyer cost, with a lag:** "September quarter the cost has not come in through us"; the cost "flows in into our
   system" in the following quarter.
4. **Retail price (the last step):** "We did have impact on cost for salt because Mithapur recorded its highest ever
   rain since 1929. And in line with mitigating the cost increase, we've announced a INR2 price increase, which will
   start getting into the market this month." (Q2 call, 18 Oct 2024).
   - **Correction:** this is **one** increase, not two. The same call puts it at "INR2 on a INR28 base, which is roughly
     around 7%". The Q3 call's "we've taken a 7% price increase after 2 years" is the same increase, in effect from
     October.
   - The earlier wording, "₹2 a pack, then 7%", was wrong.
5. **Outcome at the buyer:** margin held ("it has put us back exactly where it should be in salt. So I don't think
   there's a margin expansion there"), and market share kept rising.

**Propagation measured by quarter** (`outputs/deliverables/stepC_gj_tcpl_salt.csv`; company documents, `research/realign/tcpl_salt_kpis.csv`, 42 quotes checked):

| Period | Salt revenue | Salt volume | Implied price/mix | Retail price action | Market share |
|---|---|---|---|---|---|
| Q1 FY25 (Apr–Jun) | +9% | +8% | +1 pp | none | gains (no number) |
| Q2 FY25 (Jul–Sep) | not retrieved (Q2 deck: NSE 403, company copy empty) | +1% | — | ₹2 on ₹28 (about 7%) announced | +150 bps (MAT) |
| Q3 FY25 (Oct–Dec) | +7% | +1% | **+6 pp** | the increase in effect | +110 bps (MAT) |
| Q4 FY25 (Jan–Mar) | +13% | +5% | **+8 pp** | no new increase | +30 bps (value) |
| FY25 | +8% | +4% | +4 pp | | |

**Reading:**
- The cost reached the shelf price. Implied price/mix rose from +1 pp to +6–8 pp in the two quarters after the increase.
  Volume growth slowed to +1% in Q2 and Q3, then recovered to +5% in Q4.
- Tata Consumer gives no reason for the Q2 volume slowdown and does not mention supply.
- Price/mix also carries mix: value-added salts grew 26–35%.

**Market response:**
- **Tata Consumer:** its results day is **21 Oct 2024** (results filed at 16:52 on 18 Oct, after the close): −6.7%
  (t = −5.0). This is **tea-driven by the company's own account** ("primarily led by higher input costs for the India
  tea business") and **not attributable to salt**. 17 and 18 Oct (−1.6%, +0.1%) are shown for reference.
- **Tata Chemicals:** its results day is **18 Oct** (filed at 18:01 on 17 Oct): +1.1% (t = +0.6). Two days are flagged
  as unrelated:
  - **10 Oct:** +4.3% (t = +2.2), the first trading day after Ratan Tata's death. Business Standard: "Tata Chemicals and
    Indian Hotels Company rose up to 4 per cent … after the death of Tata Group Chairman Emeritus, Ratan Naval Tata".
  - **21 Oct:** +10.4% (t = +5.3). Zee Business: "spurted in trade today (October 21) by over 14 per cent … as the
    Reserve Bank of India rejected Tata Sons' appeal for exemption from mandatory listing"; the channel is its "3 per
    cent stake in Tata Sons".

## Confounds (carried into the memo)
- **Tea costs.** They drive Tata Consumer's margin and its 21 Oct return.
- **The price increase also recovers two years of cost inflation.** "comes after a two-year hiatus, right? So, in the
  last two years, we’ve not even taken general cost of inflation increase". The storm's share of the 7% cannot be
  separated.
- **Soda-ash prices and imports** (prices "bottomed out" in Q2; about 15% lower YoY in Q3; minimum import price). These
  drive Tata Chemicals' results more than the storm does.
- **GHCL's maintenance**, advanced to September, cut soda-ash supply in the same quarter.
- **Tata Chemicals' new capacity** came on stream in September (2.25 lakh t soda ash).
- **Unrelated Tata Chemicals moves** on 10 Oct and 21 Oct (above).
- **Archean's falling sales before the storm** (Q1 FY25 −25% QoQ) and the unexplained size of its price fall.
- **Tata Chemicals' two cost figures:** Rs 11 cr in profit after tax (deck) against about Rs 40–44 cr total cost (call).

## Recommendation as accepted
- **R1:** two material hits (Tata Chemicals, Archean) and two confirmed but immaterial (Adani Ports, GE T&D), all
  external to the pack. Tata Chemicals' loss covers both rain episodes and cannot be split.
- **R2:** the pack's chemical belt breaks at Step A.
- **R3:** Tata Chemicals → Tata Consumer is a verified, material forward link. The mechanism is a cost pass-through,
  ending in one ~7% retail price increase on Tata Salt. Margin held.
- **R4:** propagation is measured with salt revenue, volume and price by quarter. Results-day returns are reported but
  not attributed to salt.
- **R5:** the confounds above.
