# Climate shocks & supply-chain propagation — RA starter package

**One-line:** when a documented extreme event (a flood, a pollution-driven shutdown) hits the
*physical plants* of a listed firm, does the shock **propagate through the supply chain** to
firms that were never in the disaster zone — their suppliers and their customers — and can we
**see and trace that pathway in real data**?

This folder is a **real** (not simulated) sample, deliberately chosen for the **highest chance**
of a *visible, traceable* pathway: real listed firms, their real plant locations, real
financials, real daily stock prices, and a handful of well-documented real events. Nothing is
planted. Your job is to find out whether the propagation is actually there, and if so, to trace
*how* it travels — node by node, with evidence — for a couple of key events.

> Why "trace", not just "regress": an AI agent can run the direct event-study in minutes. The
> hard, valuable part — building the *real* supplier↔customer links from disclosures, confirming
> the mechanism from earnings calls and news, separating propagation from sector-wide confounds,
> and judging what is economically material — needs human reading and judgment. This package is
> built so you (with your own AI agents as assistants) do exactly that.

---

## The two key events to deep-dive

Both are documented, dated, and geographically concentrated on places where listed firms have
dense physical assets — so a propagation signal, if it exists, has the best chance of showing:

1. **Delhi-NCR GRAP-IV shutdown (Nov 2024; recurs Nov-2022, Nov-2023).** A regulatory, *exact-dated*
   halt: non-essential construction banned, industrial fuel curbs across the National Capital
   Region. Natural chain: **cement / steel → construction / real-estate / infrastructure**
   (the construction ban hits downstream sites directly; suppliers lose offtake).
2. **Gujarat floods — Vadodara/central Gujarat (Aug–Sep 2024; also 2023).** River flooding
   submerges the **Vadodara–Bharuch chemical belt**. Natural chain: **basic/organic chemicals →
   specialty chemicals / pharmaceuticals / agrochemicals** downstream.

Two more events (**Himachal floods 2023** → Baddi pharma belt; **Chennai Michaung 2023** → auto/
electronics) are included for cross-sectional breadth and robustness, not for the deep-dive.

---

## What's in here

```
data/
  companies.csv              selected firms: id, industry, #plants, asset size, ROLE (exposed/neighbour/control)
  plants.csv                 every plant: lat/lon, district, industry, project_cost (= asset distribution)
  financials_annual.csv      real financials per firm-period: revenue, EBITDA margin, growth, capex, filing date
  stock_daily.csv            real daily OHLCV + returns, 2020–2025
  extreme_events.csv         the documented events: dates, type, affected districts, source note
  event_plant_exposure.csv   which firms' plants sit in each event's districts (the direct-exposure map)
  supply_chain_scaffold.csv  CANDIDATE supplier→buyer links (industry-based HYPOTHESES — you must verify)
codebook/
  build_real_sample.py       exact, re-runnable construction of this sample (sources + selection logic)
README.md  DATA_DICTIONARY.md  INSTRUCTIONS.md  PI_NOTES.md
```

**Read `INSTRUCTIONS.md` next** — it has the research question, hypotheses, the step-by-step
tracing exercise, the extra data to fetch yourself, suggested methods, and the deliverables.
`DATA_DICTIONARY.md` documents every column. `PI_NOTES.md` is for the supervisor.

---

## Important honesty notes (read before you trust anything)

- **The supply-chain links are a scaffold, not ground truth.** `supply_chain_scaffold.csv` is a
  set of *industry-level hypotheses* ("cement firms plausibly supply construction firms"). The
  first real task is to **replace these with verified firm-to-firm links** from annual reports,
  customer/supplier disclosures, and trade data. Do not report a propagation result on an
  unverified link.
- **Financials are an annual nowcast-panel** (revenue proxy from log-sales, EBITDA margin, growth,
  capex intensity) — good for structure and scale, but **fetch fuller quarterly statements** for
  the event windows (the propagation shows up in *quarterly* input costs / inventory / guidance).
- **`project_cost` is an asset-size proxy**, not audited gross block; use it for relative
  concentration, not levels.
- **Exposure = plant district inside the event's documented footprint.** Refine it (ward/pincode,
  actual inundation/AQI maps) for the firms you deep-dive.
- This sample is assembled from **public-domain** data (exchange prices, disclosed plant locations,
  public financial filings, public disaster/regulatory records). Treat it accordingly.
