# Dataset provenance

This project uses a file that Kaggle presents as "Mental Health Dataset". Its provenance is undocumented by its source. This record states what the source declares, what it does not, and how to obtain and identify the file. See [ADR-0001](decisions/0001-position-as-portfolio-project.md) for the resulting decision.

## Source

* Page: <https://www.kaggle.com/datasets/bhavikjikadara/mental-health-dataset>
* File: `Mental Health Dataset.csv`, 31.1 MB, version 1.
* Uploader-declared license: CC BY 4.0. The license does not establish who created the data.
* Uploader-declared provenance: "I collected this dataset from the internet".
* Empty in the metadata: collection methodology, temporal coverage, geographic coverage, authors, citations.

## Column documentation

The Data Card documents 7 of the 17 columns. The report column shows where the legacy report reads a variable differently.

| Column | Source description | Legacy report reads it as |
|--------|--------------------|---------------------------|
| `Timestamp` | "Time the survey was submitted" | Survey date |
| `Gender` | "Respondent gender" | Same |
| `Country` | "Respondent country" | Same |
| `Occupation` | none | Occupation or sector |
| `self_employed` | "Are you self-employed?" | Same |
| `family_history` | "Do you have a family history of mental illness?" | Same |
| `treatment` | "Have you sought treatment for a mental health condition?" | Currently in treatment |
| `Days_Indoors` | none | Days spent indoors (isolation) |
| `Growing_Stress` | none | Growing stress reported |
| `Changes_Habits` | none | Not used |
| `Mental_Health_History` | none | Personal history, not used |
| `Mood_Swings` | none | Mood swings level |
| `Coping_Struggles` | none | Difficulty coping |
| `Work_Interest` | none | Not used |
| `Social_Weakness` | none | Social weakness |
| `mental_health_interview` | "Would you bring up a mental health issue with a potential employer in an interview?" | Participated in a mental-health interview |
| `care_options` | none | Mental-health care options available |

## Evidence

Captures taken on 2026-09-19. They are immutable: do not replace or edit them.

| File | Shows |
|------|-------|
| `audit/evidence/kaggle-metadata-2026-09-19.png` | Metadata tab: provenance, coverage, license |
| `audit/evidence/kaggle-about-2026-09-19.png` | "About Dataset" text |
| `audit/evidence/kaggle-discussion-2026-09-19.png` | Question on the collection method and the uploader's reply |
| `audit/evidence/owid-mental-health-2026-09-19.png` | Page linked in the uploader's reply |
| `audit/evidence/kaggle-datacard-columns-1-2026-09-19.png` | Data Card, column view: `Timestamp`, `Gender`, `Country` |
| `audit/evidence/kaggle-datacard-columns-2-2026-09-19.png` | Data Card, column view: `Occupation`, `self_employed`, `family_history`, `treatment` |
| `audit/evidence/kaggle-datacard-columns-3-2026-09-19.png` | Data Card, column view: `Days_Indoors`, `Growing_Stress`, `Changes_Habits`, `Mental_Health_History`, `Mood_Swings` |
| `audit/evidence/kaggle-datacard-columns-4-2026-09-19.png` | Data Card, column view: `Coping_Struggles`, `Work_Interest`, `Social_Weakness`, `mental_health_interview`, `care_options` |

Captures of third-party pages about the OSMI *Mental Health in Tech* surveys, taken on 2026-10-01, later than the captures above. They carry claims about those pages only ([ADR-0012](decisions/0012-cite-only-frozen-and-versioned-sources-as-evidence.md), rule 2); no claim about the provenance of the file used here rests on them ([ADR-0001](decisions/0001-position-as-portfolio-project.md#addendum-2026-10-01), addendum of 2026-10-01). They are immutable on the same terms as the captures above.

| File | Shows |
|------|-------|
| `audit/evidence/openml-osmi-2014-description-2026-10-01.png` | OpenML deposit "Mental-Health-in-Tech-Survey" (ID 43664), uploaded by a third party: header line (license CC BY-SA 4.0, date 2022-03-24, version 1) and the Description, which lists the columns, most with their question texts |
| `audit/evidence/openml-osmi-2014-properties-1-2026-10-01.png` | Same deposit: the first rows of its feature list (name, type, distinct and missing counts) |
| `audit/evidence/openml-osmi-2014-properties-2-2026-10-01.png` | Same deposit: the first rows of its qualities, including the number of instances and the number of features |
| `audit/evidence/figshare-osmi-1-2026-10-01.png` | figshare deposit "OSMI Mental Health in Tech Survey": file panel reading "2 files", with two dataset files of 296.57 kB and 1.05 MB whose names are truncated, the DOI, and the "Download all" link |
| `audit/evidence/figshare-osmi-2-2026-10-01.png` | Same deposit: DOI, posting line (2017-11-07, authored by Open Sourcing Mental Illness Ltd), description with its license statement, and the Licence field (CC BY 4.0) |

## Identity of the file

The legacy raw input (`data/raw/mental_health.csv` at tag `legacy-original`) has 292,364 records and 17 columns, and 5,202 nulls in `self_employed` according to the legacy ETL log. The Data Card reports about 292k rows, 17 columns and 5,202 missing values in `self_employed`. The two files are byte-identical: their SHA-256 hashes match exactly (below).

| File | SHA-256 |
|------|---------|
| Legacy raw file (`data/raw/mental_health.csv`) | `083f44e9cdf84f56abf08b9fa1862d80b87237afa74e2cacc9328a63d9291686` |
| Fresh Kaggle download (`Mental Health Dataset.csv`, downloaded 2026-09-25) | `083f44e9cdf84f56abf08b9fa1862d80b87237afa74e2cacc9328a63d9291686` |

Legacy hash computed by extracting the file read-only from the `legacy-original` tag (`git show legacy-original:data/raw/mental_health.csv`, no checkout, no working-tree change) and running `shasum -a 256` on the result. Kaggle hash computed the same way, on a fresh download via the `kaggle` CLI, unzipped and hashed outside this repository.

To compute a hash: `shasum -a 256 <file>`.

## How to obtain the file

The dataset is not versioned in this repository. Download it from the Kaggle page above and verify its SHA-256 against the table. Place it in `data/raw/`, which is ignored by git.

This is a deliberate choice, not only a size consideration. The uploader declares the file CC BY 4.0 (P1), but H1 — not yet resolved — hypothesizes that the symptom columns come from a second source. The pages consulted for the OSMI surveys state no single license: the figshare deposit authored by OSMI gives CC-BY-SA 4.0 in its description and CC BY 4.0 in its Licence field, and a third-party OpenML deposit gives CC BY-SA 4.0 (captures under [Evidence](#evidence); quotations in the [2026-10-01 addendum to ADR-0001](decisions/0001-position-as-portfolio-project.md#addendum-2026-10-01)). If H1 is confirmed, the portion of the file derived from the OSMI 2014 survey may therefore carry a license other than the one declared for the whole file. Redistributing the raw file from this repository while either question is open would mean redistributing it under a license this project cannot yet confirm is correct. See [ADR-0001](decisions/0001-position-as-portfolio-project.md).

The legacy repository (`stress-dw-legacy`, archived, unmodified) already carries a committed copy of the file at the `legacy-original` tag, for anyone auditing this project who wants to inspect the data directly.

## Known unknowns

* Who collected the data, when, how, and from which population.
* Whether the file combines several sources.
* What most variables mean (10 of 17 have no description).