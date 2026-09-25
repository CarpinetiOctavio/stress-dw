# stress-dw

Work in progress. A dimensional data warehouse (star schema, MySQL, Python ETL) built with the [Hefesto methodology](docs/methodology.md), rebuilt from scratch after an audit of a university course project.

> **Provenance limitation.** The dataset used here ([Kaggle](https://www.kaggle.com/datasets/bhavikjikadara/mental-health-dataset)) has no documented provenance: its uploader states only that it was collected from the internet, and most of its columns have no description. It is used as a methodological test bench. No output of this project should be read as a finding about any population. The raw file itself is not committed to this repository either — the same open question about its provenance extends to whether its declared license covers the whole file. See [ADR-0001](docs/decisions/0001-position-as-portfolio-project.md) and [`docs/dataset-provenance.md`](docs/dataset-provenance.md) for both.

## Background

- The original course project is preserved, archived, at [`stress-dw-legacy`](https://github.com/CarpinetiOctavio/stress-dw-legacy).
- [ADR-0000](docs/decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md) explains why the project was rebuilt from scratch instead of continued.

## Status

Specification and audit in progress. There is no runnable pipeline yet. Decisions are recorded in [`docs/decisions`](docs/decisions); audit evidence and checks are in [`docs/audit`](docs/audit).

## License

MIT for the code and documentation in this repository. The dataset is not included and is not covered by this license.