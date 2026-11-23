# Data to download by hand

Everything below could not be reached from the cloud session, or is behind a login or a licence.
Each item says what to get, where, how, and where to save it, so the scripts can pick it up.
A machine-readable copy with the same IDs is `manual_collection/REQUESTS.csv`. Source links were
checked on 18 Nov 2026 by a sub-agent (see the "Checked" note on each item and
`manual_collection/REQUESTS_verification.csv`, which has a quote for each confirmation).

**How to hand data back:** put files in the folder named under "Save as" (keep the original file
too if it is a PDF or Excel), then tell me which IDs you collected. Filled-in templates go in
`manual_collection/` next to the blank template, with `_filled` added to the name.

**What is already in hand (do not collect):**
- **Economic flows:** daily state electricity; state GST collections (monthly, all states needed); all-India cement and fertiliser output indices; rail freight Oct 2023 to Feb 2024.
- **Air quality and orders:** Delhi daily air quality for three winters; the pollution-control orders and the revised GRAP schedule of 13 Dec 2024.
- **Satellite data:** daily night lights; radar and optical images; the Indian space agency's Chennai flood map.
- **Rainfall and prices:** IMD gridded rainfall 2000–2025; prices to Nov 2026.
- **Damage and disclosures:** insurer catastrophe-loss disclosures; the Rajya Sabha answers on Gujarat production losses and Tamil Nadu flood damage; earnings calls for Apollo Hospitals, Maruti, JK Tyre and SRF.

---

## High priority: these could change a conclusion

### M1a. Monthly production of the Chennai tyre plants
- **What:** monthly tyre production (tonnes or units) for Apollo Tyres, JK Tyre, CEAT and MRF, by plant if available (Oragadam, Sriperumbudur, Chennai), **Sep 2023 to Mar 2024**.
- **Why:** the satellite shows the tyre belt lit from 6 Dec 2023, and the companies said nothing. Monthly output would show whether any production was lost (Step 2: lost versus delayed).
- **Where:** CMIE Prowess dx or CMIE Industry Outlook (institute library); ATMA, the tyre makers' association, at atmaindia.org.in.
- **Checked:** CMIE's site answers (data behind a login). Note that atmaindia.org (without .in) is a parked domain. No free monthly tyre production table was found; ATMA's figures appear to be in subscriber publications.
- **Save as:** `manual_collection/monthly_operating_filled.csv` (layout of `monthly_operating_template.csv`: nse_symbol, month, metric, unit, value, source_url, notes).

### M1b. Monthly fertiliser and chemical production by plant (Gujarat)
- **What:** monthly production by product for GSFC (Vadodara and Sikka units), GNFC (Bharuch) and Gujarat Alkalies (Vadodara, Dahej), **Jun to Dec 2023 and Jun to Dec 2024**.
- **Why:** the best single lead left. GSFC's Vadodara sites were dark on 30 Aug 2024 and its stock fell 13.5% over 20 days.
- **Where:** Department of Fertilizers (fert.gov.in) monthly production report, plant-wise if published; Fertiliser Association of India monthly statistics (faidelhi.org, members only); CMIE Industry Outlook. data.gov.in has a product-wise, month-wise national series ("product-wise and month-wise production of chemical fertilizers"), which is useful only as a control.
- **Checked:** fert.gov.in and data.gov.in do not answer from the cloud session, and a public plant-wise monthly report could not be confirmed.
- **Save as:** `manual_collection/monthly_operating_filled.csv`.

### M1c. Regional cement despatches (north India)
- **What:** monthly cement despatches for the North region, and by company if available (UltraTech, Shree Cement, ACC/Ambuja), **Oct 2023 to Mar 2025**.
- **Why:** only national cement output is public, and it shows no dip. A northern dip in Nov to Dec 2024 would measure the construction delay that DLF and NBCC described.
- **Where:** CMIE Industry Outlook (Cement); broker notes; the Cement Manufacturers' Association (cmaindia.org).
- **Checked:** the association's site answers but shows no monthly data page. CMIE's regional despatch coverage is unconfirmed, so ask the library which product has it.
- **Save as:** `manual_collection/monthly_operating_filled.csv`.

