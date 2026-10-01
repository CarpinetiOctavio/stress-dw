# stress-dw — instructions for Claude Code

Dimensional data warehouse (Hefesto methodology), rebuilt from an audited university course project. Portfolio piece for SCU, not an academic publication — no output is a finding about any population ([ADR-0001](docs/decisions/0001-position-as-portfolio-project.md)).

## Read first

- [`docs/specification.md`](docs/specification.md) — the implementation contract (the *what*). Read the relevant part before writing a query or a DDL statement.
- [`docs/decisions/`](docs/decisions/) — ADRs, the *why*. Read one before touching anything it already covers.
- [`docs/writing-conventions.md`](docs/writing-conventions.md) — style rules for everything written here: English, impersonal voice, glossing, one home per concept. Applies to code comments and commit messages, not only prose docs.
- [`docs/code-conventions.md`](docs/code-conventions.md) — Python and SQL style, naming, docstrings, testing, and error handling. Read before writing any code, not only before committing it.
- [`docs/methodology.md`](docs/methodology.md) — what "Fase N" means when an ADR or the specification cites it.
- [`docs/audit/legacy-audit.md`](docs/audit/legacy-audit.md) — the checks (A1–A13) and their method.
- [`docs/audit/phase4-closure.md`](docs/audit/phase4-closure.md) — where Fase 4 left off: how to reproduce it, its results, and what is still out of scope.

## Hard rules

- Never modify `stress-dw-legacy`. Read-only, always, even for a query — check it out locally, don't edit anything in it. [ADR-0000]
- `main` is protected. Work on a branch, open a PR, never push to `main`. [ADR-0002]
- Execute and report evidence — commands actually run, numbers actually computed. Never fill a gap from memory or assumption; say "pending" instead.
- Decisions aren't Code's to make. If a result contradicts an existing ADR or the specification, flag it and stop — resolving it happens outside this session.
- Fase 4 is specified in full in [`staging.md`](docs/specification/staging.md); every part, including update policy, is confirmed. The only work executed so far against the legacy repo is the read-only checks in `docs/audit/legacy-audit.md`. The pipeline that implements Fase 4 lives in `src/stress_dw/`; `uv run python -m stress_dw.pipeline` runs a full reload.
- English only, code and docs, no exception. The legacy repo stays in Spanish, untouched. [writing-conventions.md, rule 1]
- Every versioned text, this file included, is written in formal, impersonal third person: no personal name outside an ADR's `decision-makers` field and URLs, and no instruction addressed to a reader. The same holds for code comments, commit messages and pull-request text. Text relayed from another session is checked against this rule before it is written, even when already approved. [writing-conventions.md, rule 2]
- No indicator value is displayed, printed, logged or reported (in a file, a pull-request text or a message) until the correspondence criteria are committed and the order of [ADR-0011](docs/decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md) allows it. Running the indicators is allowed; showing their values is not. Until then, the acceptance tests that execute the indicators (C8, C9 and C10) are run as `uv run pytest tests/test_acceptance.py -k "test_c8_ or test_c9_ or test_c10_" --tb=no -rN -v`, which reports pass or fail per test without assertion messages; all other tests are run normally. A failure in one of them is reported only as a failure; if values were displayed regardless, the report states so without repeating them, so that they can be recorded under ADR-0011, rules 1 and 2. Such a failure is diagnosed only after exposure is allowed.
- Evidence follows [ADR-0012](docs/decisions/0012-cite-only-frozen-and-versioned-sources-as-evidence.md): a claim cites the frozen legacy source or a versioned artifact; outside material only as dated corroboration.

## Already decided — don't relitigate

- Star schema, one fact table `fact_response` at person grain (one row per survey response), eight dimensions. [ADR-0007]
  Reasoning in [ADR-0013](docs/decisions/0013-keep-star-schema-add-flat-consumption-view.md). A reduced star is deferred until the correspondence evidence document is merged and is not started before then.
- `explicit_recognition` and `symptom_cluster` are computed at query time; neither is ever a stored column. [ADR-0007]
- Country-to-region mapping is the fixed table in [`specification/country-region-mapping.md`](docs/specification/country-region-mapping.md), not inferred.
- Deduplicate staged records on all 17 source columns, not only the columns this specification models: 290,051 records reach staging. [ADR-0008]
