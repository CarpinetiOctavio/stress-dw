---
status: "proposed"
date: 2026-09-23
decision-makers: Octavio Carpineti
---

# Consolidated record: final Fase 1 questions and indicator definitions

## Context and Problem Statement

ADR-0003 (indicators 14–16), ADR-0004 (business questions), and ADR-0005 (indicators 1–13) each carry the full reasoning behind one piece of the specification redesign — findings, considered options, and per-item justification. Reconstructing "what did the project actually land on" means reading three separate documents and tracking which text superseded which. Nothing gathers the final, agreed state of all nine business questions and all sixteen indicators in one place, independent of the argument behind each. Should a single document consolidate that final state, distinct from both the full reasoning (the three ADRs above) and the implementation contract (`docs/specification.md`)?

## Decision Drivers

* `docs/specification.md` is reserved for the implementation contract — population, measure, and cuts as Code needs to build them — not for carrying the reasoning behind each decision. A reader still needs a place to see the final state without opening three ADRs and tracking supersession across them.
* ADR-0003, ADR-0004, and ADR-0005 were produced across a long, exploratory conversation; each is complete on its own terms, but none of them alone is a checklist of the final, combined result.
* A one-line rationale per item is enough to say *why* something ended up the way it did without repeating the full argument — the full argument stays in the ADR that made it.

## Considered Options

* No consolidation; reconstruct the final state by reading ADR-0003, ADR-0004, and ADR-0005 in full whenever it's needed.
* Consolidate into `docs/specification.md` directly, alongside the implementation contract.
* A dedicated ADR listing the final questions and indicators, each with a brief rationale, kept separate from `docs/specification.md`.

## Decision Outcome

Chosen option: "A dedicated ADR listing the final questions and indicators, each with a brief rationale, kept separate from `docs/specification.md`," because folding this into the implementation contract would blur the separation of responsibilities already established for that document, and because a standalone reference is reusable independent of whether `docs/specification.md` has been written yet.

### Final business questions

| Q | Final wording (English) | Why this is the final form |
|---|---|---|
| 1 | How does the proportion of respondents reporting explicit stress recognition (`Growing_Stress`, all three levels) differ across the months represented in this dataset, by gender? | Original wording ("evolves") implied tracked change within a followed population; the dataset has no panel structure (ADR-0004). |
| 2 | Among respondents with a family history of mental illness (`family_history = 'Yes'`), how does explicit stress recognition (`Growing_Stress`, all three levels) differ by gender and across the months represented in the dataset? | Same panel-structure correction as Q1 (ADR-0004). |
| 3 | "¿Qué ocupaciones muestran una mayor proporción de personas con estrés creciente (Growing_Stress = Yes) y dificultades de afrontamiento (Coping_Struggles = Yes), diferenciadas por país (Country), y cómo varían estos patrones al agrupar los países por región o continente?" → English: "What occupations show a higher proportion of people with growing stress (Growing_Stress = Yes) and coping difficulties (Coping_Struggles = Yes), differentiated by country (Country), and how do these patterns vary when grouping countries by region or continent?" | Reviewed, not revised — `Growing_Stress` here is part of the condition being counted, not a lens for measuring something else, so the usual three-level partition doesn't apply (ADR-0005). |
| 4 | What proportion of respondents report having ever sought treatment for a mental health condition (`treatment`, lifetime), by gender and by explicit stress recognition (`Growing_Stress`, all three levels)? | Original wording ("buscan tratamiento," present tense) read as current status; `treatment` is a lifetime measure (F3, ADR-0004). |
| 5 | How do self-reported stress recognition (`Growing_Stress`), mood-swing level (`Mood_Swings`), and social weakness (`Social_Weakness`) differ across levels of time spent indoors (`Days_Indoors`)? | Original wording ("influye") asserted causal direction a cross-sectional record cannot establish (ADR-0004). |
| 6 | How does resource availability (`care_options`, "Yes" and "Not sure" reported separately) differ by explicit stress recognition (`Growing_Stress`, all three levels), country, occupation, and gender? | Original wording treated `Growing_Stress` as binary and folded `care_options` into "≠ No" (ADR-0004). |
| 7 | Among respondents with a convergent symptom profile (elevated `Mood_Swings`, `Coping_Struggles = 'Yes'`, and elevated `Days_Indoors`), what proportion report having ever sought treatment (`treatment`, lifetime), broken down by their level of explicit stress recognition (`Growing_Stress`, all three levels)? | Original wording filtered to `Growing_Stress = 'No'` with no comparison group (F3), used present-tense "buscan tratamiento," and asserted a level of psychological awareness a self-report item can't establish (ADR-0004). |
| 7.1 | Among respondents with explicit stress recognition, a convergent symptom profile, or both, what proportion report having ever sought treatment (`treatment`, lifetime), broken down by resource availability (`care_options`, "Yes" and "Not sure" reported separately) and by which condition led to their inclusion (explicit-only / convergent-only / both)? | Original wording used present-tense "deciden buscar tratamiento" and folded `care_options` into "≠ No" (ADR-0004). |
| 7.2 | Among respondents with explicit stress recognition, a convergent symptom profile, or both, and who report having care options available, what proportion does not report lifetime treatment-seeking, broken down by their stated willingness to disclose a mental health issue to a potential employer? | Original wording ("participaron en una entrevista de salud mental") reflected the exposure/participation misreading of `mental_health_interview` that F3's addendum corrects (ADR-0004). |