### M2. Chennai flood-extent map from the Indian space agency — FOUND, now optional
- **Status:** the PDF map (sheet "2023/CY/TN/01a/07122023", RISAT-1A, 7 Dec 2023) was found on the NDEM portal and turned out to be a GeoPDF with embedded coordinates. It has been georeferenced and every Chennai plant tested (README 5.24): no tyre plant had flood water within 1 km.
- **Only if you want to refine this:** the vector layer (shapefile, KML or GeoJSON) behind the map, from NRSC or the Bhuvan/NDEM disaster portals. It would change little.
- **Save as:** `external/flood_maps_manual/`.

### M3. Supplier and customer links with revenue shares
- **What:** for the 61 traded firms, named suppliers and customers with revenue or cost shares.
- **Why:** only 11 sourced links exist; propagation (Step 4) cannot be tested without dependence shares.
- **Where:** Bloomberg (SPLC function), FactSet Revere, Capitaline or CMIE Prowess.
- **Checked:** Bloomberg SPLC is confirmed by library guides; the export format is not.
- **Save as:** `manual_collection/supply_links_filled.csv` (layout of `supply_links_template.csv`).

### M4. Plant locations for more listed firms (scale-up)
- **What:** all plant or project locations (district, state, latitude and longitude, project cost, industry, status) for a few hundred more NSE-listed firms, in the layout of `data/plants.csv`; and quarterly shares outstanding for the same firms.
- **Why:** the 2025–26 out-of-sample test uses only 61 firms and is dominated by one week. More firms is the only way to raise power (Step 6). Prices for new firms can then be fetched automatically.
- **Where:** the database behind the pack. It carries CMIE company codes and project costs, which suggests CMIE CapEx. That is my inference, so please confirm with whoever supplied the pack.
- **Checked:** institute library guides say CMIE CapEx records project location by state and district, for projects of ₹1 crore and above.
- **Save as:** `data_manual/plants_more_firms.csv`.

---

## Medium priority: fill gaps, unlikely to overturn a result

### M1d. Construction progress of NCR projects (RERA)
- **What:** quarterly progress reports (percentage completion) for the NCR projects of DLF, NBCC, Anant Raj, Parsvnath and Unitech, **Apr 2024 to Mar 2025**.
- **Why:** would show whether building actually slowed during the Nov to Dec 2024 ban.
- **Where:** Haryana RERA project pages, which carry a public quarterly schedule (example: `https://haryanarera.gov.in/view_project/quaterly_schedule_preview_open/NjQ3`); UP RERA for Noida and Ghaziabad.
- **Checked:** Haryana RERA confirmed. The UP RERA domain could not be confirmed from the cloud session.
- **Save as:** `manual_collection/monthly_operating_filled.csv` (metric = percent_complete).

### M5. Vehicle registrations by maker and state
- **What:** monthly registrations by maker for Tamil Nadu and all India, **Oct 2023 to Feb 2024**.
- **Where:** the Ministry of Road Transport and Highways' public VAHAN report, `https://analytics.parivahan.gov.in/analytics/vahanpublicreport?lang=en`. Filter by state and maker, then by month, and export.
- **Checked:** the page answers, but it is an interactive app that signs its own data requests, so it could not be automated. The old vahan4dashboard address does not answer.
- **Save as:** `manual_collection/vahan_maker_state_month.csv` (state, maker, month, registrations).

### M6. GST e-way bills by state
- **What:** number and value of e-way bills by state, monthly (Tamil Nadu, Gujarat, Delhi, Haryana, Uttar Pradesh, Karnataka, Maharashtra), **Oct 2023 to Mar 2024 and Jul 2024 to Mar 2025**.
- **Why:** closer to physical goods movement than the GST collections already in hand.
- **Where:** GST statistics page, `https://www.gst.gov.in/download/gststatistics`.
- **Checked:** the page is confirmed, but only national month-wise figures were confirmed there. A state-wise monthly e-way bill file is unconfirmed. If it isn't there, skip this item: state GST collections are already in hand.
- **Save as:** `manual_collection/eway_bills_state_month.csv` (state, month, number, value_cr).

