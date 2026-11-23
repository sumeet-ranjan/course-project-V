# Project course T5 — pricing physical climate shocks through companies' real assets

**Question.** Can we link extreme climate / black-swan events to the listed companies whose
physical plants sit where the event happens, measure the effect, and turn it into a price?

**Data.** The uploaded RA pack (`data/`): 81 Indian listed firms, 3,907 plants with coordinates and
project cost, daily stock prices 2020–2025 for 61 of the firms, four documented events, and an
industry-level supply-chain scaffold. Added here (`external/`): NIFTY 500 and sector indices
(Yahoo Finance); 26 years of daily rainfall at all 478 plant districts (NASA POWER); 26 years of
river discharge for 104 key districts (GloFAS via Open-Meteo); modelled Delhi PM2.5; 13 quarters
and 12 years of financial statements plus market cap for all 61 traded firms (screener.in).
Web-verified facts and supply-chain links are in `research/`.
Round 3 (section 5.7 onward) adds independent physical proxies: daily night-time lights at every plant
(NASA Black Marble), satellite radar flood extent (Copernicus Global Flood Monitoring), daily state
electricity use (Grid-India), nitrogen dioxide (Sentinel-5P), and a sourced third-party record
(press, industry associations, insurers, government, regulators) in `research/proxy/`.

**Picking this up in a new session:** read `HANDOVER.md` first.

**What to do next:** `NEXT_STEPS.md` (to-do list) and `MANUAL_DATA_REQUESTS.md` (what to download by hand, from where, and where to save it), with templates in `manual_collection/`. `SOURCES_TO_COLLECT.md` keeps the longer background list.

Everything is reproducible: `python3 src/00_fetch_external.py`, `07_…`, `08_…`, then `03_…` to `06_…`, `09_…`, `10_…` in order.
Round 3: `13_fetch_ntl.py` (needs a NASA Earthdata login), `14_…` to `17_…`, `19_…` to `24_…`; `18_verify_quotes.py` re-checks quoted sources.
Round 4: `26_…` (extend prices and rain), `27_…` (out-of-sample), `25_…` (night lights for 66 episode-weeks, Earthdata login), `29_…` to `33_…`, then `28_…` (expected loss and risk card, needs 25 and 31).
Tables are in `outputs/tables/`, figures in `outputs/figs/`.

---

## 1. Bottom line

1. **The asset map works; the price signal is small.** We can say, for every firm and every event,
   what share of its plant assets was in the affected area. But stock prices react only weakly:
   pooled over 8 verified event dates, firms with ≥25% of assets in the zone do not differ from unexposed
   firms (difference 0.0 pp over 3 days, +1.5 pp over 10 days, placebo p = 0.26–0.97).
2. **Two events show a real-looking direct hit, one of which is a confound.**
   - *Chennai, Cyclone Michaung (Dec 2023):* exposed firms −5.6 pp vs unexposed over 5 days
     (p = 0.05), 6 of 7 negative, and the fall scales with asset share (slope p = 0.04). Recovers
     by day 40.
   - *Delhi GRAP-IV (18 Nov 2024):* −4.0 pp over 3 days (p = 0.017), but most of it is
     Indraprastha Gas (−25%), which fell that day on a gas-allocation cut, not on pollution rules.
     Without it the gap is about −2 pp and not significant. NCR real-estate names did fall about
     4 pp more than non-NCR real estate in the first week.
   - *Gujarat flood (Aug 2024):* no drop at impact; chemical-belt names drift down 3–13% over the
     following 20 days, but unexposed firms fall too (difference −1.7 pp, p = 0.77).
   - GRAP-IV 2022 and 2023, Gujarat 2023, Himachal 2023: no negative effect.
3. **Generalising beyond four events helps a little.** Using rainfall to detect every extreme
   episode at every plant district (886 district-episodes, 449 firm-episodes with ≥2% of assets
   hit), exposed firms lose 1.2–1.7% over 10 days against the market. Against *same-date
   unexposed firms* this shrinks to 0.7–1.4 pp, rises to 1.9 pp for severe episodes hitting ≥25%
   of assets, and is statistically weak (week-clustered t between −0.5 and −2.2).
4. **A usable price number, with wide error bars.** The loss-given-event elasticity is about
   **−1.7% of equity value per 100% of assets hit** over 10 days (s.e. 1.8, p = 0.35) and about
   −3.0% over 20 days (p = 0.34). A monthly panel gives −3.1% (p = 0.24) followed by a +2.2%
   rebound the next month. So the market treats these shocks as **mostly temporary**.
5. **Supply-chain propagation: no effect on average.** The pack's scaffold (every steel and cement
   firm paired with every builder) gives no signal. With 11 verified firm-to-firm links found by
   research, linked firms move −0.4% on average; two cases are worth following up (section 5.5).
6. **What is priced is concentration, not hazard.** Firms whose assets are concentrated in few
   districts have higher idiosyncratic volatility (+16 vol points for a move from fully spread to
   single-district, p < 0.001). Hazard frequency itself does not explain volatility or returns.

7. **Company accounts show nothing.** With 13 quarters of fetched financials, sales growth and
   margins of exposed firms do not fall in or after event quarters (section 5.2).
8. **Company disclosures (section 5.6):** only the Delhi construction ban has a mechanism named by
   companies (DLF, NBCC), described as a short delay. Chennai and Gujarat have none.
9. **Facts earlier stated from memory are now checked** (section 5.1): 12 confirmed, 6 corrected,
   1 wrong (Nifty did not fall on 5–6 Nov 2024), 1 unconfirmed. No conclusion changes.

10. **Round 3, independent physical proxies and official records (sections 5.7–5.15).** They settle part of what
    disclosures could not:
    - *Chennai:* the satellite shows plant sites in Chennai city and Manali–Ennore at about half
      their normal night-time light on 6–7 Dec 2023, back to normal by 10–11 Dec. The
      Sriperumbudur–Oragadam belt, where Apollo Tyres, JK Tyre and CEAT have their plants, shows
      **no dimming** from the first clear night (6 Dec). State electricity use fell 20% and 16% on
      4–5 Dec and was normal on 6 Dec. So the physical hit was real, short (2–7 days) and
      concentrated in the city, not in the tyre belt.
    - *Does the price follow the physical hit?* **In Chennai, no** (Round 4 finds that across 66
      episodes it does; see item 11). Zone firms whose sites went dark did not
      fall more than zone firms whose sites stayed lit (difference +3.6 pp per 100% of assets,
      p = 0.74). The fall of the seven Chennai firms (₹34,000 crore against unexposed firms) is
      about 300–450 times an upper bound on the operating profit a stoppage of that length could
      cost them (₹75–105 crore). The Chennai price move is therefore not the cost of the stoppage.
    - *A confound explains much of it.* 4 Dec 2023 was also the first trading day after
      state-election results; the market jumped and energy and financials led. Measured against
      their own sector indices, the Chennai firms' gap shrinks from −4.6% to −2.6 pp over 5 days
      and to −1.1 pp over 10 days (section 5.12). The earlier "one significant event" should now
      be read as **mostly sector rotation plus two small-firm moves**. (Round 4 adds an
      Apollo Hospitals statement that the cyclone hit its Chennai centres; see item 11.)
    - *Gujarat, Aug 2024:* plant sites in Vadodara were at 54% of normal light on 30 Aug (five days
      in) and normal by 7 Sep. The Bharuch, Ankleshwar and Dahej chemical belt could not be seen
      until 5–9 Sep (cloud) and was normal by then; the radar pass of 28 Aug finds flood water
      within 500 m of only 4 of 333 plants. No third party names any sample plant as shut.
    - *Gujarat, Sep 2023:* not observable. Cloud hid the Bharuch belt from 13 to 25 Sep and the radar
      passed on 15 and 27 Sep, either side of the flood.
    - *Delhi:* read from the government's own releases, the ban on building construction is a
      Stage III measure, not Stage IV (a correction to section 5.1). Across the six Stage III
      orders of 2022–2024, NCR builders show no systematic price effect (section 5.15).

11. **Round 4 (sections 5.16–5.25):**
    - **Assets that went dark are priced.** Across 66 severe rain episodes from 2020 to 2026, firms whose plant sites lost power fell by 16% per 100% of plant cost dark over 10 days, and 23% over 20 days (p < 0.001). Exposure that stayed lit had no effect. This revises the Chennai-only reading of Round 3. It rests on 19 firm-episodes with at least 5% of assets dark, and is weaker without the Chennai week (−14% at 10 days, p = 0.06).
    - **Rainfall exposure alone is not priced,** on official IMD rainfall as well as NASA's. The fitted elasticity has no power in 2025–26.
    - **Concentration still raises volatility out of sample.**
    - **Delhi:** bad-air days predict next-day underperformance of NCR builders (−0.3 percentage points per 100 AQI points, p = 0.01). The construction-ban orders add nothing.
    - **Chennai:** Apollo Hospitals names the cyclone as a drag. Insurers provisioned ₹754 crore (GIC Re), against an industry insured loss estimated at ₹2,500 crore. The Indian space agency's radar map of 7 Dec 2023, now found and georeferenced, shows no flood water within 1 km of any tyre plant.
    - **The price:** the physical cost of outages is tiny, about ₹230–510 crore a year for all 61 firms. The market markdown implied by the dark-asset effect is about ₹21,700 crore a year.

## 2. Problems found in the pack (fix these before any further work)