### Final indicator definitions

| # | Name | Population | Measure | Cuts | Why |
|---|---|---|---|---|---|
| 1 | Stress-recognition (count) | All records | Count per `growing_stress` level | Level | Reports all three levels instead of a single "Yes" count (F5, ADR-0005). |
| 2 | Stress-recognition rate | All records | Rate per `growing_stress` level | Level × month × gender | Same, plus the month/gender view Q1 asks for (ADR-0005). |
| 3 | Family-history/stress coexistence (count) | `family_history = 'Yes'` | Count per `growing_stress` level | Level | Reports all three levels instead of one (F5, ADR-0005). |
| 4 | Family-history/stress coexistence rate | `family_history = 'Yes'` | Rate per `growing_stress` level | Level × gender × month | Renamed from "...developed stress" — coexistence, not development over time (F8, ADR-0005). |
| 5 | Stress/coping-difficulty co-occurrence (count) | `growing_stress = 'Yes' AND coping_struggles = 'Yes'` | Count | Occupation × country × region | Not partitioned by `growing_stress` — it's part of the condition counted, not a lens (documented exception, ADR-0005); region added because Q3 asks for it (F7). |
| 6 | Stress/coping-difficulty co-occurrence rate | Same as 5 | Rate | Occupation × country × region | Same reasoning as 5. |
| 7 | Lifetime treatment-seeking rate | All records | `COUNT(treatment='Yes')/COUNT(*)` and complement | Gender × `growing_stress` level | Renamed to lifetime language (F3); gender/recognition segmentation added because Q4 asks for it (F7, ADR-0005). |
| 8 | Lifetime treatment-seeking (count) | All records | `COUNT(treatment='Yes')` | Gender × `growing_stress` level | Same reasoning as 7. |
| 9 | Explicit stress-recognition rate by isolation | All records | Rate per `growing_stress` level | Isolation level | Renamed from "emotional deterioration," a claim a self-report item can't support (F8); partitioned instead of filtered to "Yes" (F5, ADR-0005). |
| 10 | Elevated mood-swings rate by isolation | All records | Rate, `Mood_Swings IN (Medium, High)`; three-level breakdown available alongside | Isolation level | Unchanged — a deliberate severity cut on an ordinal scale, not an ambiguous value folded silently (ADR-0005). |
| 11 | Social-weakness rate by isolation | All records | Rate per `social_weakness` level | Isolation level | Partitioned instead of filtered to "Yes" (F5, ADR-0005). |
| 12 | Stress/resource-access rate | All records | Rate per `growing_stress` level, crossed with `care_options` level | `growing_stress` level × `care_options` (Yes / Not sure) × country × occupation × gender | Partitioned instead of filtered to "Yes" (F5); "Yes" and "Not sure" reported separately instead of folded (F6, ADR-0005). |
| 13 | Stress/resource-access (count) | All records | Count on the same cells as 12 | Same as 12 | Same reasoning as 12. |
| 14 | Lifetime treatment-seeking rate by explicit-recognition level, within the convergent-symptom population | `symptom_cluster = TRUE` | `COUNT(treatment='Yes')/COUNT(*)` | `growing_stress` level (3) | Isolates recognition as the only variable differing between groups, holding symptom profile constant (Design A, ADR-0003). |
| 15 | Care-options-to-treatment conversion rate, by inclusion path | `explicit_recognition OR symptom_cluster`, tagged by inclusion path | Lifetime treatment rate | Inclusion path (explicit-only / convergent-only / both) × `care_options` (Yes / Not sure) | Resolves both problems F3 identified for this indicator, not only the "Not sure" fold (ADR-0003). |
| 16 | Treatment non-uptake rate under full context | Same population as 15 | Lifetime treatment rate and its complement; headline cell = `both` × `Yes` × `Yes` | Inclusion path × `care_options` × `mental_health_interview` (3 levels) | Name asserts no claim of postponement — no time-to-treatment variable exists; grounded in Andrade et al. 2014 on settled self-reliance as the more common pattern (ADR-0003). |

