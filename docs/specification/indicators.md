# Indicators by business question

The sixteen indicators are grouped by the business question each answers. Each block is headed by the question's wording as fixed in [ADR-0006](../decisions/0006-final-questions-and-indicators.md) (Q7.1: as amended in [ADR-0004](../decisions/0004-revise-business-questions.md)); the questions come from "Fase 1" (English: "Phase 1"; see [`methodology.md`](../methodology.md)). Indicator names are those of ADR-0006.

The **Pattern** column refers to [`patterns.md`](patterns.md): [A](patterns.md#pattern-a--level-distribution) is a level distribution, [B](patterns.md#pattern-b--conjunction-share) a conjunction share, [C](patterns.md#pattern-c--lifetime-treatment-share) a lifetime treatment share. Population, cuts, numerator and denominator are used as defined in the [query vocabulary](definitions.md#query-vocabulary).

## Q1 — indicators 1, 2

> How does the proportion of respondents reporting explicit stress recognition (`Growing_Stress`, all three levels) differ across the months represented in this dataset, by gender?

| # | Name | Pattern | Population | Measure | Cuts |
|---|------|---------|------------|---------|------|
| 1 | Stress-recognition (count) | A | all rows | V = `growing_stress`; numerator | none |
| 2 | Stress-recognition rate | A | all rows | V = `growing_stress`; rate | `period`, `gender` |

## Q2 — indicators 3, 4

> Among respondents with a family history of mental illness (`family_history = 'Yes'`), how does explicit stress recognition (`Growing_Stress`, all three levels) differ by gender and across the months represented in the dataset?

| # | Name | Pattern | Population | Measure | Cuts |
|---|------|---------|------------|---------|------|
| 3 | Family-history/stress coexistence (count) | A | `family_history = 'Yes'` | V = `growing_stress`; numerator | none |
| 4 | Family-history/stress coexistence rate | A | `family_history = 'Yes'` | V = `growing_stress`; rate | `gender`, `period` |

## Q3 — indicators 5, 6

> What occupations show a higher proportion of people with growing stress (Growing_Stress = Yes) and coping difficulties (Coping_Struggles = Yes), differentiated by country (Country), and how do these patterns vary when grouping countries by region or continent?

| # | Name | Pattern | Population | Measure | Cuts |
|---|------|---------|------------|---------|------|
| 5 | Stress/coping-difficulty co-occurrence (count) | B | all rows | C = `growing_stress = 'Yes' AND coping_struggles = 'Yes'`; numerator | {`occupation`, `country`}; {`occupation`, `region`} |
| 6 | Stress/coping-difficulty co-occurrence rate | B | all rows | same C; rate | same grouping sets |

The denominator is every row in the cell. `growing_stress` is part of the counted condition, not a lens on another variable: this is the documented exception in the [multi-level self-report rule](definitions.md#multi-level-self-report-rule).

## Q4 — indicators 7, 8

> What proportion of respondents report having ever sought treatment for a mental health condition (`treatment`, lifetime), by gender and by explicit stress recognition (`Growing_Stress`, all three levels)?

| # | Name | Pattern | Population | Measure | Cuts |
|---|------|---------|------------|---------|------|
| 7 | Lifetime treatment-seeking rate | C | all rows | V = `treatment`; rate, both levels | `gender`, `growing_stress` (3 levels) |
| 8 | Lifetime treatment-seeking (count) | C | all rows | numerator of the `Yes` level | `gender`, `growing_stress` (3 levels) |

## Q5 — indicators 9, 10, 11

> How do self-reported stress recognition (`Growing_Stress`), mood-swing level (`Mood_Swings`), and social weakness (`Social_Weakness`) differ across levels of time spent indoors (`Days_Indoors`)?

| # | Name | Pattern | Population | Measure | Cuts |
|---|------|---------|------------|---------|------|
| 9 | Explicit stress-recognition rate by isolation | A | all rows | V = `growing_stress`; rate | `days_indoors` (5 levels, ordered by `sort_order`) |
| 10 | Elevated mood-swings rate by isolation | A | all rows | V = `mood_swings`, three levels reported; headline rate = (numerator of `Medium` + numerator of `High`) / denominator | `days_indoors` |
| 11 | Social-weakness rate by isolation | A | all rows | V = `social_weakness`; rate | `days_indoors` |

## Q6 — indicators 12, 13

> How does resource availability (`care_options`, "Yes" and "Not sure" reported separately) differ by explicit stress recognition (`Growing_Stress`, all three levels), country, occupation, and gender?

| # | Name | Pattern | Population | Measure | Cuts |
|---|------|---------|------------|---------|------|
| 12 | Stress/resource-access rate | A | all rows | V = `care_options`, three levels (`Yes`, `Not sure`, `No`); rate | `growing_stress` (3 levels), `country`, `occupation`, `gender` |
| 13 | Stress/resource-access (count) | A | all rows | V = `care_options`; numerator | same as 12 |

The denominator is the cell's full respondent count, so the three levels add to the denominator; `Yes` and `Not sure` stay separate ([multi-level self-report rule](definitions.md#multi-level-self-report-rule)).

## Q7 — indicator 14

> Among respondents with a convergent symptom profile (elevated `Mood_Swings`, `Coping_Struggles = 'Yes'`, and elevated `Days_Indoors`), what proportion report having ever sought treatment (`treatment`, lifetime), broken down by their level of explicit stress recognition (`Growing_Stress`, all three levels)?

| # | Name | Pattern | Population | Measure | Cuts |
|---|------|---------|------------|---------|------|
| 14 | Lifetime treatment-seeking rate by explicit-recognition level, within the convergent-symptom population | C | rows where `symptom_cluster` | V = `treatment`; rate, both levels | `growing_stress` (3 levels) |

Uses [`symptom_cluster`](definitions.md#symptom_cluster); see its validity caveat. The three cells sum to the number of rows where `symptom_cluster` holds.

## Q7.1 — indicator 15

> Among respondents with explicit stress recognition, a convergent symptom profile, or both, what proportion report having ever sought treatment (`treatment`, lifetime), broken down by resource availability (`care_options`, "Yes" and "Not sure" reported separately; respondents reporting "No" are outside this question's scope), by explicit stress recognition (`Growing_Stress`, all three levels), and by whether a convergent symptom profile is present?

| # | Name | Pattern | Population | Measure | Cuts |
|---|------|---------|------------|---------|------|
| 15 | Care-options-to-treatment conversion rate | C | `(explicit_recognition OR symptom_cluster) AND care_options IN ('Yes','Not sure')` | V = `treatment`; rate, both levels | `growing_stress` (3 levels), `symptom_cluster`, `care_options` (`Yes`, `Not sure`) |

Uses [`explicit_recognition`](definitions.md#explicit_recognition) and [`symptom_cluster`](definitions.md#symptom_cluster); see its validity caveat. The `care_options` restriction is a declared population filter ([multi-level self-report rule](definitions.md#multi-level-self-report-rule)). The union excludes every row that meets neither condition, so four (`growing_stress`, `symptom_cluster`) combinations occur in the population: (`Yes`, true), (`Yes`, false), (`Maybe`, true), (`No`, true). With two `care_options` levels the indicator has up to 8 cells.

## Q7.2 — indicator 16

> Among respondents with explicit stress recognition, a convergent symptom profile, or both, and who report having care options available, what proportion does not report lifetime treatment-seeking, broken down by their stated willingness to disclose a mental health issue to a potential employer?

| # | Name | Pattern | Population | Measure | Cuts |
|---|------|---------|------------|---------|------|
| 16 | Treatment non-uptake rate under full context | C | same as indicator 15 | V = `treatment`; both levels, the `No` level (non-uptake) being the quantity of interest | `growing_stress` (3 levels), `symptom_cluster`, `care_options` (`Yes`, `Not sure`), `mental_health_interview` (3 levels) |

Uses [`symptom_cluster`](definitions.md#symptom_cluster); see its validity caveat. Up to 4 × 2 × 3 = 24 cells. Headline cell: `growing_stress = 'Yes'`, `symptom_cluster` true, `care_options = 'Yes'`, `mental_health_interview = 'Yes'`.
