# Definitions shared across the specification

Concepts used in more than one part of the specification are defined here, once. Every other part links to the definition it needs instead of restating it ([writing conventions, rule 4](../writing-conventions.md#4-introduce-before-use-one-home-per-concept)).

## Model conventions

**Identifiers.** English `snake_case`. Dimension tables are `dim_<name>`; the fact table is `fact_response`. Each dimension's surrogate primary key is `<name>_id` (`time_id`, `gender_id`, and so on), and the fact table's foreign key to it has the same name. Surrogate keys are assigned by the load and carry no meaning.

**Stored values.** A dimension attribute that holds a source value holds the source literal, unrecoded and untranslated. Any normalization (trimming, case) is declared in the data-integration phase, "Fase 4" (English: "Phase 4"; see [`methodology.md`](../methodology.md)), and applied before the dimensions are loaded.

**Nothing derived is stored beyond dimension attributes.** No table stores a ratio, a percentage, a pre-aggregated count, or a derived condition ([`explicit_recognition`](#explicit_recognition), [`symptom_cluster`](#symptom_cluster)). Every indicator is computed at query time from `fact_response` and the dimensions. A dimension may store a derived column, such as `region` in `dim_country`, because it is a pure function of that dimension's natural key ([dimension grain rule](#dimension-grain-rule)).

## Dimension grain rule

The *natural key* of a dimension is the set of source values that identifies one of its rows; [`dimensions.md`](dimensions.md) declares it for each dimension. Every column stored in a dimension is a pure function of that dimension's natural key. A dimension stores no column that depends on a value the dimension does not itself hold. A natural-key value therefore maps to exactly one dimension row. The reasoning is in [ADR-0007](../decisions/0007-person-grain-fact-table-and-dimension-grain-rule.md).

## Multi-level self-report rule

Every level of a multi-level self-report variable is reported as its own value: `growing_stress`, `social_weakness` and `mental_health_interview` ("Yes" / "No" / "Maybe"), and `care_options` ("Yes" / "No" / "Not sure"). No indicator merges "Maybe" or "Not sure" into another level. Three definitions in the specification are not folds of an ambiguous value:

* Indicators 5 and 6 count the joint condition `growing_stress = 'Yes' AND coping_struggles = 'Yes'` (documented exception, [ADR-0005](../decisions/0005-redefine-indicators-1-to-13.md), Decision Drivers).
* Indicator 10's headline cut `mood_swings IN ('Medium','High')` is a threshold on an ordinal scale.
* Indicators 15 and 16 restrict the [population](#query-vocabulary) to `care_options IN ('Yes','Not sure')`. This is a declared population filter; the two retained levels stay separate.

## Query vocabulary

* **Population**: the set of `fact_response` rows an indicator ranges over, written as a predicate over the fact row and its dimensions.
* **Cuts**: the dimension attributes or derived conditions that partition the population into cells. An empty list of cuts yields one cell.
* **Cell**: one combination of cut values that occurs in the population.
* **Denominator**: the number of population rows in the cell.
* **Numerator**: the number of those rows that meet the indicator's measure.
* **Period**: "month" in a cut means the (`year`, `month`) pair of [`dim_time`](dimensions.md#dim_time), reported as `period`.

A count indicator and its rate counterpart are the same cell: the count is the numerator column; the rate is numerator / denominator.

## Roll-up rule

A coarser cut is computed by summing the [numerators and the denominators](#query-vocabulary) of finer cells. Averaging rates across cells is not permitted.

## `explicit_recognition`

```sql
dim_symptoms.growing_stress = 'Yes'
```

`'Maybe'` and `'No'` are outside this condition. An indicator that reports `growing_stress` by level uses the three levels directly, not this condition. The condition is derived at query time and stored nowhere.

## `symptom_cluster`

```sql
dim_symptoms.mood_swings IN ('Medium','High')
AND dim_symptoms.coping_struggles = 'Yes'
AND dim_isolation.days_indoors IN ('15-30 days','31-60 days','More than 2 months')
```

The condition spans two dimensions and is evaluated per `fact_response` row, through `symptoms_id` and `isolation_id`. It is derived at query time and stored nowhere.

> **Validity caveat.** The convergence threshold of `symptom_cluster` has no external clinical validation. It is a declared heuristic over self-report items, not a validated measure, and it identifies a self-reported profile, not evaluated need or a clinical state.
