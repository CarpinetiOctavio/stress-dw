---
status: "proposed"
date: 2026-09-23
decision-makers: Octavio Carpineti
---

# Redefine indicators 14–16 around verifiable constructs

## Context and Problem Statement

Fase 1 defined three related business questions (Q7, Q7.1, Q7.2 in the legacy report) around a single idea: identify people whose stress is real but unacknowledged or untreated, and measure the gap between having a problem, having resources, and actually seeking help. `Growing_Stress` was chosen to represent the "problem" side of that gap, alongside a derived flag (`Indicador_Inferido_Estrés`) meant to catch people who normalize their symptoms and wouldn't self-report as stressed. The `Growing_Stress = 'Yes'` branch of that flag was deliberately written to exclude `Maybe`: the intent was to keep the explicit-recognition signal strict, so ambiguous cases wouldn't be folded by assumption into what counts as "having stress" — precisely to avoid overriding the normalization the project set out to measure. `Maybe` was never assigned to either side of the boolean; it simply doesn't appear in the formula.

F3 (ADR-0000, established) found that, independent of this, indicators 14–16 as specified do not measure what their names claim: no comparison group for indicator 14; `Not sure` folded into "available" and the explicit-recognition group blurred into the base population for indicator 15; no time dimension anywhere in indicator 16's formula, which makes "postponement" unmeasurable by construction. F3 also found that the legacy report read `treatment` as "currently in treatment" and `mental_health_interview` as "participated in a mental-health interview," against the Kaggle-documented descriptions of both fields.

At the time the legacy model was designed, `treatment` was understood as whether the person was currently in treatment, and `mental_health_interview` was understood as the person having had an interview that determined they were mentally unwell — a diagnostic or assessment event — rather than the disclosure-willingness item the Kaggle description ("Would you bring up a mental health issue with a potential employer in an interview?") actually describes. `conceptual-framework.md` §4 already corrects both readings; this ADR is where the correction gets applied to indicators 14–16 specifically.

How should indicators 14, 15 and 16 be redefined so each measures a construct its variables can actually support, while treating ambiguous self-report categories (`Growing_Stress = 'Maybe'`, `mental_health_interview = 'Maybe'`) consistently and without folding them into either side of a binary?

## Findings

| ID | Finding | Evidence | Status |
|----|---------|----------|--------|
| F3 | Indicators 14–16 do not measure what their names claim; `treatment` and `mental_health_interview` were read against the wrong Kaggle-documented semantics. | ADR-0000 (Findings, and its 2026-09-23 addendum on `mental_health_interview`); `conceptual-framework.md` §4, §6 | Established |

## Decision Drivers

* Minimizing assumption folded into ambiguous self-report categories was already the stated intent behind excluding `Maybe` from the original formula — that intent is worth keeping, but made explicit and applied consistently, not just to one branch of one formula.
* Andersen's behavioral model (`conceptual-framework.md` §3) treats perceived need as a graded construct, not a binary one — a three-level self-report (`Yes`/`Maybe`/`No`) is more consistent with that model than forcing a fold into two levels. No source in the project's bibliography validates a specific three-level self-report scale; this is a structural argument from the model already in use, not a claim backed by a dedicated citation.
* Indicator 14's actual question — does explicit recognition predict treatment-seeking? — requires holding the symptom profile constant across comparison groups. Comparing a symptom-defined population against an unrestricted `Growing_Stress = 'Yes'` population would confound recognition with symptom severity.
* With additive, person-grain facts, indicators 15 and 16 are not independent stored ratios — they are the same base population and the same lifetime-treatment-seeking rate, cut by an increasing number of context variables. Designing 15 without accounting for 16's extra cut produces two formulas that can silently disagree about what "the population" is.
* `treatment` reads as lifetime, not current; `mental_health_interview` reads as an attitudinal disclosure-willingness item, not an exposure event (`conceptual-framework.md` §4).
* A single cross-sectional observation per person cannot distinguish an open-ended delay in seeking treatment from a settled decision not to; Andrade et al. 2014 finds that handling the problem independently — not delay — is the most common attitudinal reason for non-uptake among people who do perceive a need. Naming indicator 16 "postponement," qualified or not, asserts the former over the latter without support.

## Considered Options