| Issue | Effect if ignored | Handling here |
|---|---|---|
| **Stock dates are one day early** for 60 of 61 firms (trading days appear Sunday–Thursday; RAJESHEXPO alone is right) | Every event window is off by a day; same-day correlation with NIFTY is 0.04 instead of 0.88 | Shifted +1 day (`src/common.py`) |
| **Himachal exposure is wrong.** Substring matching on "una", "bilaspur", "hamirpur" also catches Guna, Junagadh, Virudhunagar, Yamunanagar, Bilaspur (Chhattisgarh), Hamirpur (UP), Arunachal Pradesh | 47 of 83 "Himachal" plant rows are in other states; 22 "exposed" firms become 13 | Exact district lists |
| Keywords "tiruvallur" and "panchmahal" never match the data's "Thiruvallur" and "Panch Mahals" | Chennai and Gujarat exposure understated | Added |
| GRAP event start is 5 Nov 2024; Stage IV came into force 18 Nov 2024 | Wrong window: the 5 Nov result (−6.5 pp at 10 days) starts two weeks before the order | Both dates run; 18 Nov and the 2022/2023 dates are now verified (section 5.1) |
| 20 of 81 firms have no prices (merged or delisted: IPCL, JSW Ispat, Tata Steel BSL, Ansal, …) | Sample is 61 firms, not 81 | Dropped from return tests |
| Financials are one quarter (Dec 2024) for 64 firms, not a panel; `revenue_proxy_cr` is in rupees, not crore; capex is empty | No before/after test on fundamentals is possible | Replaced by fetched quarterly and annual statements (section 5.2) |
| NMDC +86% on 26 Oct 2022 (demerger, unadjusted); 23 Jun 2020 duplicated for every firm | Outliers in estimation windows | Removed |
| 25% of plants have zero project cost; some "districts" are state names (Rajasthan, Andhra Pradesh); firm totals look too large to be ₹ crore | Cost shares are relative weights only | Used as shares, never as rupee levels |

## 3. What was done

**Exposure (`src/common.py`).** For each firm and zone: plant cost in the affected districts ÷
total plant cost. After correction, 12–15 traded firms have ≥25% of assets in each of the NCR and
Gujarat zones, 7 in Chennai, 3 in Himachal.

**Direct event study (`03_event_study.py`).** Market-model abnormal returns against NIFTY 500
(estimation window −250 to −30 days), cumulated over [−1,+1] to [0,+40]. Nine event dates: the
pack's four, both verified GRAP-IV 2024 episodes (18 Nov and 17 Dec), and the recurrences the pack
names (GRAP-IV 2022 and 2023, Gujarat 2023). Significance comes from 1,000 random placebo dates with the same exposed and
unexposed firms, which accounts for same-day correlation and for sector tilts.
→ `event_study_summary.csv`, `event_study_firm_cars.csv`, `event_study_pooled.csv`, `figs/01_car_paths.png`

**Rainfall hazard panel (`04_hazard_panel.py`).** Three-day rainfall at each plant district compared
with that district's own 5-year return level (2000–2019 baseline).
- Validation: the rainfall confirms Vadodara Aug 2024 (1.2× the 5-year level), Himachal Jul 2023
  (2.0×, above anything in the 20-year baseline) and Chennai Dec 2023 (1.5–1.8×). It does **not**
  confirm the Gujarat 2023 event, which was a dam-release river flood with little local rain.
  Rainfall alone misses river floods.
- Detection: all episodes from Nov 2020 to Dec 2025, mapped to each firm's share of assets hit.
- Tests: event study on every firm-episode with a same-date unexposed benchmark; monthly panel
  with firm and month fixed effects.
→ `rain_*.csv`, `firm_month_hazard_panel.csv`, `figs/02_rain_validation.png`, `figs/03_rain_dose_response.png`

**Propagation (`05_propagation.py`).** Unexposed firms linked by the scaffold to a hit firm versus
unlinked unexposed firms. → `propagation_scaffold.csv`

**Pricing (`06_pricing.py`).** → `pricing_*.csv`, `district_asset_hazard_map.csv`, `figs/04_firm_hazard_scorecard.png`

## 4. Ways to attach a price, and how far each one gets

| Route | Formula | Status with this data |
|---|---|---|
| **Event-loss pricing** | loss = asset share hit × elasticity × market cap | Elasticity ≈ −1.7% (10 days) to −3.0% (20 days) per 100% of assets hit; not statistically distinguishable from zero. For a firm with 40% of assets hit, that is a 0.7–1.2% fall. Rupee values now computed (section 5.3) |
| **Expected annual loss** | Σ over districts (asset share × extreme episodes per year) × elasticity | Computed per firm in `pricing_firm_hazard_scorecard.csv`: 0.4–1.5% of equity value a year for the 15 most exposed firms. The `discount_if_permanent_pct` column capitalises this at 8% and is an **upper bound**; the rebound evidence says most of the loss is recovered |
| **Risk premium (is it already priced?)** | cross-section of return and volatility on hazard exposure and concentration | Concentration raises volatility; hazard frequency is not priced in returns (n = 61, low power) |
| **Fundamentals (cash-flow route)** | Δrevenue, Δmargin after the event, exposed vs not | Now tested on 13 quarters (section 5.2): no measurable effect on sales growth or margins |
| **Supply-chain pass-through** | downstream loss = dependence weight × upstream hit | 11 verified links found (section 5.5); no propagation on average, two leads to follow up |
| **Insurance-style / catastrophe pricing** | hazard return period × damage function × asset replacement value | Hazard return periods are built here; a damage function and audited asset values are missing |
| **Interruption bound (Round 3)** | share of plant cost dark × days dark ÷ 365 × annual operating profit | Computed for Chennai and Gujarat 2024 (section 5.13): at most tens of crores per firm, two to three orders of magnitude below the share-price moves. This is the defensible price of a short stoppage |
| **Expected annual outage loss (Round 4)** | Σ plants: cost share × extreme episodes/yr × P(dark) × days dark ÷ 365 × operating profit | Section 5.23: ₹232 crore a year (central) to ₹6,185 crore (extreme upper bound) for all 61 firms; firm-level values in `deliverable_firm_risk_card.csv` |
| **Market-implied outage markdown (Round 4)** | price effect per 100% dark (−15.9%, 10 days) × expected dark share per year × market cap | ₹21,716 crore a year for the 61 firms (0.30% of value); about 90 times the central physical cost |

## 5. Round 2: what the extra data and the verification changed

### 5.1 Verification of everything previously stated from memory (`research/verified_*.csv`)

| Claim | Verdict | Detail |
|---|---|---|
| GRAP-IV invoked 3 Nov 2022, revoked 6 Nov | Confirmed | CAQM order text read directly |
| GRAP-IV invoked 5 Nov 2023, revoked 18 Nov | Confirmed | From a legal-update site summarising CAQM orders |
| GRAP-IV in force 18 Nov 2024 | Confirmed | Order issued Sun 17 Nov, effective 8 am Mon 18 Nov, so 18 Nov is the first trading day |
| GRAP-IV revoked about 5 Dec 2024, re-imposed about 16 Dec | Confirmed, with an addition | Revoked 5 Dec (evening); re-imposed late evening 16 Dec (first trading day 17 Dec); revoked again 24 Dec |
| What Stage IV bans | **Corrected in Round 3 (section 5.15)** | Stage IV only adds linear public projects (highways, flyovers, pipelines). The ban on building construction across the region comes from **Stage III**, in all three years. The earlier reading here ("only the 2024 schedule bans all construction") is withdrawn. For builders the treatment date is the Stage III order |
| Gujarat 2023 flood began 17 Sep, caused by dam release | Corrected | Release began 16 Sep 10 am; Bharuch and Ankleshwar flooded 17–18 Sep. Cause is disputed: the dam authority cites heavy upstream rain, critics call it man-made |
| Gujarat 2024 flood 25 Aug – 5 Sep | Corrected | Peak rain 26–27 Aug, river peak 27–28 Aug, over by 30 Aug. No source found for plant shutdowns at Dahej, Ankleshwar or Bharuch |
| Chennai floods 4–12 Dec 2023 | Corrected | Heavy rain 3–4 Dec; most plants restarted by 6–8 Dec. Hyundai, Foxconn, Pegatron, TVS and Ashok Leyland stoppages confirmed. **No 2023 stoppage found for Apollo Tyres, MRF, JK Tyre or CEAT** (the Apollo filing that circulates is from the 2015 floods) |
| Himachal floods 8–25 Jul 2023 | Corrected | Extreme rain 7–11 Jul; Baddi belt cut off 10 Jul; state put industrial loss above ₹300 crore |
| IGL fell about 20% on 18 Nov 2024 because of a gas-allocation cut | Confirmed | Closed −19.9%; MGL −13.9%; no article mentions GRAP |
| Adani crash 21 Nov 2024; Adani falls 1–2 Feb 2023; 4 Jun 2024 election crash; 23 Mar 2020 crash | Confirmed | These are the anchors used to prove the one-day date shift in the pack |
| NMDC +86% is a demerger artefact | Corrected | Ex-date was 27 Oct 2022 (26 Oct was a holiday). The true raw price fell that day; the +86% in the pack is a data error, which is why it is removed |
| Saturday 1 Feb 2020 and Sunday 12 Nov 2023 sessions | Confirmed | Supports the date-shift fix |
| Steel rally in Nov 2022 was due to China reopening or export-duty removal | Corrected | The index was already up 11.8% by 15 Nov, before the duty removal on 19 Nov. China reopening is the likelier cause, supported only by a search snippet |
| Nifty fell around 5–6 Nov 2024 | **Wrong** | Nifty rose on 5 and 6 Nov and fell from 7 Nov. The earlier statement that the 5 Nov result "mixes in the US-election sell-off" is withdrawn; the pack date is simply two weeks before the order |
| Real-estate firms cited GRAP as a reason for price falls | Unconfirmed | No filing or article found for DLF, Anant Raj or NBCC. UltraTech's Q3 FY25 filing says Delhi pollution measures "slowed construction activities" without a figure |

