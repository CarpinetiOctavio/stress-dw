# Decision Records

Decisions are recorded in [MADR](https://adr.github.io/madr/) format, one file per decision, named `NNNN-title-with-dashes.md`. To add one, copy `adr-template.md` and fill it in.

Decisions that are not, or not only, recorded in a decision record are kept in the [decision log](log/README.md); its entries are not MADR records.

| ADR                                                               | Title | Status   |
|-------------------------------------------------------------------|-------|----------|
| [0000](0000-rebuild-from-scratch-instead-of-continuing-legacy.md) | Rebuild the pipeline from scratch instead of continuing on the legacy codebase | accepted |
| [0001](0001-position-as-portfolio-project.md)                     | Position the project as a portfolio piece and do not pursue academic publication | accepted |
| [0002](0002-protect-main-with-required-pull-requests.md)          | Protect `main` with required pull requests | accepted |
| [0003](0003-redefine-indicators-14-to-16.md)                      | Redefine indicators 14–16 around verifiable constructs | accepted |
| [0004](0004-revise-business-questions.md) | Revise Fase 1 business questions to match corrected variable semantics and dataset scope | accepted |
| [0005](0005-redefine-indicators-1-to-13.md) | Redefine indicators 1–13 around verifiable constructs | accepted |
| [0006](0006-final-questions-and-indicators.md) | Consolidated record: final Fase 1 questions and indicator definitions | accepted |
| [0007](0007-person-grain-fact-table-and-dimension-grain-rule.md) | Model the fact table at person grain, bound dimensions by a grain rule, and derive conditions at query time | accepted |
| [0008](0008-staging-deduplication-grain.md) | Deduplicate staged records on all 17 source columns, not the columns this specification models | accepted |
| [0009](0009-use-duckdb-as-database-engine.md) | Use DuckDB as the pipeline's database engine | accepted |
| [0010](0010-reload-dimensions-and-fact-in-one-transaction.md) | Reload the eight dimensions and the fact table in one transaction | accepted |
| [0011](0011-preregister-correspondence-criteria-before-exposing-indicator-values.md) | Fix the correspondence criteria in a commit before any indicator value is exposed, and declare what was already known about the data | accepted |
| [0012](0012-cite-only-frozen-and-versioned-sources-as-evidence.md) | Cite only the frozen legacy source and versioned artifacts, and admit outside material only as declared corroboration | accepted |
| [0013](0013-keep-star-schema-add-flat-consumption-view.md) | Keep the star schema as the definition and integrity layer, add a flat view as the consumption interface, and defer a reduced star | accepted |


## Deviations from base MADR

* **Findings section**, between Context and Problem Statement and Decision Drivers. Not part of base MADR. Use it only when the decision rests on evidence gathered against the repository, the dataset, or an external source; omit it otherwise. Each row cites where the evidence lives and marks a status of `Established`, a hypothesis still to test, or `Pending` a check.
* **Considered Options as a bullet list**, not numbered — this matches the MADR spec; it's noted here only because ADR-0000 and ADR-0001, written before this convention was fixed, use numbers. New ADRs use bullets.

## Addenda to accepted decision records

An accepted decision record is not rewritten. When a finding that grounded the decision is corrected or qualified, the record receives a dated addendum and its original text stays as written. Operational descriptions, such as a path, a command or a link, may be corrected in place.

## Finding and hypothesis IDs

Used across the decision records, the specification, the audit and the decision log:

* **`Fn`** — findings from the audit of the legacy codebase (ADR-0000): schema, ETL, fact-table design.
* **`Pn`** — findings from the audit of the dataset's provenance (ADR-0001): the source, its documentation, its license.
* **`Hn`** — hypotheses raised by an `F` or `P` finding but not yet resolved. Each `H` is tested by one or more checks (`A1`, `A2`, ...) in `docs/audit/legacy-audit.md`; a hypothesis is never cited as a finding until its check's result is in.
* **`An`** — checks of the [legacy audit](../audit/legacy-audit.md#checks); each records its method and result.
* **`Gn`** — findings on the deduplication grain ([ADR-0008](0008-staging-deduplication-grain.md)).
* **`En`** — findings on the database engine ([ADR-0009](0009-use-duckdb-as-database-engine.md)).
* **`Kn`** — categories of prior knowledge ([ADR-0011](0011-preregister-correspondence-criteria-before-exposing-indicator-values.md)).
* **`Sn`** — sources of evidence ([ADR-0012](0012-cite-only-frozen-and-versioned-sources-as-evidence.md)).
* **`Mn`** — findings on the form of the schema ([ADR-0013](0013-keep-star-schema-add-flat-consumption-view.md)).
* **`Cn`** — acceptance checks ([`acceptance.md`](../specification/acceptance.md)).
* **`In`** — invariants of the fact table ([`fact-table.md`](../specification/fact-table.md#invariants)).
* **`LOG-NNN`** — entries of the [decision log](log/README.md).
* **`LSN-NNN`** — [method lessons](../audit/lessons/README.md).

A new ADR that introduces its own evidence-backed findings continues the `F`/`P` sequence appropriate to what it audits, or starts a new letter if it audits something neither ADR-0000 nor ADR-0001 covers — state the choice in the ADR itself.