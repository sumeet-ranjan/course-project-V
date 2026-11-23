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
  - The Q3 sales slope (p = 0.05) is matched by the same slope on the pre-ban quarter (p = 0.05). It reflects B.L.
    Kashyap's earlier decline. It vanishes on the change in growth (p = 0.79) and without B.L. Kashyap.

**Panel B: Gujarat, forward (H2): Tata Chemicals → Tata Consumer.**
- **One verified link, so there is no slope.**
- **Weight:** Tata Chemicals' share of Tata Consumer's material input cost, FY24, 18.2–24.0%.
- **Supplier's hit:** about 10 days at Mithapur; 40,000 t of salt lost, against 13.48 lakh t of annual salt demand from
  Tata Consumer.
- **Buyer's response:** one retail price increase on Tata Salt, ₹2 on ₹28 (about 7%), from October 2024. Salt price/mix
  ran +1, +2, +6 and +8 pp in Q1–Q4 FY25, beside volume growth of +8%, 0%, +1% and +5% (`stepC_gj_tcpl_salt.csv`).
- **Magnitude** (`stepC_gj_salt_magnitude.csv`):
  - No document gives the part of the storm cost passed to Tata Consumer.
  - Tata Chemicals put its whole weather cost at about Rs 40 cr.
  - A 7% increase is worth at least Rs 110.4 cr a year (7% × FY24 purchases of Rs 1,576.64 cr), about 2.8 times that
    cost. This fits the company's statement that the increase also recovers two years without an inflation increase.

**Panel C: NCR, market level (not a firm link).**
- **Test:** cement makers with northern capacity minus makers with none.
- **Result:** **+2.5 pp over (−1,+5), p = 0.34.** A hit would make the gap negative. It is a coarse test with little
  power: propagation is not detected.
- **Two-firm variant: run, not interpreted.** A variant against the two documented zero-capacity makers only gave
  +10.6 pp over (−1,+5), p = 0.005. It is not interpreted because it rests on two firms. No company news explains Star
  Cement's −9.2%, and Prism Johnson's −5.9% follows its loss-making Q2 results of 13 Nov 2024
  (`research/realign/news_checks.csv`).
