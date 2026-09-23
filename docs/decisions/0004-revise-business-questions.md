---
status: "proposed"
date: 2026-09-23
decision-makers: Octavio Carpineti
---

# Revise Fase 1 business questions to match corrected variable semantics and dataset scope

## Context and Problem Statement

The nine business questions from Fase 1 (English: "Phase 1" — Hefesto's requirements-analysis phase; see `docs/methodology.md`; Q1–Q7, with Q7.1 and Q7.2 as sub-questions of Q7) were written before the corrected readings of `treatment` (lifetime, not current) and `mental_health_interview` (disclosure willingness, not exposure or participation) were established, and before the dataset's cross-sectional, no-panel-structure limitation was fully worked through. Several questions' wording still reflects the earlier, uncorrected assumptions — a wording problem, distinct from and prior to the indicator-design problems ADR-0005 addresses, since redefining the indicator underneath a stale question does not make the question itself accurate again. Should the business questions be reworded to match the dataset's actual scope and the corrected variable semantics, and if so, which ones and how?

## Findings

| ID | Finding | Evidence | Status |
|----|---------|----------|--------|
| F3 | `treatment` and `mental_health_interview` were read against the wrong semantics; several original business questions were phrased under the same misreadings (`treatment` as current status in Q4, Q7, Q7.1; `mental_health_interview` as participation/exposure in Q7.2). | ADR-0000 (Findings); ADR-0000 addendum (2026-09-23); `conceptual-framework.md` §4 | Established |
| — | The dataset is cross-sectional with no panel structure: a single survey response per respondent supports no claim of tracked change or causal influence. | `conceptual-framework.md` §5 | Established |

No new finding IDs are introduced here; both rows cite evidence already established elsewhere.

## Decision Drivers

* A stale business question, even where its underlying indicator is correctly computed, continues to advertise the wrong deliverable to anyone who reads Fase 1 without also reading the indicator's implementation — the correction needs to live where the question is asked, not only where it is answered.
* Reformulating drift-prone language ("developed," "influences," "evolution," "participated," "currently") one question at a time, as each is separately noticed, risks missing some and leaving an inconsistent standard across the set; reviewing all nine together against one shared checklist catches the full set in one pass.
* Q3 is the one question audited here and found not to need rewording — its own text already matches what its indicators (5, 6) compute. That needs to be stated explicitly, so a later audit does not mistake the absence of a revision for an oversight.

## Considered Options

* Leave the original Fase 1 question text as the historical record; note corrections only in indicator-level documentation (ADR-0005, `docs/specification.md`).
* Reword the affected questions directly, keeping the original wording as a dated note alongside each.
* Reword the affected questions directly, with no reference to the original wording.

## Decision Outcome

Chosen option: "Reword the affected questions directly, keeping the original wording as a dated note alongside each," because the original wording is itself evidence of how the project's own semantic misreadings shaped its business questions — worth keeping visible, on the same reasoning as the addendum already used for F3 — and because a reader should not have to cross-reference a second document just to know what is actually being asked.

Each original quote below is the legacy report's own Spanish text (Fase 1), followed by its literal English translation (marked `→`) preserving the original framing — including its flaws — so an English-only reader can see exactly what was originally asked, not only the corrected version. The "Revised" line is this ADR's corrected English wording, not a translation of the original.

Q3 reviewed, not revised — see Decision Drivers. The indicator-level reason its two indicators (5, 6) do not partition by `Growing_Stress` the way most others now do is documented in ADR-0005, not here; this ADR only confirms the question's own text needed no change.

### Q1 — originally:

"¿Cómo evoluciona mensualmente la proporción de personas que reportan estrés creciente (Growing_Stress = Yes) según el género (Gender)?"
→ English: "How does the monthly proportion of people reporting growing stress (Growing_Stress = Yes) evolve, by gender (Gender)?"

Problem: "evoluciona" ("evolves") implies tracked change within a followed population; the dataset has different respondents per period, not a panel.

Revised: How does the proportion of respondents reporting explicit stress recognition (`Growing_Stress`, all three levels) differ across the months represented in this dataset, by gender? Objective: compare explicit stress recognition across genders and across the surveyed period — not to trace change within a followed population, since the dataset has no panel structure.

### Q2 — originally:

"¿Qué porcentaje de personas con historial familiar de problemas de salud mental (family_history = Yes) presenta estrés creciente (Growing_Stress = Yes), y cómo varía dicha proporción a lo largo del tiempo según el género (Gender)?"
→ English: "What percentage of people with a family history of mental health problems (family_history = Yes) present growing stress (Growing_Stress = Yes), and how does that proportion vary over time by gender (Gender)?"

Problem: same panel-structure overclaim as Q1 ("varía... a lo largo del tiempo," "varies... over time").

Revised: Among respondents with a family history of mental illness (`family_history = 'Yes'`), how does explicit stress recognition (`Growing_Stress`, all three levels) differ by gender and across the months represented in the dataset? Objective: compare the co-occurrence of family history and explicit stress recognition across genders and across the surveyed period, without treating this as a tracked trend.

### Q4 — originally:

"¿Cuál es la proporción de personas que buscan tratamiento (treatment = Yes) frente a las que no (treatment = No), segmentado por género y presencia de estrés creciente (Growing_Stress)?"
→ English: "What is the proportion of people seeking treatment (treatment = Yes) versus those who are not (treatment = No), segmented by gender and the presence of growing stress (Growing_Stress)?"

Problem: "buscan tratamiento" ("are seeking treatment," present tense) reads as current status; `treatment` is a lifetime measure (F3).

Revised: What proportion of respondents report having ever sought treatment for a mental health condition (`treatment`, lifetime), by gender and by explicit stress recognition (`Growing_Stress`, all three levels)? Objective: compare lifetime treatment-seeking against explicit stress recognition, by gender.

### Q5 — originally:

"¿Cómo influye el tiempo pasado en interiores (Days_Indoors) en distintos indicadores de bienestar emocional y social, tales como estrés creciente (Growing_Stress), cambios de humor (Mood_Swings) y debilidad social (Social_Weakness)?"
→ English: "How does time spent indoors (Days_Indoors) influence different indicators of emotional and social well-being, such as growing stress (Growing_Stress), mood swings (Mood_Swings), and social weakness (Social_Weakness)?"

Problem: "influye" ("influences") asserts causal direction a single cross-sectional record per respondent cannot establish.

Revised: How do self-reported stress recognition (`Growing_Stress`), mood-swing level (`Mood_Swings`), and social weakness (`Social_Weakness`) differ across levels of time spent indoors (`Days_Indoors`)? Objective: describe how these self-reported measures co-occur with different levels of indoor time, without asserting that indoor time causes or influences them.

### Q6 — originally:

"¿Qué proporción de personas con estrés creciente (Growing_Stress = Yes) cuenta con opciones de cuidado o apoyo (care_options ≠ 'No'), diferenciadas por país (Country), ocupación (Occupation) y género (Gender)?"
→ English: "What proportion of people with growing stress (Growing_Stress = Yes) have care or support options available (care_options ≠ 'No'), broken down by country (Country), occupation (Occupation), and gender (Gender)?"

Problem: treats `Growing_Stress` as binary (`= Yes`), inconsistent with the three-level self-report the variable actually carries; folds `care_options` into `≠ 'No'`.

Revised: How does resource availability (`care_options`, "Yes" and "Not sure" reported separately) differ by explicit stress recognition (`Growing_Stress`, all three levels), country, occupation, and gender? Objective: describe how resource availability varies across geographic, occupational, and gender context.

### Q7 — originally:

"¿Cuál es la proporción de personas que, aun no reconociendo estrés explícito (Growing_Stress = No) pero presentando síntomas compatibles (Mood_Swings, Coping_Struggles, Days_Indoors elevado), buscan tratamiento (treatment = Yes) frente a quienes no lo hacen?"
→ English: "What is the proportion of people who, despite not explicitly recognizing stress (Growing_Stress = No) but presenting compatible symptoms (elevated Mood_Swings, Coping_Struggles, Days_Indoors), seek treatment (treatment = Yes), versus those who do not?"

Problem: filters to `Growing_Stress = 'No'` with no comparison group (F3); "buscan tratamiento" reads as current status; the original objective's "nivel de conciencia" ("level of awareness") asserts a psychological state a self-report item cannot establish.

Revised: Among respondents with a convergent symptom profile (elevated `Mood_Swings`, `Coping_Struggles = 'Yes'`, and elevated `Days_Indoors`), what proportion report having ever sought treatment (`treatment`, lifetime), broken down by their level of explicit stress recognition (`Growing_Stress`, all three levels)? Objective: compare lifetime treatment-seeking across levels of explicit recognition within the same symptom profile — describing a relationship between self-reported recognition and treatment-seeking, not a level of psychological awareness or a degree of mental deterioration.

### Q7.1 — originally:

"¿Cuál es la proporción de personas con estrés o síntomas asociados que, teniendo opciones de cuidado o cobertura (care_options ≠ 'No'), deciden buscar tratamiento (treatment = Yes) frente a quienes no lo hacen?"
→ English: "What is the proportion of people with stress or associated symptoms who, having care or coverage options available (care_options ≠ 'No'), decide to seek treatment (treatment = Yes), versus those who do not?"

Problem: "deciden buscar tratamiento" ("decide to seek treatment," present tense) reads as current status; folds `care_options` into `≠ 'No'`; population needs to reflect which condition (explicit recognition, symptom convergence, or both) triggered inclusion, per ADR-0003.

Revised: Among respondents with explicit stress recognition, a convergent symptom profile, or both, what proportion report having ever sought treatment (`treatment`, lifetime), broken down by resource availability (`care_options`, "Yes" and "Not sure" reported separately) and by which condition led to their inclusion (explicit-only / convergent-only / both)? Objective: measure the gap between resource availability and actual lifetime treatment-seeking, without implying an active, ongoing decision process.

### Q7.2 — originally:

"¿Entre las personas que reportan estrés o síntomas relacionados, cuál es la proporción de quienes participaron en una entrevista de salud mental (mental_health_interview ≠ 'No') y, aun teniendo cobertura (care_options ≠ 'No'), no buscan tratamiento (treatment = No)?"
→ English: "Among people who report stress or related symptoms, what is the proportion of those who participated in a mental-health interview (mental_health_interview ≠ 'No') and, despite having coverage (care_options ≠ 'No'), do not seek treatment (treatment = No)?"

Problem: "participaron en una entrevista de salud mental" ("participated in a mental-health interview") is the exposure/participation misreading of `mental_health_interview` that F3's addendum corrects; the variable's source-documented meaning is disclosure willingness ("Would you bring up a mental health issue with a potential employer in an interview?"), an attitudinal item, not an event that occurred.

Revised: Among respondents with explicit stress recognition, a convergent symptom profile, or both, and who report having care options available, what proportion does not report lifetime treatment-seeking, broken down by their stated willingness to disclose a mental health issue to a potential employer? Objective: describe whether non-uptake of treatment persists even among respondents with the fullest context this dataset can express — recognized or inferred symptoms, resource availability, and a stated attitude toward disclosure — without asserting this reflects postponement, since no time-to-treatment variable exists in the data.

### Consequences

* Good, because every question's text now matches exactly what its indicator(s) compute — no drift between what is asked and what is answered.
* Good, because the original wording, preserved and translated alongside each revision, keeps the audit trail visible to any reader without a second document or a translation step of their own.
* Bad, because the legacy report's Fase 1 still reads as originally written, unmodified per the project's own rule against touching the legacy repository; the corrected versions exist only in the new repository.
* Constraint: any future new business question must be checked against this ADR's own checklist — lifetime vs. current-state tense, panel-structure or causal-influence claims, ambiguous self-report values folded to one level, semantics of variables without a documented source description — before being added to `docs/specification.md`.

### Confirmation

`docs/specification.md` uses the corrected wording verbatim as the header for each indicator group; a mismatch between this ADR's wording and `docs/specification.md`'s wording is a documentation bug to fix, not a second valid phrasing.

## Pros and Cons of the Options

### Leave original text, correct only at the indicator level

* Good, because it touches fewer documents.
* Bad, because it lets Fase 1's own text keep asserting what F3 already found to be wrong.

### Reword directly, original kept as a dated, translated note

* Good, because it corrects the question where it is asked and preserves, in English, the record of what was originally asked and why it changed.
* Bad, because every revised question is now several blocks of text instead of one.

### Reword directly, no reference to original

* Good, because it is the shortest final document.
* Bad, because it erases the evidence of how the semantic misreadings shaped the project's own questions, without gaining anything ADR-0000's addendum pattern doesn't already justify keeping.

## More Information

* Related: [ADR-0000](0000-rebuild-from-scratch-instead-of-continuing-legacy.md) (F3, and its addendum), [ADR-0003](0003-redefine-indicators-14-to-16.md), [ADR-0005](0005-redefine-indicators-1-to-13.md), [ADR-0006](0006-final-questions-and-indicators.md).
* `docs/conceptual-framework.md` §4 (variable semantics) and §5 (what this dataset cannot measure).
* `docs/methodology.md` — what "Fase 1" and the other Hefesto phases cited throughout this document refer to.
* Legacy report, Fase 1, at tag `legacy-original`.