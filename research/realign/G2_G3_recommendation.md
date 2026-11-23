# Decisions G2 and G3: recommendations and evidence (23 Nov 2026)

These are recommendations for the user to decide (INSTRUCTIONS §5). Nothing that depends on them has been run.
Evidence tables are in `research/realign/`. Every quote has been checked against the saved document text by
`src/42_check_quotes_realign.py` (results in `quote_check_realign.csv`).

## G3. Which NCR builders count as confirmed hit firms (Step A)

**Recommendation:** NBCC and DLF are confirmed. Anant Raj, Parsvnath and Unitech are exposed but not confirmed.
Step B (suppliers) starts from NBCC and DLF.

**The shock (official, original text, `research/proxy/official_hazard_records.csv`):**
- Stage III was in force from 08:00 on 15 Nov to 5 Dec 2024, and again from 16 to 27 Dec 2024 (CAQM releases on PIB).
- Stage III bans the listed dust-generating construction activities across NCR. These include earthwork, piling,
  demolition, brick and masonry work, ready-mix plants, cement and plaster work, and loading or unloading cement.
- Exempt are railway, metro, airport, bus-terminal, defence, hospital and sanitation projects, and linear public
  projects (these are banned only under Stage IV).

| Builder | Share of plant cost in NCR | Documents read | What they say |
|---|---|---|---|
| NBCC | 94% | Q3 FY25 call (Feb 2025); Q2 call (14 Nov 2024); investor presentation (22 Nov 2024); Q3 presentation and results; Q4 presentation | Q3 call: "the third quarter is mostly impacted by the graph [sic] in Delhi and NCR area, there is a pollution" (project-management growth 1.2%); "Because last 1.5 months, there was a ban on construction in Delhi and NCR, even Noida also. So next quarter, we'll be going to achieve INR4,000 crores." The other four documents do not mention it; the Q2 call was held before the order. No exchange notice; new work orders kept being announced during the ban. |
| DLF | 42% | Q3 FY25 call (27 Jan 2025); Q3 presentation; Q3 results and notes | Call: "the 2 malls in the Delhi NCR were a little delayed because of the GRAP and the stoppage of construction". The presentation and results do not mention it and do not name the malls. |
| Anant Raj | 51% | Q3 and Q4 FY25 presentations; Q3 results and outcome; Jan 2025 clarification; Q2 call (6 Nov 2024) | No mention. No Q3 FY25 call transcript was filed (manual request M11). |
| Parsvnath | 49% | Q3 FY25 results (two filings); two May 2025 filings | No mention. The Q2 results could not be opened. |
| Unitech | 50% | None readable | The exchange copies refused the page reader (403). The company and BSE copies are image-only PDFs. |

**Caveats:** both confirmations are qualitative ("a little delayed"; project-management growth of 1.2%), and
neither gives a rupee figure. NBCC's "1.5 months" is longer than the roughly 31 days for which Stage III orders
were in force.

## G2. Exposed sets and matched controls (Step 1, deliverable 3(i))

### NCR (event day 18 Nov 2024, the first trading day after the Stage III order; second episode 17 Dec 2024)
- **Exposed:** the five traded NCR builders above.
- **IGL:** excluded everywhere. Its 18 Nov fall follows its own gas-allocation filing of 15 Nov 2024.
- **Within-zone comparison** (plants in NCR, not under the construction ban):
  - Maruti 73%, Max Healthcare 80%, Tata Communications 72%, Fortis 39%, Reliance Power 33%, RVNL 28%.
  - Rail projects and hospitals are exempt from the ban.
