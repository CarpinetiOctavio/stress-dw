---
id: LOG-014
alias: documentation-currency c
date: 2026-10-04
status: recorded
formalization: none
---

# Rename indicators 9 to 13, 15 and 16 and keep the isolation identifiers as residual

## Decision

* Indicators are renamed: 9 "Explicit stress-recognition rate by time indoors"; 10 "Elevated mood-swings rate by time indoors"; 11 "Social-weakness rate by time indoors"; 12 "Care-options response rate"; 13 "Care-options response (count)"; 15 "Lifetime treatment-seeking rate by care-options response"; 16 "Lifetime no-treatment rate by stated disclosure willingness".
* The identifiers `dim_isolation`, `isolation_id` and `duration_band` are kept and declared residual: internal names that appear in no indicator name and in no output column of any indicator.
* Accepted decision records keep the former names; [`indicators.md`](../../specification/indicators.md) is the current definition ([LOG-008](LOG-008-adr-0006-addendum.md)).

## Linked findings

Decision c of the [documentation-currency register](../../audit/documentation-currency.md#8-decide-items)'s decision list; finding DC-75 (indicator names).

## Options considered

* (c1) The renames above; the identifiers kept as residual.
* (c2) The renames above, and the identifiers renamed as well.
* (c3) The current names kept.
* Variants of single names within (c1): names for 12 and 13 that carry their `growing_stress` cut; for 16, the "treatment-seeking" wording of indicators 14 and 15, or deciding 16 together with the objective of Q7.2 (decision e).

## Option chosen

(c1), with the names as listed. PR group: PR-c.

## Reasons

* "Isolation" is how the legacy report reads `Days_Indoors`, which has no source description ([dataset provenance, column documentation](../../dataset-provenance.md#column-documentation)); "by time indoors" names the variable.
* "Conversion" and "non-uptake" imply a process, and "full context" claims more than the population supports ([writing conventions, rule 5](../../writing-conventions.md#5-names-claim-only-what-the-data-supports)).
* "Resource-access" conflicts with the neutral wording of [LOG-013](LOG-013-care-options-neutral-wording.md); "care-options response" applies it.
* "Lifetime treatment-seeking" is the wording of indicator 14's name (`indicators.md:72`).
* Indicator names are not part of the rows that `run_indicator` returns (`indicators.py:125–147`), so no indicator output changes.
* The identifiers are kept because renaming them touches 24 files, among them the DDL, the loads, six indicator queries and the acceptance checks C1, C2, C4, C5, C7 and C10, while they appear in no name and in no output column. The starting option also gave a need to repeat E3 (ADR-0009) under ADR-0013's constraint as a reason; no versioned document states that need, and it is not a reason of this decision.

## Reasons for each rejected option

* (c2): the scope of the change above, with no effect on any name or output.
* (c3): it keeps process words and a resource claim against rule 5 and against LOG-013.
* Variants of single names: names carry at most the cut that distinguishes an indicator from its neighbour (15 from 14 by `care_options`, 16 from 15 by `mental_health_interview`; this project's own interpretation of the pattern of the names), and Q6 (`indicators.md:57`) gives the four cuts of 12 and 13 equal standing, so naming one would single it out. For 16, the measure's quantity of interest is the `No` level (`indicators.md:92`), which "no-treatment" names and "treatment-seeking" would not; a name states a measure and a cut, not an objective, so it does not wait for decision e.

## Open, and where it goes

* Where and how the identifiers are declared residual: the plan of PR-c.
* The other wording sites that DC-75 lists (`dimensions.md:71` "isolation"; conceptual framework `:84`, `:86` "conversion"): the plan of PR-c.
* Whether "no-treatment" in the name of 16 can be read as "no treatment received", while `treatment` records whether treatment was sought: the plan of PR-c.
* "Fullest context" and "persists" in the objective of Q7.2 (ADR-0004 `:114`): decision e.

**Status (2026-10-06).**

* Where and how the identifiers are declared residual: done in #56.
* The other wording sites of DC-75: done in #56.
* "No-treatment" in the name of indicator 16: done in #56, by a sentence in `indicators.md`.
* "Fullest context" and "persists" in the objective of Q7.2: done in #53.
