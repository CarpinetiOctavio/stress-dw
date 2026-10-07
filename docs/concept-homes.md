# Concept homes

Each concept used in more than one place has one home: the document and section where it is explained ([writing conventions, rule 4](writing-conventions.md#4-introduce-before-use-one-home-per-concept)). Every other place links to the home instead of restating it. This list names the homes; a change of home updates this list in the same change. The reasoning behind the list is in [LOG-010](decisions/log/LOG-010-concept-home-map.md).

A decision record is a home only where the concept is the decision itself, or where no living document explains it.

| # | Concept | Home | Reason |
|---|---------|------|--------|
| 1 | Status of each check of the legacy audit | [`audit/legacy-audit.md`, Checks](audit/legacy-audit.md#checks) | The audit table records each check's method and result; a status changes only there. |
| 2 | Status of Fase 4 (English: "Phase 4"; see [`methodology.md`](methodology.md)) | [`audit/phase4-closure.md`, Status](audit/phase4-closure.md#1-status) | The closure record is dated and tied to a commit. |
| 3 | `explicit_recognition` and `symptom_cluster` | [`specification/definitions.md`](specification/definitions.md#explicit_recognition), both definitions | The specification's definitions are the contract the code implements. |
| 4 | Validity caveat of `symptom_cluster` | [`specification/definitions.md`, `symptom_cluster`](specification/definitions.md#symptom_cluster) | A caveat travels by link from one home. |
| 5 | Population filter of indicators 15 and 16 | [`specification/definitions.md`, multi-level self-report rule](specification/definitions.md#multi-level-self-report-rule) (the filter is not a fold) and [`specification/indicators.md`](specification/indicators.md) (the population) | Two concepts, two homes, each pointing to the other. |
| 6 | Exposure of indicator values | [ADR-0011](decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), rules 1, 2 and 4 | The rule is a decision; its record is its home. |
| 7 | Source columns: 17 in the file, 13 modeled, 4 not | [`specification/sources.md`, Column map](specification/sources.md#column-map) | The only table that lists the 17 columns with their destination. |
| 8 | Columns the source documents | [`dataset-provenance.md`, Column documentation](dataset-provenance.md#column-documentation) | The provenance record holds the source's text and its captures. |
| 9 | Fact grain | [`specification/fact-table.md`, Grain](specification/fact-table.md#grain) | The specification states the grain the load implements. |
| 10 | Dimension list | [`specification/dimensions.md`, Row set](specification/dimensions.md#row-set) | One table declares every dimension and its natural key. |
| 11 | Voice | [`writing-conventions.md`, rule 2](writing-conventions.md#2-voice) | The convention is the rule; the voice test implements part of it. |
| 12 | Licenses of the dataset and of the related deposits | [`dataset-provenance.md`, Source](dataset-provenance.md#source) and [How to obtain the file](dataset-provenance.md#how-to-obtain-the-file) | The provenance record holds the captures and the quotations. |
| 13 | Evidence conventions (citable sources, captures, one row per artifact) | [ADR-0012](decisions/0012-cite-only-frozen-and-versioned-sources-as-evidence.md), rules 1–4 | The rule is a decision. |
| 14 | Load rule | [`specification/sources.md`, Load rule](specification/sources.md#load-rule) | One home per rule; the staging part already points to it. |
| 15 | Deduplication rule | [`specification/staging.md`, Deduplication](specification/staging.md#deduplication) | The staging part specifies the rule the code implements; ADR-0008 holds its reasoning. |
| 16 | Staged and raw row counts | [`specification/staging.md`, Row set](specification/staging.md#row-set) | The staging part fixes the count; other documents check it, report it, or record the legacy's own count. |
| 17 | Results of check A13 | [`audit/legacy-audit.md`, Checks](audit/legacy-audit.md#checks), row A13 | Results live with the check. |
| 18 | The source's description of `mental_health_interview` | [`dataset-provenance.md`, Column documentation](dataset-provenance.md#column-documentation) | The provenance record carries the Data Card's text and its capture. |
| 19 | Wording of the business questions | [ADR-0006, Final business questions](decisions/0006-final-questions-and-indicators.md#final-business-questions), with [ADR-0004](decisions/0004-revise-business-questions.md) for the revisions | The decision records fix the wording; the specification repeats it by rule. |
| 20 | Default of `low_n_threshold`, and display of flagged cells | [`specification/patterns.md`, Reporting rules](specification/patterns.md#reporting-rules) | The parameter and the display rule are part of the reporting rules. |
| 21 | Country-to-region mapping; value domains | [`specification/country-region-mapping.md`](specification/country-region-mapping.md); [`specification/sources.md`, Value domains](specification/sources.md#value-domains) | The specification holds the fixed tables; the code transcribes them. |
| 22 | Test commands while indicator values may not be exposed | [`audit/phase4-closure.md`, Reproducing this](audit/phase4-closure.md#2-reproducing-this) | The reproduction section already holds the commands; ADR-0011 links it. |
| 23 | The legacy repository is not modified beyond its superseded notice | [ADR-0000, Decision Outcome](decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md#decision-outcome), with its [addendum on the notice](decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md#addendum-2026-10-04) | The decision record permits the one change; its addendum records it. |
| 24 | Outputs are test-bench outputs, not findings about a population | [ADR-0001, Consequences](decisions/0001-position-as-portfolio-project.md#consequences) (Constraint) | The decision record is the source. |
| 25 | SHA-256 of the source file | [`dataset-provenance.md`, Identity of the file](dataset-provenance.md#identity-of-the-file) | The identity record holds both hashes and how they were computed. |
| 26 | Hypotheses H1 and H3 | [ADR-0001, Hypotheses](decisions/0001-position-as-portfolio-project.md#hypotheses-not-findings) | No living document explains them; corrections go by addendum. Their tests live in the legacy audit. |
| 27 | Reading of `mental_health_interview` | [`conceptual-framework.md`, section 4](conceptual-framework.md#4-variable-mapping-to-andersens-behavioral-model) | The framework maps each variable. |
| 28 | `treatment` read as lifetime | [`conceptual-framework.md`, section 4](conceptual-framework.md#4-variable-mapping-to-andersens-behavioral-model) | As row 27. |
| 29 | Identifiers of findings, hypotheses, checks, log entries and lessons | [`decisions/README.md`, Finding and hypothesis IDs](decisions/README.md#finding-and-hypothesis-ids) | Writing conventions, rule 7, names it as the home. |
| 30 | Addenda to accepted decision records | [`decisions/README.md`, Addenda to accepted decision records](decisions/README.md#addenda-to-accepted-decision-records) | The README holds the conventions of decision records ([LOG-009](decisions/log/LOG-009-addendum-convention-home.md)). |
| 31 | Reading rule for figures derived from the source file | [LOG-039](decisions/log/LOG-039-reading-rule.md) | ADR-0011 and ADR-0012 hold parts; the log entry that decides the rule holds the whole. |
| 32 | Recording standard of decisions; format of lessons | [`decisions/log/README.md`, Recording standard](decisions/log/README.md#recording-standard); [`audit/lessons/README.md`, Format](audit/lessons/README.md#format) | Decided in [LOG-004](decisions/log/LOG-004-decision-log-and-lessons.md). |
| 33 | Correspondence evidence document | open: pending for the correspondence phase ([LOG-021](decisions/log/LOG-021-evidence-document-to-correspondence-phase.md)) | Defined in the correspondence phase. |
| 34 | Corrections of the legacy region mapping | [`specification/country-region-mapping.md`, Differences from the legacy mapping](specification/country-region-mapping.md#differences-from-the-legacy-mapping) | The mapping states its own differences. |
| 35 | Values about the data readable in a capture | the capture's evidence row: [`dataset-provenance.md`, Evidence](dataset-provenance.md#evidence), or [`audit/legacy-audit.md`, Evidence](audit/legacy-audit.md#evidence) | The value stays in the capture; its row states what the capture shows. Scope: values about the data; a check's own computed result has its own provenance ([LOG-011](decisions/log/LOG-011-adr-0012-scope-of-capture-values.md)). |
| 36 | Indicator names | [`specification/indicators.md`](specification/indicators.md) | The specification is the contract outputs and code follow. |
| 37 | Reading of `care_options` | [`conceptual-framework.md`, section 4](conceptual-framework.md#4-variable-mapping-to-andersens-behavioral-model) | The framework maps each variable. |
| 38 | Column groups of H1 | [LOG-040](decisions/log/LOG-040-h1-column-groups.md) | The decision that fixes the partition holds it; the audit table and the reporting rules link to it. |
