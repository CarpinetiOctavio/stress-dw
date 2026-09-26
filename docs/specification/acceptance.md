# Acceptance criteria

Each check runs as a query against the built database and staging; a post-build audit records queries and counts, not descriptions. Population, cell, numerator and denominator are used as in the [query vocabulary](definitions.md#query-vocabulary). F1, F2 and F4 are findings of [ADR-0000](../decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md).

| ID | Check | Closes |
|----|-------|--------|
| C1 | Each dimension has a unique constraint on its natural key ([dimension grain rule](definitions.md#dimension-grain-rule)), and grouping staging by that key yields exactly the dimension's row set | F1; [ADR-0007](../decisions/0007-person-grain-fact-table-and-dimension-grain-rule.md) |
| C2 | Staging joined to the eight dimensions on natural keys returns as many rows as staging ([I2](fact-table.md#invariants)) | F1; ADR-0007 |
| C3 | `fact_response` reconciles with staging: row count and `response_id` set ([I1](fact-table.md#invariants)) | ADR-0000, Confirmation; ADR-0007 |
| C4 | Schema introspection: `fact_response` has exactly the columns of [`fact-table.md`](fact-table.md#columns), and no column in any table stores a ratio, a percentage, a count, or a derived condition | F2; ADR-0007 |
| C5 | The eight foreign keys exist with the names of [`fact-table.md`](fact-table.md#columns), are enforced, and have no orphan rows ([I3](fact-table.md#invariants)) | F4 |
| C6 | Every staged country is in the [country-to-region mapping](country-region-mapping.md); `dim_country` has as many rows as distinct staged countries, at most 35 | F4 |
| C7 | Every dimension row is referenced by at least one fact row | — |
| C8 | For each indicator, the cell denominators, each counted once, sum to an independent `COUNT(*)` of the indicator's population as defined in [`indicators.md`](indicators.md); the per-pattern invariants of [`patterns.md`](patterns.md) hold | [ADR-0003](../decisions/0003-redefine-indicators-14-to-16.md) and [ADR-0005](../decisions/0005-redefine-indicators-1-to-13.md), Confirmation |
| C9 | The [cross-indicator consistency](patterns.md#cross-indicator-consistency) rules hold | ADR-0003, Confirmation |
| C10 | The row counts of [`explicit_recognition`](definitions.md#explicit_recognition) and [`symptom_cluster`](definitions.md#symptom_cluster), computed through the dimensions, equal the counts computed directly from staging columns without dimension joins | ADR-0007 |
| C11 | `staging_response`'s row count is 290,051, and every row removed during load is an exact duplicate — on all 17 source columns — of a row that was kept | [ADR-0008](../decisions/0008-staging-deduplication-grain.md) |
