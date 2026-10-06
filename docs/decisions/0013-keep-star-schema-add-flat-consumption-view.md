---
status: "accepted"
date: 2026-09-29
decision-makers: Octavio Carpineti
---

# Keep the star schema as the definition and integrity layer, add a flat view as the consumption interface, and defer a reduced star

## Context and Problem Statement

The warehouse is a star schema: one fact table at person grain and eight dimensions ([`dimensions.md`](../specification/dimensions.md)). No decision record weighed that form against alternatives. The star was adopted in the legacy project, in the logical-model phase of the methodology ("Fase 3", English: "Phase 3"; see [`methodology.md`](../methodology.md)), and carried into the rebuild. [ADR-0007](0007-person-grain-fact-table-and-dimension-grain-rule.md) compares options for the grain, for what a dimension may store and for where derived conditions live, not for the form of the schema (M3). The only written reasons for the star are the five the legacy report gave (M1). This ADR records the decision retrospectively, weighs the alternatives, and states what the star does and does not provide in this project.

Which schema form should implement the warehouse, and what should sit between it and the tools that consume it?

## Findings

Finding IDs use a new letter, `M` (model): this ADR concerns the form of the schema, which none of the letters in use (`F`, `P`, `E`, `G`, `K`, `S`) covers.

| ID | Finding | Evidence | Status |
|----|---------|----------|--------|
| M1 | **The legacy report justified the star with five general reasons:** simplicity for developers and end users; faster queries from fewer joins; compatibility with BI tools; ease of maintenance; and the methodology's own recommendation. The speed reason is stated against a normalized transactional model, not against a flat table. | Page 32 of the PDF report at [`legacy-original`](https://github.com/CarpinetiOctavio/stress-dw-legacy/tree/legacy-original) (section justifying the star schema) | Established |
| M2 | **The legacy pipeline exported the star as one flat file for the BI tool.** The export script joins the fact table with all dimensions and writes a flat CSV of 350,699 rows, described in its docstring as a flat export for Power BI. | `python/06_exportar_powerbi.py` and `CSV procesado /dw_salud_mental.csv` at `legacy-original` | Established |
| M3 | **ADR-0007's options concern grain, not the form of the schema, and it leaves the consumption layer unspecified.** Its three options are the legacy aggregated fact table, a minimal correction that keeps it, and the person-grain fact table. It states that a consumer that cannot join, such as a BI tool reading a single table, needs a view or a custom query, and that the consumption layer is not yet specified. | [ADR-0007](0007-person-grain-fact-table-and-dimension-grain-rule.md), Considered Options and Consequences | Established |
| M4 | **Most dimensions store only source values, and most derived columns are unread.** Five of the eight dimensions (`gender`, `family_history`, `occupation`, `access`, `symptoms`) store only values of the source answers. Seven derived columns exist: `month_name`, `period`, `quarter` and `semester` in `dim_time`, `region` in `dim_country`, `sort_order` and `duration_band` in `dim_isolation`. Three are read by an indicator query: `period` (indicators 2 and 4), `region` (5 and 6), `sort_order` (9 to 11). No query in `src/stress_dw/sql/indicators/` reads `month_name`, `quarter`, `semester` or `duration_band`. | [`dimensions.md`](../specification/dimensions.md); search of `src/stress_dw/sql/indicators/` for each column name at commit `af4996e` | Established |
| M5 | **Each indicator uses between one and five dimensions, all sixteen use `dim_symptoms`, and none uses all eight.** | Distinct `dim_*` names per file in `src/stress_dw/sql/indicators/` at commit `af4996e` | Established |
| M6 | **`symptom_cluster` spans two dimensions.** It is evaluated per fact row through `symptoms_id` and `isolation_id`. | [`definitions.md`](../specification/definitions.md#symptom_cluster) | Established |
| M7 | **Four of the 17 source columns are not modeled** (`self_employed`, `Changes_Habits`, `Mental_Health_History`, `Work_Interest`). Modeling one of them is an amendment to the specification. | [`sources.md`](../specification/sources.md), column map | Established |
| M8 | **Reducing the star would touch most of the repository.** At commit `af4996e` all sixteen indicator queries reference at least one of the six dimensions a reduction would move (`gender`, `family_history`, `occupation`, `access`, `isolation`, `symptoms`); `dim_symptoms` appears in 21 files under `src/`; acceptance checks C1, C5 and C7 are parametrized over the eight dimensions; at least ten documents state the number of dimensions, foreign keys or tables; and the reload evidence of ADR-0010 (E3) was measured against the current DDL. | Searches over `src/`, `tests/` and `docs/` at commit `af4996e`; [ADR-0009](0009-use-duckdb-as-database-engine.md), E3 | Established |

---

### Addendum (2026-10-04)
Decision Outcome and the option "Use a single flat table as the only model" attribute foreign-key enforcement to ADR-0009's E1. Since [ADR-0009's addendum of 2026-10-02](0009-use-duckdb-as-database-engine.md#addendum-2026-10-02), enforcement on insert rests on the captured documentation and enforcement on delete on E3 ([ADR-0009, Findings](0009-use-duckdb-as-database-engine.md#findings)); acceptance check C5 tests it. Both passages stand with those sources.

---

### Addendum (2026-10-06)
The addendum of 2026-10-04 carries the decision of [LOG-022](log/LOG-022-adr-0010-0013-addenda.md), which keeps its reasoning.

---

## Decision Drivers

* The project's purpose is to show dimensional modeling built with the Hefesto methodology, with traceability from the perspectives of a question to the dimensions of the model (M1).
* Integrity has to be enforced by the engine and the load, not assumed: closed domains through foreign keys (C5), one row per natural key (C1), and a load that aborts on a value outside its mapping (C6).
* The warehouse has to allow analysis beyond the sixteen indicators. What allows it is the person grain and the absence of stored ratios ([ADR-0007](0007-person-grain-fact-table-and-dimension-grain-rule.md)), together with the columns modeled (M7); it does not depend on the number of dimension tables.
* Consumers that read a single table need a flat interface (M2, M3).
* The correspondence phase ([ADR-0011](0011-preregister-correspondence-criteria-before-exposing-indicator-values.md)) tests the system as built; the model should not change while it is under test.
* Claims of extensibility or scalability need evidence, and none has been exercised.
* The cost of changing the model is high (M8) and buys no analytical capability.

## Considered Options

* Keep the star as built and add a flat view over it as the consumption interface.
* Reduce the star: merge `isolation` and `symptoms` into one dimension, move the dimensions that store only a source value into the fact table, and drop the derived columns no query reads.
* Extend the model with a second source through conformed dimensions.
* Use a single flat table as the only model.
* Use a snowflake schema.

## Decision Outcome

Chosen option: "Keep the star as built and add a flat view over it as the consumption interface", because it changes nothing in a system that is about to be tested, keeps the traceability and the engine-enforced integrity that justify the star in this project, and closes the consumption gap that both the legacy pipeline (M2) and ADR-0007 (M3) left open.

* **The star is the definition and integrity layer.** Dimension attributes such as `region` and `sort_order` are defined once, and domains are closed by foreign keys.
* **The flat view is the consumption interface.** A view stores nothing and computes at query time, consistent with ADR-0007. It exposes one row per response with every modeled column and the derived dimension attributes, so that a tool that reads a single table can explore beyond the sixteen indicators. The direction is decided here. Its specification and construction belong to the reporting layer, which is out of scope of [Fase 4](../audit/phase4-closure.md#6-explicitly-out-of-scope) and is done in a later change; until then ADR-0007's statement that the consumption layer is not specified holds.
* **The reduced star is deferred, not rejected.** It is the best-formed variant: each surviving dimension is read by a query, and `symptom_cluster` falls inside one dimension (M4 to M6). It is not adopted now because of its cost (M8), because it adds no analytical capability, because it changes the object under test, and because it weakens the one-to-one traceability from perspective to dimension. The conditions under which it is adopted are in Consequences.
* **The second source is postponed.** It depends on the outcome of checks A5, A6 and A10 on whether the file combines sources ([ADR-0001](0001-position-as-portfolio-project.md), H1), no indicator or question needs it, and its costs (the source's license, the mapping of value domains) are not yet assessed.
* **A single flat table is not adopted as the only model.** It is the simplest form for this workload and this ADR states that plainly. It is not adopted because it gives up traceability to the perspectives, and it moves domain enforcement from foreign keys, which ADR-0009 evidences (E1), to constraints for which no evidence has been collected.
* **The snowflake schema is not adopted.** The model has two hierarchies, country to region and month to quarter and semester, with 35 and 13 rows; separating them adds joins and keys without a benefit.

### Consequences

* Good, because the model under test does not change, and the correspondence phase can cite a stable pipeline.
* Good, because the star keeps its traceability and its engine-enforced integrity, and the consumption gap has a decided direction.
* Good, because the property that allows exploration beyond the indicators is attributed to where it comes from, the person grain and the absence of stored ratios, and not to the star.
* Bad, because the star costs more than a flat table to extend: a new column needs a dimension or an enlarged one, a foreign key, a load and checks, and the specification treats modeling an excluded column as an amendment (M7).
* Bad, because five dimensions store only source values and four derived columns are read by no query (M4): part of the model is structure without a query behind it.
* Bad, because performance is evidenced in neither direction. The report's speed reason (M1) is stated against a normalized transactional model; against a flat table the star needs more joins, and nothing has been measured.
* Bad, because four source columns are not modeled (M7), which limits exploration. This is a declared limit, not a decision to extend the model.
* Constraint: a reduction of the star is adopted only if (i) the correspondence evidence document is merged; (ii) its own decision record supersedes the parts of ADR-0007 it changes; (iii) every indicator output is preserved, shown by per-indicator hashes identical before and after (ADR-0011, rule 5), with the baseline recorded before the schema is touched; (iv) the specification is amended before the code; and (v) E3 is repeated against the new DDL, with evidence for the constraint that replaces a foreign key if a dimension moves into the fact table.
* Constraint: a design finding recorded by the correspondence phase, such as a cut the model cannot support, can reopen the model; indicator values as such do not. Because a reduction preserves every output, it cannot change a verdict of that phase. A change that alters outputs, such as modeling an excluded column or changing `symptom_cluster`, is outside this candidate and follows the amendment rule of ADR-0011.
* Constraint: the second source is considered only after A5, A6 and A10 are recorded and only if a question needs it. Until it is exercised, extensibility is this project's own interpretation, and no document presents the model as scalable or extensible as demonstrated.

### Confirmation

* [`dimensions.md`](../specification/dimensions.md), [`fact-table.md`](../specification/fact-table.md) and `CLAUDE.md` keep describing the model as built until a later decision record changes it; a change to the dimensions without one is a deviation.
* The consumption view, when built, is a view over the star with no stored data, so acceptance check C4 (no stored ratio or derived condition) keeps holding, and its specification is added under `docs/specification/` in the change that builds it.
* This ADR is revisited when the correspondence evidence document is merged: a follow-up records either a decision record that adopts a level of reduction or a note that keeps the model as built.

## Pros and Cons of the Options

### Keep the star as built and add a flat view over it

* Good, because nothing in the pipeline under test changes.
* Good, because the star keeps its traceability and its enforced integrity, and the view serves single-table consumers.
* Bad, because the star's extra structure has no query behind part of it (M4), and the view is one more artifact to specify and keep in step with the model.

### Reduce the star

* Good, because each surviving dimension is read by a query, and `symptom_cluster` falls inside one dimension, so it no longer spans two.
* Bad, because of its cost (M8) and because it adds no analytical capability.
* Bad, because it changes the object under test and weakens the one-to-one traceability from perspective to dimension.

### Extend the model with a second source

* Good, because conformed dimensions would then serve two facts, which is the situation in which dimensional modeling pays for itself.
* Bad, because it is not needed by any question, depends on the outcome of A5, A6 and A10, and adds work on licensing and on mapping value domains.

### Use a single flat table as the only model

* Good, because it is the simplest form for this workload: queries need no joins and nothing spans two dimensions.
* Bad, because it gives up traceability to the perspectives and moves domain enforcement to constraints without evidence (ADR-0009, E1).

### Use a snowflake schema

* Good, because it would normalize the two hierarchies.
* Bad, because it adds joins and keys for 35 and 13 rows.

### Dismissed without a full option

* **Fact constellation.** It needs more than one business process or grain. The model has one: a survey response. A second fact table could only be an aggregate, which is what the legacy stored and what produced F2.
* **Response-question grain.** One row per person and per question suits questionnaires that are large or that change. The indicators cross several answers of the same person (`symptom_cluster` needs three), which in that form needs self-joins or pivots.
* **Data Vault and Anchor modeling.** They target the integration of many sources with history and auditability. The model has one source and an immutable snapshot.

## More Information

* Related: [ADR-0000](0000-rebuild-from-scratch-instead-of-continuing-legacy.md) (F1, F2), [ADR-0001](0001-position-as-portfolio-project.md) (H1), [ADR-0007](0007-person-grain-fact-table-and-dimension-grain-rule.md), [ADR-0009](0009-use-duckdb-as-database-engine.md) (E1, E3), [ADR-0010](0010-reload-dimensions-and-fact-in-one-transaction.md), [ADR-0011](0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), [ADR-0012](0012-cite-only-frozen-and-versioned-sources-as-evidence.md).
* Frozen source: [`stress-dw-legacy@legacy-original`](https://github.com/CarpinetiOctavio/stress-dw-legacy/tree/legacy-original) (`f2308d29217c8130a14875d7dad7070272b92d28`).