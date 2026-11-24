# Decision G5: NCR mechanism and confounds (decided 23 Nov 2026; corrections applied)

**The question:** along the traced NCR pathway, which mechanism does the evidence support, and what are the confounds?

## Your decision (23 Nov 2026)
- **R1 accepted on the documents and quarterly numbers:** ban → builders' sites → Ahluwalia, within the zone. The price
  claim was wrong and has been corrected below. The (+21,+60) window from 18 Nov ends on 11 Feb 2025, before Ahluwalia's
  Q3 filing (16:43 that day, after the close) and its 12 Feb call. The second-episode (+6,+20) window (26 Dec–15 Jan)
  holds no Ahluwalia disclosure either.
- **R2 accepted, worded "not detected"** (not "rejected"): the market-level test has little power.
- **R3 and R4 accepted.**
- **R5 accepted,** with two confounds added: the small- and mid-cap sell-off of Jan–Feb 2025, and Q4 seasonality.
- **Cement test:** the binary version is accepted as a coarse, labelled test. +2.5 pp is the result. The +10.6 pp variant
  is **dropped**: it rested on Star Cement and Prism Johnson, and no cause for their falls could be established (below).
- **Register:** you will download Signature Global's Q3 FY25 transcript by hand. It stays "not readable" until then.

## Corrections applied (and checked)

**Release times** (`research/realign/g5_timing_docs.csv`; all quotes checked by `src/42`):
- **Q2 FY25 results:** filed on NSE "14-Nov-2024 17:16:53", after the close. 15 Nov was a market holiday, so the first
  trading day to price them is 18 Nov, which is also the ban's day 0.
- **Q2 call:** "held on 18-11-2024 at 3.00 p.m.", 30 minutes before the close. 18 Nov prices at most its first half
  hour; 19 Nov prices the rest.
- **Q3 FY25 results:** filed "11-Feb-2025 16:43:25", after the close, and first priced on 12 Feb. The investor deck
  filed at 12:33 on 12 Feb does not mention the ban.
- **Q3 call:** the 7 Feb notice reads "12-02-2025 4.00 P.M. Hrs. (I.S.T) Conference Call …". The call started after the
  close, so its guidance cut is first priced on 13 Feb.

**Window dates** (trading calendar of the return matrix):
- 18 Nov (+21,+60) runs from 18 Dec 2024 to 11 Feb 2025.
- 17 Dec (+6,+20) runs from 26 Dec 2024 to 15 Jan 2025.

