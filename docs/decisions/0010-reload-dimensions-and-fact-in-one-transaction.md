---
status: "accepted"
date: 2026-09-27
decision-makers: Octavio Carpineti
---

# Reload the eight dimensions and the fact table in one transaction

## Context and Problem Statement

[`staging.md`](../specification/staging.md)'s update policy is a full reload: every run replaces the contents of `staging_response`, the eight dimensions, and `fact_response`. Its load order gave each dimension load its own transaction, and the fact load another, and required that a step that aborts leave every table it would have written unchanged. From the second run onward, `fact_response` holds rows that reference every dimension, so a dimension cannot be emptied until those rows are gone. Under DuckDB ([ADR-0009](0009-use-duckdb-as-database-engine.md)), that cannot be done inside a single transaction by deleting rows (E3). How should the dimensions and the fact table be reloaded so that the reload succeeds and an aborted run leaves nothing partial?

## Findings

Both rows are [ADR-0009](0009-use-duckdb-as-database-engine.md)'s, cited here, not restated; E3 was added to that ADR as the evidence for this one.

| ID | Finding | Evidence | Status |
|----|---------|----------|--------|
| E1 | DuckDB's documented constraint limitations were judged not to apply to an insert-only load. | [ADR-0009](0009-use-duckdb-as-database-engine.md#findings) | Established |
| E3 | Deleting `fact_response` rows and then the dimension rows they referenced, in one transaction, fails on the foreign key, with `DELETE` and `TRUNCATE` alike. Dropping, recreating, and reloading the nine tables in one transaction succeeds, and a forced failure inside it rolls back rows, tables, and foreign keys entirely. | [ADR-0009](0009-use-duckdb-as-database-engine.md#findings) | Established |

---

### Addendum (2026-10-04)
E1, as cited here ("judged not to apply to an insert-only load"), is restated in [ADR-0009's addendum of 2026-10-02](0009-use-duckdb-as-database-engine.md#addendum-2026-10-02): its premise is that the pipeline issues no `UPDATE`; enforcement on insert rests on the captured documentation and enforcement on delete on E3; acceptance check C5 tests foreign-key enforcement on the database the pipeline builds. This record rests on E3, which is unchanged.

---

### Addendum (2026-10-06)
The addendum of 2026-10-04 carries the decision of [LOG-022](log/LOG-022-adr-0010-0013-addenda.md), which keeps its reasoning.

---

## Decision Drivers

* The full reload must work on every run, not only the first: from the second run on, `fact_response` references every dimension row (E3).
* [`staging.md`](../specification/staging.md#load-order-and-transactions)'s own requirement: a step that aborts leaves every table it would have written unchanged; nothing partial commits.
* A failed run should leave the warehouse queryable in its previous state, not empty.
* The atomicity should come from the engine's own transactions, the principle behind ADR-0009's choice of an engine that enforces what the pipeline relies on, rather than from machinery the application adds around it.
* Independent of the foreign-key failure: with one transaction per dimension, a failure in the third of eight dimension loads leaves the first two holding this run's data and the other six the previous run's. The load order did nothing to prevent that mixed state.

## Considered Options

* One transaction for the eight dimensions and `fact_response`: drop the nine tables, recreate them from their DDL, and reload them.
* An explicit step that empties `fact_response` in its own transaction before the dimensions are reloaded.
* Build the warehouse in a new `.duckdb` file and replace the previous file only when the run succeeds.

## Decision Outcome

Chosen option: "One transaction for the eight dimensions and `fact_response`", because it is the only option that makes the reload succeed on every run (E3) while keeping an aborted run's previous state intact, and it does so with DuckDB's own transactional DDL, which E3 confirms rolls back dropped and recreated tables completely.

`staging_response` keeps its own transaction, unchanged: no table references it through a foreign key, so E3 does not reach it.

### Consequences

* Good, because the full reload succeeds from the second run onward, which per-table transactions cannot do under DuckDB (E3).
* Good, because an aborted run leaves the eight dimensions and `fact_response` exactly as the previous run left them: queryable, and consistent with one another.
* Good, because it also removes the mixed state across dimensions that one transaction per dimension allowed, not only the foreign-key failure.
* Bad, because the transaction holds the nine tables' old and new contents at once until it commits; at this warehouse's size (290,051 staged records) that is not a constraint, but it would become one at a much larger volume.
* Bad, because a failure anywhere in the step discards the work of every dimension already loaded in it; a rerun starts the step over.
* Constraint: the DDL files are part of every reload, not only of the first run: the step recreates the nine tables from them, so a change to a DDL file takes effect on the next run.
* Constraint: [ADR-0009](0009-use-duckdb-as-database-engine.md)'s Consequences already anticipated that a change to the load pattern would require revisiting that decision. This ADR is that revisit. It keeps DuckDB and changes only the load pattern.

### Confirmation

[`staging.md`](../specification/staging.md#load-order-and-transactions) states the load order this ADR sets. The pipeline's tests cover a second run over a warehouse whose `fact_response` already references every dimension, and a failure forced inside the step, followed by a check that the eight dimensions and `fact_response` hold what they held before the run.

## Pros and Cons of the Options

### One transaction for the eight dimensions and `fact_response`

* Good, because it succeeds where row deletion in one transaction fails (E3).
* Good, because an abort leaves the previous run's warehouse intact, tables and foreign keys included (E3).
* Bad, because a failure late in the step discards all of the step's work.

### Empty `fact_response` in its own transaction first

* Good, because it keeps one transaction per dimension, as the load order had it.
* Bad, because a dimension failure after that step leaves `fact_response` empty until the next successful run. That is worse than the current failure mode, where the previous data stays queryable even if stale.
* Bad, because it keeps the mixed state across dimensions described in the Decision Drivers.

### Build in a new `.duckdb` file and replace it on success

* Good, because the replacement is atomic at the file level, and a failed run never touches the previous file.
* Bad, because it solves the problem one layer away from where it lives: file handling added around the engine instead of the engine's own transactional DDL, which E3 confirms already handles this correctly.

## More Information

* Related: [ADR-0009](0009-use-duckdb-as-database-engine.md) (engine; E1, E3), [ADR-0007](0007-person-grain-fact-table-and-dimension-grain-rule.md) (the fact table's foreign keys).
* The contract this decision changes: [`staging.md`](../specification/staging.md#load-order-and-transactions).
