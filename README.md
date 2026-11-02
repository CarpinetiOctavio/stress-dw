# stress-dw

I rebuilt my university course's data warehouse as a star schema in DuckDB, SQL and Python, after auditing it and finding that it [counted survey responses more than once](docs/explainers/fan-out.md) and [averaged percentages](docs/explainers/average-of-rates.md). The rebuild stores one row per response; its tests check that no join multiplies rows and that no rate is stored, and two full reloads give byte-identical outputs ([the warehouse](docs/explainers/the-warehouse.md)). The checks also showed that the source file joins columns from two sources: its symptom columns match a separately published dataset. So only one of the nine questions the warehouse was built for can be answered with it; the main one, on seeking mental-health treatment, cannot, and the repository shows [why](docs/explainers/two-sources.md).

> **Provenance.** The source file's origin is undocumented, and no output of this project is a finding about any population ([decision on the project's position](docs/decisions/0001-position-as-portfolio-project.md); [details](#data-and-provenance)).

Reading paths: in 30 seconds, the opening paragraph; in five minutes, points 1 to 3 and "How it was evaluated"; in depth, the [explainer](docs/explainers/README.md) each point links, and from it the records. Why so much work went into a file that cannot answer the question it was built around: [why and how](docs/explainers/why-and-how.md).

## Status

Pipeline closed ([Phase 4 closure](docs/audit/phase4-closure.md)); correspondence phase closed ([correspondence evidence](docs/audit/correspondence-evidence.md)). Decisions are recorded in [`docs/decisions`](docs/decisions); audit evidence and checks are in [`docs/audit`](docs/audit). The original course project is preserved, archived, at [`stress-dw-legacy`](https://github.com/CarpinetiOctavio/stress-dw-legacy).

## What this repository shows

### 1. Two errors in the course version, found, explained and fixed with tests

**Fan-out.** A dimension of the course version stored a flag computed from a column it did not store, so each response matched more than one of its rows and was counted once per match. The rebuild stores in each dimension only what its key determines, and tests confirm that no join multiplies rows ([fan-out](docs/explainers/fan-out.md)).

![Top: the legacy Dim_Sintomas stores four symptom columns and a flag that depends on Days_Indoors, which it does not store, so two rows share the same four values with different flags, and one response matches both rows and the join counts it twice. Bottom: the rebuild stores the four columns in dim_symptoms and Days_Indoors in dim_isolation, one response matches one row in each, and the two conditions are computed at query time. Illustrative rows.](docs/specification/figures/dimension-fan-out.svg)

*A flag computed from an unstored column made one response match more than one row ([fan-out](docs/explainers/fan-out.md)).*

**Average of rates.** The course version averaged stored percentages, so a row behind a few records weighed as much as a row behind many. The rebuild stores no rate and sums numerators and denominators for a coarser cut, and tests confirm both ([average of rates](docs/explainers/average-of-rates.md)).

![Top: the legacy query averages porcentaje_tratamiento over two aggregated rows, 90.0 from 9 treated of 10 records and 50.0 from 500 of 1,000, and gets 70.0: each row weighs the same, whatever the number of records behind it. Bottom: the rebuild stores no rate; a coarser cut sums the numerators and the denominators of the finer cells, 509 over 1,010, and gets 0.504 (50.4%): each record weighs the same. Illustrative rows.](docs/specification/figures/average-of-rates.svg)

*An average of rates weighs each row the same; summed numerators and denominators weigh each record the same ([average of rates](docs/explainers/average-of-rates.md)).*

### 2. The rebuilt warehouse

One row per survey response, every indicator computed at query time from the stored rows, all acceptance checks passing, and two full reloads giving byte-identical outputs ([the warehouse](docs/explainers/the-warehouse.md)).

![The star schema: fact_response, one row per staged response, holds its primary key response_id, eight foreign keys and treatment; each foreign key references the surrogate primary key of the same name in one of eight dimensions, and each dimension is shown with its natural key.](docs/specification/figures/star-schema.svg)

*One fact row per response; one dimension row per key ([the warehouse](docs/explainers/the-warehouse.md)).*

### 3. The source file is two sources joined

Checks show that its symptom columns match a separately published dataset, so the file is read as two sources joined. A question that relates the two groups shows how the sources were combined, not a relationship among respondents. The question on time spent indoors stays within one group, so its columns come from one source, and it can be answered, though its output is still not a finding about any population ([decision on the project's position](docs/decisions/0001-position-as-portfolio-project.md)); the help-seeking question relates the two, so it cannot ([two sources](docs/explainers/two-sources.md)).

![A matrix of the nine business questions against the 17 source columns, split into two column groups: group 1, the eight columns whose names are in the OSMI 2014 schema, and group 2, the eight symptom columns and Occupation, matched to RHMCD-20. Eight questions use columns from both groups; only Q5, on time spent indoors, uses columns from group 2 alone.](docs/audit/figures/one-question-of-nine.svg)

*Only the question on time spent indoors stays within one column group ([two sources](docs/explainers/two-sources.md)).*

## How it was evaluated

The criteria each output had to meet were committed before the output was seen, and the values already in the repository before that commit are declared. Where the method overreached is recorded as plainly as where it held ([how it was evaluated](docs/explainers/how-it-was-evaluated.md)). The reasons behind the method are also explained by analogy, in the [concept transfers](docs/concept-transfers/README.md).

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

The source file is obtained separately and verified before any load; see [`staging.md`](docs/specification/staging.md#extraction). The warehouse is built with `uv run python -m stress_dw.pipeline` once the source file is in place, and tests are run with `uv run pytest` ([Phase 4 closure, section 2](docs/audit/phase4-closure.md#2-reproducing-this)). The full output of every indicator, with its hash, is in [`docs/audit/correspondence-evidence/`](docs/audit/correspondence-evidence/); the cells each question reads are in the [correspondence evidence, section 4](docs/audit/correspondence-evidence.md#4-questions).

Code style is in [`docs/code-conventions.md`](docs/code-conventions.md).

## AI Disclosure

Every ADR names its decision-makers in its frontmatter; no language model appears in any. Log entries carry no such field ([LOG-004](docs/decisions/log/LOG-004-decision-log-and-lessons.md)). Language models (Claude, in chat sessions and through Claude Code) were used to draft and check text and code. From commit `be0d686` on, every commit other than a pull-request merge commit carries a `Co-Authored-By` trailer for that use; earlier commits record it irregularly.

## License

MIT for the code and documentation in this repository, except the copies of published works in `docs/references/`, which keep their own licences ([stored copies](docs/references/README.md#stored-copies)). The dataset is not included and is not covered by this license.
