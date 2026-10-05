---
id: LOG-023
alias: documentation-currency N6
date: 2026-10-04
status: recorded
formalization: none
---

# Read mental_health_interview as disclosure willingness, without anticipated stigma

## Decision

The conceptual framework's reading of `mental_health_interview` (`:38`) keeps "disclosure willingness" and drops "anticipated stigma". Its temporal part ("not yet confirmed — flagged for review …") is corrected: ADR-0000's addendum (`:30`) states that the pipeline operates on the corrected reading, and ADR-0003 and ADR-0004 adopt it (DC-58).

## Linked findings

Item N6 of the [documentation-currency register](../../audit/documentation-currency.md#8-decide-items); finding DC-58.

## Options considered

* (N6a) "Disclosure willingness" only.
* (N6b) "Disclosure willingness / anticipated stigma" kept.

## Option chosen

(N6a). PR group: PR-a2.

## Reasons

* The source's text for the column asks whether the respondent would bring up a mental health issue with a potential employer in an interview (`dataset-provenance.md:34`): a stated willingness to disclose.
* The framework itself records that the data holds no stigma items of any kind (`:51`).
* The name of indicator 16 uses "stated disclosure willingness" ([LOG-014](LOG-014-indicator-renames-and-residual-identifiers.md)).

## Reasons for each rejected option

* (N6b): it names a construct that the framework records the data does not measure.

## Open, and where it goes

* The wording at `conceptual-framework.md:38`: the plan of PR-a2.
