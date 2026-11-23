# Decision G4: NCR links from NBCC and DLF (Step B). Recommendation and evidence (23 Nov 2026)

**The question:** which links from the confirmed hit firms are real and material, and does the regional fallback
weight count? Evidence tables:
- `research/realign/stepB_builder_side.csv`
- `stepB_supplier_side.csv`
- `stepB_contractors.csv`

Every quote has been checked against the saved document text (`quote_check_realign.csv`). Links are in
`outputs/deliverables/verified_links.csv`, rows N001–N084. Nothing that depends on G4 has been run.

## Evidence

**1. The builders' own documents**
- **NBCC, BRSR FY2024-25:**
  - Procurement: "As a Project Management Consultancy (PMC), NBCC subcontracts project execution to contractors and does not directly procure construction materials or machinery."
  - Related-party purchases: 0.50% of total purchases.
  - No approved-make list was found; NBCC's tender portal returned errors.
- **DLF, BRSR FY2024-25:**
  - "Value chain partners include contractors and vendors engaged in construction of projects…"
  - Related-party purchases: "Nil".
  - 27% of input material by value comes from MSMEs; 100% is sourced within India.
  - No supplier is named. The full annual report came back empty through the page reader.

**2. Thirteen cement and steel firms** (UltraTech, Shree, ACC, Ambuja, JK Cement, JK Lakshmi, Dalmia, Tata Steel, JSW Steel, SAIL, JSPL, Jindal Stainless, APL Apollo)
- **NBCC and DLF as customers:** none of the 13 names either of them.
- **Customer concentration:** nine state that no customer reaches 10% of revenue: Shree, ACC, Ambuja, JK Lakshmi, Dalmia, Tata Steel, SAIL, JSPL and Jindal Stainless. UltraTech, JK Cement and JSW Steel annual reports refused the reader.
- **Regional mix:** no firm discloses a North or NCR sales share. Only capacity is given: UltraTech has 33.3 mtpa in the North; ACC has 25% of its capacity in its northern zone.
- **Q3 FY25 documents:** only UltraTech refers to the curbs: "Infrastructure segment registered degrowth on account of pollution control measures taken in Delhi and surrounding regions, projects on hold due to farmers agitation in Punjab and completion of major projects like RRTS." JK Cement: "Delhi will have some elections, not any major disruption." The other firms' Q3 documents say nothing.

**3. Contractors** (their own exchange filings and Q3 FY25 documents)

| Link (upstream ← hit firm) | Contracts running in Nov–Dec 2024 | Builder's share of the contractor's sales (low–high, basis) | NCR share of the contractor's work |
|---|---|---|---|
| Ahluwalia Contracts ← DLF | The Arbour, Sector 63 Gurugram (Rs 744.68 cr, May 2023; Rs 11–12 cr a month in Nov 2024). DLF City Center Downtown (Rs 1,094.7 cr, nothing executed by 31 Dec 2024) | 3.4% (Arbour run-rate ÷ FY24 revenue) to 10.0% (DLF's share of the unexecuted order book) | 33.3% of the unexecuted order book |
| B.L. Kashyap ← DLF | Mall of India DLF Downtown Ph-2 (Rs 924.11 cr, Jun 2024, 21 months). DLF The Arbour (Rs 222.66 cr) | 34.6% (DLF orders ÷ order book) to 43.5% (Ph-2 annualised ÷ FY24 revenue) | Haryana 45.4% and Delhi 10.1% of the order book |
| J. Kumar Infraprojects ← NBCC | Hari Nagar DTC depot, New Delhi (Rs 334.25 cr, Mar 2024, 24 months) | 1.6% (contract ÷ order book) to 3.4% (annualised ÷ FY24 revenue) | not stated |
| Capacit'e ← NBCC | Noida, about Rs 1,120 cr | — | rejected: awarded Feb 2025, after the ban |

**Ahluwalia's calls:**
- Q2 FY25, Nov 2024: "So now GRAP-IV is in place … That's why I've kept the margin guidance muted for the rest of the year, because we have a lot of large projects in NCR, especially Gurgaon."
- Q3 FY25, Feb 2025: "we have been hit as along with our other peers by the NGT bans in Delhi."
- Q3 FY25: DLF "compensated the labor for staying back". Work restarted "on 3rd of February", the day the last Stage III order was revoked.

The other contractors' Q3 documents say nothing.

## Recommendations (your calls)

**R1. The cement/steel hop is not verified; the firm-level chain breaks here.**
- No document on either side links a cement or steel firm to NBCC or DLF.
- NBCC says it buys no materials itself.
- Where a supplier's customer-concentration note was readable, NBCC's or DLF's share of that supplier's sales is below 10%.
- The 30 scaffold pairs for NBCC and DLF are marked "not verified". The 45 pairs for the unconfirmed builders are "not searched".

**R2. Accept the three contractor links as verified, and classify the contractors as within-zone upstream nodes.**
- Each relationship is documented on both sides: the award filing, and the contractor's own order book at 31 Dec 2024.
- But the contractors' own NCR sites were under the same ban, so their response mixes direct exposure with dependence on the builder.
- I'd trace them in Steps C–D as the first upstream hop, because they carry the clearest breadcrumbs.
- In the dose-response I'd include them flagged "within zone" and report results with and without them, so they don't pass for out-of-zone propagation.

**R3. Don't use the fallback weight.**
- Regional capacity shares measure exposure to the North market, not dependence on NBCC or DLF.
- Show the cement/steel node as a market-level branch, labelled "not a verified firm link". Its only breadcrumb is UltraTech's statement.

**R4. DLF's "2 malls" are not identified.** Mall of India DLF Downtown Phase-2 (B.L. Kashyap) is a candidate. The City Center Downtown contract showed no execution by 31 Dec 2024. I recommend recording it as a candidate, not a fact.

**R5. If you accept R2, Step C fetches the contractors' prices and quarterly results.** Ahluwalia, B.L. Kashyap and J. Kumar are listed.
