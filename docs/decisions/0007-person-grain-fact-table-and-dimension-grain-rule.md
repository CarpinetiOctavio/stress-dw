---
status: "accepted"
date: 2026-09-24
decision-makers: Octavio Carpineti
---

# Model the fact table at person grain, bound dimensions by a grain rule, and derive conditions at query time

## Context and Problem Statement

The legacy model ([ADR-0000](0000-rebuild-from-scratch-instead-of-continuing-legacy.md)) stored an aggregated fact table: one row per combination of the eight dimensions, holding pre-computed percentages. Its symptoms dimension, `Dim_Sintomas` (English: "symptoms dimension"), carried a derived column, `indicador_inferido_estres` (English: "inferred stress indicator"), whose formula depends on `days_indoors`, a value that dimension does not store. F1 records this mechanism and the report's own figures (350,699 fact rows from 290,051 staged records); its quantification against the database is pending (A2). F2 records that the fact table stores percentages without numerators or denominators, so they cannot be re-aggregated correctly.

ADR-0000 decided to rebuild on a corrected written specification and named three lessons to carry over: model `treatment` as a measure, store additive measures, and state the grain explicitly. It did not decide the grain itself, what a dimension may store, or where a condition that spans dimensions lives. [ADR-0003](0003-redefine-indicators-14-to-16.md) left one of these open for the specification: whether the derived column needs to exist in the symptoms dimension at all.

Which grain should the fact table have, what may a dimension store, and where should derived conditions live?

## Findings

No new finding IDs are introduced here; both rows cite evidence already established in ADR-0000.

| ID | Finding | Evidence | Status |
|----|---------|----------|--------|
| F1 | A dimension column depends on a value the dimension does not store; the join from staging to that dimension is ambiguous and the fact load multiplies rows. | ADR-0000, Findings | Established at documented-schema level; quantification pending (A2) |
| F2 | The fact table stores pre-aggregated ratios without numerators or denominators; the report's sample query averages them. | ADR-0000, Findings | Established |

## Decision Drivers

* F1's mechanism: when a dimension's stored columns do not determine one of its own columns, one combination of stored values can require different derived values. Whatever rule prevents this must be checkable on the dimension alone, without looking at the fact table.
* F2: an average of stored ratios is invalid when the groups differ in size. Ratios must be computable from a numerator and a denominator, so the fact table must retain what is needed to count.
* ADR-0000's Confirmation requires the fact table to reconcile with staging. A fact table with one row per staged record reconciles by comparing two counts; an aggregated one reconciles only by reconstructing the aggregation.
* The model has a single measure, `treatment`, a categorical value. At person grain every count is a row count, and no numeric measure exists that an aggregation would have to preserve.
* A condition can span dimensions. The three-symptom cluster uses `mood_swings` and `coping_struggles` from the symptoms dimension and `days_indoors` from the isolation dimension, so it is a function of neither dimension's key alone.
* The two components of the legacy flag are used separately, as cuts and, for `symptom_cluster`, as the population of indicator 14. Their union appears only as the population predicate of indicators 15 and 16, computed from the two components at query time ([ADR-0003](0003-redefine-indicators-14-to-16.md), [ADR-0006](0006-final-questions-and-indicators.md)). No indicator needs the union stored as a column.
* The cluster's threshold has no external validation ([conceptual framework, section 7](../conceptual-framework.md#7-threats-to-validity)). It is a declared heuristic that may need to change.


## Considered Options

* Keep the legacy design: an aggregated fact table, with the derived flag stored in the symptoms dimension.
* Correct the legacy design minimally: keep the aggregated fact table and the stored flag, and add `days_indoors` to the symptoms dimension so the flag becomes a function of its key.
* Person-grain fact table; dimensions bound by a grain rule; derived conditions computed at query time and stored nowhere.


## Decision Outcome

