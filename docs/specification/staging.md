# Staging

Fase 4 (English: "Phase 4"; see [`methodology.md`](../methodology.md)), the data-integration phase, populates the warehouse from the source file. This part specifies the staging table, the transformations applied before the dimensions and the fact table are loaded, load order and transactions, and update policy.

## `staging_response`

| Column | Type | Role | Rule |
|--------|------|------|------|
| `response_id` | INT | primary key | surrogate; assigned after deduplication, in source-file order |
| `response_timestamp` | DATETIME | raw value | parsed from `Timestamp` per the format confirmed by check A12 (`%m/%d/%Y %H:%M`) |
| `gender` | VARCHAR(10) | raw value | matches [`dim_gender`](dimensions.md#dim_gender-dim_family_history-dim_occupation) |
| `country` | VARCHAR(50) | raw value | matches [`dim_country`](dimensions.md#dim_country) |
| `occupation` | VARCHAR(20) | raw value | matches [`dim_occupation`](dimensions.md#dim_gender-dim_family_history-dim_occupation) |
| `family_history` | VARCHAR(3) | raw value | matches [`dim_family_history`](dimensions.md#dim_gender-dim_family_history-dim_occupation) |
| `treatment` | VARCHAR(3) | raw value | matches [`fact_response.treatment`](fact-table.md#columns) |
| `days_indoors` | VARCHAR(25) | raw value | matches [`dim_isolation`](dimensions.md#dim_isolation) |
| `growing_stress` | VARCHAR(5) | raw value | matches [`dim_symptoms`](dimensions.md#dim_symptoms) |
| `mood_swings` | VARCHAR(10) | raw value | matches `dim_symptoms` |
| `coping_struggles` | VARCHAR(3) | raw value | matches `dim_symptoms` |
| `social_weakness` | VARCHAR(5) | raw value | matches `dim_symptoms` |
| `mental_health_interview` | VARCHAR(5) | raw value | matches [`dim_access`](dimensions.md#dim_access) |
| `care_options` | VARCHAR(10) | raw value | matches `dim_access` |

Types and domains for the thirteen modeled columns are [`sources.md`](sources.md#value-domains)'s; this table does not restate them. `staging_response` holds no column for the four unmodeled source columns ([`sources.md`](sources.md#column-map)) — they are read during extraction, used to compute the deduplication key below, and discarded before this table is populated.

### Row set

One row per record surviving deduplication: 290,051, from the 292,364-row source file ([ADR-0008](../decisions/0008-staging-deduplication-grain.md)).

## Extraction

The source file's 17 columns are read in full, including the four not modeled by this specification ([`sources.md`](sources.md#column-map)) — they are needed for the deduplication key, not for any dimension or the fact table.

## Cleaning and normalization

Trimming and case normalization are declared here, as [model conventions](definitions.md#model-conventions) requires, and applied before deduplication. Check A12 found no case or whitespace variant, and no NULL, empty, or whitespace-only value, in any of the thirteen modeled columns across the full source file: the rule currently changes no value. It stays declared for any future load the source file's own guarantees do not cover.

The four unmodeled columns are not cleaned or validated. They are read at extraction only to compute the deduplication key below, then discarded: no NULL or malformed value among them reaches a column this specification stores.

## Load rule

[`sources.md`](sources.md#load-rule)'s load rule governs the thirteen modeled columns: a NULL, or a value outside its documented domain, aborts the load; no row is dropped, defaulted, or recoded to fit. Check A12 found no violation in the audited source file, so the rule currently never fires; it is enforced on every load, not only the first.

## Deduplication

[ADR-0008](../decisions/0008-staging-deduplication-grain.md)'s decision: two raw rows are the same staged record only if they agree on all 17 source columns, `Timestamp` included. The first occurrence in source-file order is kept; later exact duplicates are dropped. This step runs after cleaning and before the four unmodeled columns are discarded, since the deduplication key needs them.

## `Timestamp` parsing

Parsed to `response_timestamp` as `%m/%d/%Y %H:%M`, the format check A12 confirmed against the full source file (0 unparsable values). `dim_time`'s `year` and `month` are derived from `response_timestamp` at dimension load, not stored twice.

## Load order and transactions

1. `staging_response`, from the cleaned, deduplicated extraction. One transaction; the load rule's abort applies to the whole staging load, not a single row.
2. The eight dimensions, each by `SELECT DISTINCT` on its [natural key](definitions.md#dimension-grain-rule) from `staging_response` ([row set](dimensions.md#row-set)). Independent of each other; any order. Each dimension load is its own transaction.
3. `fact_response`, last, joining `staging_response` to all eight dimensions on their natural keys ([invariant I2](fact-table.md#invariants)). One transaction; a foreign key that fails to resolve aborts the fact load, consistent with [invariant I3](fact-table.md#invariants).

A step that aborts leaves every table it would have written unchanged from before the run; nothing partial commits.

## Update policy

*Proposed; not yet confirmed.* A full reload: every run truncates and repopulates `staging_response`, the eight dimensions, and `fact_response` from the source file, rather than appending to what a previous run loaded.

The legacy report's argument for full reload — recalculating pre-aggregated percentages on any new row is expensive — does not apply here: [ADR-0007](../decisions/0007-person-grain-fact-table-and-dimension-grain-rule.md) stores no pre-aggregated value anywhere. The reason proposed instead: the source file is a fixed historical export with no documented collection methodology or update cadence ([ADR-0001](../decisions/0001-position-as-portfolio-project.md)), so there is no real incremental-arrival scenario to design against for this project. An incremental policy would need a defined mechanism for new data to arrive, which this project does not have; specifying one without that would be designing for a use case this project cannot exercise.

## More information

* Related: [ADR-0007](../decisions/0007-person-grain-fact-table-and-dimension-grain-rule.md) (fact grain), [ADR-0008](../decisions/0008-staging-deduplication-grain.md) (deduplication).
* Acceptance: [`acceptance.md`](acceptance.md), C11.