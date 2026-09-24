---
status: "accepted"
date: 2026-09-20
decision-makers: Octavio Carpineti
---

# Rebuild the pipeline from scratch instead of continuing on the legacy codebase

## Context and Problem Statement

The legacy project (written in Spanish for the university course *Base de Datos II*, UCC) implements a Hefesto-based dimensional model over a Kaggle mental-health dataset of survey-style records whose provenance is undocumented (see ADR-0001): a star schema (one fact table, eight dimensions) in MySQL, a six-script Python ETL, and a Looker Studio report. The legacy ETL log (`logs/etl_log.txt`) has entries on 6, 8 and 9 November 2025. It records the raw CSV load (292,364 records, 17 columns) and cleaning to 290,051 records (2,313 rows removed as exact duplicates across all 17 columns, including `Timestamp`; no other rule removed rows) on 6 November; two staging loads of 290,051 records on 9 November (13:10 and 22:01; the staging count after the second load is still 290,051); and the fact-table load of 350,699 aggregated records on 9 November at 22:07. The log records no timezone. The repository has two commits, both dated 13 November 2025 (UTC-3); the last is [`f2308d2`](https://github.com/CarpinetiOctavio/stress-dw-legacy/commit/f2308d29217c8130a14875d7dad7070272b92d28).


A later audit of the legacy report found defects that originate in the specification, not in isolated bugs (see Findings). Should the project continue on the legacy codebase, or be rebuilt?

## Findings

| ID | Finding | Evidence | Status |
|----|---------|----------|--------|
| F1 | **Grain inconsistency (fan-out) in `Dim_Sintomas`.** The dimension stores five columns, but the formula of its derived column depends on `days_indoors`, which is not stored. Over the four stored source columns the maximum is 3×3×2×3 = 54 combinations (270 if `days_indoors` is included); the report states ~259 combinations and 350,699 fact rows from 290,051 staged records. | Report, Phase 3 (`Dim_Sintomas`) and Phase 4 (scripts 3 and 4) | Established at documented-schema level. Quantification against the database pending (`docs/audit/legacy-audit.md`). |
| F2 | **Pre-aggregated ratios without numerators or denominators.** The fact table stores percentages; the report's sample query averages them (`AVG(porcentaje_estres)`), an unweighted mean of ratios. The Looker Studio chart on treatment by gender applies `AVG` to these columns. | Report, Phase 3 (fact table) and sample query; Looker Studio report configuration | Established (report text and report configuration). |
| F3 | **Indicators 14–16 do not measure what their names claim.** No comparison group for "unrecognized symptoms"; "Maybe" treated inconsistently with the report's own granularity section; "Not sure" counted as an available resource; "postponement" defined without any time dimension. The report also reads two variables differently from the uploader's descriptions: it reads `treatment` as "currently in treatment" (the description reads "Have you sought treatment for a mental health condition?") and `mental_health_interview` as "participated in a mental-health interview" (the description reads "Would you bring up a mental health issue with a potential employer in an interview?"). | Report, Phase 1 (Q7, 7.1, 7.2), Phase 2 (indicator formulas) and Phase 3 (`Dim_Acceso`); Kaggle Data Card, [columns 2](../audit/evidence/kaggle-datacard-columns-2-2026-09-19.png) and [4](../audit/evidence/kaggle-datacard-columns-4-2026-09-19.png) (retrieved 2026-09-19) | Established against the report text and the uploader's descriptions. The other variables involved (`care_options` and the symptom columns) have no source description (ADR-0001, P6). |
| F4 | **Internal documentation inconsistencies.** The fact-table structure lists `id_historial` twice (for the occupation FK); `Dim_Tiempo` was expected to hold 30–36 periods but the report states 13 loaded; 36 countries are documented but 35 reported as loaded. | Report, Phase 3 and Phase 4 | Established in the report. Not checked against code or database. |

Dataset provenance is a separate finding and does not depend on the codebase; it is addressed in ADR-0001.

---

### Addendum (2026-09-23)
F3's description of the legacy's misreading of mental_health_interview is grounded in the report's own text, which treats the field as participation/exposure ("ha participado en entrevista de salud mental"). At the time the legacy model was designed, the field was treated as indicating whether a person had gone through an interview that determined they were mentally unwell — a diagnostic or assessment event, not mere attendance. Rebuilding from scratch, per ADR-0003, this reading is corrected: the field is read according to its Kaggle-documented description ("Would you bring up a mental health issue with a potential employer in an interview?"), an attitudinal disclosure-willingness item, not an exposure or diagnostic event; the new pipeline operates on this corrected reading rather than the original one. This addendum records the original treatment of the field for traceability. It does not change F3's status — F3 remains Established against the report's text.

---

## Decision Drivers

* F1 and F2 are defects in the specification of grain and measures; they propagate through schema, ETL and reporting.
* The audit is only reproducible against an unmodified legacy state, so the legacy must stay citable as it was.
* Lessons to carry over: `treatment` modeled as a measure, not a dimension attribute (the legacy corrected this late: Phase 3, "Dim_Acceso: Corrección" (Spanish: "Dim_Acces: Correction")); additive measures; explicit grain.
* The new repository is written in English from the first commit; the legacy stays in Spanish.

## Considered Options

1. Continue on the legacy codebase (refactor in place).
2. Patch the legacy repository in place for F1–F4, keeping its history.
3. Copy the legacy code into a new repository and refactor there.
4. Rebuild from scratch on a corrected written specification; archive the legacy as a reference; inherit no code.

## Decision Outcome

Chosen option: "Rebuild from scratch on a corrected written specification", because F1 and F2 sit in the design of grain and measures rather than in isolated lines of code, the legacy must remain unmodified to serve as the audit's reference (the only addition permitted is a superseded notice), and starting from a written specification lets each finding be closed with a test.

### Consequences

* Good, because every finding maps to an acceptance test instead of an in-place fix.
* Good, because the legacy history and the audit stay verifiable (tag `legacy-original`).
* Bad, because it costs more time than patching.
* Bad, because no legacy figure can be cited as a current result until reproduced in the new repository.

### Confirmation

* `docs/audit/legacy-audit.md` holds the queries and counts quantifying F1–F4.
* The specification maps each finding to a test: every natural-key group in staging resolves to exactly one row per dimension (no fan-out); the fact table reconciles with staging; the fact table stores additive measures and ratios are computed at query time from explicit numerators and denominators; each indicator definition names a construct its variables can support.
* A post-build audit checks the implementation against the specification with queries and counts.

## Pros and Cons of the Options

### Continue on the legacy codebase
* Good, because it is the fastest path.
* Bad, because it preserves the grain and measure design that causes F1 and F2.

### Patch the legacy repository in place
* Good, because it keeps a single history.
* Bad, because it destroys the unmodified reference the audit relies on.

### Copy the legacy code into a new repository
* Good, because it reuses working ETL pieces.
* Bad, because the inherited structure anchors the design that contains the defects.

### Rebuild from scratch on a corrected specification
* Good, because it addresses the findings at their source and keeps the legacy intact.
* Bad, because of the rebuild cost.

## More Information

* Legacy mirror at the original state: [`stress-dw-legacy@legacy-original`](https://github.com/CarpinetiOctavio/stress-dw-legacy/tree/legacy-original) (`f2308d29217c8130a14875d7dad7070272b92d28`).
* Original repository: [`OctavioCarpineti/DW_DB2`](https://github.com/OctavioCarpineti/DW_DB2).
* Related: [ADR-0001](0001-position-as-portfolio-project.md).