Chosen option: "Person-grain fact table; dimensions bound by a grain rule; derived conditions computed at query time and stored nowhere", because it is the only option that removes the mechanism behind F1 and the cause of F2 together, without adding a second copy of any value.

* **Fact grain.** One row per staged record. The single measure is `treatment`, stored as its raw categorical value. The row's identifier is the staged record's, so each fact row traces to its source row.
* **Dimension grain rule.** Every column stored in a dimension is a pure function of that dimension's natural key. The normative text is the [dimension grain rule](../specification/definitions.md#dimension-grain-rule).
* **The symptoms dimension.** It stores the four symptom columns and no derived column. `days_indoors` lives only in the isolation dimension and is not duplicated.
* **Derived conditions.** `explicit_recognition` and `symptom_cluster` are computed at query time, across dimensions, through the fact row. The legacy flag has no successor column. Their definitions are in [`definitions.md`](../specification/definitions.md).

### Consequences

* Good, because F1 cannot recur by construction: the grain rule is checkable per dimension (group staging by natural key and expect one dimension row per group), and the join from staging to the dimensions multiplies no rows.
* Good, because F2 cannot recur: nothing pre-aggregated is stored, every rate is a numerator over a denominator computed from rows, and a coarser cut sums numerators and denominators.
* Good, because reconciliation with staging is a count comparison, and each fact row traces to its source row.
* Good, because the cluster's threshold is written in one definition; changing it is a change to a query, not a reload.
* Bad, because every indicator is computed at query time. The cost at the volume of the legacy staging (290,051 records) has not been measured; that it is negligible is an assumption to check once the pipeline exists.
* Bad, because a condition spanning two dimensions is a column of neither. A consumer that cannot join, such as a BI tool reading a single table, needs a view or a custom query. The consumption layer of the rebuild is not yet specified.
* Constraint: a new dimension attribute must satisfy the grain rule, and a new measure must be additive per row.
* Constraint: an indicator that needs a condition across dimensions defines it in [`definitions.md`](../specification/definitions.md), not as a stored column.

### Confirmation

[`acceptance.md`](../specification/acceptance.md) holds the checks: natural-key uniqueness per dimension (C1), a join from staging to the dimensions that multiplies no rows (C2), reconciliation of the fact table with staging (C3), a schema with no stored ratio or derived condition (C4), and agreement between each derived condition computed through the dimensions and computed directly from staging (C10). A post-build audit records their queries and counts.

## Pros and Cons of the Options

### Keep the legacy design

* Good, because nothing already built changes.
* Bad, because it preserves the mechanism behind F1 and the pre-aggregated ratios behind F2.

### Correct the legacy design minimally

* Good, because it is the smallest change, and the flag becomes a function of its key, which removes F1's mechanism.
* Bad, because the ceiling of the symptoms dimension rises from 54 to 270 combinations (ADR-0000, F1) and `days_indoors` is stored in two dimensions: two homes for one value.
* Bad, because the aggregated fact table still stores ratios (F2) unless the fact grain changes too.
* Bad, because it keeps a stored flag whose only use, as the population predicate of indicators 15 and 16, a query computes from its two components.

### Person-grain fact table, conditions at query time

* Good, because it removes both F1's mechanism and F2's cause, and needs no second copy of any value.
* Bad, because of the query-time cost and the consumption-layer constraint listed under Consequences.


## More Information

* Related: [ADR-0000](0000-rebuild-from-scratch-instead-of-continuing-legacy.md) (F1, F2, lessons to carry over), [ADR-0003](0003-redefine-indicators-14-to-16.md) (the flag's existence left to the specification), [ADR-0006](0006-final-questions-and-indicators.md).
* [`conceptual-framework.md`](../conceptual-framework.md), section 7.
* The contract that implements this decision: [`docs/specification.md`](../specification.md), in particular [`dimensions.md`](../specification/dimensions.md) and [`fact-table.md`](../specification/fact-table.md).
