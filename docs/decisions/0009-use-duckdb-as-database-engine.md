---
status: "accepted"
date: 2026-09-25
decision-makers: Octavio Carpineti
---

# Use DuckDB as the pipeline's database engine

## Context and Problem Statement

No ADR has fixed the database engine that implements the star schema [`docs/specification.md`](../specification.md) defines. [`fact-table.md`](../specification/fact-table.md) currently states "Foreign keys are enforced by the database (InnoDB)" — a MySQL-specific detail inherited from the legacy project ([ADR-0000](0000-rebuild-from-scratch-instead-of-continuing-legacy.md)) without ever being decided for this rebuild. Invariant I3 and acceptance check C5 require genuine, database-level foreign-key enforcement, not a declared constraint the engine merely accepts as documentation. Which database engine should implement the specification's schema?

## Findings

Two rows, E1 and E2, evaluate constraint enforcement in engines considered below. Neither audits the legacy codebase (ADR-0000, `F`) or the dataset's provenance (ADR-0001, `P`), and neither continues [ADR-0008](0008-staging-deduplication-grain.md)'s `G` sequence, which is specific to that decision's dedup-grain evidence — this ADR starts its own letter, `E`, for "engine." E3 was added on 2026-09-27, after this decision was accepted; it leaves the decision standing and is the evidence for [ADR-0010](0010-reload-dimensions-and-fact-in-one-transaction.md).

| ID | Finding | Evidence | Status |
|----|---------|----------|--------|
| E1 | DuckDB enforces primary-key, foreign-key, and uniqueness constraints at insert and delete time. Documented limitations are narrow: a row rewritten by an `UPDATE` within the same statement that inserted it can miss re-validation, and index-based constraint checks under concurrent transactions can be evaluated too eagerly. Neither scenario arises under [`staging.md`](../specification/staging.md)'s load pattern — single writer, insert-only, no post-load `UPDATE`. See E3: this premise does not hold under a full reload. See also the 2026-10-02 addendum. | DuckDB documentation, Constraints and Indexes pages (fetched 2026-09-26) | Established |
| E2 | SQLite disables foreign-key enforcement by default; it requires `PRAGMA foreign_keys = ON` per connection, and an omitted pragma silently drops enforcement with no error. See the 2026-10-02 addendum. | SQLite documentation, foreign key support | Established |
| E3 | **Under [`staging.md`](../specification/staging.md)'s full reload, DuckDB evaluates a foreign key against rows already deleted in the same transaction.** Against this repository's DDL, with one `fact_response` row referencing one row in each dimension: deleting a referenced dimension row aborts, as it should; deleting the `fact_response` row and then the dimension row in two separate transactions succeeds; the same two deletes in one transaction fail on the foreign key, with `DELETE` and with `TRUNCATE` alike. Dropping `fact_response` and the eight dimensions, recreating them from their DDL, and reloading them, all in one transaction, succeeds. A failure forced inside that transaction, after the drops, the recreation, and a partial reload, followed by a rollback, restores the pre-run state entirely: every row, all ten tables, and `fact_response`'s eight foreign keys. The full reload deletes rows, so E1's "insert-only" premise does not describe it. | Test matrix run with DuckDB 1.5.5 against the DDL in `src/stress_dw/sql/schema/`, 2026-09-27; added after this decision, and cited by [ADR-0010](0010-reload-dimensions-and-fact-in-one-transaction.md) | Established |

---

### Addendum (2026-10-02)

E1 and E2 cited documentation pages without a capture ([ADR-0012](0012-cite-only-frozen-and-versioned-sources-as-evidence.md), rule 2). The pages were captured on 2026-10-01 and 2026-10-02 (the date in each file name). The captures carry claims about those pages only, and E1 and E2 are restated below to what the captures show. The E1 and E2 rows above carry a pointer to this addendum; their text is otherwise unchanged. E3 rests on this repository's own test matrix and is unchanged.

| File | Taken | Shows | Documentation version |
|------|-------|-------|-----------------------|
| [`duckdb-constraints-1-2026-10-01.png`](../audit/evidence/duckdb-constraints-1-2026-10-01.png) | 2026-10-01 | DuckDB "Constraints" page, `duckdb.org/docs/current/sql/constraints`: introduction, performance note and syntax diagram | Version selector reads "1.5 current"; the URL uses `/docs/current/`, not a pinned version |
| [`duckdb-constraints-2-2026-10-01.png`](../audit/evidence/duckdb-constraints-2-2026-10-01.png) | 2026-10-01 | Same page, "Foreign Keys" section: example, the error raised for a missing referenced key, the ART-index sentence, and the warning on over-eager evaluation | Same as above |
| [`duckdb-indexes-limitations-1-2026-10-01.png`](../audit/evidence/duckdb-indexes-limitations-1-2026-10-01.png) | 2026-10-01 | DuckDB "Indexes" page, `duckdb.org/docs/current/sql/indexes`: "Limitations of ART Indexes" and "Constraint Checking in UPDATE Statements", with example and error | Same as above |
| [`duckdb-indexes-limitations-2-2026-10-01.png`](../audit/evidence/duckdb-indexes-limitations-2-2026-10-01.png) | 2026-10-01 | Same page, "Over-Eager Constraint Checking in Foreign Keys": conditions, example, error and explanation | Same as above |
| [`duckdb-indexes-limitations-3-2026-10-02.png`](../audit/evidence/duckdb-indexes-limitations-3-2026-10-02.png) | 2026-10-02 | Same page, "Constraint Checking in UPDATE Statements" in full: example and error, the workaround paragraph, and its example inside `BEGIN` and `COMMIT` | Same as above |
| [`sqlite-foreign-keys-2026-10-01.png`](../audit/evidence/sqlite-foreign-keys-2026-10-01.png) | 2026-10-01 | SQLite "SQLite Foreign Key Support", `sqlite.org/foreignkeys.html`: section 2, "Enabling Foreign Key Support", and the start of section 3 | No documentation version shown |

