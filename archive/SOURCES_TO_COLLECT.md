# Sources to collect manually

**Round 4: the current, checked list of what to download by hand is `MANUAL_DATA_REQUESTS.md` (IDs M1a–M13).** This file is the longer background list from Rounds 1–3; where the two differ, follow `MANUAL_DATA_REQUESTS.md`.

Site addresses are from memory; search the name if a link has moved. Save findings in the
templates in `manual_collection/` so they plug into the existing scripts.

## 1. Company disclosures (feeds step 1)

| Source | Where | What to pull |
|---|---|---|
| BSE corporate announcements | bseindia.com → Corporates → Corporate Announcements | Filings by company and date range, including "disruption of operations" notices |
| NSE corporate filings | nseindia.com → Companies → Corporate Filings → Announcements | Same; cross-check against BSE |
| Earnings-call transcripts | Company investor-relations pages; screener.in company page → Documents → Concalls | Search for: cyclone, flood, Michaung, GRAP, construction ban, pollution, shutdown, force majeure |
| Annual reports and sustainability reports (BRSR) | Company sites; BSE annual-report section | Risk sections, plant-wise capacity, customer and supplier concentration |
| Rating rationales | crisil.com, icra.in, careratings.com, indiaratings.co.in | Named key customers and suppliers, plant locations, stoppage mentions |

Firms and windows:

| Case | Firms | Announcement window | Earnings call |
|---|---|---|---|
| Chennai | Apollo Tyres, MRF, JK Tyre, CEAT, Maruti Suzuki, Hindustan Unilever, Apollo Hospitals | 1–20 Dec 2023 | Q3 FY24 (Jan–Feb 2024) |
| Delhi | DLF, Anant Raj, NBCC, UltraTech, Shree Cement, ACC | 15 Nov 2024 – 15 Jan 2025 | Q3 FY25 (Jan–Feb 2025) |
| Gujarat 2024 | Petronet LNG, GAIL, IOC, BPCL, Gujarat Alkalies, GNFC, GSFC, Aarti Industries, UPL, SRF | 25 Aug – 30 Sep 2024 | Q2 FY25 (Oct–Nov 2024) |
| Gujarat 2023 | Same firms | 15 Sep – 15 Oct 2023 | Q2 FY24 (Oct–Nov 2023) |

## 2. Monthly operating data (feeds step 2)