* For indicator 14 — Design A: population is the three-symptom convergence cluster only, partitioned by `Growing_Stress` (`Yes`/`Maybe`/`No`); each partition's lifetime-treatment rate reported separately.
* For indicator 14 — Design B: "implicit" group is the convergence cluster with `Growing_Stress != 'Yes'`; "explicit" group is `Growing_Stress = 'Yes'` with no symptom restriction; the two rates compared directly.
* For `Growing_Stress = 'Maybe'` generally — fold into `No` (not recognized).
* For `Growing_Stress = 'Maybe'` generally — fold into `Yes` (recognized, low confidence).
* For `Growing_Stress = 'Maybe'` generally — keep as its own reporting category, never folded.
* For indicator 15 — keep the population as a single collapsed flag (`Growing_Stress = 'Yes' OR` convergence cluster), matching Q7.1's literal wording as a union.
* For indicator 15 — keep the union, but tag each row by which condition triggered inclusion (explicit-only / convergent-only / both), and report `care_options` (`Yes`/`Not sure`) crossed with that tag instead of collapsing to one rate.
* For indicator 16 — fuse `mental_health_interview` `Yes` and `Maybe` into one "willing/uncertain" level.
* For indicator 16 — keep `mental_health_interview` at its three native levels (`Yes`/`Maybe`/`No`), added as a third cross-cut on top of indicator 15's population and `care_options` split.
* For indicator 16's name — keep "postponement" (qualified as indefinite), accepting the interpretive claim it carries.
* For indicator 16's name — drop "postponement" entirely; name and report the non-uptake rate itself, with an explicit validity note that the data cannot distinguish ongoing delay from settled non-uptake.

## Decision Outcome

**Indicator 14** — Design A, with `Growing_Stress = 'Maybe'` kept as its own category. Population: `Mood_Swings IN ('Medium','High') AND Coping_Struggles = 'Yes' AND Days_Indoors IN ('15-30 days','31-60 days','More than 2 months')`. Partitioned by `Growing_Stress` into three groups; lifetime-treatment rate (`COUNT(treatment='Yes')/COUNT(*)`) reported for each. New name: *lifetime treatment-seeking rate by explicit-recognition level, within the convergent-symptom population*.

**Indicator 15** — the tagged-union design. Population: `Growing_Stress = 'Yes' OR` (the same three-symptom cluster), with each row tagged `explicit_only` / `convergent_only` / `both`, crossed with `care_options IN ('Yes','Not sure')`. Lifetime-treatment rate reported per cell (up to 3×2 = 6 cells). New name: *care-options-to-treatment conversion rate, by inclusion path*.

**Indicator 16** — three native levels, no fusion. Same population and inclusion-path tag as indicator 15, crossed with `care_options` × `mental_health_interview IN ('Yes','Maybe','No')` (up to 3×2×3 = 18 cells). For each cell, both the lifetime-treatment rate and its complement (non-uptake) are reported, since the complement is the quantity of interest here. New name: *treatment non-uptake rate under full context*. The cell `inclusion_path = both, care_options = 'Yes', mental_health_interview = 'Yes'` — explicit recognition and symptom convergence both present, definite resource availability, definite disclosure willingness — is reported as the headline figure: the closest the dataset can come to describing the fullest context it can express, alongside whether treatment was still not sought. This is not postponement in a temporal sense — no time-to-treatment variable exists in the source data (F3), and none is inferable — nor in a weaker, undated sense either: a single cross-sectional observation per person cannot tell someone in the middle of an open-ended delay apart from someone who has settled on not seeking care, and the more common pattern in the cited literature is the latter (Andrade et al. 2014). The name and the reported number describe the gap itself, without asserting which of those two states it reflects.

Chosen because this is the only combination across the three indicators that never forces an ambiguous self-report value into an interpretation the data doesn't support (`Maybe` on either variable), that keeps indicator 14's comparison groups matched on symptom profile so the result isolates recognition rather than severity, that makes 15 and 16 the same base computation with one added cut instead of two formulas that can silently disagree on population, and that does not name indicator 16 after a process (postponement) the data cannot establish is even occurring.

### Consequences