The pipeline's lock file pins DuckDB 1.5.5. Whether the "1.5 current" pages describe that release is not verified.

**E1, restated.**

* **Enforcement.** The Constraints page states: "Constraints enforce certain properties over data that is inserted into a table." For foreign keys it states: "The constraint enforces that the key exists in the other table", with an example in which an insert that references a missing key fails. The captured pages do not state delete-time enforcement; E3 establishes it for this repository's DDL.
* **`UPDATE`.** The documented limitation runs opposite to the one E1 wrote. "UPDATE statements on indexed columns and columns that cannot be updated in place are transformed into a DELETE of the original row followed by an INSERT of the updated row." The rewrite happens per chunk of data, and the page's example raises a primary-key violation for keys that would not collide once the statement completes: a spurious violation, not a missed re-validation. The page adds: "The same limitation exists in other DBMSs, like PostgreSQL."
* **Over-eager foreign-key checks.** The Constraints page warns: "Indexes have certain limitations that might result in constraints being evaluated too eagerly". The Indexes page documents the foreign-key case. It arises when a table has a foreign key, an `UPDATE` touches a composite payload column (the page names `LIST` and `STRUCT`) of the referenced primary-key table, and the row that the rewrite deletes is still referenced. The stated reason is that DuckDB "does not yet support" looking ahead.
* **Concurrent transactions.** E1's clause on index-based checks "under concurrent transactions" was not found in the captured pages and is withdrawn.

On the Consequence about DuckDB's narrower track record: by the page's own statement, the `UPDATE` limitation is not specific to DuckDB. The over-eager foreign-key limitation is stated without comparison to other systems. The statement about PostgreSQL is DuckDB's own; no PostgreSQL page is captured. Whether this changes the weight of that Consequence is not decided here.

**E2, restated.** The SQLite page states: "Foreign key constraints are disabled by default (for backwards compatibility), so must be enabled separately for each database connection." It also states that foreign-key support "must still be enabled by the application at runtime, using the PRAGMA foreign_keys command." E2's clause that an omitted pragma "silently drops enforcement with no error" is not stated on the captured page. It is this record's inference from the default: a connection that does not issue the pragma does not enforce foreign keys.

**The Consequence that E1's limitations do not apply, restated.** Both limitations documented on the captured pages are triggered by an `UPDATE` statement. The pipeline issues none. Its writes are `INSERT` statements, `DROP TABLE` within the reload of [ADR-0010](0010-reload-dimensions-and-fact-in-one-transaction.md), and one `DELETE` of every row of `staging_response`, a table no foreign key references. The conclusion therefore holds, but on that premise rather than on a "write-once" load: E3 shows that reloading by deletion fails on the foreign keys, and ADR-0010 handles that by dropping and recreating the tables.

**Parts of this record that rest on the restated findings.** The Decision Driver that rules out SQLite because "the failure mode is silent, not a hard error"; the chosen-option rationale, "under this pipeline's actual load pattern (E1)"; the Consequence on DuckDB's "narrower track record"; and, under Pros and Cons, the SQLite item "a silent gap" and the DuckDB items "under its actual load pattern (E1)" and "less battle-tested". Their weight is not changed here.

**Open point: an explicit `DELETE` followed by `INSERT` of the same keys.** The Indexes page gives a workaround for its `UPDATE` limitation: "A workaround is to split the UPDATE into a DELETE ... RETURNING ... followed by an INSERT", and "All statements should be run inside a transaction via BEGIN, and eventually COMMIT." Its example, on a table with a primary key, deletes every row and inserts the same keys again inside one transaction. The staging reload issues the same DELETE-then-INSERT sequence on `staging_response`, which has a primary key and is referenced by no foreign key (`load_staging` in `src/stress_dw/staging.py`). The difference is the source of the reinserted rows: the page's example holds the deleted rows in a temporary table, whereas the pipeline reinserts from the staged frame. The captured page does not address a run at full size. `test_a_second_run_replaces_the_first_instead_of_appending` in `tests/test_staging.py` covers the case at test size only; the acceptance checks load staging once, into a new database (fixture `warehouse` in `tests/test_acceptance.py`), so no check runs the staging reload a second time on the source file.

---

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