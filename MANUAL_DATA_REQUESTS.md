# Data to download by hand (deliverables only)

Since 23 Nov 2026 this list keeps only the items that serve one of the four deliverables in
`docs_from_pack/INSTRUCTIONS.md` §6. The earlier, longer list is in `archive/MANUAL_DATA_REQUESTS_round4.md`
(items M1a, M2, M4–M10 and M13 are dropped). The machine-readable copy is `manual_collection/REQUESTS.csv`.

**How to hand data back:** put the files in the folder named under "Save as" (keep the original PDF or
Excel too), then tell me which IDs you collected. Nothing from these files enters a deliverable until I
have read the original document and quoted it.

## For Step B and deliverable 2 (verified links)

### M3. Supplier and customer links with dependence shares (high)
- **What:**
  - (a) Named cement and steel suppliers of the NCR builders NBCC, DLF and Anant Raj, with each builder's share of the supplier's sales, or the supplier's share of the builder's material cost.
  - (b) Named buyers of the Vadodara/Bharuch chemical firms (GSFC, Gujarat Alkalies, GNFC, SRF, Aarti, Kiri, Bodal), with the supplier's share of each buyer's input cost.
- **Why:** the forward test needs the supplier's share of the buyer's input cost. The backward test needs the buyer's share of the supplier's sales. Public filings rarely name these counterparties.
- **Where:** Bloomberg (SPLC function), FactSet Revere, Capitaline or CMIE Prowess (institute library).
- **Save as:** `manual_collection/supply_links_filled.csv` (layout of `supply_links_template.csv`), plus the export file.

### M12. Customs shipment records (high if M3 is not available)
- **What:** shipments by company, with consignee/consignor names, quantities and values:
  - Gujarat chemical firms above: Jun–Dec 2024.
  - NCR builders: steel imports, Oct 2024–Feb 2025.
- **Why:** one of the link sources the instructions name; it also gives a size for the dependence weight.
- **Where:** Volza, Exim Trade Data or Seair (paid; Volza offers a small free sample).
- **Save as:** `manual_collection/shipments/` (the exports as downloaded).

## For Steps A and D (shock at source, mechanism)

### M11. Earnings-call transcripts not found on the exchange (medium)
- **What:**
  - Anant Raj, Q3 FY25 (call held Jan–Feb 2025).
  - Gujarat Alkalies, Q2 FY25 (Oct–Nov 2024).
  - Shree Cement, Q3 FY25.
  - Only if the calls were held.
- **Where:** anantrajlimited.com (investors page), gacl.com ("other financial information"), shreecement.com (Analyst/Investor Meet section), or BSE filings.
- **Save as:** `research/transcripts/`.

### M1d. Construction progress of NCR projects, RERA (low)
- **What:** quarterly progress reports (percentage complete) for the NCR projects of DLF, NBCC and Anant Raj, Jul 2024 to Mar 2025.
- **Why:** shows whether building actually stopped during the ban (Step A), beyond what the companies said.
- **Where:** Haryana RERA project pages carry a public quarterly schedule (example: `https://haryanarera.gov.in/view_project/quaterly_schedule_preview_open/NjQ3`); UP RERA for Noida and Ghaziabad.
- **Save as:** `manual_collection/monthly_operating_filled.csv` (metric = percent_complete).

## For Step C (response at each node)

### M1b. Monthly production by plant, Gujarat (medium)
- **What:** monthly production by product for GSFC (Vadodara), Gujarat Alkalies (Vadodara, Dahej) and GNFC (Bharuch), Jun to Dec 2024.
- **Why:** the only direct test of whether a Vadodara plant lost output in Aug–Sep 2024 (Step A), and the hit firm's Δoutput (Step C).
- **Where:** Department of Fertilizers monthly production report (fert.gov.in, does not answer from the cloud session); Fertiliser Association of India statistics (faidelhi.org, members only); CMIE Industry Outlook.
- **Save as:** `manual_collection/monthly_operating_filled.csv`.

### M1c. Regional cement despatches, north India (medium)
- **What:** monthly cement despatches for the North region, and by company if available (UltraTech, Shree Cement, ACC/Ambuja), Jul 2024 to Mar 2025.
- **Why:** the supplier node's volume response to the NCR ban (Step C). Quarterly accounts mix all regions.
- **Where:** CMIE Industry Outlook (Cement), broker notes, Cement Manufacturers' Association (cmaindia.org).
- **Save as:** `manual_collection/monthly_operating_filled.csv`.