Sourcing limits: several official pages blocked automated reading, so some rows rest on page
summaries rather than the original text. Each CSV row says which.

### 5.2 Fundamentals (`09_fundamentals_river_rupees.py`, `fundamentals_panel.csv`)

Quarterly panel of 61 firms, Sep 2023 to Dec 2025, firm and quarter fixed effects.
**No measurable hit to sales growth or operating margin**, from named events, rain episodes or
river-flood episodes, in the event quarter or the one after. Every coefficient is statistically
insignificant and most are positive (for example, named events: margin +3.1 pp per 100% of assets
hit, p = 0.16). In the event quarters, exposed firms' median sales growth was 3.0% against 2.0%
for unexposed firms (Chennai), 3.0% against 2.0% (Gujarat 2024), and 10.5% against 5.0% (Delhi 2024).
Shutdowns of a few days do not show up in quarterly accounts. This agrees with the share-price rebound.

### 5.3 Rupee value (`rupee_losses_named_events.csv`)

Market cap = current shares × the pack's adjusted price, so historical values are approximate.

| Event and window | Exposed firms | Combined market cap before | Change relative to unexposed firms |
|---|---|---|---|
| Chennai cyclone, 5 days | 7 | ₹7.33 lakh crore | −₹34,000 crore (−4.6%) |
| Chennai, excluding Hindustan Unilever | 6 | ₹1.31 lakh crore | −₹5,100 crore (−3.9%) |
| Delhi GRAP-IV 18 Nov 2024, 3 days | 12 | ₹9.14 lakh crore | −₹17,100 crore (−1.9%) |
| Delhi, excluding IGL | 11 | ₹8.85 lakh crore | −₹9,700 crore (−1.1%) |
| Gujarat flood 2024, 20 days | 15 | ₹3.21 lakh crore | −₹8,700 crore (−2.7%) |

Hindustan Unilever is 85% of the Chennai rupee figure. Its 38% "Chennai exposure" comes from
unaudited plant-cost data and no flood link was found, so the ex-HUL figure is the safer one.
None of these rupee amounts is a confirmed climate loss; only Chennai is statistically distinguishable from noise.

### 5.4 Flood extent and air quality

- **River discharge** (`river_validation_named_events.csv`, `figs/05_river_validation.png`): confirms
  Chennai strongly (about 2× the 5-year flow level) and Vadodara-area rivers in Aug 2024 (1.2–1.5×
  at Anand and Kheda). For the Narmada at Bharuch in Sep 2023 the model shows a spike but only
  0.9× the 5-year level, because the model does not represent dam operations. Himachal flash
  floods are also missed. **Dam releases and flash floods need the documented record.**
- **Stock reaction to 173 river-flood episodes:** none (+0.3 pp over 10 days for firms with ≥25%
  of assets hit, t = 0.3). Rainfall remains the better trigger.
- **Delhi PM2.5:** only modelled values were reachable, and they understate Delhi peaks badly
  (`delhi_pm25_grap_episodes.csv`). Official monitor data were blocked from this environment.
  The verified order dates are the reliable treatment variable.

### 5.5 Verified supply-chain links (`research/verified_links_all.csv`, `10_verified_links.py`)

32 sourced rows; 11 usable firm-to-firm links inside the sample. The best evidenced:
- Petronet LNG (Dahej) → GAIL 60%, IOC 30%, BPCL 10% of long-term volumes; Torrent Power 12% of tolling capacity (ICRA).
- Gujarat Alkalies (via its 60% joint venture) → NALCO: at least 56% of the plant's caustic soda (CARE).
- GAIL → IGL: about 78% of IGL's gas purchases (derived from IGL's annual report, approximate).
- Apollo Tyres → Maruti Suzuki (named, no share).

Not found: named customers for MRF, CEAT and JK Tyre; cement or steel suppliers to any developer;
inter-chemical links in the Gujarat belt; iron-ore customer shares for NMDC.

Across 32 event–link cases, the linked firm's 10-day abnormal return averages −0.4% and 53% are
negative, which is no propagation on average. Two cases stand out and both need a mechanism before they count:
- **Chennai:** Maruti (Apollo's customer, no Chennai assets) fell 8.4% over 10 days (4th percentile
  of its own placebo distribution). But no Apollo stoppage in 2023 could be confirmed.
- **Gujarat 2024:** Petronet's offtakers GAIL, BPCL and IOC fell 7.5–9.9% over 20 days (5th–14th
  percentile). Oil prices were falling in the same weeks, and no Dahej disruption was found.

### 5.6 Step 1 done: company disclosures (`research/step1_disclosure_findings.csv`)

A free page-reader service (Jina, the engine inside the agent-reach tool) made the exchange and
regulator sites readable. With it I pulled 407 NSE announcements (37 firm-windows,
`research/nse_announcements_index.csv`) and 25 earnings-call transcripts
(`research/transcripts/`, hits in `research/transcript_keyword_hits.csv`).

| Case | Exchange filings in the event window | Earnings call after the event | Verdict |
|---|---|---|---|
| **Delhi GRAP-IV 2024** | No stoppage notice from any of 8 firms | **DLF:** two NCR malls "a little delayed because of the GRAP and the stoppage of construction". **NBCC:** Q3 growth "mostly impacted by the GRAP", "last 1.5 months there was a ban on construction". UltraTech, ACC, Max Healthcare: no mention | **Mechanism named** by two developers; described as a short delay, no rupee figure, catch-up expected next quarter |
| **Indraprastha Gas** | IGL's own filing of 15 Nov 2024: "reduction in domestic gas allocation" | n/a | **Confound confirmed from the primary source** |
| **Chennai cyclone 2023** | No notice from any of 7 firms | Apollo Tyres, CEAT, Hindustan Unilever: no mention of the cyclone or any Chennai loss. Maruti and Apollo Hospitals transcripts unreadable; MRF and JK Tyre have none | **No mechanism found.** The one statistically significant price result has no company-level explanation so far |
| **Gujarat flood 2024** | No notice from any of 12 firms | 9 calls read; none mentions the flood. Shutdowns discussed are planned maintenance | **No mechanism found** |
| **Gujarat flood 2023** | No notice from any of 10 firms | 6 calls read; none mentions the flood | **No mechanism found** |

What this changes:
- The **Delhi construction ban is now the only event with a named company-level mechanism**, and the
  companies themselves call it a delay, not a loss. That matches the data: NCR real-estate stocks
  dipped about 4 pp in the first week and recovered, and quarterly accounts show nothing.
- The **Chennai price drop should be treated as unexplained**, not as a confirmed climate effect.
  The Maruti lead (customer of Apollo Tyres) loses its footing: Apollo reported no disruption.
- The **Gujarat offtaker lead is dropped**: Petronet's call does not mention any Dahej disruption, and
  GAIL attributes lower gas volumes to weak power demand in a long monsoon.

Source reachability with the reader: NSE announcements, BSE company pages, the pollution
commission's order list, PIB, PPAC, rating-agency PDFs and Business Standard now work. Still
unreachable: the CPCB bulletin archive, the US-embassy air-quality files, the river-gauge portal
(loads empty) and image-only PDFs.

## 5b. Round 3: independent physical proxies (Step 1b), pricing check and official records (Step 3)

### 5.7 Night-time lights at the plant coordinates (`13_fetch_ntl.py`, `14_ntl_extract.py`, `15_ntl_analysis.py`)

**Data.** NASA Black Marble daily product VNP46A2 (collection 2, 15 arc-second ≈ 450 m pixels),
244 tile-nights covering 31 days before to 30 days after each event, read at all 2,513 plants
inside the tiles (124,042 plant-nights, `external/ntl_plant_daily.csv.gz`). Five nights
(25–29 Jul 2024) are missing at NASA.

**Method.** For each plant: the 3 × 3 pixel block (about 1.4 km) around its coordinate; only
high-quality, cloud-free retrievals; tonight's radiance divided by the same pixels' own normal
(median of nights before the event and from day 15 on). A reading is used only if at least 5 of
the 9 pixels are valid and at least 80% of the surrounding 10 km is cloud-free, because readings
at a cloud edge come out low. A site is called **dark** if its first clean reading after the
event is below 60% of normal.

