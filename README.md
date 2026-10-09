# stress-dw

Work in progress. A dimensional data warehouse (star schema, [DuckDB](docs/decisions/0009-use-duckdb-as-database-engine.md), Python ETL) built with the [Hefesto methodology](docs/methodology.md), rebuilt from scratch after an audit of a university course project.

> **Provenance limitation.** The dataset used here ([Kaggle](https://www.kaggle.com/datasets/bhavikjikadara/mental-health-dataset)) has no documented provenance: its uploader states only that it was collected from the internet, and most of its columns have no description. It is used as a methodological test bench. No output of this project should be read as a finding about any population. The raw file itself is not committed to this repository either — the same open question about its provenance extends to whether its declared license covers the whole file. See [ADR-0001](docs/decisions/0001-position-as-portfolio-project.md) and [`docs/dataset-provenance.md`](docs/dataset-provenance.md) for both.

## Background

- The original course project is preserved, archived, at [`stress-dw-legacy`](https://github.com/CarpinetiOctavio/stress-dw-legacy).
- [ADR-0000](docs/decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md) explains why the project was rebuilt from scratch instead of continued.

## Status

Data integration is closed for this rebuild as of commit `9f31ab0`; the closure record is in [`phase4-closure.md`](docs/audit/phase4-closure.md#1-status). Decisions are recorded in [`docs/decisions`](docs/decisions); audit evidence and checks are in [`docs/audit`](docs/audit).

## Source verification

Claims that rest on published work are checked against copies of the sources, not only cited. The [verification register](docs/references/README.md) records, for each claim, the printed page and a verbatim quotation, together with the SHA-256 of the copy consulted and where it was obtained; a script checks both against a copy. Given a directory holding the copies, under the file names the register gives (the one copy whose licence permits redistribution is stored in the repository):

```sh
uv run python -m stress_dw.references <directory>
```

The rule and its reasoning are in [LOG-048](docs/decisions/log/LOG-048-verifiable-source-checks.md).

## Development

Requires [uv](https://docs.astral.sh/uv/), which installs the Python version pinned in `.python-version` and every dependency declared in `pyproject.toml`:

```sh
uv sync
uv run ruff check && uv run ruff format --check
uv run mypy
```

Tests are run with the two commands of [Phase 4 closure, section 2](docs/audit/phase4-closure.md#2-reproducing-this) while [ADR-0011](docs/decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md) does not allow indicator values to be exposed.

The source file is obtained separately and verified before any load; see [`staging.md`](docs/specification/staging.md#extraction). Code style is in [`docs/code-conventions.md`](docs/code-conventions.md).

## License

MIT for the code and documentation in this repository, except the copies of published works in `docs/references/`, which keep their own licences ([stored copies](docs/references/README.md#stored-copies)). The dataset is not included and is not covered by this license.