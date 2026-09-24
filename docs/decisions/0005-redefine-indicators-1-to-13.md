---
status: "accepted"
date: 2026-09-23
decision-makers: Octavio Carpineti
---

# Redefine indicators 1–13 around verifiable constructs

## Context and Problem Statement

ADR-0003 corrected indicators 14–16: ambiguous self-report values kept as their own reporting category instead of folded, `care_options = 'Yes'` separated from `'Not sure'`, and each indicator named after a construct its variables can actually support. Re-examining indicators 1–13 under the same scrutiny — prompted by the parallel revision of the business questions in ADR-0004 — surfaces the same defect class in several of them, plus two problems specific to this group: indicator names that claim more than a single cross-sectional self-report item can support, and indicators that do not implement the exact grouping their own business question requests. Should indicators 1–13 be redefined to correct these, and if so, which ones and how?

This ADR continues the `F` sequence from ADR-0000 rather than starting a new letter: these are the same class of specification defect F3 identified — an indicator not measuring what its name or its business question claims — found here in the indicators outside ADR-0003's scope, not a new category of audit.

## Findings

| ID | Finding | Evidence | Status |
|----|---------|----------|--------|
| F5 | Indicators 1, 2, 3, 4, 9, 11, 12, and 13 filter a three-level self-report variable (`Growing_Stress` or `Social_Weakness`) down to a single value — typically `'Yes'` — silently assuming an interpretation for `'Maybe'`. The same defect class F3 identified for indicators 14–16, found here in indicators outside that ADR's scope. | Legacy report, Fase 2 (English: "Phase 2" — Hefesto's OLTP-analysis phase; see `docs/methodology.md`; original indicator formulas) | Established |
| F6 | Indicators 12 and 13 fold `care_options IN ('Yes', 'Not sure')` into a single "has access" category, obscuring the distinction between definite and uncertain resource availability — the same fold F3 identified for indicator 15. | Legacy report, Fase 2 (original indicator formulas) | Established |
| F7 | Indicators 5 and 6 do not implement the region-level grouping Q3 explicitly requests — Q3's own text: "al agrupar los países por región o continente" (English: "when grouping countries by region or continent"). Indicators 7 and 8 do not implement the gender or recognition-level segmentation Q4 explicitly requests — Q4's own text: "cómo varía dicha proporción... según el género" (English: "how that proportion varies... by gender"). | Legacy report, Fase 1 (English: "Phase 1" — Hefesto's requirements-analysis phase; see `docs/methodology.md`; Q3, Q4) and Fase 2 (original indicator formulas) | Established |
| F8 | Indicator names 4 and 9 describe a process or a clinical state that a single cross-sectional self-report item cannot establish. Indicator 4's original name: "proporción con historial familiar que **desarrollan** estrés" (English: "proportion with family history who **develop** stress") — "develop" implies change over time. Indicator 9's original name: "proporción con **deterioro emocional** por aislamiento" (English: "proportion with **emotional deterioration** from isolation") — "emotional deterioration" is a clinical claim. The dataset shows co-occurrence within one survey response, not development over time or clinical deterioration. | Legacy report, Fase 2 (indicator names); `conceptual-framework.md` §5 | Established |

## Decision Drivers

* The principle behind ADR-0003 — a respondent's own answer left ambiguous should not be resolved by the pipeline's assumption — applies with no exception to every indicator built on a three-level self-report field, not only 14–16.
* Indicators 5, 6 and Q3 are the one case where partitioning by a self-report level does not apply: in that pair, `Growing_Stress` is not a lens used to measure some other variable — it is one of the two variables the business question names jointly as the condition of interest. Q3's own text: "estrés **y** dificultades de afrontamiento" (English: "stress **and** coping difficulties"). There is no separate measured variable whose reading would be biased by how `'Maybe'` is treated, because recognition itself is part of what is being counted. This exception is documented here explicitly so a later reviewer does not read the absence of partitioning as an oversight.
* Indicator 10's `Mood_Swings IN ('Medium', 'High')` cut is a deliberate severity threshold on an ordinal three-level scale, not an ambiguous value folded silently — re-examined under F5 and confirmed not to be an instance of it. It is left unchanged for the same reason 5 and 6 are: nothing here substitutes an assumption for what the respondent actually reported.
* A business question that names a specific grouping (region for Q3, gender for Q4) is not answered by an indicator that omits it, even where every other part of the indicator is otherwise correct.
* An indicator's name is read by people who never look at its query; a name claiming more than a single self-report item can support misleads that reader regardless of how carefully the query itself is written.
* `symptom_cluster`'s lack of external clinical validation (`conceptual-framework.md` §7) is already established and does not need to be re-argued here — but it needs to be repeated at every point this document or `docs/specification.md` defines or uses `symptom_cluster`, not stated once and assumed to carry forward.

## Considered Options

* Leave indicators 1–13 as originally defined; record the newly found gaps only as known limitations, without changing formulas or names.
* Apply the corrections that change population filters (F5, F6) only, leaving indicator names and missing groupings (F7, F8) for a later, separate pass.
* Apply all four corrections (F5, F6, F7, F8) together, across every indicator they affect.

## Decision Outcome

Chosen option: "Apply all four corrections together, across every indicator they affect," because leaving any of them unresolved would mean shipping the same defect class ADR-0003 already argued against, in the same specification, for a subset of indicators arbitrarily excluded from the fix.

**Indicators 1, 2 — stress recognition (count / rate).** Population: all records. Measure: distribution across the three levels of `Growing_Stress` (F5), not a single "Yes" rate. Cuts: level only (1); month × gender (2). No rename — "estrés creciente" ("growing stress") already describes exactly what is counted.

**Indicators 3, 4 — family history and stress.** Population: `family_history = 'Yes'`. Measure: distribution across the three levels of `Growing_Stress` (F5). Cuts: level only (3); level × gender × month (4). Indicator 4 renamed from "... que desarrollan estrés" (English: "...who develop stress") to *family-history/stress coexistence rate* (F8) — coexistence within one response, not development over time.

**Indicators 5, 6 — stress and coping difficulty by occupation/country.** Population and condition unchanged: `Growing_Stress = 'Yes' AND Coping_Struggles = 'Yes'`, not partitioned (documented exception to F5, per Decision Drivers). Corrected to add region as an explicit cut alongside country and occupation, in both the count (5) and the rate (6) — Q3 asks for the region-level view in both, not only the rate. The legacy's country-to-region mapping is reproduced verbatim in `docs/specification.md` rather than left implicit in `dim_country`'s existence.

**Indicators 7, 8 — treatment-seeking.** Renamed to *lifetime treatment-seeking rate* (7, reporting both uptake and its complement) and *lifetime treatment-seeking (count)* (8) — same semantic correction F3 already established for `treatment`, applied here for the first time to these two. Corrected to add gender × `Growing_Stress`-level (three levels) as an explicit cut on both (F7) — Q4 asks for this segmentation and the original formulas did not implement it.

**Indicator 9 — stress recognition by isolation.** Renamed from "deterioro emocional" (English: "emotional deterioration") to *explicit stress-recognition rate by isolation level* (F8) — a self-report recognition rate, not a measure of emotional deterioration. Partitioned by all three levels of `Growing_Stress` (F5) instead of filtering to `'Yes'`.

**Indicator 10 — mood swings by isolation.** Unchanged. `Mood_Swings IN ('Medium', 'High')` is a deliberate severity cut, not an instance of F5 (Decision Drivers).

**Indicator 11 — social weakness by isolation.** Partitioned by all three levels of `Social_Weakness` (F5) instead of filtering to `'Yes'`.

**Indicators 12, 13 — stress and resource access.** Population no longer filtered to `Growing_Stress = 'Yes'` — partitioned by all three levels (F5). `care_options = 'Yes'` and `care_options = 'Not sure'` reported separately instead of folded into "has access" (F6) — the same correction F3 established for indicator 15, applied here for the first time to 12 and 13. Country × occupation × gender kept as cuts, per Q6.

### Consequences

* Good, because every indicator built on a three-level self-report field now treats all three levels the same way across all sixteen indicators, with no undocumented exception.
* Good, because indicators 5, 6, 7, and 8 now answer the exact grouping their own business question asks for, not a narrower version of it.
* Bad, because several indicators that were a single scalar rate become a small table of rates (up to three `Growing_Stress` levels crossed with whatever other cuts apply) — the same reporting trade-off ADR-0003 already accepted for 14–16, now extended to more of the sixteen.
* Constraint: `symptom_cluster`'s validity caveat must be repeated at every point `docs/specification.md` defines or uses it, not stated once and assumed to carry over.

### Confirmation

`docs/specification.md` implements each of indicators 1–13 as a query pattern over the person-grain fact table, matching this ADR's population, measure, and cuts exactly. A post-build audit checks that each indicator's reported cells sum back to its declared population size, the same method already used for 14–16.

## Pros and Cons of the Options

### Leave as originally defined, record gaps as limitations

* Good, because it changes nothing already built.
* Bad, because it ships the same defect class ADR-0003 already argued against, for eight indicators arbitrarily excluded from the fix.

### Apply population-filter corrections only (F5, F6)

* Good, because it fixes the part of the defect most similar to what ADR-0003 already covered.
* Bad, because indicators 5–8 would still not answer the exact grouping their own business questions ask for, and indicators 4 and 9 would still carry names that overclaim.

### Apply all four corrections together

* Good, because it closes the entire defect class found in this audit in one pass, consistent with how ADR-0003 was scoped.
* Bad, because it is the largest single change of the four options, touching more of `docs/specification.md` at once.

## More Information

* Related: [ADR-0000](0000-rebuild-from-scratch-instead-of-continuing-legacy.md) (F3), [ADR-0003](0003-redefine-indicators-14-to-16.md), [ADR-0004](0004-revise-business-questions.md), [ADR-0006](0006-final-questions-and-indicators.md).
* `docs/conceptual-framework.md` §5 (what this dataset cannot measure) and §7 (`symptom_cluster`'s validity caveat).
* `docs/methodology.md` — what "Fase 1" and "Fase 2" cited throughout this document refer to.
* Legacy report, Fase 1 (Q3, Q4) and Fase 2 (original indicator formulas), at tag `legacy-original`.