### M7. Railway freight loading by commodity and zone
- **What:** monthly loading by commodity (cement, clinker, coal, iron ore, fertilisers), all India and Northern Railway, **Oct 2024 to Mar 2025** (plus Oct 2023 to Mar 2024 for comparison).
- **Why:** the government press releases stop after Feb 2024.
- **Where:** Railway Board, Directorate of Statistics & Economics, monthly statistical summaries. Example path: `https://nfr.indianrailways.gov.in/railwayboard/uploads/directorate/stat_econ/downloads/June_20.pdf`.
- **Checked:** these sites do not answer from the cloud session. Whether a zone-by-commodity monthly table exists is unconfirmed.
- **Save as:** `manual_collection/rail_freight_month.csv` (month, zone, commodity, million_tonnes).

### M8. Official river-gauge and dam-release records
- **What:** hourly level of the Narmada at Golden Bridge, Bharuch, 15 to 20 Sep 2023; Vishwamitri at Kala Ghoda, Vadodara, 25 to 31 Aug 2024; Sardar Sarovar outflow (cusecs) hourly, 15 to 19 Sep 2023.
- **Why:** press-reported levels are in hand (README 5.15); official series would firm up timing and the dam-release trigger.
- **Where:**
  - India-WRIS (`https://indiawris.gov.in/wris/`, free registration). The Narmada station is called "Bharuch" in CWC data, not "Golden Bridge".
  - CWC flood forecasting (`https://ffs.india-water.gov.in/`).
  - Gujarat Water Resources Department's daily dam abstract, which gives storage, inflow and outflow (`https://wrd.guj.nic.in/dam/pdf.php`).
- **Checked:** none of these answers from the cloud session.
- **Save as:** `manual_collection/river_gauge_filled.csv` (layout of `river_gauge_template.csv`).

### M9. Tyre and rubber monthly statistics
- **What:** monthly natural-rubber consumption by the tyre sector, and monthly tyre production (all India), **Oct 2023 to Mar 2024**.
- **Where:** Rubber Board's monthly "Rubber Statistical News" PDFs (rubberboard.gov.in); ATMA (atmaindia.org.in).
- **Checked:** rubberboard.gov.in gives a certificate error from the cloud session.
- **Save as:** `manual_collection/monthly_operating_filled.csv`.

---

## Low priority and optional

### M10. Station-level hourly air quality in NCR
- **What:** hourly PM2.5 at stations in Gurugram, Noida, Ghaziabad, Faridabad and Delhi, 25 Oct to 31 Dec of 2022, 2023 and 2024.
- **Why:** daily city air quality is complete for three winters; stations near the project sites would sharpen the treatment.
- **Where:** CPCB Central Control Room data repository, `https://airquality.cpcb.gov.in/ccr` (15-minute or hourly averages). **Do not use app.cpcbccr.com**, which appears to be a commercial site.
- **Checked:** the official address does not answer from the cloud session.
- **Save as:** `manual_collection/delhi_aqi_station_hourly.csv`.

### M11. Earnings-call transcripts not found on the exchange
- **What:** Gujarat Alkalies (Q2 FY24, Q2 FY25), Anant Raj (Q3 FY25), Shree Cement (Q3 FY25), if calls were held.
- **Where:** gacl.com ("other financial information"), anantrajlimited.com (investors page), shreecement.com (Analyst/Investor Meet section), or BSE filings.
- **Checked:** the domains are correct and each page has a transcript heading. Whether recent quarters are posted is unconfirmed; Gujarat Alkalies' only transcript link is a 2019 file.
- **Save as:** `research/transcripts/`.

### M12. Customs shipment records (paid)
- **What:** shipments by company for the Chennai tyre makers (Nov 2023 to Jan 2024) and Dahej chemical firms (Aug to Oct 2024).
- **Where:** Volza, Exim Trade Data or Seair (paid; Volza offers a small free sample).

### M13. Google Earth Engine access (a resource, not data)
- **What:** a Google Earth Engine service-account key, provided through the secure credential form (never in chat).
- **Why:** lets night lights, radar and optical water be computed at every plant for all ~1,000 rain episodes of 2020–2026, without downloading about 200 GB of tiles. That turns the plant-level test from 66 episode-weeks into the full panel, which matters because the dark-asset result (README 5.17) rests on 19 firm-episodes.
- **Where:** non-commercial registration at `https://code.earthengine.google.com/register`.

---

## What I need from you besides data
- Approve the application "NASA GESDISC DATA ARCHIVE" on your NASA Earthdata profile if you want the NASA copy of the nitrogen dioxide and rainfall archives (a public mirror was used instead).
- Confirm the source of the pack (item M4).
