# Instructions — climate shocks & supply-chain propagation

**Audience:** pre-doctoral RAs with your own AI coding/research agents. Use the agents freely for
data wrangling, scraping, event-study code, and first-pass reading — but the *judgments* below
(which links are real, which mechanism is operating, what is a confound) are yours to make and
defend. The whole point of this project is to do the tracing an agent can't do alone.

---

## 1. The research problem

> **When a localized, documented extreme event damages the physical plants of a listed firm, does
> the shock propagate along the supply chain to firms that were never in the disaster zone?**

Direct damage (your plant floods) is obvious and easy to measure. The interesting, under-measured
question is **indirect propagation**: a flooded *chemical supplier* starves a *pharma buyer*
hundreds of km away of a key input; an NCR *construction ban* idles the sites that a *cement/steel
supplier* feeds. We want to (a) establish whether this propagation is detectable in financials and
stock returns, and (b) **trace the causal pathway** for two key events in enough mechanistic detail
that a referee would believe it.

### Hypotheses
- **H1 (direct).** Directly-exposed firms (a plant in the event district) show negative abnormal
  operating/financial/return responses around the event vs matched controls.
- **H2 (forward propagation).** *Buyers* of a hit supplier, themselves **not** in the event zone,
  show a **lagged** negative response, **scaled by input dependence** (share of COGS from that
  supplier).
- **H3 (backward propagation).** *Suppliers* to a hit firm lose offtake → a smaller, lagged
  negative response scaled by revenue dependence on the hit firm.
- **H4 (dose-response & placebo).** Effects grow with exposure concentration × event severity ×
  dependence; firms with **no exposure and no chain link** to hit firms show **nothing** (placebo).

---

## 2. The two deep-dives (the heart of the project)

For **E_NCR_GRAP_2024** and **E_GJ_FLOOD_2024**, build a **node-by-node traced pathway** and
back every link with evidence. For each event:

**Step A — Confirm the shock at the source.** Pick 2–3 directly-exposed firms with high exposure
concentration (plant cost ÷ firm total, from `event_plant_exposure` + `companies`). Confirm the
plant was actually hit and operations actually stopped — from **company disclosures** (BSE/NSE
announcements, force-majeure notices), **earnings-call transcripts**, and **news**. Record dates.

**Step B — Build the REAL chain (replace the scaffold).** `supply_chain_scaffold.csv` only *guesses*
links from industry. Replace each candidate with **verified firm-to-firm relationships**:
- annual-report customer/supplier concentration, related-party, and segment notes;
- management commentary ("we source X% of input Y from …");
- trade data (import/export shipment records, e.g. Volza/Exim-style) and distributor lists;
- for each verified link, estimate the **dependence weight** (supplier's share of the buyer's input
  cost, or buyer's share of the supplier's sales) — even a bracketed estimate with a cited basis.

**Step C — Measure the response at each node.** For the hit firm and each verified
supplier/buyer, compute the **cumulative abnormal return (CAR)** around the relevant window (see
§4) and look at the next **quarterly** financials (revenue, EBITDA margin, inventory, input cost,
guidance). Note the **timing/lag** at each hop.

**Step D — Confirm the mechanism, not just the correlation.** A price move near an event is not
proof of propagation. For each downstream hit, find the **disclosure breadcrumb** that names the
channel (an input shortage, a cost spike, a project delay attributed to the shock) and rule out
coincident confounds (a sector-wide demand shock, an unrelated regulatory event, the market).

**Step E — Draw the pathway.** Produce a labelled diagram: *event → exposed plant(s) → hit firm
(evidence, dates) → verified link (dependence) → downstream/upstream firm (CAR, Δfinancials,
evidence, lag)*. This diagram + its evidence table is the primary deliverable.

---

## 3. Data you must fetch yourself (your agents can help)
- **Real supply-chain links:** annual reports / investor presentations (customer & supplier
  concentration, segments, related-party); shipment/customs trade data; distributor & vendor lists;
  any FactSet/Bloomberg/Capitaline supply-chain module you have access to.
- **Quarterly financials & disclosures:** screener.in / Capitaline / company filings (quarterly
  revenue, margins, inventory, segment); **BSE/NSE announcements**; **earnings-call transcripts**
  (where force-majeure / input-shortage / guidance language lives).
- **Event ground-truth:** IMD rainfall bulletins & CWC flood reports; **CAQM GRAP orders** (exact
  stage/date); AQI records; news archives; EM-DAT. Refine each event's window and footprint.
- **Benchmarks:** NIFTY/sector indices for the market model; a peer set for matched controls.

## 4. Suggested methods (pre-doc toolkit)
- **Event study.** Market-model (or FF-style) abnormal returns; estimation window well before the
  event; report CAR over tight (−1,+5) and propagation-appropriate wider windows; non-overlapping,
  and cluster/bootstrap SEs by event-date (returns are cross-sectionally correlated on a given day).
- **DiD / two-way FE.** Exposed vs matched-control firms, pre vs post, firm + time fixed effects,
  on quarterly operating outcomes.
- **Cross-sectional dose-response.** Regress downstream CAR (or Δmargin) on **dependence weight ×
  (supplier hit severity)**, controlling for own direct exposure, sector, size.
- **Lag structure.** Estimate the propagation lag (buffer stocks delay the hit); plot CAR by weeks-
  since-event for suppliers vs buyers.
- **Placebo / falsification.** Same tests on `control` firms and on *unexposed, unlinked* firms
  must return nulls. A positive placebo means a confound is driving your result — find it.

## 5. Use your AI agents for … vs. decide yourself
| Hand to the agent | Keep for yourself |
|---|---|
| scrape/clean financials, transcripts, trade data | **which** firm-to-firm links are real & material |
| write event-study / DiD / regression code | **which** mechanism the evidence actually supports |
| summarize 50 disclosures, extract dates | ruling out confounds; judging economic magnitude |
| build the exposure & dependence tables | the final causal-pathway claim and its caveats |

## 6. Deliverables
1. **Two traced-pathway diagrams** (one per key event) with an evidence table per node (date,
   source, quote, CAR, Δfinancial, lag).
2. **Verified supply-chain links file** (replacing the scaffold) with dependence weights + sources.
3. **Results tables:** (i) direct event study/DiD, (ii) propagation dose-response, (iii) placebos.
4. **A 3–5 page memo**: what you found, how strong it is, and — explicitly — **what the manual
   trace caught that a purely automated pipeline would have missed or gotten wrong.** That last
   section is the real output of this exercise.

## 7. Suggested order of work
1. Reproduce the **direct** event study on the two key events (agent-fast) — get oriented.
2. Do **Step A–B** for one chain (NCR cement/steel→construction is the cleanest; dated regulatory
   shock) — confirm source shock + verify 2–3 real links.
3. Measure & confirm propagation (Step C–D), estimate the lag, run the placebo.
4. Repeat for the Gujarat chemicals chain.
5. Generalize: dose-response across all verified links; write the memo.

*Start small and real — one verified link traced convincingly beats a regression on 100 guessed ones.*
