# Phase 4 closure

## 1. Status

Fase 4 (English: "Phase 4"; see [`methodology.md`](../methodology.md)), Data Integration, is closed for this rebuild as of commit `9f31ab0`. The pipeline specified in [`staging.md`](../specification/staging.md) populates `staging_response`, the eight dimensions, and `fact_response`, and the query layer computes the sixteen indicators of [`indicators.md`](../specification/indicators.md). Acceptance checks C1–C11 of [`acceptance.md`](../specification/acceptance.md) are automated and pass against the SHA-256-verified source file. This is not the legacy project's Phase 4: the engine is DuckDB, not MySQL ([ADR-0009](../decisions/0009-use-duckdb-as-database-engine.md)), and the pipeline was rebuilt from scratch rather than continued ([ADR-0000](../decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md)).

## 2. Reproducing this

The source file is not versioned. How to obtain it, and why it is not in the repository, is in [`staging.md`](../specification/staging.md#extraction). It is expected at `data/raw/mental_health.csv`, with SHA-256 `083f44e9cdf84f56abf08b9fa1862d80b87237afa74e2cacc9328a63d9291686`. The pipeline aborts on any other file.

From the repository root:

```
uv sync
uv run python -m stress_dw.pipeline   # full reload into data/stress_dw.duckdb; prints the counts of section 3
uv run pytest                         # 195 passed with the source file present
```

Without the source file, `uv run pytest` reports 101 passed and 94 skipped. The skipped tests are the acceptance checks, which need the real file; a skip is not a pass.

Verified against commit `9f31ab0`, from an empty database file.

## 3. Pipeline results

| Stage | Rows |
|-------|------|
| Source file | 292,364 |
| Removed as exact duplicates on all 17 source columns ([ADR-0008](../decisions/0008-staging-deduplication-grain.md)) | 2,313 |
| `staging_response` | 290,051 |
| `fact_response` | 290,051 |

| Dimension | Rows | |
|-----------|------|---|
| `dim_time` | 13 | |
| `dim_gender` | 2 | |
| `dim_family_history` | 2 | |
| `dim_occupation` | 5 | |
| `dim_country` | 35 | |
| `dim_isolation` | 5 | |
| `dim_access` | 9 | at its [ceiling](../specification/dimensions.md#row-set) |
| `dim_symptoms` | 54 | at its [ceiling](../specification/dimensions.md#row-set) |

Calendar months within the staged range (2014-08 to 2016-02) with no staged record, and so no `dim_time` row: 2015-01, 2015-03, 2015-10, 2015-11, 2015-12, 2016-01. The load report lists them as information, not as a failure ([`dimensions.md`](../specification/dimensions.md#dim_time)).

## 4. Acceptance checks C1–C11

Each check is defined in [`acceptance.md`](../specification/acceptance.md); this table only maps it to the tests that implement it. Tests are in `tests/test_acceptance.py` unless noted; the number in parentheses is the count of parametrized cases.

| Check | Verifies | Tests | Status |
|-------|----------|-------|--------|
| C1 | Each dimension is unique on its natural key and matches staging grouped by it | `test_c1_the_dimension_is_unique_on_its_natural_key` (8), `test_c1_grouping_staging_by_the_natural_key_yields_the_dimension_row_set` (8) | Pass |
| C2 | Staging joined to the eight dimensions multiplies no rows | `test_c2_joining_staging_to_the_eight_dimensions_multiplies_no_rows` | Pass |
| C3 | `fact_response` reconciles with staging: row count and `response_id` set | `test_c3_fact_response_reconciles_with_staging` | Pass |
| C4 | Every table has exactly the specified columns and types | `tests/test_schema.py::test_table_has_exactly_the_specified_columns_and_types` (10), against the schema DDL; `test_c4_the_built_table_has_exactly_the_specified_columns_and_types` (10), against the database the pipeline builds | Pass |
| C5 | The eight foreign keys exist, are enforced, and leave no orphan | `test_c5_the_eight_foreign_keys_exist_with_the_specified_names`, `test_c5_the_foreign_keys_are_enforced`, `test_c5_no_fact_row_is_orphaned` (8) | Pass |
| C6 | Every staged country is in the mapping; `dim_country` has one row per staged country | `test_c6_every_staged_country_is_in_the_mapping`, `test_c6_dim_country_has_one_row_per_staged_country_at_most_35` | Pass |
| C7 | Every dimension row is referenced by a fact row | `test_c7_every_dimension_row_is_referenced_by_a_fact_row` (8) | Pass |
| C8 | Cell denominators sum to each indicator's population, counted from staging; the pattern invariants hold | `test_c8_cell_denominators_sum_to_the_population_counted_from_staging` (16), `test_c8_pattern_a_numerators_sum_to_the_cell_denominator` (13), `test_c8_pattern_b_numerators_sum_to_the_rows_satisfying_the_condition` (2), `test_c8_region_cells_are_sums_over_their_countries` (2) | Pass |
| C9 | Cross-indicator consistency | `test_c9_the_count_indicator_equals_the_rate_indicators_numerators` (4), `test_c9_indicator_8_equals_the_yes_numerators_of_indicator_7`, `test_c9_indicator_16_summed_over_mental_health_interview_equals_indicator_15` | Pass |
| C10 | `explicit_recognition` and `symptom_cluster` select the same rows through the dimensions as from staging | `test_c10_both_paths_count_the_same_rows` (2), `test_c10_both_paths_select_the_same_response_ids` (2) | Pass |
| C11 | Staging holds 290,051 rows, and every removed row is a 17-column duplicate of a kept one | `test_c11_staging_holds_290051_rows`, `test_c11_the_source_file_has_292364_rows_and_290051_distinct_ones`, `test_c11_every_removed_row_is_a_17_column_duplicate_of_a_kept_row` | Pass |

## 5. Decisions

Every decision record is indexed in [`decisions/README.md`](../decisions/README.md). Three govern this phase directly:

* [ADR-0008](../decisions/0008-staging-deduplication-grain.md): what counts as one staged record.
* [ADR-0009](../decisions/0009-use-duckdb-as-database-engine.md): the database engine, including finding E3.
* [ADR-0010](../decisions/0010-reload-dimensions-and-fact-in-one-transaction.md): how the dimensions and the fact table are reloaded.

## 6. Explicitly out of scope

**Reporting layer.** Not built. Whether a cell flagged by `low_n` is shown or hidden is a decision assigned to the reporting layer, not made here ([`patterns.md`](../specification/patterns.md#reporting-rules)). The cross-column-group caveat carries the same deferral: which columns count as "described by the source" depends on [conceptual framework, section 7](../conceptual-framework.md#7-threats-to-validity) and on checks A5, A6, and A10 below, so the caveat's presentation is left to the reporting layer as well.

**Legacy-audit checks still Pending.** [`legacy-audit.md`](legacy-audit.md) has the full method and result for each.

| ID | Why it is still open | Effect on this rebuild |
|----|----------------------|------------------------|
| A2 | The mechanism is established at the documented-schema level (F1, [ADR-0000](../decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md)); the group counts that would quantify the `Dim_Sintomas` (English: "symptoms dimension") fan-out against the legacy database have not been computed. | None: audits why the legacy was discarded. |
| A3 | The fact table's actual foreign-key name for occupation has not been read from the legacy DDL. | None: audits the legacy schema. |
| A5 | Cramér's V between the dataset's documented-provenance columns and its symptom columns has not been computed; with A6, one of the two checks of hypothesis H1 ([ADR-0001](../decisions/0001-position-as-portfolio-project.md)). | No numeric effect. Conditions how cross-column-group results are interpreted; deferred to the reporting layer. |
| A6 | The `Timestamp` distribution has not been compared against the OSMI 2014 survey's own distribution; the other of the two checks of hypothesis H1. | Same as A5. |
| A7 | The treatment rate by gender has not been recomputed from staging with an explicit numerator and denominator, and compared with the unweighted `AVG` of the legacy chart (F2). | None: audits the legacy chart. |
| A9 | The implementation of `indicador_inferido_estres` (English: "inferred stress indicator") in the legacy ETL has not been read and diffed against the documented Fase 2 formula. | None: audits the legacy script. |
| A10 | The eight shared symptom columns have not been compared against RHMCD-20 for row-level or marginal-distribution matches (H3). | No numeric effect. Same deferral as A5 and A6. |
| A11 | 2 of the 35 entries (Mexico, Georgia) were verified directly against UNSD M49 ([`country-region-mapping.md`](../specification/country-region-mapping.md)); the other 33 are pending. | Affects stored data: `dim_country.region` is assigned from this mapping. A discrepancy among the remaining 33 would change indicators 5 and 6 at the region level. |

## 7. Verification

Fase 4's pipeline and full test suite were executed against the SHA-256-verified dataset, producing the results in section 3 and the C1–C11 statuses in section 4. Separately, a read-only review of the public repository re-ran the lint, type, and test tooling without the dataset, reproduced the merge conflicts noted during PR sequencing, and cross-checked the query-layer SQL against [`indicators.md`](../specification/indicators.md), [`patterns.md`](../specification/patterns.md), and [`definitions.md`](../specification/definitions.md).