`symptom_cluster` (`mood_swings IN ('Medium','High') AND coping_struggles='Yes' AND days_indoors IN ('15-30 days','31-60 days','More than 2 months')`) and `explicit_recognition` (`growing_stress='Yes'`) are the two components that replace the legacy's single OR'd `Indicador_Inferido_Estrés` flag. Neither the collapsed flag nor any of indicators 14–16 individually needs it stored as one column; both components are computed at query time, joining `dim_symptoms` and `dim_isolation` through the fact table (dimension-design discussion, this conversation; formalized here for reference).

### Consequences

* Good, because the final state of all nine questions and sixteen indicators is readable in one place, without needing to reconstruct it from three separate ADRs.
* Good, because each entry's one-line rationale points back to the ADR that argued it, so nothing here needs to be taken on faith.
* Bad, because this document's content will need a manual update if any of ADR-0003, ADR-0004, or ADR-0005 is amended after this one is written — it is a snapshot, not a live derivation.

### Confirmation

Every question and indicator listed here traces to a specific ADR (0003, 0004, or 0005); a discrepancy between this document and one of those three is a documentation bug in whichever was updated without updating the other.

## Pros and Cons of the Options

### No consolidation

* Good, because it creates no document to keep in sync.
* Bad, because "what did we end up with" requires reading three ADRs in full every time it comes up.

### Consolidate into `docs/specification.md`

* Good, because it avoids a fourth document.
* Bad, because it mixes the implementation contract with the "why," exactly the separation of responsibilities already established for that document.

### Dedicated ADR

* Good, because it is reusable on its own and keeps `docs/specification.md` limited to the contract.
* Bad, because it is one more document to keep in sync if the underlying ADRs change.

## More Information

* Related: [ADR-0000](0000-rebuild-from-scratch-instead-of-continuing-legacy.md) (F3), [ADR-0003](0003-redefine-indicators-14-to-16.md), [ADR-0004](0004-revise-business-questions.md), [ADR-0005](0005-redefine-indicators-1-to-13.md).
* `docs/conceptual-framework.md` §3 (Andrade et al. 2014), §5, §7.
* `docs/methodology.md` — the Hefesto phases each question and indicator traces back to.