# The warehouse

What the rebuild built, and how its correctness is checked.

![The star schema: fact_response, one row per staged response, holds its primary key response_id, eight foreign keys and treatment; each foreign key references the surrogate primary key of the same name in one of eight dimensions, and each dimension is shown with its natural key.](../specification/figures/star-schema.svg)

*One fact row per staged response, with a foreign key to each dimension; each dimension holds one row per natural key ([`dimensions.md`, Row set](../specification/dimensions.md#row-set)).*

* **Method.** The business questions and their indicators were derived with the [Hefesto methodology](../methodology.md) and revised after the audit ([ADR-0004](../decisions/0004-revise-business-questions.md)); each indicator is one SQL statement ([`indicators.md`](../specification/indicators.md)).
* **Model.** A star schema: one fact table at response grain, where one row is one survey response and no column identifies a respondent ([`fact-table.md`, Grain](../specification/fact-table.md#grain)), and its dimensions ([`dimensions.md`](../specification/dimensions.md#row-set)). Every indicator is computed at query time, and nothing derived is stored beyond dimension attributes ([model conventions](../specification/definitions.md#model-conventions); [ADR-0007](../decisions/0007-person-grain-fact-table-and-dimension-grain-rule.md)). Why the star is kept: [ADR-0013](../decisions/0013-keep-star-schema-add-flat-consumption-view.md).
* **Pipeline.** Extraction, cleaning and deduplication in Python (pandas); the schema, the loads and the indicators in SQL under [`src/stress_dw/sql/`](../../src/stress_dw/sql/), run from Python on [DuckDB](../decisions/0009-use-duckdb-as-database-engine.md). Staging is loaded in one transaction; the dimensions and the fact table are then dropped, recreated and reloaded in a second one ([load order](../specification/staging.md#load-order-and-transactions); [ADR-0010](../decisions/0010-reload-dimensions-and-fact-in-one-transaction.md)).
* **Acceptance.** Checks C1 to C11 pass ([`acceptance.md`](../specification/acceptance.md); [Phase 4 closure, section 4](../audit/phase4-closure.md#4-acceptance-checks-c1c11)).
* **Reproducibility.** Two full reloads give byte-identical indicator outputs ([correspondence evidence, section 1](../audit/correspondence-evidence.md#1-reproduction)).
* **Outputs.** The full output of every indicator, with its hash, is in [`audit/correspondence-evidence/`](../audit/correspondence-evidence/); the cells each question reads are in the [correspondence evidence, section 4](../audit/correspondence-evidence.md#4-questions).

The reasons behind the grain, the deduplication key and the reading of stress recognition are explained by analogy in the [concept transfers](../concept-transfers/README.md), each with its result here.
