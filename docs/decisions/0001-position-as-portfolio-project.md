---
status: "accepted"
date: 2026-09-20
decision-makers: Octavio Carpineti
---

# Position the project as a portfolio piece and do not pursue academic publication

## Context and Problem Statement

The project had two intended destinations: academic publication and a professional portfolio. The legacy course project was completed in November 2025 (ETL log entries of 6–9 November 2025; see [ADR-0000](0000-rebuild-from-scratch-instead-of-continuing-legacy.md)). In September 2026 an audit examined whether the dataset can support empirical claims. It found that the source documents neither the dataset's provenance nor most of its variables (see Findings). The dimensional model was designed around this file's columns, so resolving the provenance would mean working with a different dataset, that is, a different project. Should this project still pursue academic publication?

## Findings

All sources were retrieved on 2026-09-19. Captures are stored in `docs/audit/evidence/`.

| ID | Finding | Evidence | Status |
|----|---------|----------|--------|
| P1 | **The source declares no provenance.** The dataset page states only "I collected this dataset from the internet". Collection methodology, temporal coverage, geographic coverage, authors and citations are empty in the dataset metadata. The uploader declares the license as CC BY 4.0. | [Metadata tab](../audit/evidence/kaggle-metadata-2026-09-19.png) | Established |
| P2 | **The only answer on the collection method does not document it.** A user asked in the dataset's discussion how the data was collected; the uploader replied with a link to the Our World in Data mental-health topic page, which presents aggregate country-level statistics from third-party sources, not individual-level records. | [Discussion](../audit/evidence/kaggle-discussion-2026-09-19.png); [linked page](../audit/evidence/owid-mental-health-2026-09-19.png) | Established |
| P3 | **The "About Dataset" text does not match the file.** It describes text-analysis features (readability indices, sentiment scores); none is among the file's 17 columns. | [About Dataset](../audit/evidence/kaggle-about-2026-09-19.png); ETL log column list at tag `legacy-original` | Established |
| P4 | **The legacy report contradicts itself on the source.** It names the source as the "Mental Health in Tech Survey" while listing Business, Corporate, Housewife, Student and Others as occupations. | Legacy report, Introduction and Phase 1, at tag `legacy-original` | Established |
| P5 | **The "2014–2016" label derives from the `Timestamp` values.** The Data Card reports a minimum of 2014-08-27, a maximum of 2016-02-01 and about 292k valid rows; no temporal coverage is declared. | [Data Card, columns 1](../audit/evidence/kaggle-datacard-columns-1-2026-09-19.png) | Established |
| P6 | **Column-level documentation covers 7 of 17 columns.** Descriptions exist for `Timestamp`, `Gender`, `Country`, `self_employed`, `family_history`, `treatment` and `mental_health_interview`. None exists for `Occupation`, `care_options` or the eight symptom columns (`Days_Indoors`, `Growing_Stress`, `Changes_Habits`, `Mental_Health_History`, `Mood_Swings`, `Coping_Struggles`, `Work_Interest`, `Social_Weakness`). | Data Card, columns [1](../audit/evidence/kaggle-datacard-columns-1-2026-09-19.png) to [4](../audit/evidence/kaggle-datacard-columns-4-2026-09-19.png) | Established |
| P7 | **The documented question texts coincide with the OSMI 2014 codebook, but the file is far larger.** The texts for `self_employed`, `family_history` and `treatment` match those of the OSMI 2014 *Mental Health in Tech* survey as published on [OpenML](https://k8sapi.openml.org/d/43664). That survey has 1,259 responses according to a [published analysis](https://www.r-bloggers.com/2017/05/an-interesting-study-exploring-mental-health-conditions-in-the-tech-workplace/); the file has about 292k rows. OSMI publishes its 2014 and 2016 surveys under CC BY-SA 4.0 ([deposit](https://figshare.com/articles/dataset/OSMI_Mental_Health_in_Tech_Survey/5579458)). | [Data Card, columns 2](../audit/evidence/kaggle-datacard-columns-2-2026-09-19.png) | Coincidences and figures established. Relation to OSMI is a hypothesis (H1). |
| P8 | **Marginal distributions differ sharply between column groups.** Columns with a source description are skewed: `Gender` 82% Male, `Country` 59% United States, `family_history` 40% true, `mental_health_interview` 79% No and 18% Maybe. The symptom columns and `Occupation` are close to uniform: each level of the three-level symptom columns holds between 29% and 37% of the rows (`Growing_Stress` 34% / 32% / 34%), `Coping_Struggles` is 47% / 53%, and the two largest levels of the five-level `Days_Indoors` and `Occupation` hold 22% and 21%, and 23% and 21%. `care_options` (undocumented) is 41% No, 33% Yes, 27% other. Values are read from the Data Card and rounded. | Data Card, columns [1](../audit/evidence/kaggle-datacard-columns-1-2026-09-19.png) to [4](../audit/evidence/kaggle-datacard-columns-4-2026-09-19.png) | Observation established. Interpretation is a hypothesis (H1, H2). |
| P9 | **The legacy input corresponds to the Kaggle file.** The legacy ETL log reports 292,364 raw records, 17 columns and 5,202 nulls in `self_employed`; the Data Card reports about 292k rows, 17 columns and 5,202 missing values in `self_employed`. | ETL log at tag `legacy-original`; [Data Card, columns 2](../audit/evidence/kaggle-datacard-columns-2-2026-09-19.png) | Coincidences established. Byte-level identity pending SHA-256 comparison (`docs/dataset-provenance.md`). |

### Hypotheses (not findings)

* **H1.** The file combines records derived from an OSMI-type survey (the described columns) with columns from another source (the symptom columns). Test: compare the distributions of `Timestamp`, `Gender`, `Country`, `family_history` and `treatment` with the OSMI 2014 data; measure association (Cramér's V) between the two column groups. A near-zero association across groups, with real structure inside the OSMI-type group, would support H1.
* **H2.** The rows are replicated or resampled. Test: duplicate rate and unique-profile counts ignoring `Timestamp`.

Both tests belong to the legacy audit (`docs/audit/legacy-audit.md`), not to this ADR.

## Decision Drivers

* No claim about a population, a period or an instrument can be supported by the source's documentation (P1 to P3, P6).
* The model is built around this file's columns, so making publication conditional on resolving the provenance is not practical: the resolution would be a different dataset and a different project.
* The file has no age or education columns, which also limits any adjusted analysis.
* If H1 holds, associations between variables from different sources would be artifacts, so indicators built on them could not be read as findings about anyone.
* The portfolio value of the project does not depend on population claims: it rests on rigor, on the audit and on transparency about limitations.
* The audit came after the course project. The record must state that chronology and not present the limitations as known in advance.

## Considered Options

1. Pursue academic publication using this dataset as-is.
2. Keep publication as a conditional goal, pending documentation of the provenance.
3. Replace the dataset with a documented source and keep the publication goal.
4. Position the project as a portfolio piece; the dataset is a declared methodological test bench; publication is not pursued for this project.

## Decision Outcome

Chosen option: "Position the project as a portfolio piece and do not pursue academic publication", because empirical claims cannot be supported (P1 to P3, P6), the conditional path (option 2) depends on a resolution that would replace the dataset and therefore the project, and the strongest honest contribution is a transparent audit and a rebuild carried out with the highest rigor the material allows.

### Consequences

* Good, because the project's story is verifiable: a course project, a later audit, documented findings and a rebuild on a corrected specification.
* Good, because no claim exceeds the evidence.
* Bad, because it gives up the publication path for this project.
* Bad, because the conceptual framework and modeling lessons can only be reused in a future project on documented data, which would be a separate decision.
* Constraint: documentation and results must not present any indicator as a finding about a population. Outputs are reported as outputs of a test bench.

### Confirmation

* `docs/dataset-provenance.md` records the source metadata as retrieved (with date), the column documentation, the evidence index, the SHA-256 of the file used and how to obtain it.
* The README states the provenance limitation on its first screen.
* The specification defines each indicator with a name that its variables can support.
* No document states prevalence or treatment-gap figures as findings.
* The tests for H1 and H2 are run and their results recorded in `docs/audit/legacy-audit.md`.

## Pros and Cons of the Options

### Pursue publication with this dataset as-is
* Good, because it keeps the original ambition.
* Bad, because the source's documentation cannot support the empirical component.

### Keep publication as a conditional goal
* Good, because it keeps the door open.
* Bad, because the condition (documented provenance for the same file) may never be met, and meeting it by changing dataset means a new project.

### Replace the dataset with a documented source
* Good, because it would make an empirical component defensible.
* Bad, because the model, ETL and specification would have to be redone around different variables.

### Portfolio piece with a declared test bench
* Good, because it claims only what the material supports.
* Bad, because publication is off the table for this project.

## More Information

* Related: [ADR-0000](0000-rebuild-from-scratch-instead-of-continuing-legacy.md).
* Source: [bhavikjikadara/mental-health-dataset](https://www.kaggle.com/datasets/bhavikjikadara/mental-health-dataset) (Kaggle).
* Evidence index: `docs/dataset-provenance.md`.