# Decision Records

Decisions are recorded in [MADR](https://adr.github.io/madr/) format, one file per decision, named `NNNN-title-with-dashes.md`. To add one, copy `adr-template.md` and fill it in.

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


## Deviations from base MADR

* **Findings section**, between Context and Problem Statement and Decision Drivers. Not part of base MADR. Use it only when the decision rests on evidence gathered against the repository, the dataset, or an external source; omit it otherwise. Each row cites where the evidence lives and marks a status of `Established`, a hypothesis still to test, or `Pending` a check.
* **Considered Options as a bullet list**, not numbered — this matches the MADR spec; it's noted here only because ADR-0000 and ADR-0001, written before this convention was fixed, use numbers. New ADRs use bullets.

## Finding and hypothesis IDs

Used consistently across ADR-0000, ADR-0001, and `docs/audit/legacy-audit.md`:

* **`Fn`** — findings from the audit of the legacy codebase (ADR-0000): schema, ETL, fact-table design.
* **`Pn`** — findings from the audit of the dataset's provenance (ADR-0001): the source, its documentation, its license.
* **`Hn`** — hypotheses raised by an `F` or `P` finding but not yet resolved. Each `H` is tested by one or more checks (`A1`, `A2`, ...) in `docs/audit/legacy-audit.md`; a hypothesis is never cited as a finding until its check's result is in.

A new ADR that introduces its own evidence-backed findings continues the `F`/`P` sequence appropriate to what it audits, or starts a new letter if it audits something neither ADR-0000 nor ADR-0001 covers — state the choice in the ADR itself.