* Good, because no self-reported ambiguity is silently resolved by the pipeline's own logic instead of being reported as what it is.
* Good, because 15 and 16 share one validated base rate — a discrepancy between them, if the implementation introduces one, is a bug to catch, not two independent things to separately get right.
* Good, because indicator 16's name and validity note match the project's existing standard for declared-heuristic constructs (`conceptual-framework.md` §7, on `Indicador_Inferido_Estrés`'s convergence threshold) instead of setting a looser one just for this indicator.
* Bad, because the output is a set of rates per cell, not a single scalar per indicator — reporting and visualization need to handle that.
* Bad, because up to 18 cells for indicator 16 raises a small-`n` problem for the rarer combinations; the specification needs a minimum-count rule before a cell's rate is reported (undecided here, flagged for `docs/specification.md`).
* Constraint: `Indicador_Inferido_Estrés` as a single OR'd boolean is no longer used by any of 14–16 in this design — each of its two components (`Growing_Stress = 'Yes'`, and the three-symptom cluster) is used separately as a tag, not collapsed. Whether that column still needs to exist in `Dim_Sintomas` at all, or gets replaced by the cluster condition alone plus the raw `Growing_Stress` value already stored, is a schema decision for `docs/specification.md`, not this ADR.

### Confirmation

`docs/specification.md` implements these as query patterns over person-grain additive facts (counts, not stored ratios), not as three pre-aggregated percentage columns. A post-build audit sums each design's cell counts back to its declared population size (the three-symptom cluster for 14; the tagged union for 15 and 16) and checks it against a direct `COUNT(*)` on the same filter, run independently.

## Pros and Cons of the Options

### Indicator 14 — Design A

* Good, because it isolates recognition as the only variable that differs between groups.
* Good, because `Maybe` gets a real row instead of a forced decision.
* Bad, because it doesn't produce a single "recognition gap" percentage — three rates, not one contrast.

### Indicator 14 — Design B

* Good, because it produces one direct explicit-vs-implicit contrast, simpler to report.
* Bad, because the explicit group isn't restricted to the same symptom profile, so any gap conflates recognition with severity.

### `Growing_Stress = 'Maybe'` — fold into `No` or `Yes`

* Good, because it keeps every indicator binary and simpler to report.
* Bad, because it substitutes an assumption about what `Maybe` means for the data itself — the exact bias the original formula tried to avoid by excluding it from the explicit branch in the first place.

### `Growing_Stress = 'Maybe'` — own category

* Good, because it makes no assumption about a value the respondent themselves left ambiguous.
* Bad, because every indicator that uses `Growing_Stress` now reports three groups instead of two.

### Indicator 15 — collapsed union

* Good, because it matches Q7.1's literal wording most directly and produces one rate per `care_options` level.
* Bad, because it reproduces F3's blurring problem: within the `TRUE` group, explicit self-reporters and symptom-only cases are indistinguishable.

### Indicator 15 — tagged union

* Good, because it resolves F3's blurring problem directly instead of only the `Not sure` half of it.
* Bad, because it triples the number of reported cells relative to the collapsed version.

### Indicator 16 — fused `mental_health_interview`

* Good, because it keeps the output to 2×2 instead of 3×2 cells.
* Bad, because it applies the same unexamined fold to a second attitudinal variable that indicator 14 already argued against for `Growing_Stress`.

### Indicator 16 — three native levels

* Good, because it's consistent with the same principle applied to `Growing_Stress`.
* Bad, because 18 cells raises the small-`n` problem noted in Consequences.

### Indicator 16 name — keep "postponement" (qualified as indefinite)

* Good, because it preserves the original motivating language and reads as more immediately meaningful.
* Bad, because "indefinite" removes the claim of a known timeframe but not the claim of an ongoing process — the data cannot establish that the observed non-uptake is a process in progress rather than a settled outcome, and the project's own cited literature suggests the settled case is more common.

### Indicator 16 name — non-uptake rate, with a validity note

* Good, because the name asserts nothing beyond what a single cross-sectional observation can support.
* Bad, because it is less immediately evocative of the original motivating question than "postponement" was.

## More Information

* Related: [ADR-0000](0000-rebuild-from-scratch-instead-of-continuing-legacy.md) (F3, and its 2026-09-23 addendum), [ADR-0001](0001-position-as-portfolio-project.md).
* `docs/conceptual-framework.md` §3 (Andrade et al. 2014, on independent problem-handling as the most common attitudinal barrier), §4 (variable mapping, `treatment` and `mental_health_interview` reinterpretation, with its own 2026-09-23 addendum), and §6 (original direction for indicators 14–16). Once this ADR is accepted, §6 should be updated with a pointer to it, so the two documents don't drift apart.
* Legacy report, Fase 1 (Q7, 7.1, 7.2) and Fase 2 (original indicator formulas), at tag `legacy-original`.