# stress-dw

A star-schema data warehouse ([DuckDB](docs/decisions/0009-use-duckdb-as-database-engine.md), SQL, Python), built around a help-seeking question in mental health and evaluated against criteria committed before its indicator output was exposed. Checks show that the source file joins columns from two sources, so only one of the nine questions can be answered with it, and the repository shows why.

The original course design named mental-health professionals as the end users of its outputs, with the destigmatization of mental-health problems among its aims ([report at `legacy-original`](https://github.com/CarpinetiOctavio/stress-dw-legacy/blob/legacy-original/Informe%20DW/DW%20-%20Estr%C3%A9s%20y%20Salud%20Mental.pdf), pp. 5, 9 and 32). This rebuild keeps its help-seeking question (Q7), revised in [ADR-0004](docs/decisions/0004-revise-business-questions.md), and is built to show, for respondents with a convergent self-reported symptom profile, what share report having ever sought treatment, by their level of explicit stress recognition. It was built with the [Hefesto methodology](docs/methodology.md) and turns raw survey responses into indicators. The symptom profile it uses is self-reported, not a diagnosis ([`symptom_cluster`](docs/specification/definitions.md#symptom_cluster)).

It was rebuilt from scratch after an audit of the university course version found a dimension fan-out and averaged percentages ([ADR-0000](docs/decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md)). Checks run before the indicator output was read ([ADR-0011](docs/decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), rule 4) show that the file combines columns from two sources: its symptom columns match a separately published dataset ([legacy audit](docs/audit/legacy-audit.md), rows A5, A6 and A10). Questions that relate columns from the two sources therefore cannot be answered with this file. The help-seeking question is one of them: `treatment` belongs to one column group, and stress recognition and the symptom profile to the other ([LOG-040](docs/decisions/log/LOG-040-h1-column-groups.md)). The [correspondence evidence](docs/audit/correspondence-evidence.md) finds that one of the nine questions can be answered, the one on time spent indoors, whose columns all come from one source; the other eight relate the two sources, and three of them also have too few responses, or none, in some cells. The indicator outputs reproduce exactly: what fails is not the computation but what this file can support.

> **Provenance.** The source file's origin is undocumented, and no output of this project is a finding about any population ([ADR-0001](docs/decisions/0001-position-as-portfolio-project.md); [details](#data-and-provenance)).

![A matrix of the nine business questions against the 17 source columns, split into two column groups: group 1, the eight columns whose names are in the OSMI 2014 schema, and group 2, the eight symptom columns and Occupation, matched to RHMCD-20. Eight questions use columns from both groups; only Q5, on time spent indoors, uses columns from group 2 alone.](docs/audit/figures/one-question-of-nine.svg)

*Eight of the nine questions relate columns from both groups; only the one on time spent indoors stays within one ([evidence, section 4](docs/audit/correspondence-evidence.md#4-questions)).*

## Status

Pipeline closed ([`phase4-closure.md`](docs/audit/phase4-closure.md)); correspondence phase closed ([correspondence evidence](docs/audit/correspondence-evidence.md)). Decisions are recorded in [`docs/decisions`](docs/decisions); audit evidence and checks are in [`docs/audit`](docs/audit).

## Start here

* [Correspondence criteria](docs/audit/correspondence-criteria.md): what each question's indicator output had to allow for the question to correspond, committed at `ed49662` (#75) and amended twice, both times before any result of checks A5, A6 or A10 ([section 7](docs/audit/correspondence-criteria.md#7-amendments)).
* [Concept transfers](docs/concept-transfers/README.md): why the method is built as it is, explained through concepts from other fields and demonstrated on this repository's artifacts, each with the point where the analogy breaks ([ADR-0014](docs/decisions/0014-explain-the-method-through-declared-concept-transfers.md)).
* [Scope and proportion](docs/audit/lessons/scope-and-proportion.md): where the method overreached, with effort out of proportion to what it could change (LSN-014, LSN-015).

## Concepts and results

Each row pairs a concept with what it changed in this repository and the evidence of that change.

| Concept | Applied here | Result |
|---|---|---|
| [Dimension grain rule](docs/specification/definitions.md#dimension-grain-rule) | Every column a dimension stores depends only on that dimension's key. The legacy symptoms dimension stored an inferred stress flag whose formula used `days_indoors`, a column it did not store, so every staged record matched more than one row of that dimension; the rebuild splits the flag into two conditions computed at query time ([`explicit_recognition`](docs/specification/definitions.md#explicit_recognition), [`symptom_cluster`](docs/specification/definitions.md#symptom_cluster)) | Checked by C1 and C2 ([`acceptance.md`](docs/specification/acceptance.md)); the legacy fan-out is measured in [legacy audit, A2](docs/audit/legacy-audit.md#checks) |
| [Additive measures; roll-up rule](docs/specification/definitions.md#roll-up-rule) | No rate is stored; a rate is a numerator over a denominator, and a coarser cut sums both | The legacy average of ratios set against the weighted rate in [legacy audit, A7](docs/audit/legacy-audit.md#checks); cell denominators checked against an independent count by C8 |
| [Grain](docs/concept-transfers/grain-and-cross-sections.md) | A fact row is one survey response; no column identifies a respondent, and the months are not a panel | The grain renamed to response grain ([ADR-0007, addendum of 2026-10-04](docs/decisions/0007-person-grain-fact-table-and-dimension-grain-rule.md#addendum-2026-10-04)); the first question reworded from how a share "evolves" to how it differs across months ([ADR-0004](docs/decisions/0004-revise-business-questions.md)) |
| [Sets and multisets](docs/concept-transfers/sets-and-multisets.md) | Rows equal on every column but `Timestamp` may come from different respondents, so deduplication keys on all 17 source columns | Deduplicating on the 13 modeled columns would merge rows the source keeps apart ([ADR-0008, Findings, G1](docs/decisions/0008-staging-deduplication-grain.md#findings)); every dropped row is an exact duplicate, checked by C11 |
| [Proxy](docs/concept-transfers/proxy-and-construct-validity.md) | Stress recognition is read from a self-report item, and the symptom profile is self-reported, not a diagnosis | The premise is stated where the condition is defined ([LOG-012](docs/decisions/log/LOG-012-explicit-recognition-premise.md)); no verdict states validity ([criteria, section 0](docs/audit/correspondence-criteria.md#0-scope)) |
| [Pre-registration; data leakage](docs/concept-transfers/preregistration-and-data-leakage.md) | The correspondence criteria were committed before the indicator output was exposed | Values of the same quantities already in the repository before that commit are listed and declared; the first confirmation item is recorded as not met ([evidence, section 3](docs/audit/correspondence-evidence.md#3-post-commit-exposures)) |
| [Boundary cases](docs/concept-transfers/boundary-cases.md) | Two fresh language-model sessions, of the same family as the models that drafted the criteria, applied them to boundary cases against a key written by a co-drafting party | In the final round, both readers gave the key's verdict on every case; the agreement shows one reading for readers of that family, not for every reader ([criteria, section 0](docs/audit/correspondence-criteria.md#0-scope)) |
| [Two column groups](docs/decisions/log/LOG-040-h1-column-groups.md); [H1](docs/decisions/0001-position-as-portfolio-project.md#hypotheses-not-findings) | The file joins columns from two sources; a question that relates them cannot be answered with it | A10 matches the symptom columns to a published dataset ([legacy audit, Reading branch](docs/audit/legacy-audit.md#reading-branch)); one question of nine corresponds ([evidence, section 4](docs/audit/correspondence-evidence.md#4-questions)) |
| [Overfitting](docs/concept-transfers/overfitting.md); [parsimony](docs/concept-transfers/parsimony.md) | A rule whose verdict changed no correspondence verdict was patched after each review | A stopping rule set in advance ended the process, and the documentary verdict was removed ([LOG-051](docs/decisions/log/LOG-051-stopping-rule-documentary-audit-readings.md); [LSN-014 and LSN-015](docs/audit/lessons/scope-and-proportion.md)) |

![Top: the legacy Dim_Sintomas stores four symptom columns and a flag that depends on Days_Indoors, which it does not store, so two rows share the same four values with different flags, and one response matches both rows and the join counts it twice. Bottom: the rebuild stores the four columns in dim_symptoms and Days_Indoors in dim_isolation, one response matches one row in each, and the two conditions are computed at query time. Illustrative rows.](docs/specification/figures/dimension-fan-out.svg)

*The legacy dimension's flag depended on a column it did not store, so records matched several rows; the rebuild stores only what its key determines ([legacy audit, A2](docs/audit/legacy-audit.md#checks)).*

[`docs/concept-homes.md`](docs/concept-homes.md) is the index of concept homes.

## What was built

![The star schema: fact_response, one row per staged response, holds its primary key response_id, eight foreign keys and treatment; each foreign key references the surrogate primary key of the same name in one of eight dimensions, and each dimension is shown with its natural key.](docs/specification/figures/star-schema.svg)

*One fact row per staged response, with a foreign key to each of the eight dimensions; each dimension holds one row per natural key ([`dimensions.md`, Row set](docs/specification/dimensions.md#row-set)).*

* **Model.** A fact table at response grain ([`fact-table.md`, Grain](docs/specification/fact-table.md#grain)) and eight dimensions ([`dimensions.md`, Row set](docs/specification/dimensions.md#row-set)); every indicator is computed at query time, and nothing derived is stored beyond dimension attributes ([model conventions](docs/specification/definitions.md#model-conventions); [ADR-0007](docs/decisions/0007-person-grain-fact-table-and-dimension-grain-rule.md)).
* **Pipeline.** Extraction, cleaning and deduplication in Python (pandas); the schema, the loads of the dimensions and the fact table, and the sixteen indicators in SQL under [`src/stress_dw/sql/`](src/stress_dw/sql/), run from Python. Staging is loaded in one transaction; then the eight dimensions and the fact table are dropped, recreated and reloaded in a second one ([load order](docs/specification/staging.md#load-order-and-transactions); [ADR-0010](docs/decisions/0010-reload-dimensions-and-fact-in-one-transaction.md)).
* **Questions and indicators.** Nine business questions and sixteen indicators, each indicator one SQL statement ([`indicators.md`](docs/specification/indicators.md)).
* **Acceptance.** Checks C1 to C11 ([`acceptance.md`](docs/specification/acceptance.md)), run by the test suite when the source file is present ([Phase 4 closure, section 4](docs/audit/phase4-closure.md#4-acceptance-checks-c1c11)).
* **Reproducibility.** Two full reloads give byte-identical indicator outputs ([correspondence evidence, section 1](docs/audit/correspondence-evidence.md#1-reproduction)).

## What a working resource would need

A resource that could answer the questions that relate the two sources would record symptoms and treatment from the same respondent ([criteria, section 3.2](docs/audit/correspondence-criteria.md#32-branch-h1-holds)), with a documented provenance ([ADR-0001](docs/decisions/0001-position-as-portfolio-project.md)), and with the measures this file lacks, such as stigma, a need assessed rather than self-reported, and more than one observation of the same respondent over time.

* [Conceptual framework, section 5, "What this dataset cannot measure"](docs/conceptual-framework.md#5-what-this-dataset-cannot-measure).
* [`legacy-audit.md`, Reading branch](docs/audit/legacy-audit.md#reading-branch): why every result that relates the two groups is read under "H1 holds".
* [LOG-046](docs/decisions/log/LOG-046-user-of-the-outputs.md): what the outputs cannot serve under ADR-0001.

## Background

- The original course project is preserved, archived, at [`stress-dw-legacy`](https://github.com/CarpinetiOctavio/stress-dw-legacy).
- [ADR-0000](docs/decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md) explains why the project was rebuilt from scratch instead of continued.

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

## AI Disclosure

Every ADR names its decision-makers in its frontmatter; no language model appears in any. Log entries carry no such field ([LOG-004](docs/decisions/log/LOG-004-decision-log-and-lessons.md)). Language models (Claude, in chat sessions and through Claude Code) were used to draft and check text and code. From commit `be0d686` on, every commit other than a pull-request merge commit carries a `Co-Authored-By` trailer for that use; earlier commits record it irregularly.

## License

MIT for the code and documentation in this repository, except the copies of published works in `docs/references/`, which keep their own licences ([stored copies](docs/references/README.md#stored-copies)). The dataset is not included and is not covered by this license.
