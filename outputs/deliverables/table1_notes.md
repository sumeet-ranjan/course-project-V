# Table 1: direct event study and DiD (deliverable 3(i)). How to read it

Built by `src/43_direct_event_study.py`, a rerun of the existing engine (`src/es_lib.py`), with the firm sets
of decision G2 (`research/realign/g2_decision.csv`, from `src/45_g2_decision.py`).

**Files**
- `table1_direct.csv`: one row per event × group × benchmark × window. Columns:
  - `statistic`: the CAR difference in return units (0.01 = 1 percentage point).
  - `p_two_sided`, `p_one_sided_neg`: share of 1,000 random event days with an equally large statistic (one-sided: equally negative).
  - `n_placebo`: placebo days with data. It is below 1,000 when a firm outside the sample has no price history at the placebo date; its prices start in Jun 2021.
- `table1_direct_firms.csv`: CAR per firm and window. These are the node CARs for the evidence tables.
- `table1_returns_25nov2024.csv`: raw and abnormal returns on 25 Nov 2024 (day +4) for the builders, the developer controls and the benchmark indices.
- `table1_did.csv`: quarterly DiD, with firm and quarter fixed effects and SE clustered by firm.

**Method:** market model against NIFTY 500, estimation window [−250, −30] trading days. CARs need at least 70% of days.

**Windows:** (−1,+5), (+6,+20) and (+21,+60), which do not overlap. For NCR also (−1,+3), which ends on 22 Nov 2024, before the PSU rally of 25 Nov.

**NCR caveats**
- Event day 18 Nov 2024 is the first trading day under both the Stage III order (14 Nov, in force 15 Nov, a market holiday) and the Stage IV order.
- The re-imposition on 17 Dec 2024 is day +20.
- Stage III was in force again on 3–5 Jan, 9–12 Jan, 15–17 Jan and 29 Jan–3 Feb 2025, all inside (+21,+60) (`research/realign/grap_jan2025_orders.csv`). So (+21,+60) is not a clean post-event window.
- Adani group firms are not in any control or placebo set. ACC is flagged as contaminated for Step C: it fell 7.3% on 21 Nov 2024, the day of the Adani indictment.

**Gujarat caveats**
- Controls are matched by sub-industry first: fertiliser pool (Chambal, NFL, Paradeep) or specialty pool (Vinati, Clean Science, Sudarshan).
- A firm goes in the fertiliser pool if fertiliser plants are ≥ 25% of its plant cost in the pack: GSFC 50%, GNFC 29%, Zuari 100%.
- Size comes second. SRF, UPL, Kiri, Bodal and Zuari have no control within 0.5–2 times their market cap. They are kept, but they are not size-matched.
- The Vadodara footprint is defined by sites (any plant in Vadodara district): GSFC, Gujarat Alkalies, Bodal and Kiri.
  - Kiri is included under the same site rule; the user named only the first three.
  - Bodal: 11 of its 12 Vadodara sites had no usable night-light reading. The twelfth (plant 650, zero project cost in the pack) read dark on 30 Aug.

**DiD caveats**
- Only 2–3 exposed firms per NCR group, and few quarters with YoY growth.
- The unconfirmed builders' margins are extreme (distressed firms), so those coefficients are uninformative.
- statsmodels warned of a degenerate cluster variance in at least one regression.
- Read the DiD as descriptive.
