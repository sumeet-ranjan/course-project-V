# Data dictionary

All ids join on **`nse_symbol`** (= `asset_id` in `stock_daily.csv`) and/or **`co_code`**.
Monetary values are in **₹ crore** (1 cr = 10 million). Coordinates are WGS-84 (EPSG:4326).

### `companies.csv` — one row per firm
| column | meaning |
|---|---|
| `nse_symbol` | NSE ticker; the primary key; equals `asset_id` in stock data |
| `co_code` | internal company code (joins to `financials_annual`) |
| `company` | registered company name |
| `primary_industry` | modal industry across the firm's plants |
| `n_plants` | number of plant records for the firm |
| `total_project_cost_cr` | sum of plant `project_cost` — a firm-size / asset proxy |
| `role` | `directly_exposed` (a plant sits in an event district), `chain_neighbour` (industry up/downstream of an exposed firm — a propagation *candidate*), or `control` (same industries, no event-district plant) |

### `plants.csv` — one row per plant (the asset distribution)
| column | meaning |
|---|---|
| `nse_symbol`, `co_code`, `company` | owning firm |
| `lat`, `lon` | plant coordinates |
| `dist_name` | district (used to match events) |
| `industry_name` | plant's industry/product line |
| `project_cost_cr` | disclosed project cost — relative asset weight of this plant |

### `financials_annual.csv` — one row per firm-period (real)
| column | meaning |
|---|---|
| `nse_symbol`, `co_code` | firm |
| `fund_period` | fiscal period the statement covers |
| `fund_filing_date` | when it was filed (use for look-ahead-safe event alignment) |
| `revenue_proxy_cr` | revenue (= exp(`f_log_sales`)) |
| `f_log_sales` | log revenue |
| `f_g_log_sales` | revenue growth (Δ log sales) |
| `f_ebitda_margin` | EBITDA margin |
| `f_capex_intensity` | capex / sales |
| `n_plants` | plant count at filing |

*Coverage is partial and annual — fetch quarterly statements for the event windows yourself.*

### `stock_daily.csv` — one row per firm-day (real)
| column | meaning |
|---|---|
| `asset_id` | = `nse_symbol` |
| `date` | trading date |
| `open`,`high`,`low`,`close` | daily prices (split/bonus handling: verify before CAR) |
| `volume` | shares traded |
| `daily_return` | close-to-close simple return |

### `extreme_events.csv` — one row per event
| column | meaning |
|---|---|
| `event_id` | event key (joins to `event_plant_exposure`) |
| `type` | `flood` / `pollution_shutdown` |
| `name` | human description |
| `start`, `end` | event window (refine per event from primary sources) |
| `affected_district_keywords` | `|`-separated district substrings used to flag exposure |
| `is_key_event` | `True` for the two deep-dive events (NCR-GRAP, Gujarat-flood) |
| `note` | what happened + why these firms are plausibly affected |

### `event_plant_exposure.csv` — one row per (event, exposed plant)
| column | meaning |
|---|---|
| `event_id`, `nse_symbol` | event and exposed firm |
| `plant_lat`, `plant_lon`, `district`, `industry` | the exposed plant |
| `plant_project_cost_cr` | that plant's asset weight (→ exposure concentration = plant cost ÷ firm total) |

### `supply_chain_scaffold.csv` — CANDIDATE links (HYPOTHESES, not verified)
| column | meaning |
|---|---|
| `supplier`, `buyer` | `nse_symbol`s of a hypothesised supplier→buyer pair (both in-sample) |
| `supplier_industry`, `buyer_industry` | their industries |
| `hint` | the industry rule that generated the guess (e.g., `cement->construction`) |
| `status` | always `HYPOTHESIS_verify_from_disclosures` — **replace with verified links before use** |
