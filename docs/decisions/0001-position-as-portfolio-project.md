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
* **H3 (added 2026-09-22, after H1/H2 above).**  The eight undocumented symptom columns (Days_Indoors, Growing_Stress, Changes_Habits, Mental_Health_History, Mood_Swings, Coping_Struggles, Work_Interest, Social_Weakness) match, verbatim, the columns of the RHMCD-20 dataset (Salehin, Amin et al., Mendeley, DOI 10.17632/pxjmjyfdh2.1, published 2023-12-18). If confirmed, this identifies the second source hypothesized in H1 — and raises an additional inconsistency: RHMCD-20 is framed around COVID-era quarantine and postdates the file's claimed 2014–2016 Timestamp range by nearly a decade. Test: compare marginal distributions of the eight shared columns against RHMCD-20; test for row-level matches on those columns.

* All three tests belong to the legacy audit (`docs/audit/legacy-audit.md`), not to this ADR.

---

### Addendum (2026-10-01)

P7 is qualified by captures of two third-party pages taken on 2026-10-01 and listed in the [Evidence section of `dataset-provenance.md`](../dataset-provenance.md#evidence). They close the debts that [ADR-0012](0012-cite-only-frozen-and-versioned-sources-as-evidence.md) records for P7's links to OpenML and figshare. P7's text is unchanged; the points below correct it and replace part of its support.

* **Question texts.** The OpenML deposit of the 2014 *Mental Health in Tech* survey, captured at `openml.org/search?type=data&status=active&id=43664`, gives a question text for most columns in its Description. Four of the seven columns the Data Card documents match those texts: `self_employed`, `family_history`, `treatment` and `mental_health_interview`. P7 names three; it omits `mental_health_interview`, whose Data Card description, "Would you bring up a mental health issue with a potential employer in an interview?", is the text OpenML shows for that column (written `mentalhealthinterview` in the Description and `mental_health_interview` in the feature list). For `Timestamp`, `Gender` and `Country`, the Description lists the column name without a question text, so no text comparison is possible.
* **Size of the 2014 survey.** The survey size P7 states is carried by the number of instances in the capture of the deposit's properties, which replaces the published analysis P7 cites; the number of features is in the same capture. Both describe the OpenML deposit, which a third party uploaded; its relation to the files OSMI itself publishes is not verified.
* **The OpenML link.** P7 links a host different from the one captured, `k8sapi.openml.org`. The capture is the citable record of the page.
* **figshare.** The deposit `10.6084/m9.figshare.5579458` reads "posted on 2017-11-07, 17:44 authored by Open Sourcing Mental Illness Ltd". Its file panel reads "2 files" and shows two dataset files of 296.57 kB and 1.05 MB, whose names are truncated in the capture; its description reads: "One survey was performed in 2014 and the other in 2016."
* **License.** The pages state no single license for the OSMI surveys. The figshare description, first paragraph of the main column, reads: "These data sets are survey results collected by OSMI and are made available by the CC-BY-SA 4.0 license." The figshare Licence field, right column under "LICENCE", reads "CC BY 4.0". The OpenML deposit states "CC BY-SA 4.0" in its header line. P7's statement that OSMI publishes its 2014 and 2016 surveys under CC BY-SA 4.0 rests on the figshare description alone, and the same deposit's Licence field states CC BY 4.0. Which license governs the surveys is unresolved.
* **Scope.** This addendum compares column names and question texts only. It is not evidence about H1 or H3, which remain with checks A5, A6 and A10 of the [legacy audit](../audit/legacy-audit.md), and it does not change this record's position: the file's provenance is undocumented by its source and unresolved.

---

### Addendum (2026-10-04)
P9's byte-level identity, pending when P9 was written, is established by check A1: the SHA-256 of the legacy raw file equals that of a fresh download of the Kaggle file ([legacy audit](../audit/legacy-audit.md#checks), A1; the hash is in [`dataset-provenance.md`](../dataset-provenance.md)). The legacy input and the Kaggle file are the same file.

---

### Addendum (2026-10-06)
P7 is qualified by a reading of the column list in the Description of the capture `openml-osmi-2014-description-2026-10-01.png` ([evidence](../dataset-provenance.md#evidence)). Eight of the 17 columns of the file occur in it: `Timestamp`, `Gender`, `Country`, `self_employed`, `family_history`, `treatment` and `care_options` by the same name, and `mental_health_interview` written `mentalhealthinterview`. `Occupation` and the eight symptom columns do not occur; the deposit lists `work_interfere`, a name different from `Work_Interest`. For `care_options` the Description gives the question text "Do you know the options for mental health care your employer provides?"; the Data Card has no text to compare it with. As in the addendum of 2026-10-01, the reading compares the column names and question texts of a third-party deposit and is not evidence about H1 or H3. [LOG-040](log/LOG-040-h1-column-groups.md) uses it to fix the column groups of H1.

---

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