- **Eligible matched controls** (listed developers whose own Q2 FY25 presentation shows no NCR project; `controls_ncr_developers.csv`):
  - Brigade, Puravankara, Ajmera, Keystone Realtors and Kolte-Patil.
  - Sunteck, the weakest case: the deck says "MMR-Focused", but there is no footprint slide.
  - From the sample: Lodha and Vascon (no NCR plant in the pack's data).
- **Excluded from the controls:**
  - Sobha, Godrej Properties and Mahindra Lifespace (they have NCR projects).
  - Prestige, Oberoi, Phoenix, Arvind SmartSpaces and Shriram (not verifiable: documents refused or partial).
  - Rajesh Exports (the pack lists both jewellery and housing plants).
- **Matching:** the two eligible controls nearest in market cap on 14 Nov 2024 (`g2_proposal.csv`):

| Exposed | Matched controls (size ratio to the exposed firm) |
|---|---|
| NBCC | Brigade (1.10), Keystone (0.38) |
| DLF | Lodha (0.65), Brigade (0.14). DLF has no close match. |
| Anant Raj | Brigade (1.10), Keystone (0.38) |
| Unitech | Kolte-Patil (1.33), Ajmera (1.46) |
| Parsvnath | Vascon (1.57), Kolte-Patil (4.05) |

  Robustness check: all eligible controls, equal-weighted.
- **The pack's control firms:**
  - Torrent Power is out (your decision of 22 Nov).
  - Adani Green and Adani Power come out of the NCR comparisons: they fell 18.9% and 9.1% on 21 Nov 2024, the day of the Adani indictment.
  - MRPL is a refinery, not an industry match. Keep it for the placebo table only.

### Gujarat (event day 26 Aug 2024; the first trading day of the flood, with peak rain on 26–27 Aug)

**Exposed set: two footprints, both to be reported (my recommendation).**
- **Pack footprint (corrected districts), chemical firms with ≥25% of plant cost in the zone:** Kiri, Gujarat Alkalies, Bodal, GNFC, SRF, GSFC, Aarti, UPL, DCM Shriram, Zuari (10).
  - Almost all of this exposure is in Bharuch district (Dahej, Ankleshwar, Jhagadia). There, no flood disruption of the estates has been found.
  - Share of plant cost in Bharuch: Kiri 98%, Gujarat Alkalies 88%, GNFC 87%, SRF 81%, Bodal 69%, Aarti 59%, UPL 53%, GSFC 50%, DCM Shriram 46%, Zuari 41%.
- **Documented flood footprint (Vadodara district only):** GSFC (29% of plant cost) and Bodal (20%). Every other firm is under 2%.
- **The other exposed firms** (Petronet, Borosil Renewables, Modern Threads, Nectar Lifesciences, CEAT, MRF) have no chemical-industry match. They are reported against all unexposed sample firms, outside the matched design.

**Eligible matched controls** (own FY2023-24 documents show no plant anywhere in Gujarat; `controls_gj_chemicals.csv`, quotes checked):
- Fertiliser:
  - Chambal: Gadepan, Kota. "No" rests on the Directors' Report, which puts its three urea plants at one location.
  - National Fertilizers: Punjab, Haryana and Madhya Pradesh (its BRSR filing).
  - Paradeep Phosphates: Odisha and Goa (BRSR).
- Specialty chemicals:
  - Vinati Organics: Maharashtra (plant-location list).
  - Clean Science: Maharashtra (plant-location list).
  - Sudarshan Chemical: Maharashtra (BRSR).

**Excluded:**
- Plants in the zone: Coromandel (the evidence is a FY2020-21 report), Tata Chemicals, Galaxy Surfactants and NOCIL.
- DCW: its plant is in Gujarat (Dhrangadhra) but outside the zone. It is excluded under the stricter "no plant in Gujarat" rule, which is your call.
- No complete plant list could be read: Deepak Fertilisers, Balaji Amines, Fine Organic, RCF and Chemplast Sanmar.

**Matching:** the two controls nearest in market cap on 23 Aug 2024 (`g2_proposal.csv`):

| Exposed | Matched controls (size ratio) |
|---|---|
| GNFC | Paradeep (0.99), Sudarshan (0.87) |
| GSFC | Paradeep (0.99), Sudarshan (0.87) |
| Gujarat Alkalies | NFL (1.26), Sudarshan (1.46) |
| Aarti | Vinati (0.91), Chambal (0.91) |
| DCM Shriram | Chambal (1.11), Clean Science (0.90) |
| SRF | Vinati (0.28), Chambal (0.28). No close match. |
| UPL | Vinati (0.44), Chambal (0.44). No close match. |
| Kiri | NFL (2.95), Sudarshan (3.44). No close match. |
| Bodal | NFL (6.8), Sudarshan (8.0). No close match. |
| Zuari | NFL (8.0), Sudarshan (9.3). No close match. |

Robustness checks: all six controls, equal-weighted; and matching within sub-industry (fertiliser with fertiliser, specialty with specialty).

## The user's decisions (23 Nov 2026)
- **G3: approved.**
  - NBCC and DLF are the confirmed hit firms. Anant Raj, Parsvnath and Unitech are exposed, not confirmed.
  - The NBCC passage naming Amrapali and GPRA, with the 8–10% growth expected otherwise, was added to `ncr_stepA_evidence.csv`.
  - "1.5 months" is read as the 15 Nov–27 Dec 2024 span.
- **G2, NCR: approved with changes.**
  - Confirmed and unconfirmed builders are reported separately.
  - The main benchmark is all eligible developer controls, equal-weighted; the nearest two by size is the robustness check.
  - NBCC gets a PSU benchmark and a window ending 22 Nov, and the controls' returns on 25 Nov are shown.
  - Adani Enterprises is also dropped. ACC is flagged as contaminated for Step C.
  - The placebo firms are listed with exclusions and reasons (`outputs/deliverables/placebo_firms.csv`).
- **G2, Gujarat: approved with changes.**
  - Both footprints are reported. The Vadodara footprint is defined by sites, adding Gujarat Alkalies' Vadodara complex (dark on 30 Aug).
  - Step A starts from GSFC and Gujarat Alkalies. Bodal's Vadodara plants had no usable reading.
  - DCW is excluded.
  - Controls are matched by sub-industry first and size second. All ten firms are kept, and the five are not described as size-matched.
  - The user checks the five unverified controls by hand.
- **Implementation notes:**
  - Kiri is also in the Vadodara-site set, under the same site rule.
  - One Bodal Vadodara site (plant 650, zero project cost in the pack) did have a reading: dark on 30 Aug.
  - The fertiliser pool takes firms with ≥ 25% of plant cost in fertiliser plants: GSFC, GNFC, Zuari.