**Ahluwalia's price evidence, restated** (`outputs/deliverables/stepC_ncr_contractor_net.csv`, `stepC_ncr_disclosure_days.csv`; `src/55`):
- Net = CAR minus the mean of the five unlinked contractors (NCC, PSP, Cemindia/ITD, L&T, Capacit'e).
- p for the net comes from the same difference on random days. About 800 days are usable, because the peers' price
  history starts in Jun 2021.
- Robustness for the small- and mid-cap sell-off: the unlinked small and mid caps only (L&T excluded).

| Window (dates) | What it holds for Ahluwalia | CAR (p) | Unlinked mean | **Net (p)** | Net of small/mid only (p) |
|---|---|---|---|---|---|
| 18 Nov (0,0): 18 Nov | **Q2 results day** (results filed 14 Nov 17:16; down 2.78% by 10:32 on the profit fall); also the ban's day 0 | −2.8% (0.16) | +1.9% | **−4.7% (0.04)** | −5.0% (0.04) |
| 18 Nov (+1,+1): 19 Nov | **first day the Q2 call is priced** (call 3.00 pm on 18 Nov; GRAP-IV statement on page 8 of 13) | −1.2% (0.55) | +0.1% | −1.3% (0.55) | −1.7% (0.43) |
| 18 Nov (0,+1) | both | −4.0% (0.18) | +2.0% | **−6.0% (0.06)** | −6.7% (0.04) |
| 18 Nov (−1,+3): 14–22 Nov | the above | −11.9% (0.03) | −2.0% | −10.0% (0.06) | −9.4% (0.07) |
| 18 Nov (−1,+5): 14–26 Nov | the above | −7.8% (0.19) | −0.0% | −7.8% (0.21) | −7.5% (0.23) |
| 18 Nov (+6,+20): 27 Nov–17 Dec | no disclosure | +7.1% (0.45) | +3.1% | +4.0% (0.60) | +3.6% (0.62) |
| 18 Nov (+21,+60): 18 Dec–11 Feb | **no Ahluwalia disclosure** | −33.4% (0.02) | −1.5% | −31.9% (0.04) | −30.9% (0.06) |
| 17 Dec (−1,+5): 16–24 Dec | no disclosure | −1.1% (0.84) | +5.5% | −6.6% (0.27) | −8.0% (0.21) |
| 17 Dec (+6,+20): 26 Dec–15 Jan | **no Ahluwalia disclosure** | −19.5% (0.02) | −2.0% | −17.5% (0.07) | −16.5% (0.09) |
| 12 Feb (0,0): 12 Feb | **Q3 results day** (revenue −7.3% YoY) | −2.9% (0.15) | +1.1% | −4.0% (0.08) | −3.9% (0.10) |
| 12 Feb (+1,+1): 13 Feb | **first day the Q3 call is priced**: FY25 growth guided to 8.5–9% | −2.3% (0.25) | −0.1% | −2.2% (0.28) | −2.4% (0.27) |
| 12 Feb (0,+1) | both | −5.2% (0.08) | +1.1% | **−6.3% (0.05)** | −6.2% (0.05) |

**Reading:**
- On its two disclosure days, Ahluwalia fell 4.7% (18 Nov) and 6.3% (12–13 Feb) more than the unlinked contractors.
- Neither day is clean:
  - 18 Nov is also the ban's day 0, and B.L. Kashyap (−3.5%) and J. Kumar (−1.9%) fell that day too.
  - On 12 Feb, B.L. Kashyap also fell 3.9% with no filing of its own (its Q3 results came out on 7 Feb).
  - The guidance-cut day itself (13 Feb) is −2.2% net (p = 0.28).
- The two large late falls survive netting (−31.9%, p = 0.04; −17.5%, p = 0.07) and the small/mid-cap check. But they
  contain no Ahluwalia disclosure, and **their cause is not identified**. Candidates are the ban's January recurrences,
  the small- and mid-cap sell-off and unknown firm news. They are **not** evidence for the mechanism.

**Quarterly numbers, corrected** (the company's own figures, Q4 FY25 call of 2 Jun 2025):
- **Q3 FY25:** turnover Rs 951.95 cr, "a negative growth of 7.26%".
- **Q4 FY25:** Rs 1,215.84 cr against Rs 1,163.66 cr, "growth of 4.48%" YoY. This replaces "Q4 +27.7% QoQ (catch-up)".
  Management itself says "The 4 th Quarter is always the best quarter in terms of performance".
- **FY25:** Rs 4,098.62 cr against Rs 3,855.29 cr, **+6.3%**, below the "8.5%-9%" guided on 12 Feb 2025. The guidance
  was earlier "about 10%".
- **The company's own account of the lag:** "we lost approximately two to three months, two months in Q3 and nearly a
  month in Q4 of FY '25".

## Node table (corrected)

| Node | Own statement (original document) | Price response | Quarterly change | Reading |
|---|---|---|---|---|
| **DLF** (hit firm) | "the 2 malls in the Delhi NCR were a little delayed because of the GRAP and the stoppage of construction" (27 Jan 2025): Summit Plaza and Midtown Plaza | +5.8% over (−1,+5) (p = 0.12) | Q3 sales +0.5% YoY; construction outflow Rs 521 cr (Q2) → Rs 591 cr (Q3) | Delay confirmed and small; the cash spend did not fall; no price effect |
| **NBCC** (hit firm) | Amrapali and 70% of GPRA "severely hitted by the NGT"; project-management growth 1.2% against "8% to 10%"; a ban of "1.5 months" | −4.1% to 22 Nov (p = 0.36); +1.3% against the PSU index | consolidated Q3 sales +15.9% YoY | Hit confirmed, quantified on one segment; no price effect; upstream branch open |
| **Ahluwalia** ← DLF (material, within zone) | Q2 and Q3 calls: GRAP-IV, idle labour, guidance cut to 8.5–9%, restart on 3–4 Feb; Q4 call: "two months in Q3 and nearly a month in Q4" lost | disclosure days net of unlinked contractors: −4.7% (18 Nov, p = 0.04), −6.3% (12–13 Feb, p = 0.05); late falls not attributed (above) | Q3 −7.3% YoY; Q4 +4.5% YoY; FY25 +6.3% vs 8.5–9% guided | **Mechanism documented at this node** by the firm's statements and numbers; price evidence limited to two mixed disclosure days |
| **B.L. Kashyap** ← DLF (link verified, site hit not documented) | no mention | +0.1% over (−1,+5); net +0.1% (p = 0.99) | Q3 −25.3% YoY, already −18.3% in Q2 | Not confirmed; decline predates the ban |
| **J. Kumar** ← NBCC (not material) | no mention | +3.0% over (−1,+5); net +3.1% (p = 0.55) | Q3 +22% YoY | Low dose; no effect, as expected |
| **Unlinked contractors** | no mention | mean −0.0% over (−1,+5) | Q3 from −10.6% to +22.7% YoY | Comparison group |
| **Cement/steel, firm level** | no document links any supplier to NBCC or DLF | — | — | **The chain breaks here** (DLF's outflow is 0.7–14% of any supplier's revenue) |
| **Cement, market level** | UltraTech's North row names the curbs as one of three reasons for infrastructure degrowth; housing and commercial grew | **+2.5 pp over (−1,+5), p = 0.34** (makers with northern capacity minus makers with none; wrong sign for a hit) | — | **Not detected** (coarse, labelled test with little power) |

**The dropped cement variant:**
- It compared the northern makers with the two documented zero-capacity makers only, and gave +10.6 pp (p = 0.005).
- It rested on Star Cement (−9.2% over (−1,+5)) and Prism Johnson (−5.9%). The news check
  (`research/realign/news_checks.csv`) found:
  - **Prism Johnson** reported "a second straight quarter of losses" on 13 Nov 2024, the day before the window, and its
    "shares … fell 2.5 per cent post results".
  - **Star Cement** had no filing or news in 14–26 Nov other than its results call material (results on 8 Nov).
- No cause can be stated for Star, so the variant is dropped.

**Other firms attributing an effect** (`hit_register_NCR.csv`): Ashiana Housing (−13.64% QoQ in area constructed) and
Godrej Properties (billing milestones moved from Q3 to Q4). Signature Global, Max Estates and Unitech: not readable.

## Confounds
| Confound | Affects | Handling | Status |
|---|---|---|---|
| IGL's gas-allocation cut (18 Nov) | old direct test | IGL excluded everywhere | closed |
| Adani indictment (21 Nov) | ACC, Ambuja, Adani firms | out of controls, placebos and the cement test | closed |
| PSU rally (25 Nov) | NBCC | window ending 22 Nov; PSU benchmark | controlled |
| Ahluwalia's own Q2 results (14 Nov, after the close; priced 18 Nov) and call (18 Nov, 3.00 pm) | Ahluwalia on 18–19 Nov | cannot be separated from the ban's day 0; reported day by day | open (by construction) |
| Ban recurrences: Stage III on 3–5, 9–12, 15–17 Jan and 29 Jan–3 Feb 2025 | all late windows | recorded from PIB | (+21,+60) is not a clean post-event window |
| **Small- and mid-cap sell-off, Jan–Feb 2025** (added at G5) | Ahluwalia's late windows (a small cap) | net of the unlinked small and mid caps only: −30.9% (p = 0.06), −16.5% (p = 0.09) | reduces but does not remove the late falls; their cause is not identified |
| **Q4 seasonality** (added at G5) | any QoQ reading of Q4 | Q4 reported YoY (+4.5%) and as the full year (+6.3%); "The 4 th Quarter is always the best quarter" | handled |
| Maharashtra election (20 and 23 Nov) | developer controls | not separated | possible |
| Farmers' agitation; RRTS completion | cement market level | named by UltraTech with the curbs | cannot be separated |
| B.L. Kashyap's revenue fall before the ban | B.L. Kashyap | Q2 already −18% YoY | explains its quarter better |
| "NGT ban" wording | text screening | companies call CAQM's GRAP order the "NGT ban"; NBCC spells GRAP "graph" | manual-trace point |

## Recommendation as accepted
- **R1 (accepted on documents and quarterly numbers):** the within-zone chain is ban → builders' sites (DLF, NBCC) →
  contractor (Ahluwalia). The effect is within the zone. Price evidence at the contractor is limited to two disclosure
  days, each mixed with other news.
- **R2 (accepted, reworded):** propagation to out-of-zone suppliers is **not detected**. No firm-level link exists, and
  the market-level test (+2.5 pp, p = 0.34) has little power.
- **R3 (accepted):** NBCC's upstream branch stays open; B.L. Kashyap is a verified but unconfirmed node.
- **R4 (accepted):** the hit firms' own price responses are nil.
- **R5 (accepted, extended):** carry into the memo the Ahluwalia timing, the January recurrences, the Maharashtra
  election, the small- and mid-cap sell-off and Q4 seasonality.

## Checkpoint-4 review (23 Nov 2026): changes applied
- **18 Nov treated like February.**
  - 18 Nov is Ahluwalia's Q2 results day. Business Standard, 10:32 IST: "slipped 2.78% … after the civil construction
    company's consolidated net profit declined 29.78%".
  - 19 Nov is the first day the Q2 call is priced. The call began at 3.00 pm; the GRAP-IV statement is on page 8 of 13.
  - Net of the unlinked contractors:
    - results days: 18 Nov −4.7% (p = 0.04), 12 Feb −4.0% (p = 0.08);
    - call days: 19 Nov −1.3% (p = 0.55), 13 Feb −2.2% (p = 0.28).
  - **The days that price the company's ban statements show no significant move.**
- **Ahluwalia is directly exposed.** 33.3% of its unexecuted order book is in Delhi NCR (31 Dec 2024,
  `contractor_ncr_orderbook.csv`). Transmission is inside the zone: builder to contractor at NCR sites.
- **Dose-response:** the dose is shown beside each contractor's own NCR order-book share. With eight firms the two
  cannot be separated (`table2_notes.md`).
- **NBCC's upstream branch is closed.** NBCC's own filings name the GPRA contractors: Varindera Constructions Ltd
  (Sarojini Nagar IV-B, Rs 955.82 cr, Aug 2023), Shapoorji Pallonji & Co. Pvt Ltd (Netaji Nagar Pkg I) and Girdhari Lal
  Constructions Pvt Ltd (Sarojini Nagar Pkg I). Gaursons is on the Amrapali projects (trade press only).
  - None was listed in Nov 2024. Varindera had only filed a DRHP, on 30 Sep 2024.
  - So there is no price or filed quarterly data (`nbcc_contractors.csv`).
  - Capacit'e's NBCC order (Leisure Valley, Greater Noida) is dated 14 Feb 2025, after the event.
- **Cement:** one line kept in the table notes. The two-firm variant was run (+10.6 pp, p = 0.005) and is not
  interpreted, because it rests on two firms.

## Checkpoint-5 review (23 Nov 2026): corrections applied
- **The call days stand as reported.** 19 Nov −1.3% (p = 0.55) and 13 Feb −2.2% (p = 0.28), net: not
  distinguishable from zero.
- **18 Nov for Ahluwalia** is now labelled "day 0 of the ban and Q2 results day; not separable".
  - **B.L. Kashyap** is placed beside it. It filed nothing between its Q2 results of 11 Nov and a routine
    trading-window notice on 31 Dec 2024.
  - Net of the unlinked contractors, on 18 Nov: B.L. Kashyap −5.4% (p = 0.06); Ahluwalia −4.7% (p = 0.04).
  - Over (−1,+5): B.L. Kashyap +0.1% (p = 0.99); Ahluwalia −7.8% (p = 0.21).
  - The firm without news of its own fell on day 0 about as much as Ahluwalia.
- **Takeover targets among the unlinked contractors**, flagged in `stepC_ncr_unlinked_flags.csv`:
  - PSP Projects: NSE news query at 15:30 on 19 Nov 2024 ("Adani Group in advanced stage talks to buy 60% stake");
    Adani Infra open offer that evening.
  - Cemindia, then ITD Cementation: open offer by Renew Exim DMCC, 25 Oct 2024 (after 22:00).
  - Every net figure is now reported with and without them (columns `net_ex_targets`, `p_net_ex_targets_two_sided`).
  - Without them: 18 Nov Ahluwalia −4.4% (p = 0.05) and B.L. Kashyap −5.0% (p = 0.07); (−1,+5) Ahluwalia −11.6%
    (p = 0.08); 19 Nov −0.1% (p = 0.95); 13 Feb −2.7% (p = 0.24).
- **Zero-alpha CARs (beta kept)** are now beside the market-model CARs for (+6,+20) and (+21,+60), in table 1 and both
  node tables.
  - Ahluwalia (+21,+60): −33.4% market model; −29.7% zero-alpha (p = 0.02); net −26.7% (p = 0.06); net without the
    takeover targets −19.4% (p = 0.15).
  - 17 Dec (+6,+20): −19.5%; zero-alpha −19.0% (p = 0.03); net −17.1% (p = 0.08).
  - Your alpha terms reproduce exactly: Unitech −17.7 of −23.5, RVNL −13.0 of −17.3, Anant Raj −9.5 of −18.1,
    NBCC −6.6.
- **Steel: the approved makes could not be retrieved.** NBCC's works tenders sit on the e-procurement portal behind a
  CAPTCHA, which was not attempted. NBCC's general conditions only refer to a "List of approved makes of materials".
  - The test stops at the materiality bound: DLF's FY24 construction outflow (Rs 1,642 cr) is at most 0.7% (Tata
    Steel), 0.9% (JSW), 1.6% (SAIL), 3.3% (JSPL) or 4.3% (Jindal Stainless) of a steel maker's FY24 revenue.
  - No regression.

## Checkpoint-5 review (23 Nov 2026): the cement delivery test (main cement result)
The specification was written into `outputs/deliverables/table2_notes.md` before the run (12:05 UTC), with two amendments
made before the run: the geocode rule at 12:20, and plant-count doses at 12:37. Frozen copies and hashes are in
`research/realign/cement_test_spec_20261123*.md`. Full results are in `table2_notes.md` ("Results").
- **Who delivers:**
  - **Plants:** 194 plants of 23 listed makers, from original documents. 20 lie within 300 km of Delhi by road, all
    UltraTech (9), Shree (5), JK Cement (2), Ambuja (2), ACC (1) and JK Lakshmi (1). Ambuja's and ACC's units come
    from the site lists in their FY2023-24 annual reports.
  - **Market:** the CCI order (2017) names the same makers bidding district by district in Haryana.
  - **Not obtained:** NBCC's approved makes (behind a CAPTCHA, not attempted) and the makers' NCR ready-mix plants.
- **Result: null.**
  - Coefficient on the share of plants within 300 km, controlling for the rest of the North: +0.06 (p 0.52) over
    (−1,+1) with ACC and Ambuja; +0.18 (p 0.19) over (−1,+5); +0.23 (p 0.26) over (+6,+20). For 17 Dec: −0.14
    (p 0.32) and −0.19 (p 0.37).
  - The same holds without takeover-related makers and with the 150 km dose.
  - Q3 volume −0.32 (p 0.31), matched by the pre-ban quarter (−0.28, p 0.50).
- **Could it detect the ban?** No.
  - The largest possible Q3 loss is 9.6% of output (Shree), below twice the cross-maker spread of volume growth
    (15 pp).
  - A 30-day loss is too small for a CAR test unless the market expected it to last.
- **Deviation:** the takeover flag was narrowed after the first run, from every merger or stake filing to deals in a
  cement business, because the broad flag left one exposed maker. Both versions are reported.
- **Confounds named:** northern prices (the control's coefficient is near zero); Shree's price over volume (its Q2
  call); deals in Oct-Dec 2024; new capacity (none documented near Delhi); and Q2 results dates (Mangalam, Prism).
- **Steel:** stops at the materiality bound, with no regression.
- **The old market-level test** (+2.5 pp, p 0.34) is kept in the notes as the comparison.

## Close-out (24 Nov 2026): the author's calls on the cement test, and the final run
- **Accepted:** the plant-count dose as the main version; the narrowed takeover flag, with both versions kept with
  their numbers; the Ambuja and ACC denominators and no lead-distance dose.
- **Fixed before the final run:**
  - Mangalam's Aligarh grinding unit (FY2024-25 report; IBM 0.75 MTPA), giving a count dose of 0.50;
  - Nuvoco's ten plants (Bhiwani 118 km), from its own call, decks and press release and from IBM;
  - one row for the Ambuja group, so that Rajpura is not counted twice;
  - a capacity-weighted robustness dose (IBM *Indian Minerals Yearbook 2022*, Table 1, and company documents);
  - a sample without Mangalam.
- **Result: unchanged (null).**
  - Coefficient −0.06 over (−1,+1) (p 0.36), −0.01 over (−1,+5) (p 0.90), +0.03 for 17 Dec (p 0.70).
  - Every sample and dose gives p ≥ 0.23.
  - Q3 volume −0.24 (p 0.41), matched before the ban (−0.16).
  - The signs are now mixed: (−1,+1) turns negative with Mangalam in.
  - Details are in `outputs/deliverables/table2_notes.md`.

