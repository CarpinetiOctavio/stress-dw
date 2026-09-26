# stress-dw — instructions for Claude Code

Dimensional data warehouse (Hefesto methodology), rebuilt from an audited university course project. Portfolio piece for SCU, not an academic publication — no output is a finding about any population ([ADR-0001](docs/decisions/0001-position-as-portfolio-project.md)).

## Read first

- [`docs/specification.md`](docs/specification.md) — the implementation contract (the *what*). Read the relevant part before writing a query or a DDL statement.
- [`docs/decisions/`](docs/decisions/) — ADRs, the *why*. Read one before touching anything it already covers.
- [`docs/writing-conventions.md`](docs/writing-conventions.md) — style rules for everything written here: English, impersonal voice, glossing, one home per concept. Applies to code comments and commit messages, not only prose docs.
- [`docs/code-conventions.md`](docs/code-conventions.md) — Python and SQL style, naming, docstrings, testing, and error handling. Read before writing any code, not only before committing it.
- [`docs/methodology.md`](docs/methodology.md) — what "Fase N" means when an ADR or the specification cites it.
- [`docs/audit/legacy-audit.md`](docs/audit/legacy-audit.md) — the checks (A1–A13) and their method.

## Hard rules

- Never modify `stress-dw-legacy`. Read-only, always, even for a query — check it out locally, don't edit anything in it. [ADR-0000]
- `main` is protected. Work on a branch, open a PR, never push to `main`. [ADR-0002]
- Execute and report evidence — commands actually run, numbers actually computed. Never fill a gap from memory or assumption; say "pending" instead.
- Decisions aren't Code's to make. If a result contradicts an existing ADR or the specification, flag it and stop — resolving it happens outside this session.
- Fase 4 (staging, cleaning, load, update policy) has no specification yet. Don't build or run pipeline code until it exists and is confirmed. Until then, the only in-scope work against the legacy repo is the read-only checks in `docs/audit/legacy-audit.md`.
- English only, code and docs, no exception. The legacy repo stays in Spanish, untouched. [writing-conventions.md, rule 1]

## Already decided — don't relitigate

- Star schema, one fact table `fact_response` at person grain (one row per survey response), eight dimensions. [ADR-0007]
- `explicit_recognition` and `symptom_cluster` are computed at query time; neither is ever a stored column. [ADR-0007]
- Country-to-region mapping is the fixed table in [`specification/country-region-mapping.md`](docs/specification/country-region-mapping.md), not inferred.
- Deduplicate staged records on all 17 source columns, not only the columns this specification models: 290,051 records reach staging. [ADR-0008]
