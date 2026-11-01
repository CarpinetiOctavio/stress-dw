# Correspondence evidence

The final report of [ADR-0011](../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), named and structured by [LOG-045](../decisions/log/LOG-045-correspondence-evidence-document.md). It applies the [correspondence criteria](correspondence-criteria.md) to the indicator output and reports, question by question, whether the output lets the determination named by the question's objective be made. Every verdict is an output of a methodological test bench, not a finding about any population; what no verdict states is listed in the [criteria, section 0](correspondence-criteria.md#0-scope).

## 1. Reproduction

* **Criteria commit:** `ed49662` (#75).
* **Repository commit of the runs:** `3dd8068` (#81). The outputs were produced there by `uv run python -m stress_dw.evidence`, and the same command reproduces them byte for byte at `e006d34`.
* **Source file:** SHA-256 in [`dataset-provenance.md`, Identity of the file](../dataset-provenance.md#identity-of-the-file).
* **Recipe:** two full reloads (`run_pipeline`), each into its own database file; on each, every indicator is computed by `run_indicator` with its number, 1 to 16, and the default `low_n` threshold ([`patterns.md`, Reporting rules](../specification/patterns.md#reporting-rules)).
* **Canonical serialization** ([ADR-0011](../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), rule 5): stated in the docstring of [`src/stress_dw/evidence.py`](../../src/stress_dw/evidence.py), with rates at six decimal places.
* **Comparison of the two runs:** identical for 16 of 16 indicators ([`hashes.csv`](correspondence-evidence/hashes.csv)). Section 4 cites each indicator by number and by the first 12 characters of its SHA-256.

The full output of each indicator is the generated CSV in [`correspondence-evidence/`](correspondence-evidence/), with the SHA-256 of both runs in [`hashes.csv`](correspondence-evidence/hashes.csv); this closes the open point of [LOG-045](../decisions/log/LOG-045-correspondence-evidence-document.md) on where the full outputs sit.

Indicators 5 and 6, and 12 and 13, have identical outputs: each pair shares its population and cuts, and every output row carries both the numerator and the rate ([`patterns.md`, Output columns](../specification/patterns.md#output-columns)), so the count indicator and the rate indicator are one output, read twice.

This section meets the fourth item of ADR-0011, Confirmation.

## 2. Branch applied

"H1 holds", by rule R1 of the [criteria, section 3.4](correspondence-criteria.md#34-mapping-of-a5-a6-and-a10-to-a-branch). The results of A5, A6 and A10 and the branch they give are in [`legacy-audit.md`](legacy-audit.md#checks) (rows A5, A6 and A10, and [Reading branch](legacy-audit.md#reading-branch)). No result is read under both branches: the premise of `care_options` holds, and the test of `Occupation` against RHMCD-20 confirms ([criteria, section 7](correspondence-criteria.md#second-amendment-of-2026-10-29-before-any-result-of-a5-a6-or-a10), second amendment of 2026-10-29).

Third item of ADR-0011, Confirmation: the criteria commit `ed49662`, which contains the two reading branches, is an ancestor of `b278bec` (#79), which records the results of A5, A6 and A10 (`git merge-base --is-ancestor ed49662 b278bec`).

## 3. Post-commit exposures

The value scan searched every commit reachable from `8b67c52`, trees and commit messages, for each indicator value; its method is in the docstring of [`src/stress_dw/evidence.py`](../../src/stress_dw/evidence.py). [`value-scan.csv`](correspondence-evidence/value-scan.csv) lists 53 hits, one per value and path at the first commit that holds it, each classed by the commit's place in the order of ADR-0011, rule 4, and read as the same quantity as the indicator value or a different one, with the reason in `note`.

* **Post-commit exposures:** two. The staged-record count, 290,051, which is indicator 1's denominator, is written in two concept transfers ([`grain-and-cross-sections.md`](../concept-transfers/grain-and-cross-sections.md); [`sets-and-multisets.md`](../concept-transfers/sets-and-multisets.md)) by `c93c6e1` (#76), after the criteria commit and before exposure was allowed. The value was in the repository at the parent of the criteria commit, so it was known by access when the criteria were fixed ([LOG-049](../decisions/log/LOG-049-reading-rule-by-repository-access.md), item 2; [criteria, section 1](correspondence-criteria.md#1-declaration-of-prior-knowledge)). The other eight hits after the criteria commit and before exposure are of a different quantity.
* **First item of ADR-0011, Confirmation: not met.** The criteria commit does not precede every commit that contains an indicator value. Fourteen hits before it are of the same quantity:
  * twelve of the staged-record count, in the specification, decision records, audit documents, `CLAUDE.md` and one commit message;
  * two in [ADR-0001](../decisions/0001-position-as-portfolio-project.md), P8: the shares of the levels of `Growing_Stress`, whole percentages, declared as K1 ([criteria, section 1](correspondence-criteria.md#1-declaration-of-prior-knowledge), item 1).

  The other 25 hits before the criteria commit are of a different quantity.
* **In order:** four hits after exposure was allowed, two of them of the same quantity: the lifetime treatment rates by gender of check A7 (#80), which equal cells of indicator 7.
* **Second item of ADR-0011, Confirmation:** the [criteria, section 1](correspondence-criteria.md#1-declaration-of-prior-knowledge), lists the four items of rule 2.
* **Not searched:** counts below 1,000, which occur everywhere as unrelated numbers; whole percentages written without the percent sign; and pull-request descriptions, which are not in the history (ADR-0011, K3; declared in the [criteria, section 1](correspondence-criteria.md#1-declaration-of-prior-knowledge)).

## 4. Questions

Every verdict is read under "H1 holds" (section 2). The criteria of each question are applied as committed, with the amendments of the [criteria, section 7](correspondence-criteria.md#7-amendments), both made before any result of A5, A6 or A10; there is no post-exposure amendment. The status of every required cell is in [`required-cells.csv`](correspondence-evidence/required-cells.csv), written by `uv run python -m stress_dw.correspondence` from the published outputs; the same command prints the reading lists and cell tables below. In the cell tables, a level rate is written as numerator (rate), and a cell the output does not report is marked missing.

Within each gender, the rates of indicators 2 and 4 are equal in every period, and those of indicator 7 at every level of `growing_stress`. The denominators of indicators 2 and 4 differ and are whole multiples of 431 rows for `Female` and 390 for `Male`. No verdict depends on this ([criteria, section 3.2](correspondence-criteria.md#32-branch-h1-holds)).

| Question | Indicators | Crosses the groups | Verdict | Cause |
|---|---|---|---|---|
| Q1 | 1, 2 | yes | does not correspond | provenance; data volume |
| Q2 | 3, 4 | yes | does not correspond | provenance; data volume |
| Q3 | 5, 6 | yes | does not correspond | provenance |
| Q4 | 7, 8 | yes | does not correspond | provenance |
| Q5 | 9, 10, 11 | no | corresponds | — |
| Q6 | 12, 13 | yes | does not correspond | provenance; data volume |
| **Q7 (central)** | 14 | yes | does not correspond | provenance |
| Q7.1 | 15 | yes | does not correspond | provenance |
| Q7.2 | 16 | yes | does not correspond | provenance |

Q7 is the help-seeking question the [README](../../README.md) opens with. The causes are the loci of the [criteria, section 4](correspondence-criteria.md#4-locus-of-a-mismatch). In plain terms, provenance: "under the reading that the file joins two sources, this cross says nothing about respondents"; data volume: "too few responses, or none, in a cell to read the comparison".

In every question that crosses the groups, the determination criterion C1 needs a relationship among respondents, so under "H1 holds" it is not met, with the locus provenance ([criteria, section 3.2](correspondence-criteria.md#32-branch-h1-holds)), whatever its cells show. Its cells are still read, and every locus they set is named ([criteria, section 4](correspondence-criteria.md#4-locus-of-a-mismatch)). The criteria unable to fail are met: checks C8 and C9 pass (`uv run pytest`).

### Q1

* **Criteria:** [Q1](correspondence-criteria.md#q1).
* **Indicators:** 1 (`f0669c53fcfe`), 2 (`5e6f599e0251`).
* **C1:** not met. Loci: provenance; data volume: 13 strata, 26 required cells: 17 present, 9 missing, 0 flagged. At least two strata exist, so the locus reasoning or design does not apply.
* **Verdict:** does not correspond. Cause: "under the reading that the file joins two sources, this cross says nothing about respondents"; "too few responses, or none, in a cell to read the comparison".
* **Design findings:** none.

Reading list:

| Stratum | Reading | Missing | Flagged |
|---|---|---|---|
| period=2014-08 | readable | 0 | 0 |
| period=2014-09 | readable | 0 | 0 |
| period=2014-10 | not readable | 1 | 0 |
| period=2014-11 | not readable | 1 | 0 |
| period=2014-12 | readable | 0 | 0 |
| period=2015-02 | readable | 0 | 0 |
| period=2015-04 | not readable | 1 | 0 |
| period=2015-05 | not readable | 1 | 0 |
| period=2015-06 | not readable | 1 | 0 |
| period=2015-07 | not readable | 1 | 0 |
| period=2015-08 | not readable | 1 | 0 |
| period=2015-09 | not readable | 1 | 0 |
| period=2016-02 | not readable | 1 | 0 |

Cells read (indicator 2):

| period | gender | denominator | Yes | No | Maybe | low_n |
|---|---|---|---|---|---|---|
| 2014-08 | Male | 215280 | 70656 (0.328205) | 69000 (0.320513) | 75624 (0.351282) | false |
| 2014-08 | Female | 46979 | 18639 (0.396752) | 14170 (0.301624) | 14170 (0.301624) | false |
| 2014-09 | Male | 9360 | 3072 (0.328205) | 3000 (0.320513) | 3288 (0.351282) | false |
| 2014-09 | Female | 1724 | 684 (0.396752) | 520 (0.301624) | 520 (0.301624) | false |
| 2014-10 | Male | missing |  |  |  |  |
| 2014-10 | Female | 431 | 171 (0.396752) | 130 (0.301624) | 130 (0.301624) | false |
| 2014-11 | Male | 390 | 128 (0.328205) | 125 (0.320513) | 137 (0.351282) | false |
| 2014-11 | Female | missing |  |  |  |  |
| 2014-12 | Male | 390 | 128 (0.328205) | 125 (0.320513) | 137 (0.351282) | false |
| 2014-12 | Female | 431 | 171 (0.396752) | 130 (0.301624) | 130 (0.301624) | false |
| 2015-02 | Male | 8580 | 2816 (0.328205) | 2750 (0.320513) | 3014 (0.351282) | false |
| 2015-02 | Female | 2155 | 855 (0.396752) | 650 (0.301624) | 650 (0.301624) | false |
| 2015-04 | Male | 1170 | 384 (0.328205) | 375 (0.320513) | 411 (0.351282) | false |
| 2015-04 | Female | missing |  |  |  |  |
| 2015-05 | Male | 780 | 256 (0.328205) | 250 (0.320513) | 274 (0.351282) | false |
| 2015-05 | Female | missing |  |  |  |  |
| 2015-06 | Male | missing |  |  |  |  |
| 2015-06 | Female | 431 | 171 (0.396752) | 130 (0.301624) | 130 (0.301624) | false |
| 2015-07 | Male | 390 | 128 (0.328205) | 125 (0.320513) | 137 (0.351282) | false |
| 2015-07 | Female | missing |  |  |  |  |
| 2015-08 | Male | 780 | 256 (0.328205) | 250 (0.320513) | 274 (0.351282) | false |
| 2015-08 | Female | missing |  |  |  |  |
| 2015-09 | Male | 390 | 128 (0.328205) | 125 (0.320513) | 137 (0.351282) | false |
| 2015-09 | Female | missing |  |  |  |  |
| 2016-02 | Male | 390 | 128 (0.328205) | 125 (0.320513) | 137 (0.351282) | false |
| 2016-02 | Female | missing |  |  |  |  |

### Q2

* **Criteria:** [Q2](correspondence-criteria.md#q2).
* **Indicators:** 3 (`25dcc631a9e2`), 4 (`277d13169d51`).
* **C1:** not met. Loci: provenance; data volume: 13 strata, 26 required cells: 16 present, 10 missing, 0 flagged. At least two strata exist, so the locus reasoning or design does not apply.
* **Verdict:** does not correspond. Cause: "under the reading that the file joins two sources, this cross says nothing about respondents"; "too few responses, or none, in a cell to read the comparison".
* **Documentary layer:** in the [criteria, Q2](correspondence-criteria.md#q2). It gives no verdict ([LOG-051](../decisions/log/LOG-051-stopping-rule-documentary-audit-readings.md); LOG-045, addendum of 2026-10-25).
* **Design findings:** none.

Reading list:

| Stratum | Reading | Missing | Flagged |
|---|---|---|---|
| period=2014-08 | readable | 0 | 0 |
| period=2014-09 | readable | 0 | 0 |
| period=2014-10 | not readable | 1 | 0 |
| period=2014-11 | not readable | 1 | 0 |
| period=2014-12 | not readable | 1 | 0 |
| period=2015-02 | readable | 0 | 0 |
| period=2015-04 | not readable | 1 | 0 |
| period=2015-05 | not readable | 1 | 0 |
| period=2015-06 | not readable | 1 | 0 |
| period=2015-07 | not readable | 1 | 0 |
| period=2015-08 | not readable | 1 | 0 |
| period=2015-09 | not readable | 1 | 0 |
| period=2016-02 | not readable | 1 | 0 |

Cells read (indicator 4):

| period | gender | denominator | Yes | No | Maybe | low_n |
|---|---|---|---|---|---|---|
| 2014-08 | Male | 73710 | 24192 (0.328205) | 23625 (0.320513) | 25893 (0.351282) | false |
| 2014-08 | Female | 28877 | 11457 (0.396752) | 8710 (0.301624) | 8710 (0.301624) | false |
| 2014-09 | Male | 3120 | 1024 (0.328205) | 1000 (0.320513) | 1096 (0.351282) | false |
| 2014-09 | Female | 862 | 342 (0.396752) | 260 (0.301624) | 260 (0.301624) | false |
| 2014-10 | Male | missing |  |  |  |  |
| 2014-10 | Female | 431 | 171 (0.396752) | 130 (0.301624) | 130 (0.301624) | false |
| 2014-11 | Male | 390 | 128 (0.328205) | 125 (0.320513) | 137 (0.351282) | false |
| 2014-11 | Female | missing |  |  |  |  |
| 2014-12 | Male | 390 | 128 (0.328205) | 125 (0.320513) | 137 (0.351282) | false |
| 2014-12 | Female | missing |  |  |  |  |
| 2015-02 | Male | 2730 | 896 (0.328205) | 875 (0.320513) | 959 (0.351282) | false |
| 2015-02 | Female | 862 | 342 (0.396752) | 260 (0.301624) | 260 (0.301624) | false |
| 2015-04 | Male | 390 | 128 (0.328205) | 125 (0.320513) | 137 (0.351282) | false |
| 2015-04 | Female | missing |  |  |  |  |
| 2015-05 | Male | 390 | 128 (0.328205) | 125 (0.320513) | 137 (0.351282) | false |
| 2015-05 | Female | missing |  |  |  |  |
| 2015-06 | Male | missing |  |  |  |  |
| 2015-06 | Female | 431 | 171 (0.396752) | 130 (0.301624) | 130 (0.301624) | false |
| 2015-07 | Male | 390 | 128 (0.328205) | 125 (0.320513) | 137 (0.351282) | false |
| 2015-07 | Female | missing |  |  |  |  |
| 2015-08 | Male | 780 | 256 (0.328205) | 250 (0.320513) | 274 (0.351282) | false |
| 2015-08 | Female | missing |  |  |  |  |
| 2015-09 | Male | 390 | 128 (0.328205) | 125 (0.320513) | 137 (0.351282) | false |
| 2015-09 | Female | missing |  |  |  |  |
| 2016-02 | Male | 390 | 128 (0.328205) | 125 (0.320513) | 137 (0.351282) | false |
| 2016-02 | Female | missing |  |  |  |  |

### Q3

* **Criteria:** [Q3](correspondence-criteria.md#q3), with the [second amendment of 2026-10-29](correspondence-criteria.md#second-amendment-of-2026-10-29-before-any-result-of-a5-a6-or-a10) (criteria, section 7). The test of `Occupation` against RHMCD-20 confirms, so results that involve `Occupation` follow the branch of the mapping rule. The amendment supersedes the reading under both branches stated for `Occupation` in the criteria, section 3.1, in Q3's Branches entry, and in [LOG-045](../decisions/log/LOG-045-correspondence-evidence-document.md), item 4. Q3 receives one verdict.
* **Indicators:** 5 (`edf4bac7593c`), 6 (`edf4bac7593c`).
* **C1:** not met. Locus: provenance. Cells: by country, 35 strata, 175 required cells: 175 present, 0 missing, 0 flagged; by region, 6 strata, 30 required cells: 30 present, 0 missing, 0 flagged. At least two regions exist.
* **Verdict:** does not correspond. Cause: "under the reading that the file joins two sources, this cross says nothing about respondents".
* **Design findings:** none.

Reading list, countries:

| Stratum | Reading | Missing | Flagged |
|---|---|---|---|
| country=Australia | readable | 0 | 0 |
| country=Belgium | readable | 0 | 0 |
| country=Bosnia and Herzegovina | readable | 0 | 0 |
| country=Brazil | readable | 0 | 0 |
| country=Canada | readable | 0 | 0 |
| country=Colombia | readable | 0 | 0 |
| country=Costa Rica | readable | 0 | 0 |
| country=Croatia | readable | 0 | 0 |
| country=Czech Republic | readable | 0 | 0 |
| country=Denmark | readable | 0 | 0 |
| country=Finland | readable | 0 | 0 |
| country=France | readable | 0 | 0 |
| country=Georgia | readable | 0 | 0 |
| country=Germany | readable | 0 | 0 |
| country=Greece | readable | 0 | 0 |
| country=India | readable | 0 | 0 |
| country=Ireland | readable | 0 | 0 |
| country=Israel | readable | 0 | 0 |
| country=Italy | readable | 0 | 0 |
| country=Mexico | readable | 0 | 0 |
| country=Moldova | readable | 0 | 0 |
| country=Netherlands | readable | 0 | 0 |
| country=New Zealand | readable | 0 | 0 |
| country=Nigeria | readable | 0 | 0 |
| country=Philippines | readable | 0 | 0 |
| country=Poland | readable | 0 | 0 |
| country=Portugal | readable | 0 | 0 |
| country=Russia | readable | 0 | 0 |
| country=Singapore | readable | 0 | 0 |
| country=South Africa | readable | 0 | 0 |
| country=Sweden | readable | 0 | 0 |
| country=Switzerland | readable | 0 | 0 |
| country=Thailand | readable | 0 | 0 |
| country=United Kingdom | readable | 0 | 0 |
| country=United States | readable | 0 | 0 |

Reading list, regions:

| Stratum | Reading | Missing | Flagged |
|---|---|---|---|
| region=Africa | readable | 0 | 0 |
| region=Asia | readable | 0 | 0 |
| region=Europe | readable | 0 | 0 |
| region=Latin America and the Caribbean | readable | 0 | 0 |
| region=Northern America | readable | 0 | 0 |
| region=Oceania | readable | 0 | 0 |

Cells flagged by `low_n`: none, in either grouping set.

### Q4

* **Criteria:** [Q4](correspondence-criteria.md#q4).
* **Indicators:** 7 (`61837cbd0c9e`), 8 (`ac68cafba366`).
* **C1:** not met. Locus: provenance. Cells: 6 required cells: 6 present, 0 missing, 0 flagged.
* **Verdict:** does not correspond. Cause: "under the reading that the file joins two sources, this cross says nothing about respondents".
* **Design findings:** none.

Cells read (indicator 7, `Yes` level of `treatment`):

| gender | growing_stress | denominator | Yes | low_n |
|---|---|---|---|---|
| Male | Yes | 78080 | 36096 (0.462295) | false |
| Male | No | 76250 | 35250 (0.462295) | false |
| Male | Maybe | 83570 | 38634 (0.462295) | false |
| Female | Yes | 20691 | 14364 (0.694215) | false |
| Female | No | 15730 | 10920 (0.694215) | false |
| Female | Maybe | 15730 | 10920 (0.694215) | false |

### Q5

* **Criteria:** [Q5](correspondence-criteria.md#q5).
* **Indicators:** 9 (`4ec0adf588a9`), 10 (`0ffdbbc650c2`), 11 (`71cd90e6e7da`).
* **Branch:** not applicable; Q5 crosses no groups ([criteria, Q5](correspondence-criteria.md#q5), Branches).
* **C1:** met. The five `days_indoors` cells are present and none is flagged, in each of the three indicators.
* **Verdict:** corresponds. For each of the three measures, the share of responses at each answer level can be compared across the five levels of time spent indoors. It does not mean that the shares differ, or that they do not, nor that time indoors causes or influences any of them ([criteria, Q5](correspondence-criteria.md#q5), In plain terms).
* **Design findings:** none.

Cells read, indicator 9 (`growing_stress`):

| days_indoors | denominator | Yes | No | Maybe | low_n |
|---|---|---|---|---|---|
| Go out Every day | 57981 | 17171 (0.296149) | 19001 (0.327711) | 21809 (0.376140) | false |
| 1-14 days | 63113 | 22399 (0.354903) | 19989 (0.316718) | 20725 (0.328379) | false |
| 15-30 days | 53474 | 18522 (0.346374) | 17534 (0.327898) | 17418 (0.325728) | false |
| 31-60 days | 60058 | 20826 (0.346765) | 20962 (0.349029) | 18270 (0.304206) | false |
| More than 2 months | 55425 | 19853 (0.358196) | 14494 (0.261507) | 21078 (0.380298) | false |

Indicator 10 (`mood_swings`):

| days_indoors | denominator | Low | Medium | High | low_n |
|---|---|---|---|---|---|
| Go out Every day | 57981 | 18996 (0.327625) | 17539 (0.302496) | 21446 (0.369880) | false |
| 1-14 days | 63113 | 25353 (0.401708) | 21199 (0.335890) | 16561 (0.262402) | false |
| 15-30 days | 53474 | 15830 (0.296032) | 19132 (0.357781) | 18512 (0.346187) | false |
| 31-60 days | 60058 | 22298 (0.371274) | 21073 (0.350877) | 16687 (0.277848) | false |
| More than 2 months | 55425 | 16687 (0.301074) | 21441 (0.386847) | 17297 (0.312079) | false |

Indicator 11 (`social_weakness`):

| days_indoors | denominator | Yes | No | Maybe | low_n |
|---|---|---|---|---|---|
| Go out Every day | 57981 | 15346 (0.264673) | 16314 (0.281368) | 26321 (0.453959) | false |
| 1-14 days | 63113 | 21683 (0.343558) | 21935 (0.347551) | 19495 (0.308890) | false |
| 15-30 days | 53474 | 17781 (0.332517) | 19006 (0.355425) | 16687 (0.312058) | false |
| 31-60 days | 60058 | 20352 (0.338872) | 17292 (0.287922) | 22414 (0.373206) | false |
| More than 2 months | 55425 | 15835 (0.285701) | 21930 (0.395670) | 17660 (0.318629) | false |

### Q6

* **Criteria:** [Q6](correspondence-criteria.md#q6), with the [second amendment of 2026-10-29](correspondence-criteria.md#second-amendment-of-2026-10-29-before-any-result-of-a5-a6-or-a10) (criteria, section 7), as in Q3: the amendment supersedes the reading under both branches stated for `Occupation` in the criteria, section 3.1, in Q6's Branches entry, and in LOG-045, item 4. The premise of `care_options` holds (section 2). Q6 receives one verdict.
* **Indicators:** 12 (`2012c311774d`), 13 (`2012c311774d`).
* **C1:** not met. Loci: provenance; data volume: 35 strata, 1,050 required cells: 705 present, 345 missing, 219 flagged. At least two strata exist, so the locus reasoning or design does not apply. Missing cells are listed in [`required-cells.csv`](correspondence-evidence/required-cells.csv); flagged cells are listed below.
* **Verdict:** does not correspond. Cause: "under the reading that the file joins two sources, this cross says nothing about respondents"; "too few responses, or none, in a cell to read the comparison".
* **Design findings:** none.

Reading list:

| Stratum | Reading | Missing | Flagged |
|---|---|---|---|
| country=Australia | readable | 0 | 0 |
| country=Belgium | not readable | 0 | 20 |
| country=Bosnia and Herzegovina | not readable | 15 | 11 |
| country=Brazil | not readable | 15 | 0 |
| country=Canada | readable | 0 | 0 |
| country=Colombia | not readable | 15 | 11 |
| country=Costa Rica | not readable | 15 | 11 |
| country=Croatia | not readable | 15 | 11 |
| country=Czech Republic | not readable | 15 | 11 |
| country=Denmark | not readable | 15 | 0 |
| country=Finland | not readable | 15 | 11 |
| country=France | not readable | 15 | 0 |
| country=Georgia | not readable | 15 | 11 |
| country=Germany | not readable | 15 | 0 |
| country=Greece | not readable | 15 | 0 |
| country=India | not readable | 0 | 9 |
| country=Ireland | readable | 0 | 0 |
| country=Israel | not readable | 15 | 0 |
| country=Italy | not readable | 15 | 0 |
| country=Mexico | not readable | 15 | 11 |
| country=Moldova | not readable | 15 | 11 |
| country=Netherlands | not readable | 0 | 9 |
| country=New Zealand | not readable | 0 | 9 |
| country=Nigeria | not readable | 15 | 11 |
| country=Philippines | not readable | 15 | 11 |
| country=Poland | not readable | 0 | 20 |
| country=Portugal | not readable | 15 | 11 |
| country=Russia | not readable | 15 | 0 |
| country=Singapore | not readable | 15 | 0 |
| country=South Africa | not readable | 0 | 9 |
| country=Sweden | readable | 0 | 0 |
| country=Switzerland | not readable | 15 | 0 |
| country=Thailand | not readable | 15 | 11 |
| country=United Kingdom | readable | 0 | 0 |
| country=United States | readable | 0 | 0 |

<details>
<summary>Cells flagged by <code>low_n</code> (indicator 12)</summary>

| country | growing_stress | occupation | gender | denominator | low_n |
|---|---|---|---|---|---|
| Belgium | Yes | Business | Male | 25 | flagged |
| Belgium | Yes | Business | Female | 29 | flagged |
| Belgium | Yes | Housewife | Male | 24 | flagged |
| Belgium | Yes | Others | Male | 18 | flagged |
| Belgium | Yes | Student | Male | 28 | flagged |
| Belgium | No | Business | Male | 18 | flagged |
| Belgium | No | Business | Female | 26 | flagged |
| Belgium | No | Corporate | Male | 29 | flagged |
| Belgium | No | Corporate | Female | 19 | flagged |
| Belgium | No | Housewife | Female | 24 | flagged |
| Belgium | No | Others | Male | 26 | flagged |
| Belgium | No | Others | Female | 25 | flagged |
| Belgium | No | Student | Male | 20 | flagged |
| Belgium | Maybe | Business | Male | 23 | flagged |
| Belgium | Maybe | Business | Female | 24 | flagged |
| Belgium | Maybe | Corporate | Male | 23 | flagged |
| Belgium | Maybe | Corporate | Female | 24 | flagged |
| Belgium | Maybe | Others | Male | 25 | flagged |
| Belgium | Maybe | Others | Female | 25 | flagged |
| Belgium | Maybe | Student | Female | 25 | flagged |
| Bosnia and Herzegovina | Yes | Business | Male | 25 | flagged |
| Bosnia and Herzegovina | Yes | Housewife | Male | 24 | flagged |
| Bosnia and Herzegovina | Yes | Others | Male | 18 | flagged |
| Bosnia and Herzegovina | Yes | Student | Male | 28 | flagged |
| Bosnia and Herzegovina | No | Business | Male | 18 | flagged |
| Bosnia and Herzegovina | No | Corporate | Male | 29 | flagged |
| Bosnia and Herzegovina | No | Others | Male | 26 | flagged |
| Bosnia and Herzegovina | No | Student | Male | 20 | flagged |
| Bosnia and Herzegovina | Maybe | Business | Male | 23 | flagged |
| Bosnia and Herzegovina | Maybe | Corporate | Male | 23 | flagged |
| Bosnia and Herzegovina | Maybe | Others | Male | 25 | flagged |
| Colombia | Yes | Business | Male | 25 | flagged |
| Colombia | Yes | Housewife | Male | 24 | flagged |
| Colombia | Yes | Others | Male | 18 | flagged |
| Colombia | Yes | Student | Male | 28 | flagged |
| Colombia | No | Business | Male | 18 | flagged |
| Colombia | No | Corporate | Male | 29 | flagged |
| Colombia | No | Others | Male | 26 | flagged |
| Colombia | No | Student | Male | 20 | flagged |
| Colombia | Maybe | Business | Male | 23 | flagged |
| Colombia | Maybe | Corporate | Male | 23 | flagged |
| Colombia | Maybe | Others | Male | 25 | flagged |
| Costa Rica | Yes | Business | Male | 25 | flagged |
| Costa Rica | Yes | Housewife | Male | 24 | flagged |
| Costa Rica | Yes | Others | Male | 18 | flagged |
| Costa Rica | Yes | Student | Male | 28 | flagged |
| Costa Rica | No | Business | Male | 18 | flagged |
| Costa Rica | No | Corporate | Male | 29 | flagged |
| Costa Rica | No | Others | Male | 26 | flagged |
| Costa Rica | No | Student | Male | 20 | flagged |
| Costa Rica | Maybe | Business | Male | 23 | flagged |
| Costa Rica | Maybe | Corporate | Male | 23 | flagged |
| Costa Rica | Maybe | Others | Male | 25 | flagged |
| Croatia | Yes | Business | Male | 25 | flagged |
| Croatia | Yes | Housewife | Male | 24 | flagged |
| Croatia | Yes | Others | Male | 18 | flagged |
| Croatia | Yes | Student | Male | 28 | flagged |
| Croatia | No | Business | Male | 18 | flagged |
| Croatia | No | Corporate | Male | 29 | flagged |
| Croatia | No | Others | Male | 26 | flagged |
| Croatia | No | Student | Male | 20 | flagged |
| Croatia | Maybe | Business | Male | 23 | flagged |
| Croatia | Maybe | Corporate | Male | 23 | flagged |
| Croatia | Maybe | Others | Male | 25 | flagged |
| Czech Republic | Yes | Business | Male | 25 | flagged |
| Czech Republic | Yes | Housewife | Male | 24 | flagged |
| Czech Republic | Yes | Others | Male | 18 | flagged |
| Czech Republic | Yes | Student | Male | 28 | flagged |
| Czech Republic | No | Business | Male | 18 | flagged |
| Czech Republic | No | Corporate | Male | 29 | flagged |
| Czech Republic | No | Others | Male | 26 | flagged |
| Czech Republic | No | Student | Male | 20 | flagged |
| Czech Republic | Maybe | Business | Male | 23 | flagged |
| Czech Republic | Maybe | Corporate | Male | 23 | flagged |
| Czech Republic | Maybe | Others | Male | 25 | flagged |
| Finland | Yes | Business | Male | 25 | flagged |
| Finland | Yes | Housewife | Male | 24 | flagged |
| Finland | Yes | Others | Male | 18 | flagged |
| Finland | Yes | Student | Male | 28 | flagged |
| Finland | No | Business | Male | 18 | flagged |
| Finland | No | Corporate | Male | 29 | flagged |
| Finland | No | Others | Male | 26 | flagged |
| Finland | No | Student | Male | 20 | flagged |
| Finland | Maybe | Business | Male | 23 | flagged |
| Finland | Maybe | Corporate | Male | 23 | flagged |
| Finland | Maybe | Others | Male | 25 | flagged |
| Georgia | Yes | Business | Male | 25 | flagged |
| Georgia | Yes | Housewife | Male | 24 | flagged |
| Georgia | Yes | Others | Male | 18 | flagged |
| Georgia | Yes | Student | Male | 28 | flagged |
| Georgia | No | Business | Male | 18 | flagged |
| Georgia | No | Corporate | Male | 29 | flagged |
| Georgia | No | Others | Male | 26 | flagged |
| Georgia | No | Student | Male | 20 | flagged |
| Georgia | Maybe | Business | Male | 23 | flagged |
| Georgia | Maybe | Corporate | Male | 23 | flagged |
| Georgia | Maybe | Others | Male | 25 | flagged |
| India | Yes | Business | Female | 29 | flagged |
| India | No | Business | Female | 26 | flagged |
| India | No | Corporate | Female | 19 | flagged |
| India | No | Housewife | Female | 24 | flagged |
| India | No | Others | Female | 25 | flagged |
| India | Maybe | Business | Female | 24 | flagged |
| India | Maybe | Corporate | Female | 24 | flagged |
| India | Maybe | Others | Female | 25 | flagged |
| India | Maybe | Student | Female | 25 | flagged |
| Mexico | Yes | Business | Male | 25 | flagged |
| Mexico | Yes | Housewife | Male | 24 | flagged |
| Mexico | Yes | Others | Male | 18 | flagged |
| Mexico | Yes | Student | Male | 28 | flagged |
| Mexico | No | Business | Male | 18 | flagged |
| Mexico | No | Corporate | Male | 29 | flagged |
| Mexico | No | Others | Male | 26 | flagged |
| Mexico | No | Student | Male | 20 | flagged |
| Mexico | Maybe | Business | Male | 23 | flagged |
| Mexico | Maybe | Corporate | Male | 23 | flagged |
| Mexico | Maybe | Others | Male | 25 | flagged |
| Moldova | Yes | Business | Male | 25 | flagged |
| Moldova | Yes | Housewife | Male | 24 | flagged |
| Moldova | Yes | Others | Male | 18 | flagged |
| Moldova | Yes | Student | Male | 28 | flagged |
| Moldova | No | Business | Male | 18 | flagged |
| Moldova | No | Corporate | Male | 29 | flagged |
| Moldova | No | Others | Male | 26 | flagged |
| Moldova | No | Student | Male | 20 | flagged |
| Moldova | Maybe | Business | Male | 23 | flagged |
| Moldova | Maybe | Corporate | Male | 23 | flagged |
| Moldova | Maybe | Others | Male | 25 | flagged |
| Netherlands | Yes | Business | Female | 29 | flagged |
| Netherlands | No | Business | Female | 26 | flagged |
| Netherlands | No | Corporate | Female | 19 | flagged |
| Netherlands | No | Housewife | Female | 24 | flagged |
| Netherlands | No | Others | Female | 25 | flagged |
| Netherlands | Maybe | Business | Female | 24 | flagged |
| Netherlands | Maybe | Corporate | Female | 24 | flagged |
| Netherlands | Maybe | Others | Female | 25 | flagged |
| Netherlands | Maybe | Student | Female | 25 | flagged |
| New Zealand | Yes | Business | Female | 29 | flagged |
| New Zealand | No | Business | Female | 26 | flagged |
| New Zealand | No | Corporate | Female | 19 | flagged |
| New Zealand | No | Housewife | Female | 24 | flagged |
| New Zealand | No | Others | Female | 25 | flagged |
| New Zealand | Maybe | Business | Female | 24 | flagged |
| New Zealand | Maybe | Corporate | Female | 24 | flagged |
| New Zealand | Maybe | Others | Female | 25 | flagged |
| New Zealand | Maybe | Student | Female | 25 | flagged |
| Nigeria | Yes | Business | Male | 25 | flagged |
| Nigeria | Yes | Housewife | Male | 24 | flagged |
| Nigeria | Yes | Others | Male | 18 | flagged |
| Nigeria | Yes | Student | Male | 28 | flagged |
| Nigeria | No | Business | Male | 18 | flagged |
| Nigeria | No | Corporate | Male | 29 | flagged |
| Nigeria | No | Others | Male | 26 | flagged |
| Nigeria | No | Student | Male | 20 | flagged |
| Nigeria | Maybe | Business | Male | 23 | flagged |
| Nigeria | Maybe | Corporate | Male | 23 | flagged |
| Nigeria | Maybe | Others | Male | 25 | flagged |
| Philippines | Yes | Business | Male | 25 | flagged |
| Philippines | Yes | Housewife | Male | 24 | flagged |
| Philippines | Yes | Others | Male | 18 | flagged |
| Philippines | Yes | Student | Male | 28 | flagged |
| Philippines | No | Business | Male | 18 | flagged |
| Philippines | No | Corporate | Male | 29 | flagged |
| Philippines | No | Others | Male | 26 | flagged |
| Philippines | No | Student | Male | 20 | flagged |
| Philippines | Maybe | Business | Male | 23 | flagged |
| Philippines | Maybe | Corporate | Male | 23 | flagged |
| Philippines | Maybe | Others | Male | 25 | flagged |
| Poland | Yes | Business | Male | 25 | flagged |
| Poland | Yes | Business | Female | 29 | flagged |
| Poland | Yes | Housewife | Male | 24 | flagged |
| Poland | Yes | Others | Male | 18 | flagged |
| Poland | Yes | Student | Male | 28 | flagged |
| Poland | No | Business | Male | 18 | flagged |
| Poland | No | Business | Female | 26 | flagged |
| Poland | No | Corporate | Male | 29 | flagged |
| Poland | No | Corporate | Female | 19 | flagged |
| Poland | No | Housewife | Female | 24 | flagged |
| Poland | No | Others | Male | 26 | flagged |
| Poland | No | Others | Female | 25 | flagged |
| Poland | No | Student | Male | 20 | flagged |
| Poland | Maybe | Business | Male | 23 | flagged |
| Poland | Maybe | Business | Female | 24 | flagged |
| Poland | Maybe | Corporate | Male | 23 | flagged |
| Poland | Maybe | Corporate | Female | 24 | flagged |
| Poland | Maybe | Others | Male | 25 | flagged |
| Poland | Maybe | Others | Female | 25 | flagged |
| Poland | Maybe | Student | Female | 25 | flagged |
| Portugal | Yes | Business | Male | 25 | flagged |
| Portugal | Yes | Housewife | Male | 24 | flagged |
| Portugal | Yes | Others | Male | 18 | flagged |
| Portugal | Yes | Student | Male | 28 | flagged |
| Portugal | No | Business | Male | 18 | flagged |
| Portugal | No | Corporate | Male | 29 | flagged |
| Portugal | No | Others | Male | 26 | flagged |
| Portugal | No | Student | Male | 20 | flagged |
| Portugal | Maybe | Business | Male | 23 | flagged |
| Portugal | Maybe | Corporate | Male | 23 | flagged |
| Portugal | Maybe | Others | Male | 25 | flagged |
| South Africa | Yes | Business | Female | 29 | flagged |
| South Africa | No | Business | Female | 26 | flagged |
| South Africa | No | Corporate | Female | 19 | flagged |
| South Africa | No | Housewife | Female | 24 | flagged |
| South Africa | No | Others | Female | 25 | flagged |
| South Africa | Maybe | Business | Female | 24 | flagged |
| South Africa | Maybe | Corporate | Female | 24 | flagged |
| South Africa | Maybe | Others | Female | 25 | flagged |
| South Africa | Maybe | Student | Female | 25 | flagged |
| Thailand | Yes | Business | Male | 25 | flagged |
| Thailand | Yes | Housewife | Male | 24 | flagged |
| Thailand | Yes | Others | Male | 18 | flagged |
| Thailand | Yes | Student | Male | 28 | flagged |
| Thailand | No | Business | Male | 18 | flagged |
| Thailand | No | Corporate | Male | 29 | flagged |
| Thailand | No | Others | Male | 26 | flagged |
| Thailand | No | Student | Male | 20 | flagged |
| Thailand | Maybe | Business | Male | 23 | flagged |
| Thailand | Maybe | Corporate | Male | 23 | flagged |
| Thailand | Maybe | Others | Male | 25 | flagged |

</details>

### Q7

* **Criteria:** [Q7](correspondence-criteria.md#q7).
* **Indicator:** 14 (`89517806a9d9`): lifetime treatment-seeking in the rows where `symptom_cluster` holds, a self-reported profile ([validity caveat](../specification/definitions.md#symptom_cluster)), partitioned by the three levels of `growing_stress` (indicator 14; [ADR-0003](../decisions/0003-redefine-indicators-14-to-16.md)).
* **C1:** not met. Locus: provenance. Cells: 3 required cells: 3 present, 0 missing, 0 flagged.
* **Verdict:** does not correspond. Cause: "under the reading that the file joins two sources, this cross says nothing about respondents". `treatment` belongs to the OSMI group, and `growing_stress` and the columns of `symptom_cluster` to the other ([LOG-040](../decisions/log/LOG-040-h1-column-groups.md)).
* **Design findings:** none.

Cells read (indicator 14, `Yes` level of `treatment`):

| growing_stress | denominator | Yes | low_n |
|---|---|---|---|
| Yes | 18265 | 9426 (0.516069) | false |
| No | 17907 | 9036 (0.504607) | false |
| Maybe | 17176 | 8670 (0.504774) | false |

### Q7.1

* **Criteria:** [Q7.1](correspondence-criteria.md#q71). The premise of `care_options` holds (section 2).
* **Indicator:** 15 (`22e4281080ef`).
* **C1:** not met. Locus: provenance. Cells: 8 required cells: 8 present, 0 missing, 0 flagged.
* **Verdict:** does not correspond. Cause: "under the reading that the file joins two sources, this cross says nothing about respondents".
* **Documentary layer:** in the [criteria, Q7.1](correspondence-criteria.md#q71). It gives no verdict ([LOG-051](../decisions/log/LOG-051-stopping-rule-documentary-audit-readings.md); LOG-045, addendum of 2026-10-25).
* **Design findings:** none.

Cells read (indicator 15, `Yes` level of `treatment`):

| growing_stress | symptom_cluster | care_options | denominator | Yes | low_n |
|---|---|---|---|---|---|
| Yes | true | Yes | 6050 | 4367 (0.721818) | false |
| Yes | true | Not sure | 4953 | 2012 (0.406218) | false |
| Yes | false | Yes | 26478 | 18985 (0.717010) | false |
| Yes | false | Not sure | 21684 | 8662 (0.399465) | false |
| Maybe | true | Yes | 5618 | 4007 (0.713243) | false |
| Maybe | true | Not sure | 4602 | 1814 (0.394176) | false |
| No | true | Yes | 5856 | 4176 (0.713115) | false |
| No | true | Not sure | 4797 | 1890 (0.393996) | false |

### Q7.2

* **Criteria:** [Q7.2](correspondence-criteria.md#q72). The premise of `care_options` holds (section 2).
* **Indicator:** 16 (`84ea62685552`): the `No` level of `treatment`, the share who report no lifetime treatment-seeking.
* **C1:** not met. Locus: provenance. Cells: 8 strata, 24 required cells: 24 present, 0 missing, 0 flagged.
* **Verdict:** does not correspond. Cause: "under the reading that the file joins two sources, this cross says nothing about respondents".
* **Design findings:** none.

Reading list, headline stratum first:

| Stratum | Reading | Missing | Flagged |
|---|---|---|---|
| growing_stress=Yes; symptom_cluster=true; care_options=Yes | readable | 0 | 0 |
| growing_stress=Yes; symptom_cluster=true; care_options=Not sure | readable | 0 | 0 |
| growing_stress=Yes; symptom_cluster=false; care_options=Yes | readable | 0 | 0 |
| growing_stress=Yes; symptom_cluster=false; care_options=Not sure | readable | 0 | 0 |
| growing_stress=Maybe; symptom_cluster=true; care_options=Yes | readable | 0 | 0 |
| growing_stress=Maybe; symptom_cluster=true; care_options=Not sure | readable | 0 | 0 |
| growing_stress=No; symptom_cluster=true; care_options=Yes | readable | 0 | 0 |
| growing_stress=No; symptom_cluster=true; care_options=Not sure | readable | 0 | 0 |

Cells read (indicator 16, `No` level of `treatment`):

| growing_stress | symptom_cluster | care_options | mental_health_interview | denominator | No | low_n |
|---|---|---|---|---|---|---|
| Yes | true | Yes | Yes | 219 | 81 (0.369863) | false |
| Yes | true | Yes | No | 4782 | 1268 (0.265161) | false |
| Yes | true | Yes | Maybe | 1049 | 334 (0.318398) | false |
| Yes | true | Not sure | Yes | 115 | 69 (0.600000) | false |
| Yes | true | Not sure | No | 3928 | 2193 (0.558299) | false |
| Yes | true | Not sure | Maybe | 910 | 679 (0.746154) | false |
| Yes | false | Yes | Yes | 976 | 346 (0.354508) | false |
| Yes | false | Yes | No | 20832 | 5646 (0.271025) | false |
| Yes | false | Yes | Maybe | 4670 | 1501 (0.321413) | false |
| Yes | false | Not sure | Yes | 525 | 315 (0.600000) | false |
| Yes | false | Not sure | No | 17076 | 9631 (0.564008) | false |
| Yes | false | Not sure | Maybe | 4083 | 3076 (0.753368) | false |
| Maybe | true | Yes | Yes | 210 | 72 (0.342857) | false |
| Maybe | true | Yes | No | 4404 | 1214 (0.275658) | false |
| Maybe | true | Yes | Maybe | 1004 | 325 (0.323705) | false |
| Maybe | true | Not sure | Yes | 115 | 69 (0.600000) | false |
| Maybe | true | Not sure | No | 3604 | 2049 (0.568535) | false |
| Maybe | true | Not sure | Maybe | 883 | 670 (0.758777) | false |
| No | true | Yes | Yes | 219 | 75 (0.342466) | false |
| No | true | Yes | No | 4590 | 1266 (0.275817) | false |
| No | true | Yes | Maybe | 1047 | 339 (0.323782) | false |
| No | true | Not sure | Yes | 120 | 72 (0.600000) | false |
| No | true | Not sure | No | 3756 | 2136 (0.568690) | false |
| No | true | Not sure | Maybe | 921 | 699 (0.758958) | false |

### Query-time cost (DC-21)

[ADR-0007](../decisions/0007-person-grain-fact-table-and-dimension-grain-rule.md) computes every indicator at query time and leaves its cost at the volume of the staged records as an assumption to check once the pipeline exists (documentation-currency register, DC-21). Measured by `uv run python -m stress_dw.query_time`: on one full reload, each indicator was run once to warm up and five times measured through `run_indicator`. Medians range from 2.5 ms (indicator 3) to 10.7 ms (indicator 12); every value is in [`query-time.csv`](correspondence-evidence/query-time.csv). Environment: DuckDB 1.5.5, Python 3.12.14, macOS 14.5 on an Apple M2 Max (arm64, 12 logical CPUs, 32 GB of memory). This is a measurement only; ADR-0007 states no threshold.