**Three things that were checked rather than assumed**
- *Date stamp.* The file dated UTC day D is the overpass at about 01:50 India time on D+1 (the
  companion product's view time over Chennai for the 3 Dec file is 20.32 h UTC). Dates below are
  India dates.
- *Quality flags.* Collection 2 uses 0 = high quality, 1 = poor (outlier or possible cloud),
  2–5 = poor, 255 = none. This differs from collection 1, which I had remembered.
- *Noise.* On ordinary nights the median of a cluster of sites varies by ±10–30%, and single
  nights at 0.69–0.74 occur with no event. A single low night is not evidence; the Chennai
  result rests on consecutive nights below every ordinary night and a visible recovery.

**What the satellite can and cannot see.** It measures outdoor lighting around 01:50 at the site
and its surroundings: power off or on. It does not measure output. It sees nothing through cloud,
which removes the first nights of every event here.

| Event | First nights with no reading (cloud) | First clean night | Lit zone sites read in the first week | Dark (< 60% of normal) |
|---|---|---|---|---|
| Chennai, Dec 2023 | 4 and 5 Dec | 6 Dec (68% of sites), 7 Dec (97%) | 79 of 79 | 49 (62%) |
| Gujarat, Aug 2024 | 25–29 Aug | 30 Aug (23% of sites, almost all in Vadodara) | 69 of 310 | 43 (62% of those read) |
| Gujarat, Sep 2023 | 16–19 Sep; Bharuch belt 13–25 Sep | 21 Sep (Vadodara only) | 113 of 313 | 3 (3%) |

Cluster medians, radiance ÷ normal (`ntl_subarea_summary.csv`, `figs/06_ntl_subareas.png`):

| Cluster (sites) | Nights after the event | Ordinary nights |
|---|---|---|
| Chennai city (35) | 6 Dec 0.56, 7 Dec 0.46, 10 Dec 0.86, 14 Dec 1.09 | median 1.04, lowest 0.69 (14 nights) |
| Manali–Ennore (16) | 7 Dec 0.50, 10 Dec 0.68, 11 Dec 1.01 | median 1.00, lowest 0.79 (9 nights) |
| Sriperumbudur–Oragadam (12) | 6 Dec 0.96, 7 Dec 0.94, 9 Dec 0.92, 10 Dec 1.03 | median 1.08, 10th percentile 0.77 |
| Vadodara, Aug 2024 (80) | 30 Aug 0.54, 7 Sep 0.89 | 0.89–1.06 (6 nights) |
| Bharuch–Ankleshwar–Jhagadia, Aug 2024 (68) | none until 9 Sep (0.99) | 0.98–1.47 (6 nights) |
| Dahej–Vilayat, Aug 2024 (125) | none until 5 Sep (0.74), then 14 Sep 1.06 | 0.91–1.20 (6 nights) |
| Bharuch–Ankleshwar–Jhagadia, Sep 2023 (67) | none until 26 Sep (0.87) | median 1.05, lowest 0.74 (27 nights) |
| Vadodara, Sep 2023 (80) | 21 Sep 0.92 | median 1.04, lowest 0.69 (31 nights) |

Named sites on their first clean night (`ntl_plant_event.csv`, `figs/07_ntl_plant_maps.png`):
- Apollo Tyres, Oragadam: 0.99. JK Tyre, Sriperumbudur: 0.84. CEAT: 1.13 (its second site is unlit
  in normal times, so unreadable). **None dark.**
- Hindustan Unilever's central-Chennai entry: 0.49, back above 0.8 on 10 Dec. This coordinate is
  in the old city centre and may be an office address rather than a factory.
- Apollo Hospitals: 15 of 16 Chennai sites dark. Indo Rama (Manali): 0.72. Vascon's housing project: 0.65.
- GSFC, Vadodara (Fertilizernagar): 18 of 19 sites dark on 30 Aug 2024 (0.35–0.44), 23% of its
  plant cost; next clean night 7 Sep, by then normal. Indian Oil, Koyali: 12 of 23 sites dark.

**Reading.** The Chennai outage is confirmed and dated: lights at about half on 6–7 Dec,
recovered by 10–11 Dec, in the city and the northern industrial strip. The tyre belt was lit by
the first night the satellite could see. What happened there on 4 and 5 Dec is not observable.

### 5.8 Satellite radar flood extent at the plant coordinates (`16_flood_gfm.py`)

Source: Copernicus Global Flood Monitoring, which maps flood water on every Sentinel-1 radar pass
(20 m pixels; public, no login). Radar sees through cloud, but only on the days it passes.

| Event | Radar passes (official Copernicus catalogue) | Result |
|---|---|---|
| Chennai, Dec 2023 | **None between 30 Nov 2023 and 17 Jan 2024** | No radar flood map is possible from Sentinel-1 |
| Gujarat, Sep 2023 | 15 Sep (day before the release) and 27 Sep (nine days after the peak) | Peak missed; nothing to test |
| Gujarat, Aug 2024 | 28 Aug 2024, 06:32 India time, near the river peak | 333 of 342 zone plants inside the image |

Gujarat, 28 Aug 2024 (`flood_plant_event.csv`, `figs/08_flood_gujarat_2024.png`):
- No plant coordinate sits on a flood pixel. Flood water lies within 250 m of 2 plants, within
  500 m of 4, within 1 km of 24.
- The four within 500 m: two UPL renewable-energy sites near Vagra (about 590 flood pixels each
  inside the circle, none before the event), one Bodal Chemicals site (198), and a GNFC power unit
  (32, but 35 were already there on 16 Aug, so standing water, not new flooding).
- **Limit:** on average the radar is blind over 45% of the 500 m circle around a plant, because it
  cannot detect water between buildings. It can show flooded open land next to a plant; it cannot
  rule out water inside a built-up compound. Vadodara city, which was flooded, shows almost no
  flood pixels for this reason.

Other flood maps (`research/proxy/flood_map_products.csv`): the Indian space agency published PDF
map sheets for Gujarat (same radar scene) and for Chennai (its own radar, 7 Dec 2023). The Chennai
links returned "not found" on the live site, so that map was not read. No UN, Charter or
Copernicus emergency product with downloadable data exists for any of the three events.

### 5.9 Electricity use by state (`19_power_demand.py`, `figs/10_power_demand.png`)

Daily energy supplied by state from Grid-India's daily reports (through Robbie Andrew's public
compilation; Grid-India's own site does not answer from here). Each day is compared with the same
weekday in the previous two weeks.

| Event | Lowest day | Neighbouring states that day | Days below −3% | Back to normal | Shortfall |
|---|---|---|---|---|---|
| Chennai, Dec 2023 (Tamil Nadu) | −19.7% on 4 Dec (−15.9% on 5 Dec) | Karnataka −3.3%, Kerala +2.5% | 3 | 6 Dec, then +3 to +7% for a week | 119 GWh = 0.4 day of the state's normal use |
| Gujarat, Aug 2024 | −34.9% on 27 Aug | Maharashtra −9.6%, Rajasthan −7.2% | 8 | 2 Sep | 779 GWh = 1.9 days |
| Gujarat, Sep 2023 | −31.5% on 19 Sep | Rajasthan −31.0%, Maharashtra −9.7% | 15+ | not within two weeks | not attributable |

- Tamil Nadu is the clean case: a two-day dip confined to the state, then a week above normal.
- Gujarat in Aug 2024 dipped for eight days, but rain also cuts farm pumping and cooling, so this
  is an upper bound on lost industrial load.
- Gujarat in Sep 2023 moved with Rajasthan, so it reflects region-wide rain, not the Narmada flood.

### 5.10 Nitrogen dioxide over the clusters (`20_no2.py`)

Sentinel-5P nitrogen dioxide (5.5 × 3.5 km pixels, one pass a day at about 1:30 pm), from the
public Planetary Computer copy, 14 days before to 12 days after each event (104 granules listed, 97 with pixels over a cluster). A day
is used only if at least half of a cluster's pixels pass the product's quality filter, which
removes cloudy scenes (`no2_box_event.csv`, `figs/11_no2.png`).

| Event | Usable days per cluster (of about 27) | What they show |
|---|---|---|
| Chennai, Dec 2023 | City and Manali–Ennore 4, tyre belt 2, Bengaluru (control) 5 | One usable day before the event, so no baseline. 6 Dec reads 1.36 times that day; Bengaluru reads 2.15 times its own. No dip |
| Gujarat, Aug 2024 | Vadodara 2, Bharuch belt 5, Dahej 7, Indore (control) 5 | Bharuch 0.77 and Dahej 0.82 on 30 Aug, back to 1.05–1.16 on 1 Sep; the control read 0.57–0.72 on 27–29 Aug. Not distinguishable from weather |
| Gujarat, Sep 2023 | Vadodara 8, Bharuch belt 5, Dahej 15, Indore 5 | Dahej 1.13–1.15 on 20–21 Sep (three to four days after the peak), against 0.84–1.26 before. No dip at Dahej. Bharuch–Ankleshwar: no usable day until 28 Sep |

**Verdict: not informative for these events.** The same cloud that hides the night lights removes
most days, rain itself lowers the reading everywhere, and day-to-day swings of ±30% or more in
the controls are as large as any plausible effect. The one usable statement is that Dahej showed
normal levels on 20–21 Sep 2023. The near-real-time version of the product was used (the
full-orbit files are about 580 MB each); one granule (22 Aug 2024) failed to download.

### 5.11 Third-party record (`research/proxy/third_party_*.csv`, `flow_data.csv`)

Collected by sub-agents with a source link and verbatim quote on every row, then re-checked by
`18_verify_quotes.py`: across all sub-agent files of Rounds 3 and 4 (third-party record, flows,
official records, damage disclosures, government documents, transcripts), 300 quotes were found on
their source pages or in the saved transcripts and 28 table rows were confirmed number by number;
2 were not matched (two Petronet press-release pages, for figures not used here); 116 come from PDF
or spreadsheet sources that were not text-checked (the collecting agents checked those against the
text they fetched); 47 rows are marked as search-result snippets only; 35 carry no quote
(`research/proxy/quote_check.csv`). Rows marked `search_snippet` are leads, not established facts.

**Chennai, Dec 2023**
- State-run industrial parks: 878 of 960 units working by 7 Dec; Irungattukottai 206 of 206,
  Oragadam 110 of 126, Sriperumbudur 60 of 90, Gummidipoondi 220 of 250 (Deccan Herald, 7 Dec,
  quoting the state government). This agrees with the lights: the tyre belt was running by 6–7 Dec.
- Ambattur estate (small and medium firms, in the city): stopped at least two days; half of the
  south phase restarted by 7 Dec and another quarter by 11 Dec; associations put losses above
  ₹3,000 crore across estates against the state's ₹967 crore; 4,800 units in 24 estates affected.
- Power: Chennai's demand fell to 112 MW on 4 Dec, 1,500 MW on 5 Dec, and reached the pre-flood
  2,641 MW on 7 Dec (DT Next, quoting the utility).
- Chennai Petroleum (Indian Oil's subsidiary), Manali refinery: flooded; the pollution board
  traced the Ennore oil spill to it and issued directions on 11 Dec. No shutdown dates found.
- Coromandel International, Ennore (not in the sample): ammonia leak on 26 Dec that a state
  committee linked to cyclone damage to a pipeline; shut from 27 Dec 2023 to 21 May 2024. This is
  the longest documented plant closure tied to the cyclone.
- Insurance: early estimates of ₹1,500–2,000 crore insured against about ₹12,000 crore economic
  loss; most small firms uninsured. The state asked the centre for ₹7,033 crore interim and
  ₹12,659 crore permanent relief.
- **Not found:** any third-party report of a 2023 stoppage at Apollo Tyres, MRF, JK Tyre or CEAT;
  any parts or tyre shortage at a carmaker outside Chennai.

**Gujarat, Aug 2024**
- Vadodara city under water for about 72 hours; 118 power feeders shut, 12 still shut on 29 Aug,
  99% restored by 2 Sep. This matches the lights (dark on 30 Aug, normal by 7 Sep).
- The only plant named anywhere is GE T&D India, Vadodara (not in the sample), which filed a
  disruption notice. Dahej port suspended berthing on 29 Aug.
- **Corrected in Round 4 from the official text:** Rajya Sabha Unstarred Question 107 (answered
  25 Nov 2024) says 958 industrial units in Gujarat were affected by this monsoon's heavy rains and
  that Gujarat asked for Rs 36,811 lakh (₹368 crore) for production loss. That is ten times the
  ₹36.81 crore reported in the trade press, and it covers all of Gujarat, not only Vadodara
  (`research/proxy/docs/RS_AU107_25Nov2024_production_loss_heavy_rains.pdf`).
- **Not found:** any report naming a sample-firm plant, any estate-level statement, any
  pollution-board order, any aggregate insurance figure.

**Gujarat, Sep 2023**
- Ankleshwar under water to first-floor height; the main rail line closed for about 12 hours on
  17–18 Sep; relief paid to shops and traders. **No factory or industrial estate is named.**
- Dam release: began around 10 am–noon on 16 Sep and reached about 18 lakh cusecs early on 17 Sep
  (two sources that differ on the hour; one is an advocacy group).

**Flows**
- Petronet's Dahej terminal: 210 TBtu in Jul–Sep 2023 (182 a year earlier) and 225 TBtu in
  Jul–Sep 2024 (210 a year earlier). No dip in either flood quarter. Monthly figures for Dahej
  alone are not published; India's LNG imports were higher in Aug and Sep 2024 than a year before.
- Cement output (all India, year on year): Oct 2024 +3.3%, Nov +13.0%, Dec +4.0%, Jan 2025 +14.5%,
  Feb +10.5%. No national dip in the Delhi construction-ban months; regional data were not found.
- Maruti production: Dec 2023 121,028 units against 124,722 a year earlier; Jan 2024 204,876
  against 186,044. No sign of a parts shortage after Chennai.
- **Not reached:** GST e-way bills by state, vehicle registrations by maker and state, industry
  production by maker (gated), railway loading for Oct 2024–Feb 2025.

### 5.12 Event study rerun with plant-level hits (`17_plant_level_event_study.py`, `figs/09_…`)

Exposure is rebuilt as the share of a firm's plant cost at sites that were actually dark, and
separately the share in the zone but not shown dark. Same engine and placebo inference as section 3.

| Chennai, days 0 to 5 | Firms | Difference vs unexposed | p |
|---|---|---|---|
| ≥ 25% of plant cost in the zone (original measure) | 7 | −5.6 pp | 0.05 |
| ≥ 10% of plant cost at dark sites | 2 (Hindustan Unilever, Apollo Hospitals) | −4.3 pp | 0.21 |
| ≥ 10% in the zone but not dark | 5 | −6.1 pp | 0.07 |
| Per 100% of assets: dark −14.1 pp, not dark −17.7 pp | | difference +3.6 pp | 0.74 |

- **The stock reaction does not scale with assets actually dark.** The largest falls are JK Tyre
  (−9.0%) and Vascon (−11.2%), whose sites were lit or only dimmed; CEAT, also lit, rose.
- A continuous "how much dimmer" measure gives a significant slope (p = 0.03), but it rests on
  three firms and mainly on Vascon, a small builder with one Chennai project. I do not rely on it.
- Gujarat 2024: only GSFC has more than 10% of its assets at dark sites. It fell 13.5% over 20
  days against 3.0% for unexposed firms (p = 0.26 for one firm). Radar-flooded assets are below
  5% of plant cost for every firm, so there is nothing to test.
- The hazard panel (`04_hazard_panel.py`, 886 district-episodes) was **not** rerun with
  plant-level hits: that needs daily tiles for five years (about 200 GB). The two events above
  are the test.

**Confound found: the election-result rally (`23_chennai_sector_check.py`).** Monday 4 Dec 2023
was also the first trading day after state-election results. The Sensex and Nifty rose about 2%
that day to record highs, led by financials and energy (confirmed from search summaries of ICICI
Direct and Business Standard reports; row 11 of `research/verified_market_confounds.csv`). In
this project's data the market rose 3.6% over days 0–5, and sector indices moved apart: energy
+4.2% abnormal, autos −1.6%, consumer goods −2.1%, real estate −2.2%, pharma and health −3.2%.
The Chennai-exposed firms are tyre makers, a hospital chain, a consumer-goods firm and builders.

| Firm | Sector index | Abnormal return, days 0–5 | Sector index, same days | Firm minus sector | Firm minus sector, days 0–10 |
|---|---|---|---|---|---|
| Apollo Tyres | Auto | −1.7% | −1.6% | −0.1 pp | −0.7 pp |
| JK Tyre | Auto | −9.0% | −1.6% | −7.4 pp | +1.7 pp |
| CEAT | Auto | +1.1% | −1.6% | +2.7 pp | +7.3 pp |
| Apollo Hospitals | Pharma | −3.0% | −3.2% | +0.2 pp | −2.6 pp |
| Hindustan Unilever | Consumer goods | −3.9% | −2.1% | −1.8 pp | 0.0 pp |
| Vascon Engineers | Real estate | −11.2% | −2.2% | −9.0 pp | −12.3 pp |
| Indo Rama | none in the data | −5.2% | n/a | n/a | n/a |

- Against their own sector indices the six firms average **−2.6 pp over 5 days and −1.1 pp over
  10 days**, against −4.6% and −4.0% before the adjustment. About half of the 5-day gap and
  three-quarters of the 10-day gap is sector rotation in the rally week.
- What is left sits in two small firms, JK Tyre (gone by day 10) and Vascon, whose sites were not dark.
- The placebo dates used for the p-value control for sector tilts on average, but not for a
  one-off sector shock on the event day itself. **The Chennai p = 0.05 should not be read as a
  cyclone effect.**

### 5.13 Pricing check: is the price move the size of the stoppage? (`21_interruption_pricing.py`)

Upper bound on operating profit lost = share of plant cost dark × days until light is back above
80% (cloudy nights counted as dark) ÷ 365 × the year's operating profit, with no catch-up allowed.
A cruder bound idles all zone assets for the length of the state electricity dip.

| Chennai, 7 exposed firms | ₹ crore |
|---|---|
| Market-value change over 5 days, relative to unexposed firms | −34,018 |
| Upper bound on lost operating profit, dark assets | 105 |
| Upper bound, all zone assets idle for 3 days | 75 |

- The price move is about 320 to 450 times the bound. For Hindustan Unilever alone: −₹28,900
  crore against a bound of ₹46–91 crore.
- **Conclusion for pricing:** a stoppage of a few days is worth well under 0.1% of these firms'
  value. Whatever moved the Chennai stocks in that week, it was not the cost of the interruption.
  The usable price of such an event is the interruption bound itself, not the share-price move.
- Gujarat 2024: exposed firms did not lose value against unexposed firms over 5 days.

### 5.14 What Round 3 changes

| Case | Before | Now |
|---|---|---|
| Chennai, Dec 2023 | Significant price drop, no mechanism | Physical hit confirmed and dated (city and Manali–Ennore dark for 2–7 days; state power −20%). The tyre plants were lit from the first clear night, no third party reports them shut, the price drop does not follow the dark assets, and about half of it is the sector rotation of the election-result rally. **The price drop is not explained by the physical event** |
| Gujarat, Aug 2024 | No drop at impact, no mechanism | Vadodara sites dark on 30 Aug and normal by 7 Sep; chemical belt unobserved in the first week, normal after; almost no radar flood water at plants; no plant named by anyone. **Consistent with no material hit to the sample firms** |
| Gujarat, Sep 2023 | No effect, no mechanism | **Not observable** by lights or radar; press names no factory |
| Delhi, Nov–Dec 2024 | Mechanism named (short delay) | No national dip in cement output; regional data not found. The ban turns out to be a Stage III measure; across six Stage III orders in 2022–2024 there is no systematic price effect (section 5.15). **A short delay named by two builders, with no repeatable price signal** |

### 5.15 Step 3: official records (`research/proxy/official_hazard_records.csv`, `delhi_aqi_daily.csv`, `24_grap_stage3_event_study.py`)

**Pollution-control orders.** All 21 Stage III and Stage IV orders of the winters 2022–2024 were
read from the government's own press releases (pib.gov.in), replacing the summary-based rows.
- Every Stage IV date in `src/common.py` is confirmed, including 8 am on 18 Nov 2024.
- Two additions for Dec 2024: Stage III was revoked together with Stage IV on 5 Dec, and was
  re-imposed on 16 Dec a few hours before Stage IV, staying until 27 Dec.
- **Correction.** I read four of the releases myself. The construction ban for buildings is a
  Stage III measure in every year: "Enforce strict ban on construction and demolition activities
  in the entire NCR, except for the following categories of projects" (29 Oct 2022 and 2 Nov 2023).
  Stage IV adds only "C&D activities in linear public projects such as highways, roads, flyovers".
  In 2024 the revised Stage III bans listed dust-generating work (earthwork, piling, demolition,
  road works) rather than all construction, so the 2024 ban is if anything narrower.
- The exact text of the schedule revised on 13 Dec 2024 was not read.

**Rerun on the Stage III dates.** In 2024 the Stage III orders lead to the same first trading
days already used (15 Nov 2024 was not a trading day), so the 2024 results stand. In 2022 and
2023 the Stage III orders came 3–5 days before the Stage IV dates used so far.

| Stage III order | First trading day | NCR real estate minus other real estate, days 0–5 | p | All NCR-exposed minus unexposed, days 0–5 | p |
|---|---|---|---|---|---|
| 29 Oct 2022 | 31 Oct 2022 | −3.6 pp | 0.47 | +1.0 pp | 0.65 |
| 4 Dec 2022 | 5 Dec 2022 | +1.7 pp | 0.72 | −1.9 pp | 0.45 |
| 2 Nov 2023 | 3 Nov 2023 | +9.3 pp | 0.07 | +1.7 pp | 0.49 |
| 14 Jan 2024 | 15 Jan 2024 | +3.8 pp | 0.42 | +5.2 pp | 0.04 |
| 14 Nov 2024 | 18 Nov 2024 | −3.6 pp | 0.47 | −2.4 pp | 0.34 |
| 16 Dec 2024 | 17 Dec 2024 | −0.2 pp | 1.00 | +0.1 pp | 0.97 |

- Across six construction-ban orders the real-estate gap is negative three times and positive
  three times (mean +1.3 pp), with five NCR builders against three others. **There is no
  systematic price effect of the construction ban.** The Nov 2024 dip stands alone.
- The 14 Jan 2024 "significant" positive gap is a reminder that with 12 firms one event in twenty
  will look significant by chance.

**Delhi air quality.** Daily index for all 68 days of 25 Oct–31 Dec in each of 2022, 2023 and
2024 (`research/proxy/delhi_aqi_daily.csv`, 204 rows), from UrbanEmissions' parsed copy of the
pollution board's daily bulletins. Seventeen values were checked against figures quoted in
government releases and all matched (12 for 2022–2023 by the sub-agent, 5 for 2024 by me). In
2024 the index peaked at 494 on 18 Nov, the first day of Stage IV, and was 165 on 5 Dec when the
restrictions were lifted. The pollution board's own site still does not answer. The series is
ready to use as a continuous treatment; it has not yet been put into a regression.

**River levels** (press and one advocacy group quoting official gauges; the Central Water
Commission's bulletins could not be read):
- Narmada at the Golden Bridge, Bharuch: danger mark 24 ft, crossed after 4:30 am on 17 Sep 2023;
  peak about 40.5 ft (12.34–12.35 m) between the evening of 17 Sep and 5 am on 18 Sep (sources
  differ on the hour), 0.30 m below the 1970 record. Dam outflow rose from 1.45 lakh cusecs around
  noon on 16 Sep to 18.4 lakh by 5 am on 17 Sep.
- Vishwamitri at Kala Ghoda, Vadodara: crossed the 26 ft danger mark about 4 pm on 26 Aug 2024,
  peaked at about 35–37 ft on 27 Aug (the sensor read 35.25 ft with the bridge overtopped), and
  fell below the danger mark at 10 am on 30 Aug. This fits the lights: Vadodara still at 54% of
  normal at 01:50 on 30 Aug.

## 5c. Round 4: out-of-sample test, plant-level hits across many episodes, and the remaining reachable data (sections 5.16–5.25)

### 5.16 Out-of-sample test with the existing 61 firms (`26_fetch_extend.py`, `27_out_of_sample.py`, `figs/12_out_of_sample.png`)

Prices were extended to 17 Nov 2026 from Yahoo Finance. On the 2024–25 overlap their returns
match the pack's (correlation ≥ 0.99 for 58 of 61 firms), which also confirms the one-day date
fix. Rainfall was extended with NASA POWER. Its source changes from MERRA-2 to a near-real-time
model on 1 Oct 2026 (checked in the API headers), so the test stops at 30 Sep 2026. Fit period:
Nov 2020–Dec 2024 (720 district-episodes, 383 firm-episodes). Test period: Jan 2025–Sep 2026
(299 and 142).

| Question | Fit 2020–24 | Test 2025–26 | Verdict |
|---|---|---|---|
| Loss elasticity (CAR minus same-date unexposed, per 100% of assets hit), 5 / 10 / 20 days | 0.0 / −1.6 / −2.4%, none significant | +1.6 / +1.1 / −3.7%, none significant | No predictive power: out-of-sample R² ≈ 0 |
| Firm-episodes with ≥25% of assets hit, mean CAR minus unexposed, 10 / 20 days | −1.2 / −0.5% (88 cases) | −2.4 / −5.4% (35 cases, 10 weeks; t = −1.8 / −2.3) | Test period more negative than fitted (−1.3 / −1.0%), but 17 of 32 cases (excluding Reliance Power) fall in one week, 6–12 Jul 2026 |
| Do the same districts get hit again? | — | Spearman 0.18 (p < 0.001); 56% of the top-fifth districts hit again vs 43% of the rest; firm level 0.28 (p = 0.03) | Weak but real persistence |
| Concentration → idiosyncratic volatility | +0.17 per unit of district HHI (p < 0.001) | +0.12 (p = 0.04) | Holds out of sample |
| Hazard frequency → idiosyncratic volatility | +0.14 (p = 0.04) | 0.00 (p = 0.99) | Does not hold |

- The July 2026 week is not a sector fall: the real-estate index rose 5.5% (abnormal) in the
  five days after 6 Jul 2026 while the exposed builders lagged the same-date unexposed firms.
- Reliance Power fell about 40% over 20 days after a Jul 2025 Rajasthan episode. A fall that size
  is unlikely to be a rain effect (its cause was not checked), so figures without it are also
  reported: −4.2% at 20 days, t = −3.5.
- A model of volatility fitted on 2020–24 predicts 2025–26 volatility with r = 0.57, but last
  period's volatility alone does better (rank correlation 0.85).

### 5.17 Plant-level hits across 66 severe rain episodes (`25_ntl_episodes.py`, `figs/13_ntl_episodes.png`)

The cheaper version of rerunning the hazard panel with plant-level hits. Every week from Nov 2020
to Sep 2026 in which an extreme-rain episode touched ≥ 10% of a traded firm's plant cost (66
weeks) was covered with daily night lights for the first 11 nights. Each site is compared with
NASA's annual cloud-free composite of the year before and with control plants more than 200 km
away on the same night. The design was validated on the two events done in full (section 5.7):
84% agreement on which Chennai sites were dark (rank correlation 0.91) and 73% for Gujarat 2024 (0.82).

**How often do sites in extreme-rain districts go dark?** Of 6,047 plants in hit districts (5,063
lit), 2,543 could be seen on a clean night in the first week (the rest were under cloud); 320 of
those (12.6%) were below 60% of normal, against a 3.7% false-alarm rate on control plants. So
roughly one site in eleven in a district with extreme rain loses power for a few nights. The
share rises with severity: 25% when rain exceeds twice the 5-year level. Dark sites took a median
5–8.5 nights to return above 80% of normal (cloudy nights counted as dark, so an upper bound).

**Does the stock reaction follow the assets that went dark?** Across the 482 firm-episodes in those
weeks:

| CAR minus same-date unexposed, per 100% of plant cost | 0–5 days | 0–10 days | 0–20 days | 0–40 days |
|---|---|---|---|---|
| Assets that went dark | **−11.3%** (p = 0.001) | **−15.9%** (p < 0.001) | **−23.2%** (p < 0.001) | −17.2% (p = 0.09) |
| Assets in hit districts that stayed lit or were not seen | +1.1% (p = 0.30) | 0.0% | −2.0% (p = 0.45) | +0.9% |
| Firm-episodes with ≥5% of plant cost dark (19 cases, 11 weeks), mean | −3.1% | −4.7% | −6.6% | −6.4% |

Robustness:
- Dropping the Chennai week gives −14% at 10 days (p = 0.055) and −21% at 20 days (p = 0.03).
- Dropping Chennai and Gujarat 2024 gives −16% (p = 0.06) and −19% (p = 0.08).
- Controlling for exposure × rain severity gives −13% (p = 0.03) at 10 days.
- Sector effects, winsorising, and dropping any other single firm or week leave it negative and significant.

**This revises the Round 3 reading.** In Chennai alone, firms whose sites stayed lit fell as much
as those that went dark, and section 5.12 found no dose-response. Across 66 episodes the market
does mark down firms whose sites lose power, and only those. The effect builds over 20 days and
has not reversed by day 40. It rests on 19 firm-episodes with at least 5% of assets dark, so it
is evidence, not proof. Its size is still out of proportion to the cost of the outage: a firm with
20% of plant cost dark for a week loses about 3% of market value, while the stoppage itself costs
well under 0.1% (section 5.13).

### 5.18 Delhi air quality as a continuous treatment (`29_delhi_aqi_panel.py`, `figs/14_delhi_aqi.png`)

Daily data for 25 Oct–31 Dec of 2022, 2023 and 2024 (138 trading days). The long-short series is
NCR builders (NBCC, Anant Raj, Unitech, Parsvnath, DLF) minus the 42 firms with no NCR plants,
regressed with winter effects and Newey-West standard errors.

| Treatment (known before the market opens) | NCR builders minus no-NCR firms, % per day | All NCR-exposed firms |
|---|---|---|
| Delhi AQI the previous day, per 100 points | **−0.33** (p = 0.011) | **−0.26** (p = 0.033) |
| Change in AQI the previous day | +0.08 (p = 0.79) | −0.17 (p = 0.38) |
| Stage III in force / Stage IV in force | +0.21 / +0.26 (not significant) | −0.06 / +0.23 |
| First day of a tighter stage | −0.42 (p = 0.43) | −0.57 (p = 0.20) |

- **The AQI coefficient survives several checks:** within-winter trends (−0.33, p = 0.016), adding the stage dummies (−0.46, p = 0.002), robust regression (−0.32, p = 0.06), and dropping the 3 or 6 largest days.
- **Placebos are flat:** the AQI of another winter on the same calendar dates gives −0.06 and −0.16 (not significant).
- **By winter:** each winter alone is negative, and 2024 is significant on its own.
- **Reading:** on bad-air days NCR builders underperform the next day, by about 0.3 percentage points per 100 AQI points. The formal construction-ban orders add nothing negative once air quality is controlled. This is the first repeatable price signal tied to Delhi pollution in the project. It is about pollution days, not about the ban itself, and rests on five builders.

### 5.19 Optical check for standing water at the Chennai plants (`30_chennai_optical.py`)

Sentinel-2 (6, 11 Dec 2023) and Landsat 8 (7 Dec) were the only optical views in the event window.
- **Coverage:** only 3–32 of the 82 zone plants had at least 30% of their 500 m circle cloud-free on any event scene.
- **Tyre plants:** the Apollo Tyres and JK Tyre plants at Oragadam and Sriperumbudur were under cloud on every event scene. CEAT's two Sriperumbudur plants were visible on 7 Dec, with no water flagged.
- **Chennai city:** a lenient water index (MNDWI > 0) shows wet ground or water within 500 m of 4–6 of 13–16 visible city plants on 6 Dec, including the Hindustan Unilever and Vascon sites. The stricter Sentinel-2 scene classification flags none, so this is wet ground or water that cannot be confirmed. On 11 Dec, two Gummidipoondi and one or two Manali–Ennore sites show new water on the strict measure.
- **Verdict:** optical imagery adds little. The Indian space agency's radar map (found later in Round 4, section 5.24) settles the flooding question for the tyre plants.

### 5.20 Official monthly flows (`32_flows_round3.py`, `research/proxy/flow_data_round3.csv`)

**State GST collections** (the government's monthly state tables; Jul 2024 onward from GSTN's PDFs).
Collections in month M mostly reflect supplies in month M−1. Test: the state's share of seven
states' collections in the event month against the average of the months either side, minus the
same calculation one year apart.

| Event | Collection month | Change, % of the state's normal collections | Share of all state-months with a larger move (placebo, 98) |
|---|---|---|---|
| Chennai, Dec 2023 (Tamil Nadu) | Jan 2024 | −7.1% | 15% |
| Gujarat, Aug 2024 | Sep 2024 | −7.0% | 17% |
| Gujarat, Sep 2023 | Oct 2023 | −8.8% | 10% |
| Delhi ban, Nov 2024 (Delhi / Haryana / UP) | Dec 2024 | −1.1% / +21% / −4.0% | 85% / 2% / 39% |
| Delhi ban, Dec 2024 (Delhi / Haryana / UP) | Jan 2025 | −2.7% / −16% / +1.9% | 55% / 5% / 68% |

- The three flood events all show a one-month dip of 7–9% of state collections, each about as
  large as one ordinary month in six to ten: consistent with a short activity loss, not
  significant on its own.
- Haryana's series swings by ±20% month to month (also visible in its published growth rates),
  so its Delhi-ban numbers are noise. Delhi itself shows nothing.

**Other series.**
- All-India cement output rose in Nov 2024 (+13.5% year on year, revised) and Dec 2024 (+4.6%); fertiliser output rose 1–2%.
- Rail freight monthly releases exist only for Oct 2023–Feb 2024 (Dec 2023 total +6.4% year on year). The Oct 2024–Mar 2025 releases were not found, so there is no Delhi rail test (manual request M7).
- Plant-level fertiliser output was not reachable (manual request M1b).

### 5.21 Disclosures, round 4 (`research/transcripts_round3.csv`, `research/proxy/damage_disclosures.csv`)

**Earnings calls.**
- **Apollo Hospitals** (Q3 FY24 call, 9 Feb 2024, from the company's own PDF) names the cyclone:
  "some impact from seasonality, holidays and the cyclone in Chennai", and "we had a couple of
  centers in Chennai. There was an extended delay for us to recuperate back to the business". This
  is the first company-level mechanism for Chennai, and it matches the night lights: 15 of Apollo
  Hospitals' 16 Chennai sites were dark on 6–7 Dec.
- **No mention of the events:** Maruti (Q3 FY24), JK Tyre (Q3 FY24) and SRF (Q2 FY24). These three were read from a third-party transcript mirror (alphaspread.com), because the exchange filings contain only cover letters.
- **No call held:** MRF.
- **No call or transcript on the exchange:** Gujarat Alkalies, Anant Raj and Shree Cement (manual request M11).

**Damage.**
- **Michaung (Q3 FY24):**
  - GIC Re, the national reinsurer, made a ₹754 crore provision for "Cyclone Michaung (Tamil Nadu floods)".
  - New India Assurance reported a ₹358 crore net impact for Michaung together with other floods that quarter.
  - ICICI Lombard's presentation cites a market estimate of ₹2,500 crore of insured losses, with its own share at 5.88%.
- **Gujarat floods:** insurers report quarterly catastrophe losses (ICICI Lombard ₹94 crore in Q2 FY25, New India ₹600–700 crore) without a Gujarat-only figure. Go Digit says the floods added about 2 points to its loss ratio and mentions "fire claims, especially in Gujarat during the flood in Baroda".
- **Sample companies:** none booked an exceptional item or flood-related charge for any of the three events in the results read. Five filings could not be read (Indo Rama, Bodal Chemicals Q2 FY25, Borosil Renewables Q2 FY24, Petronet Q2 FY25, Aarti Q2 FY24).
- **Industry:** no official General Insurance Council or IRDAI claim total was found in an original document.
- **Damage term for pricing:** the insured loss of Michaung (₹2,500 crore industry-wide) is two orders of magnitude below the ₹34,000 crore fall in the seven exposed firms' market value in that week, and none of it is attributed to them.

### 5.22 Rainfall triggers rebuilt on the official IMD grid (`31_imd_hazard.py`, `figs/15_imd_vs_nasa.png`)

Source: India Meteorological Department (Pune), daily gridded rainfall at 0.25° from rain gauges,
2000–2025, downloaded from imdpune.gov.in (26 yearly files). Same rules as section 3: 3-day totals,
each district's own 5-year level from 2000–2019, episodes from Nov 2020.

| Named event | IMD: peak 3-day rain ÷ 5-year level | NASA POWER (used so far) |
|---|---|---|
| Himachal, Jul 2023 (Solan, Shimla, Kullu, Una, Sirmaur) | 1.5–1.9 | 1.4–2.0 |
| Chennai, Dec 2023 (Chennai, Kancheepuram, Tiruvallur) | 1.2–1.3 | 1.5–1.8 |
| Gujarat, Aug 2024 | Kheda 1.86; Vadodara 0.84; Anand 0.68; Bharuch 0.36 | 1.21; 1.17; 1.30; 0.79 |
| Gujarat, Sep 2023 (dam release) | Bharuch 0.12; Vadodara 0.39 | 0.22; 0.61 |

- **The two rainfall products disagree on which places count as extreme.** IMD finds 704 district-episodes and NASA 886 (Nov 2020–Dec 2025). Only 41% of IMD episodes have a NASA episode in the same district within 3 days, and 33% the other way round. District counts have a rank correlation of only 0.16. At district scale, 3-day extremes are local, and a 0.25° gauge grid and a 0.5° reanalysis often differ.
- **The stock result does not change.** With IMD triggers, the elasticity per 100% of assets hit is −0.8% (5 days), −0.5% (10 days) and −4.7% (20 days, t = −1.7). Firms with ≥ 25% of assets hit (80 cases) move −0.8%, −0.8% and −1.5%, none significant. Rainfall-defined exposure barely moves prices on either product. What the market responds to is a plant actually losing power (section 5.17).
- **Data choice:** IMD is now the default hazard source for the expected-loss model (section 5.23). NASA is kept for 2026, because IMD's yearly file for 2026 is not out yet.


### 5.23 Expected annual loss from outages, and the firm risk card (`28_expected_interruption_loss.py`, `figs/16_interruption_vs_equity.png`)

Inputs:
- Extreme episodes per year at each plant's district (IMD, Nov 2020–Dec 2025).
- Probability that a site goes dark when its district has an extreme episode: 12.6% observed; 7.5% net of the false-alarm rate on control plants (5.1% averaged across weeks; 3.7% if pooled over all control plant-nights, which would give 8.9%) (section 5.17).
- Nights dark: median 7, 75th percentile 9 (cloudy nights counted as dark).
- Operating profit in the latest full financial year.

No catch-up of lost output is allowed, so every case overstates the cost of a short stoppage.

| 61 traded firms | Central | High | Upper bound: every episode darkens every plant in the district for 14 days | Market markdown implied by the dark-asset price effect | Share-price route from rainfall exposure (not significant) |
|---|---|---|---|---|---|
| Sum, ₹ crore a year | 232 | 514 | 6,185 | 21,716 | 41,045 |
| % of the firms' combined market value (₹71.4 lakh crore) | 0.003% | 0.007% | 0.09% | 0.30% | 0.57% |
| Median firm, % of its market value | 0.002% | 0.005% | 0.06% | 0.25% | — |

- **The physical cost of extreme-rain outages is tiny.** The median firm loses about a tenth of a day's operating profit a year; the most exposed (DLF) loses about a quarter of a day. Even the deliberately extreme upper bound is under 0.5% of market value for every firm. The largest is BPCL at 0.48%, because of its many coastal storage sites.
- **The market charges more than the physical cost.** The markdown implied by section 5.17 (−15.9% per 100% of plant cost dark over 10 days) is about 90 times the central interruption cost and 3.5 times the extreme upper bound. By day 40 the markdown is still about −17% per 100% dark (p = 0.09), so it is not clearly temporary.
- **Possible reasons the markdown exceeds the stoppage cost** (none tested here): damage and repair costs, which no company booked (section 5.21); lost sales that are not caught up; or the market treating an outage as news about a site's future risk.
- **The deliverable** is `outputs/tables/deliverable_firm_risk_card.csv`, one row per firm (81). It holds each firm's shares in the four event zones, its largest district and that district's share, its concentration score (district HHI), expected extreme episodes per year at its plants, expected outage loss (central, high and upper), the market-implied markdown, and caveats.

### 5.24 Chennai plants on the Indian space agency's radar flood map (`33_nrsc_chennai_flood.py`, `figs/17_nrsc_chennai_plants.png`)

A sub-agent found the NRSC map that earlier passes could not reach: "Flood / Rain affected areas
during Michaung Cyclone in Parts of Tamilnadu State", map 2023/CY/TN/01a/07122023, from RISAT-1A
radar of 7 Dec 2023, 06:00 India time (pre-flood image 5 Nov 2023), downloaded from the NDEM portal
(`research/proxy/docs/NDEM_TN_Michaung_7Dec2023_map.pdf`). The PDF is a GeoPDF: its map frame
carries WGS84 corner coordinates (12.30–13.54°N, 78.90–80.78°E), so it can be georeferenced exactly.
Rendered at about 35 m per pixel; the overlay lines up with the coastline and district boundaries.

| Sub-area (plants) | Plants with ≥ 5% of the 500 m circle flooded | Plants with any flood pixel within 500 m | Median distance to nearest flood pixel |
|---|---|---|---|
| Chennai city (35) | 0 | 0 | 1.3 km |
| Manali–Ennore (16) | 0 | 7 (at most 3.7% of the circle) | 0.5 km |
| Sriperumbudur–Oragadam (13) | 0 | 0 | 1.8 km |
| Gummidipoondi (6) | 0 | 0 | 1.6 km |
| Other zone (12) | 0 | 3 | 0.8 km |

- The Apollo Tyres, JK Tyre and CEAT tyre plants have no flood or standing water within 1 km on
  7 Dec. This agrees with the night lights (lit from 6 Dec) and with the state government's
  statement that most units in the Oragadam and Sriperumbudur estates were working by 7 Dec.
- **Limits:** the image was taken three days after the peak rain. Radar cannot see water between
  buildings, so city sites read dry although the city flooded (the same blind spot as the Gujarat
  radar map, section 5.8). The map's disclaimer says the red layer includes standing water in
  paddy fields and has had no ground check. Most of the red lies in farmland south and west of the
  industrial belts.

### 5.25 What Round 4 changes

| Question | Before Round 4 | Now |
|---|---|---|
| Does the price follow assets that physically went dark? | No (Chennai alone, section 5.12) | **Yes, across 66 episodes**: −16% per 100% of plant cost dark over 10 days, −23% over 20; lit or unseen exposure has no effect. Rests on 19 firm-episodes with ≥ 5% dark |
| Is rainfall-defined exposure priced? | Weakly, not significant | Still no, on official IMD triggers too, and out of sample (2025–26) the fitted elasticity explains nothing |
| Are the hazard maps stable? | Assumed | Districts hit in 2020–24 are somewhat more likely to be hit in 2025–26 (rank correlation 0.18). Rainfall products disagree on most individual episodes |
| Is concentration priced? | Yes (volatility) | Yes, also out of sample (2025–26) |
| Were the Chennai tyre plants flooded? | Unknown (no Sentinel-1 radar pass) | No flood or standing water within 1 km of any tyre plant on the space agency's RISAT-1A map of 7 Dec (section 5.24) |
| Chennai mechanism | None at company level | Apollo Hospitals names the cyclone; insurers set aside ₹754 crore (GIC Re); industry insured loss estimated at ₹2,500 crore; Tamil Nadu GST collections dip ~7% in Jan 2024 (not significant alone) |
| Delhi | Short delay named; no repeatable price effect of the orders | Bad-air days predict next-day underperformance of NCR builders (−0.3 pp per 100 AQI points, p = 0.01); the orders themselves still add nothing |
| Price of the risk | Equity elasticity (not significant) | Physical outage cost: about ₹230–510 crore a year for the 61 firms, under 0.01% of value. The market markdown is far larger and is the price the market actually charges |


## 6. Recommended next steps, in order of value

Everything reachable from the cloud session has now been done. What remains needs data that must
be downloaded by hand; the list, with sources and where to save each file, is
`MANUAL_DATA_REQUESTS.md` (machine-readable: `manual_collection/REQUESTS.csv`).
1. **Monthly plant-level output** (requests M1a–M1c): tyre makers for Dec 2023, GSFC Vadodara for Aug–Sep 2024, northern cement despatches for Nov 2024–Feb 2025. The only way to tell output lost from output delayed, and to test whether the dark-asset markdown (section 5.17) reflects real lost output.
2. **More firms' plant locations** (M4): the dark-asset result rests on 19 firm-episodes; a few hundred more firms would multiply that.
4. **Licensed supply-chain data** (M3) for the propagation test.
5. **Optional: Google Earth Engine access** (M13) to run the plant-level night-light test on all ~1,000 rain episodes instead of 66 weeks.

## 7. Limits

Small sample (61 stocks, 3–15 highly exposed firms per event). Rainfall grid is about 50 km, so it
is a district-level proxy, not plant-level flooding. Exposure is plant cost share, an unaudited
proxy. Event dates are now verified (section 5.1), some through page summaries rather than original text. No result
here establishes supply-chain propagation.

Round 3 limits:
- Night lights measure power at the site and its surroundings at 01:50, not production, and see
  nothing through cloud. The first two nights of Chennai and the first five of Gujarat 2024 are
  missing. A site lit on 6 Dec may still have been shut on 4–5 Dec.
- Night-to-night noise is ±10–30% at cluster level. Site-level "dark" calls are reliable only
  where a whole cluster moves together over consecutive nights (Chennai city, Manali–Ennore, Vadodara).
- Radar flood maps exist for one of three events, and cannot see water inside built-up areas.
- State electricity includes homes and farms, and rain itself lowers demand.
- The plant-level event study has 2 to 7 firms per group. Its value is that it fails to show a
  dose-response, not that it proves the absence of one.
- The pack's plant list looks like a project database (several rows per site, offices and housing
  projects mixed with factories). "Share of plant cost dark" inherits that.
- The third-party record was searched mainly in English.

Round 4 limits:
- The dark-asset price effect rests on 19 firm-episodes (11 weeks) with at least 5% of plant cost
  dark; the episode design compares one night with an annual composite and same-night controls, and
  agrees with the full method on 73–84% of sites.
- The out-of-sample period (Jan 2025–Sep 2026) has 142 firm-episodes, and its high-exposure result
  is dominated by one week (6–12 Jul 2026).
- IMD and NASA rainfall disagree on most individual extreme episodes; any result that depends on
  which exact districts were "hit" by rain is fragile. Rainfall data stop at Dec 2025 (IMD) and
  Sep 2026 (NASA, MERRA-2 source).
- The expected outage loss uses plant cost shares (unaudited relative weights) and an outage
  probability from 66 episode-weeks; it assumes no catch-up of output.
- Three transcripts (Maruti, JK Tyre, SRF) were read from a third-party mirror, not the company's
  own file. Insurer catastrophe figures are mostly not attributed to a single event.
