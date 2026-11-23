# Decision G7: Gujarat hit firms (Step A outside the pack) and the forward chain. Recommendation and evidence (23 Nov 2026)

**The question:** which firms count as confirmed hit firms for the Gujarat event, and does the Tata Chemicals →
Tata Consumer chain hold as a traced forward path (H2)?

**Where the evidence is** (every quote checked against the saved original by `src/42`):
- `research/realign/gj_hit_firms_docs.csv`
- `gj_tata_chain_docs.csv`
- `outputs/deliverables/hit_register_GJ.csv`
- `evidence_GJ.csv`
- `stepC_gj_*.csv`

**The storm (IMD's own records):**
- National Bulletin No. 24 (29 Aug 2024): "The deep depression over Saurashtra & Kachchh moved slowly southwestwards…"
- Tropical Cyclone Advisory No. 1 (30 Aug 2024): "DEEP DEPRESSION INTENSIFIED INTO A CYCLONIC STORM 'ASNA'".

## Hit firms (all external to the pack's 81)

| Firm (site) | In the pack's footprint? | Market cap on 23 Aug 2024 | What the firm's own documents say | Number | Price response at the storm (CAR, p) | Q2 FY25 (Jul–Sep) |
|---|---|---|---|---|---|---|
| **Tata Chemicals** (Mithapur, Devbhumi Dwarka) | no | Rs 27,307 cr | Call (filed 24 Oct 2024): "very heavy rains, which impacted our operations for almost 10 days"; "this weather impact has had 30,000 tons on soda ash and about 40,000 tons on salt"; cost "around Rs.40 crore, of which Rs.25 crore was on account of unstable operation, the increased cost, and Rs.15 crore of the insurance claim". Deck (17 Oct 2024): "PAT includes impact of ₹ 11 Cr one -off on account of unprecedented heavy rains in Mithapur". Press release: "Unprecedented heavy rains in July and August impacted Mithapur operations" | about 10 days; 30,000 t soda ash; 40,000 t salt; Rs 11 cr one-off in PAT (deck); about Rs 40 cr cost (call) | −0.8% over (−1,+5) (p = 0.81); −5.7% over (+6,+20) (p = 0.31) | sales 0% YoY, +5.5% QoQ; margin 15% (−5 pp YoY) |
| **Archean Chemical** (Kutch) | no | Rs 9,880 cr | Deck (11 Nov 2024): "Exceptional item is due to Asna cyclone impact resulting in loss of Industrial salt stock of Rs. 40.18 Crs (4.72 Lakhs MT)"; results notes (8 Nov 2024): Rs 4,018.27 lakh | Rs 40.18 cr; 4.72 lakh t | **−15.8% over (−1,+5) (p = 0.04)** | sales −17% YoY |
| **Adani Ports** (Mundra, Tuna) | no | Rs 3,43,518 cr | Cargo update (2 Sep 2024): "operations at Mundra and Tuna impacted for 4 days equivalent due to inclement weather" | 4 days equivalent | −2.4% (p = 0.53); −7.3% over (+6,+20) (p = 0.24) | sales +6% YoY, −6.5% QoQ |
| **GE T&D India** (Vadodara) | **yes** | Rs 43,922 cr | Own filing (6 Sep 2024) refers to "our earlier disclosure dated August 27, 2024" and says: "There is no damage to the property … except the Production disruption because the labor was unable to reach to the Plant." The 27 Aug notice itself was not retrieved (Business Standard relayed it on 28 Aug). Q2 call: no mention | no amount | −2.0% (p = 0.75); −19.7% over (+6,+20) (p = 0.12) | sales +59% YoY (no visible hit) |

**The pack's chemical belt** (its own branch):
- The Vadodara sites of GSFC and Gujarat Alkalies were dark on 30 Aug (night lights). Bodal's had no usable reading.
- But no pack firm's Q2 FY25 call or exchange filing (25 Aug–30 Sep 2024) attributes an effect to the flood.
- **The chain breaks at Step A** for the pack.

## Forward chain (H2): Tata Chemicals → Tata Consumer Products (edible salt)

**The link** (`verified_links.csv` row G001):
- Tata Chemicals' Annual Report FY2024-25: "For edible Salt, Tata Consumer Products Limited (TCPL) continues to be a single customer". It gives salt demand from TCPL as 13.48 lakh MT.
- **Not found:** the "more than 85% of its salt from Tata Chemicals" statement in Tata Consumer's IAR 2022-23, as read (MD&A, statutory reports, website pages). The closest lines are "Our supply partner, Tata Chemicals Limited has the largest manufacturing facility for producing vacuum evaporated salt in India" and, on the risk page, "Added alternate suppliers for Salt portfolio."

**FY24 weights (both sides agree):**
- Tata Consumer's related-party filings show purchases from Tata Chemicals of Rs 758.46 cr (H1) + Rs 818.18 cr (H2) = **Rs 1,576.64 cr**.
- Tata Chemicals' standalone note says one customer was 36% of FY24 revenue (Rs 4,384 cr), which is about Rs 1,578 cr.
- **Tata Consumer's share of Tata Chemicals' sales:** 10.2% (consolidated) to 36% (standalone).
- **Tata Chemicals' share of Tata Consumer's material input cost:** 18.2% (consolidated) to 24.0% (standalone).

**The downstream node: Tata Consumer's Q2 FY25 call (18 Oct 2024; transcript filed 23 Oct)**
- **The shock reached it as cost:** "We did have impact on cost for salt because Mithapur recorded its highest ever rain since 1929. And in line with mitigating the cost increase, we've announced a INR2 price increase".
- **The channel, in its own words:** "Remember the cost comes in at Mithapur which then flows in into our system. When we knew this cost is coming through because they had to buy brine because of the excessive rains, our own fields could not supply the brine. Therefore, we had to buy brine which is the cost."
- **The cost lagged into the next quarter:** "September quarter the cost has not come in through us."
- **The outcome:** "For salt I think more or less we mitigated the cost increase … You could see us maintaining/inching up slightly the margin."
- **Volumes kept growing:** salt market share +150 bps (MAT); India Foods +28%.

**Q3 FY25 (call 30 Jan 2025):**
- "we've taken a 7% price increase, but it has put us back exactly where it should be in salt. So I don't think there's a margin expansion there."
- Salt volume +1%; share +110 bps.
- No mention of Mithapur or of supply.

**The market (`stepC_gj_results_days.csv`; market model estimated before 26 Aug 2024):**
- **Tata Consumer:** its Q2 results were filed at 16:52 IST on 18 Oct, after the close. The first trading day to price them, 21 Oct, shows −6.7% (t = −5.0). The days you named, 17 and 18 Oct, show −1.6% and +0.1%. The call attributes the margin fall to tea: "Margin actually contracted 30 bps to 14.9%, primarily led by higher input costs for the India tea business".
- **Tata Chemicals:** its Q2 results were filed at 18:01 IST on 17 Oct and priced on 18 Oct: +1.1% (t = +0.6).

**Quarterly numbers:** Tata Consumer's consolidated sales were +12.9% YoY in Sep 2024 (margin 15%, +1 pp) and +16.8% in Dec 2024 (margin 13%, −2 pp). The Dec quarter is the one into which the salt cost "flows".

## Confounds
- **Tata Chemicals dates the rains to "July and August".** The Mithapur loss is not provably the late-August system alone, though IMD places the deep depression over Saurashtra & Kutch, where Mithapur is.
- **Tata Chemicals' two cost figures differ:** Rs 11 cr one-off in profit after tax (deck) against about Rs 40–44 cr of total weather cost (call). Both are quoted.
- **GHCL**, the other Gujarat soda-ash maker: "we advanced our plant maintenance activities to September from October, resulting in temporary volume loss in this quarter" (Q2 FY25 call). The planned boiler shutdown from 16 Sep 2024 is documented only in trade press; the filing was not retrieved. This affects soda-ash supply in the same quarter.
- **Archean's sales were already falling** (Q1 FY25 −25% QoQ), before the storm.
- **Results-day returns, 21 Oct 2024:** Tata Consumer −6.7% (t = −5.0), Tata Chemicals +10.4% (t = +5.3).
  - Tata Consumer's move is its results reaction. Its own call puts it on tea: tea costs up "about 25% to 30%", and the group margin fell "primarily" because of tea.
  - Tata Chemicals' move falls outside its own results window. It is unexplained (not checked).
- **Soda-ash market** (Tata Chemicals' calls):
  - Q2: prices "bottomed out"; imports from Iran, Russia and Turkey rose.
  - Q3: India soda-ash prices about 15% lower YoY because of imports; a minimum import price was imposed.
  - These drive Tata Chemicals' results more than the storm does.
- **New capacity:** "around the month of September, all our expansion capacities came on stream" (2.25 lakh t soda ash, 140,000 t bicarbonate). This offsets the lost volume in the same quarter.

## Recommendation (your call)
**R1. Confirm four hit firms**, all external to the pack, each from its own document:
- **Tata Chemicals (Mithapur):** about 10 days; 30,000 t soda ash; 40,000 t salt; Rs 11 cr one-off in profit after tax (deck), about Rs 40 cr cost (call).
- **Archean (Kutch):** Rs 40.18 cr; 4.72 lakh t; "Asna cyclone".
- **Adani Ports (Mundra, Tuna):** "4 days equivalent".
- **GE T&D India (Vadodara):** production disruption, no damage, no amount. The original 27 Aug notice was not retrieved; the company's own 6 Sep filing refers to it.

Three of the four are outside the pack's listed districts. Only GE T&D is inside. Record Tata Chemicals' own dating of the rains to "July and August".

**R2. Keep the pack's chemical belt as a separate branch that breaks at Step A.** The plants went dark, but no firm says anything.

**R3. Accept Tata Chemicals → Tata Consumer as a verified, material forward link (H2).**
- It is documented on both sides, with consistent FY24 weights: 18–24% of Tata Consumer's material inputs, 10–36% of Tata Chemicals' sales.
- The traced mechanism is a cost pass-through, not a shortage. The supplier bought brine; the cost flowed into Tata Consumer's salt cost in the following quarter; Tata Consumer raised Tata Salt prices (₹2 a pack from October; 7% in Q3); margin held, and volume and share grew.
- The propagation is real, but mitigated by pricing. Its measurable size at the buyer is small next to tea.

**R4. Measure Tata Consumer's market response on 21 Oct 2024**, the first trading day after its results; show 17–18 Oct alongside. Treat the −6.7% as tea-driven by the company's own account, not as salt propagation.

**R5. Carry the confounds into the memo:** tea costs, soda-ash prices and imports, GHCL's maintenance, Tata Chemicals' new September capacity, and the unexplained +10.4% on 21 Oct.
