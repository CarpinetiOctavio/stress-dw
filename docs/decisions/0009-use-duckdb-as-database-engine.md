---
status: "accepted"
date: 2026-09-25
decision-makers: Octavio Carpineti
---

# Use DuckDB as the pipeline's database engine

## Context and Problem Statement

No ADR has fixed the database engine that implements the star schema [`docs/specification.md`](../specification.md) defines. [`fact-table.md`](../specification/fact-table.md) currently states "Foreign keys are enforced by the database (InnoDB)" — a MySQL-specific detail inherited from the legacy project ([ADR-0000](0000-rebuild-from-scratch-instead-of-continuing-legacy.md)) without ever being decided for this rebuild. Invariant I3 and acceptance check C5 require genuine, database-level foreign-key enforcement, not a declared constraint the engine merely accepts as documentation. Which database engine should implement the specification's schema?

## Findings

Two rows, E1 and E2, evaluate constraint enforcement in engines considered below. Neither audits the legacy codebase (ADR-0000, `F`) or the dataset's provenance (ADR-0001, `P`), and neither continues [ADR-0008](0008-staging-deduplication-grain.md)'s `G` sequence, which is specific to that decision's dedup-grain evidence — this ADR starts its own letter, `E`, for "engine."

| ID | Finding | Evidence | Status |
|----|---------|----------|--------|
| E1 | DuckDB enforces primary-key, foreign-key, and uniqueness constraints at insert and delete time. Documented limitations are narrow: a row rewritten by an `UPDATE` within the same statement that inserted it can miss re-validation, and index-based constraint checks under concurrent transactions can be evaluated too eagerly. Neither scenario arises under [`staging.md`](../specification/staging.md)'s load pattern — single writer, insert-only, no post-load `UPDATE`. | DuckDB documentation, Constraints and Indexes pages (fetched 2026-09-26) | Established |
| E2 | SQLite disables foreign-key enforcement by default; it requires `PRAGMA foreign_keys = ON` per connection, and an omitted pragma silently drops enforcement with no error. | SQLite documentation, foreign key support | Established |

## Decision Drivers

* I3/C5 require enforcement the engine actually performs, not metadata the application must remember to activate — this is what rules out SQLite (E2): the failure mode is silent, not a hard error.
* The specification's own workload is analytical, not transactional: one measure, no post-load updates ([ADR-0007](0007-person-grain-fact-table-and-dimension-grain-rule.md)), and every indicator is an aggregation over cuts ([`patterns.md`](../specification/patterns.md)). The engine should be chosen for read-heavy aggregation, not write throughput.
* This is a portfolio piece ([ADR-0001](0001-position-as-portfolio-project.md)); a reviewer should be able to run the pipeline and inspect the warehouse without provisioning a server or supplying credentials.
* The portfolio's destination includes an active course on relational databases at the host institution, taught through DuckDB via Marimo notebooks. An engine choice that overlaps with coursework already in progress is a stronger demonstration of current fluency than one chosen only from prior, unrelated exposure.
* `fact-table.md`'s existing "(InnoDB)" reference was never the output of a decision — whatever is chosen here is what that line should cite going forward.

## Considered Options

* MySQL
* PostgreSQL
* SQLite
* DuckDB

## Decision Outcome

Chosen option: "DuckDB", because it is the only option that requires no server to reproduce, enforces the constraints I3/C5 need under this pipeline's actual load pattern (E1), is purpose-built for the analytical workload this warehouse is, and overlaps directly with coursework already in progress.

### Consequences

* Good, because the pipeline and the warehouse it produces need no infrastructure beyond a Python environment — cloning the repository and running the load script is enough to reproduce and inspect it.
* Good, because E1's limitations do not apply to this pipeline's write-once, single-writer load pattern; I3/C5 hold in practice, not only on paper.
* Good, because the same warehouse is directly explorable from the notebook environment already in use for related coursework, without a translation step.
* Bad, because DuckDB's constraint system has a narrower track record than MySQL's or PostgreSQL's decades of production use; its documented limitations (E1) don't apply here, but they exist, and a future change to the load pattern — a second writer, an in-place update — would require revisiting this decision.
* Bad, because it demonstrates less of the "operate a persistent, multi-user database server" experience that MySQL or PostgreSQL would; a reviewer looking for that specific skill won't find it here.
* Constraint: [`fact-table.md`](../specification/fact-table.md)'s "Foreign keys are enforced by the database (InnoDB)" no longer describes the target engine and must be corrected to cite this ADR.
* Constraint: [`code-conventions.md`](../code-conventions.md)'s example of a typically-incomplete type stub names `mysql.connector`; with no MySQL dependency in the pipeline, that example no longer applies and should name DuckDB's Python client instead, if a comparable gap exists there.

### Confirmation

The load scripts connect through DuckDB's Python client and write to a `.duckdb` file. Acceptance check C5 ([`acceptance.md`](../specification/acceptance.md)) runs against that file and confirms foreign-key enforcement holds in practice, not only per E1's citation of DuckDB's own documentation.

## Pros and Cons of the Options

### MySQL

* Good, because its foreign-key enforcement is mature and widely proven, with a longer production track record than DuckDB's.
* Bad, because it requires a running server for anyone to reproduce the portfolio piece.
* Bad, because it fits a transactional workload more than the analytical one this warehouse actually has.

### PostgreSQL

* Good, because its foreign-key enforcement is equally mature, and its analytical SQL (window functions, CTEs) is strong.
* Bad, because it carries the same server-provisioning friction as MySQL.
* Bad, because it has no particular tie to work already in progress elsewhere in the portfolio's context.

### SQLite

* Good, because it requires no server, matching the zero-infrastructure goal DuckDB also meets.
* Bad, because foreign-key enforcement is off by default (E2) — a silent gap in exactly the invariant (I3) this decision exists to protect.
* Bad, because it is not built for the aggregation-heavy queries this warehouse's query layer runs.

### DuckDB

* Good, because it requires no server, enforces the constraints this project needs under its actual load pattern (E1), and is purpose-built for analytical aggregation over a star schema.
* Bad, because its constraint system is less battle-tested outside the load pattern this project uses, and it demonstrates less "operate a database server" experience than the alternatives.

## More Information

* Related: [ADR-0000](0000-rebuild-from-scratch-instead-of-continuing-legacy.md) (the legacy's MySQL choice, not binding here), [ADR-0001](0001-position-as-portfolio-project.md) (portfolio destination), [ADR-0007](0007-person-grain-fact-table-and-dimension-grain-rule.md) (the workload this engine serves).
* Evidence: DuckDB documentation (constraints, indexes); SQLite documentation (foreign key support).
* Files this decision corrects: [`fact-table.md`](../specification/fact-table.md), [`code-conventions.md`](../code-conventions.md).