| Data | Source |
|---|---|
| Vehicle production and sales by maker | SIAM monthly releases; Maruti's monthly production filing on BSE |
| Tyre production | ATMA (Automotive Tyre Manufacturers' Association); Rubber Board monthly rubber consumption |
| Cement production (national, monthly) | Index of Eight Core Industries, Office of the Economic Adviser (eaindustry.nic.in) |
| Regional cement dispatches and prices | Broker channel checks; CMIE |
| Real-estate launches and sales, Delhi region | Developers' quarterly pre-sales updates on BSE; PropEquity, Anarock, PropTiger reports |
| LNG terminal utilisation (Dahej) and gas consumption | PPAC monthly reports (ppac.gov.in) |
| Fertiliser production by plant | Department of Fertilizers monthly bulletin |
| Firm-level monthly or plant-level series | CMIE Prowess and CMIE Industry Outlook, through an institute library |

Window: at least six months before and after each event month (Jul 2023, Sep 2023, Dec 2023, Aug 2024, Nov–Dec 2024).

## 3. Official hazard data (feeds step 3)

| Data | Source |
|---|---|
| Delhi daily air-quality index | CPCB daily AQI bulletin archive (cpcb.nic.in); station data at the CPCB central control room portal (app.cpcbccr.com) |
| Pollution-control orders | caqm.nic.in → Orders/Directions: Stage III and IV invoke and revoke orders, 2022–2024 |
| River levels and flood forecasts | Central Water Commission flood forecast portal (ffs.india-water.gov.in); India-WRIS |
| Sardar Sarovar releases, Sep 2023 | Sardar Sarovar Narmada Nigam daily status; CWC reservoir bulletin |
| Rainfall and cyclone reports | IMD district rainfall data; Cyclone Michaung preliminary report (mausam.imd.gov.in) |
| Mapped flood extent | NRSC Bhuvan disaster services flood maps; Copernicus Global Flood Monitoring; UNOSAT |
| Event loss records | EM-DAT (free academic registration); state disaster-management authority memoranda |

## 4. Supply-chain links (feeds step 4)

| Source | Notes |
|---|---|
| Bloomberg (SPLC function) | Supplier and customer lists with estimated revenue shares; fastest if a terminal is available |
| FactSet Revere, Capitaline, CMIE Prowess (related-party and product tables) | Check which the library licenses |
| Annual-report related-party notes and segment notes | Free, slow; best for joint ventures and group firms |
| Customs shipment data (Volza, Exim Trade Data, Seair) | For imported inputs: rubber, benzene, LNG cargoes |
| Auto industry supplier lists | ACMA directory; makers' vendor-award announcements |

Specific gaps from the research passes: named customers of MRF, CEAT and JK Tyre; Maruti's tyre
suppliers; cement and steel suppliers to DLF, Anant Raj, NBCC; regional sales mix of UltraTech,
ACC and Shree Cement; buyers of GNFC, GSFC, Gujarat Alkalies and Aarti products; NMDC's iron-ore
customer shares; gas suppliers to GNFC, GSFC and Gujarat Alkalies.

## 5. Scaling up (feeds step 6)

| Data | Source |
|---|---|
| Historical market cap and adjusted prices | NSE bhavcopy archive; Prowess; Bloomberg |
| Plant locations for more listed firms | The source database behind the pack (ask whoever supplied it) |

## Suggested order
1. Chennai disclosures (free, a few hours; tests the one statistically significant result).
2. Delhi orders and daily AQI bulletins.
3. Maruti and SIAM monthly data.
4. Supply-chain export from a licensed database.

## 6. Independent proxies (feeds step 1b)

| Proxy | Source | Access |
|---|---|---|
| Night-time lights, daily | NASA Black Marble VNP46A2 (LAADS DAAC / Earthdata) | Free; Earthdata login |
| Radar flood extent | Copernicus Global Flood Monitoring; Sentinel-1 via Copernicus Data Space; NRSC Bhuvan; UNOSAT | Free |
| Nitrogen dioxide | Sentinel-5P TROPOMI (Copernicus Data Space; Google Earth Engine) | Free |
| Electricity demand | Grid-India (formerly POSOCO) daily and monthly reports | Free |
| Vehicle registrations | VAHAN dashboard (vahan.parivahan.gov.in) | Free |
| Railway freight loading | Indian Railways monthly freight statistics; Ministry of Railways releases on PIB | Free |
| GST e-way bills | GSTN monthly statistics | Free |
| LNG and gas throughput | PPAC monthly reports | Free |
| Company-level shipments | Volza, Exim Trade Data, Seair | Paid |
| Insurance claims | General Insurance Council; insurers' quarterly disclosures | Free |
| Disaster-loss memoranda | State disaster-management authorities; Ministry of Home Affairs | Free |
| Closure and restart orders | Gujarat and Tamil Nadu pollution control boards; factory inspectorates | Free |

### Status of section 6 after Round 3 (what worked from the cloud session)

| Proxy | Status | Where it came from |
|---|---|---|
| Night-time lights | Done | NASA cloud archive `data.laadsdaac.earthdatacloud.nasa.gov`, found through the CMR search; Earthdata login |
| Radar flood extent | Done for Gujarat Aug 2024 | Copernicus Global Flood Monitoring: `https://stac.eodc.eu/api/v1` collection GFM, files on `data.eodc.eu`; no login |
| Nitrogen dioxide | Done, not informative (cloud) | Microsoft Planetary Computer `sentinel-5p-l2-netcdf` (public). The NASA copy needs the "NASA GESDISC DATA ARCHIVE" application approved on the Earthdata profile |
| Electricity demand | Done at state level | `https://robbieandrew.github.io/india/data/POSOCO_data.csv` (Grid-India daily reports, compiled) |
| Vehicle registrations | Not reachable | Portal drops the connection; collect by hand |
| Railway freight | Partial | PIB monthly releases; Oct 2024–Feb 2025 not found |
| GST e-way bills | Not reachable | Collect by hand from the GSTN statistics page |
| LNG and gas throughput | Done (quarterly Dahej, monthly national) | Petronet press releases; PPAC LNG import spreadsheet |
| Insurance claims | Partial | Trade press; no General Insurance Council figure confirmed |
| Disaster-loss memoranda | Partial | Press reports of the Tamil Nadu memorandum; Gujarat parliamentary reply unread |
| Closure and restart orders | Chennai only | Press reports of pollution-board directions |

To collect by hand next (highest value first): the Indian space agency's Chennai flood map of
7 Dec 2023; monthly output of the tyre makers and of GSFC Vadodara; regional cement dispatches for
north India, Nov 2024–Feb 2025; vehicle registrations by maker for Tamil Nadu, Nov 2023–Jan 2024.
