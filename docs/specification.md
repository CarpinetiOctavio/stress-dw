# Pipeline specification

This document specifies the implementation contract for the pipeline: dimension grains, the fact table schema, and each indicator's population, measure, and cuts. It states the *what*, not the *why*. For the reasoning behind these decisions — audit findings, rejected alternatives, corrected variable semantics, literature grounding — see the ADRs (`docs/decisions/`) and `docs/conceptual-framework.md`; this document does not repeat their content.

The specification is split into parts so that each can be read for one task. A concept used in more than one part is defined once, in [`definitions.md`](specification/definitions.md), and every other part links to it ([writing conventions, rule 4](writing-conventions.md#4-introduce-before-use-one-home-per-concept)).

## Parts

| Part | Holds | Read it for |
|------|-------|-------------|
| [`definitions.md`](specification/definitions.md) | The [model conventions](specification/definitions.md#model-conventions), the [dimension grain rule](specification/definitions.md#dimension-grain-rule), the [multi-level self-report rule](specification/definitions.md#multi-level-self-report-rule), the [query vocabulary](specification/definitions.md#query-vocabulary), the [roll-up rule](specification/definitions.md#roll-up-rule), and the derived conditions [`explicit_recognition`](specification/definitions.md#explicit_recognition) and [`symptom_cluster`](specification/definitions.md#symptom_cluster) | any task; read first |
| [`sources.md`](specification/sources.md) | The 17 source columns, which 13 are modeled, and their documented value domains | staging profile, domain checks |
| [`staging.md`](specification/staging.md) | The data-integration pipeline: the staging table, extraction, cleaning and normalization, the application of the load rule, deduplication, `Timestamp` parsing, load order and transactions, update policy | staging and load |
| [`dimensions.md`](specification/dimensions.md) | The eight dimensions: [natural keys](specification/definitions.md#dimension-grain-rule), columns, derivations, row sets | dimension DDL and load |
| [`country-region-mapping.md`](specification/country-region-mapping.md) | The fixed country-to-region mapping used by `dim_country` | `dim_country` load |
| [`fact-table.md`](specification/fact-table.md) | `fact_response`: columns, grain, invariants | fact DDL and load |
| [`patterns.md`](specification/patterns.md) | The three query patterns and the reporting rules | query and view layer |
| [`indicators.md`](specification/indicators.md) | The sixteen indicators, grouped by business question | query and view layer |
| [`acceptance.md`](specification/acceptance.md) | The acceptance criteria, each tied to the finding it closes | tests and the post-build audit |

## Phases

"Fase N" (English: "Phase N") denotes the Nth phase of the Hefesto methodology; [`methodology.md`](methodology.md) maps the four phases. The data-integration phase, Fase 4, is specified in [`staging.md`](specification/staging.md): staging structure, cleaning, deduplication, normalization, `Timestamp` parsing, load order and transactions, and update policy. Its status is recorded in the [closure record](audit/phase4-closure.md#1-status). The deduplication rule is [ADR-0008](decisions/0008-staging-deduplication-grain.md)'s decision ([`staging.md`, Deduplication](specification/staging.md#deduplication)), and the staged and raw row counts are in [its row set](specification/staging.md#row-set).

## Open items and dependencies

* **Checks that may amend this specification.** A8, A11 and A12 (the `dim_time` and `dim_country` row sets, the [country-to-region mapping](specification/country-region-mapping.md), the [value domains](specification/sources.md#value-domains)) and A5, A6, A10 (the validity of results that cross the two groups of source columns). The status and result of each are in the [audit table](audit/legacy-audit.md#checks).
* **Code conventions.** Style, linting, naming beyond the [model conventions](specification/definitions.md#model-conventions), docstrings and test structure are set in [`code-conventions.md`](code-conventions.md).
