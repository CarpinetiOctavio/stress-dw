# Query patterns and reporting rules

Sixteen indicators are parameter sets of three patterns. The terms used here (population, cuts, cell, numerator, denominator, period) are defined in the [query vocabulary](definitions.md#query-vocabulary); [`indicators.md`](indicators.md) gives each indicator's parameters.

## Output columns

Every output row carries the cut values; `level` (patterns A and C only); `numerator`; `denominator`; `rate`; and `low_n`. The rules for `rate` and `low_n` are under [Reporting rules](#reporting-rules).

## Pattern A — level distribution

Parameters: population P; variable V (a stored categorical attribute); cuts K.

One output row per cell and per level of V. `numerator` is the number of rows in the cell with V equal to the level; `denominator` is the number of rows in the cell. Every level of V that occurs in P appears in every cell; a level with no rows in a cell has `numerator` 0.

Invariants: within a cell, the numerators over all levels sum to the denominator; the cell denominators, each counted once, sum to the size of P.

## Pattern B — conjunction share

Parameters: population P; condition C (a conjunction of tests on stored attributes); cuts K.

One output row per cell. `numerator` is the number of rows in the cell that satisfy C; `denominator` is the number of rows in the cell.

Invariants: the cell denominators sum to the size of P; the cell numerators sum to the number of rows in P that satisfy C.

Where the cuts name both country and region, two grouping sets are produced: {occupation, country} and {occupation, region}. The region-level numerators and denominators are sums over the countries of the region ([roll-up rule](definitions.md#roll-up-rule)).

## Pattern C — lifetime treatment share

Pattern A with V = `treatment`. Both levels are reported: the `Yes` row is the lifetime treatment-seeking share, and the `No` row is its complement. The pattern is named separately because indicators 14 to 16 define P and K through derived conditions.

Indicators 14, 15 and 16 use [`symptom_cluster`](definitions.md#symptom_cluster); see its validity caveat.

## Cross-indicator consistency

* For each count/rate pair (1–2, 3–4, 5–6, 8–7, 13–12), the count indicator equals the numerator of the rate indicator's cells, summed to the count indicator's cuts.
* Indicator 16, summed over `mental_health_interview`, equals indicator 15 cell by cell, numerator and denominator.

## Reporting rules

* **Rate.** `rate` = `numerator` / `denominator`. It is NULL, never 0, when `denominator` is 0. A zero denominator arises only when cells are materialized by a cross join over cut domains, since cells are otherwise formed from rows present in the population.
* **Low-count flag.** `low_n` is true when `denominator` is below `low_n_threshold`, a parameter of the query layer whose default is 30. The default is a rule-of-thumb convention with no validated source in this project: it flags instability and is not a validity threshold. No row is suppressed in SQL; whether to show or hide flagged cells is decided by the reporting layer. Numerators are not flagged.
* **Names.** Outputs carry the indicator names of [`indicators.md`](indicators.md). They are not relabeled with words that [writing conventions, rule 5](../writing-conventions.md#5-names-claim-only-what-the-data-supports) excludes.
* **`symptom_cluster`.** Any output that uses [`symptom_cluster`](definitions.md#symptom_cluster) is accompanied by the caveat written in its definition.
* **Cross-column-group results.** Results that cross a column the source describes with a symptom column are subject to the pending checks on the source's provenance ([conceptual framework, section 7](../conceptual-framework.md#7-threats-to-validity); checks A5, A6 and A10 of the [legacy audit](../audit/legacy-audit.md)).
* **Status of results.** Every output is an output of a methodological test bench ([ADR-0001](../decisions/0001-position-as-portfolio-project.md)); none is stated as prevalence or as a treatment gap in any population.
