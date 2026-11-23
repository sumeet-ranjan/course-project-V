# Table 3: placebos (deliverable 3(iii)). How to read it

Built by `src/58_tables_dose_placebo.py`.
- **Files:** `table3_placebo.csv` (one row per test × event × window) and `table3_placebo_firms.csv` (each firm's CAR,
  with flags). The firm lists and the reasons for each exclusion are in `placebo_firms.csv` (from `src/45`).
- **Statistic:** the same CAR test as table 1, i.e. the equal-weighted mean CAR and, beside it, the median CAR.
  - Each has a two-sided p-value from the same statistic on 1,000 random event days.
  - The table also shows the share of firms whose own CAR has p < 0.05; about 5% is expected under the null.

**A. Unexposed, unlinked placebo firms.**
- **NCR:** 24 firms, none with an NCR plant or a candidate link. Mean CAR −1.3% to +2.3%, p = 0.30–0.83. Medians
  −3.0% to +1.2%. Between none and three firms are individually significant per window, against about one expected.
- **Gujarat:** the list was approved with changes at the checkpoint-4 review (23 Nov 2026).
  - **Reliance Power dropped.** It fell 20.7% abnormal over (−1,+5) after SEBI's final order of 22 Aug 2024 against
    Anil Ambani. The stock fell 5.0% on each of 23, 26 and 27 Aug, the size of a lower circuit
    (`research/realign/news_checks.csv`).
  - **With Reliance Power,** the mean was −4.9% and the median −2.4%.
  - **Without it (12 firms):** mean −3.6% (p = 0.21), median −2.1% (p = 0.43) over (−1,+5); nulls in the later windows.
  - **Unitech's −16.7%** is half model artefact. Its raw return was −9.6%. The market model expected +7.1%, because its
    estimation-window alpha is +0.85% a day (its 2024 rally). The median is reported for this reason.
  - **Tata Steel is flagged as a Tata group firm.** It shares a chairman with Tata Chemicals, and Tata Chemicals holds
    0.25% of it (Rs 477 cr). No supply link was found. Tata group news on 10 Oct and 21 Oct 2024 falls inside its
    (+21,+60) window.
  - **Re-screen against the external hit firms** (`research/realign/gj_placebo_rescreen.csv`):
    - No placebo firm is named in Tata Chemicals' FY2024-25 annual report as a customer. Archean names no customers.
    - The FY2023-24 annual reports of Indo Rama, MRPL, Rajesh Exports, Unitech and Vardhman Holdings do not mention
      Tata Chemicals, Archean, soda ash, bromine or sulphate of potash.
    - The own reports of Jindal Steel & Power, Jindal Stainless, Lodha, NBCC, SAIL and NMDC were not read: the
      re-screen was stopped, and NMDC's report did not load.
    - No firm was excluded on this check.

**B. G2 control firms.**
- **NCR developers with no NCR project (8 firms):** nulls, p ≥ 0.17.
- **Gujarat fertiliser and specialty firms with no Gujarat plant (6 firms):** −4.7% mean (p = 0.10) and −5.2% median
  (p = 0.07) over (−1,+5).
  - All six fell: Paradeep −7.9%, NFL −6.6%, Clean Science −6.1%, Sudarshan −4.2%, Vinati −1.9%, Chambal −1.5%.
  - No single firm drives it, and its cause is not identified.
  - It is the benchmark of the Gujarat direct test, so part of the pack belt's +5.5 pp (wrong sign) is the controls'
    own fall.

**C. Unlinked comparison contractors (zero dose, 5 firms).**
- Nulls, except 16–24 Dec 2024 (17 Dec (−1,+5)): +5.5% mean (p = 0.07) and +6.3% median (p = 0.05).
  - The rise is led by Capacit'e (+12.1%), PSP (+7.3%) and Cemindia (+6.3%). Its cause was not checked.
  - It inflates Ahluwalia's net figure for that window (−6.6%, p = 0.27), which is not used as evidence.
