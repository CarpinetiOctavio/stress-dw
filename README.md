# stress-dw

The original course design named mental-health professionals as the end users of its outputs, with the destigmatization of mental-health problems among its aims ([report at `legacy-original`](https://github.com/CarpinetiOctavio/stress-dw-legacy/blob/legacy-original/Informe%20DW/DW%20-%20Estr%C3%A9s%20y%20Salud%20Mental.pdf), pp. 5, 9 and 32). This rebuild keeps its help-seeking question (Q7), revised in [ADR-0004](docs/decisions/0004-revise-business-questions.md), and is built to show, for respondents with a convergent self-reported symptom profile, what share report having ever sought treatment, by their level of explicit stress recognition. It is a star-schema data warehouse ([DuckDB](docs/decisions/0009-use-duckdb-as-database-engine.md), Python ETL), built with the [Hefesto methodology](docs/methodology.md), that turns raw survey responses into indicators. The symptom profile it uses is self-reported, not a diagnosis ([`symptom_cluster`](docs/specification/definitions.md#symptom_cluster)).

It was rebuilt from scratch after an audit of the university course version found a dimension fan-out and averaged percentages ([ADR-0000](docs/decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md)). Checks run before the indicator output was read ([ADR-0011](docs/decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), rule 4) show that the file combines columns from two sources: its symptom columns match a separately published dataset ([legacy audit](docs/audit/legacy-audit.md), rows A5, A6 and A10). Questions that relate columns from the two sources therefore cannot be answered with this file. The help-seeking question is one of them: `treatment` belongs to one column group, and stress recognition and the symptom profile to the other ([LOG-040](docs/decisions/log/LOG-040-h1-column-groups.md)). The correspondence phase reports, question by question, which can be answered and why.

> **Provenance.** The source file's origin is undocumented, and no output of this project is a finding about any population ([ADR-0001](docs/decisions/0001-position-as-portfolio-project.md); [details](#data-and-provenance)).

## Background

- The original course project is preserved, archived, at [`stress-dw-legacy`](https://github.com/CarpinetiOctavio/stress-dw-legacy).
- [ADR-0000](docs/decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md) explains why the project was rebuilt from scratch instead of continued.

## Status

Pipeline closed ([`phase4-closure.md`](docs/audit/phase4-closure.md)); correspondence phase in progress. Decisions are recorded in [`docs/decisions`](docs/decisions); audit evidence and checks are in [`docs/audit`](docs/audit).

## Data and provenance

> **Provenance limitation.** The dataset used here ([Kaggle](https://www.kaggle.com/datasets/bhavikjikadara/mental-health-dataset)) has no documented provenance: its uploader states only that it was collected from the internet, and most of its columns have no description. It is used as a methodological test bench. No output of this project should be read as a finding about any population. The raw file itself is not committed to this repository either — the same open question about its provenance extends to whether its declared license covers the whole file. See [ADR-0001](docs/decisions/0001-position-as-portfolio-project.md) and [`docs/dataset-provenance.md`](docs/dataset-provenance.md) for both.

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

Tests are run with `uv run pytest` ([Phase 4 closure, section 2](docs/audit/phase4-closure.md#2-reproducing-this)).

The source file is obtained separately and verified before any load; see [`staging.md`](docs/specification/staging.md#extraction). Code style is in [`docs/code-conventions.md`](docs/code-conventions.md).

## License

MIT for the code and documentation in this repository, except the copies of published works in `docs/references/`, which keep their own licences ([stored copies](docs/references/README.md#stored-copies)). The dataset is not included and is not covered by this license.