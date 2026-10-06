---
id: LOG-007
alias: documentation-currency home-map timing
date: 2026-10-02
status: recorded
formalization: none
---

# Confirm the home map in stage 2 and write overlapping pointers in stage 3

## Decision

The concept-to-home map of the documentation-currency register is confirmed in stage 2, before any correction pull request. A pointer (REF or CONDENSE) that falls on a place a stage-3 correction also changes is written in that correction's pull request; stage 5 keeps only the pointers with no such overlap. A pointer written in stage 3 carries its claim-preservation table in the same pull request, drafted with that stage's plans.

## Linked findings

The [register](../../audit/documentation-currency.md#5-findings)'s concept-to-home map (section 7) and its list of stage-3 overlaps.

## Options considered

* (a) Every REF and CONDENSE in stage 5, as first planned.
* (b) The map confirmed in stage 2; pointers that overlap a stage-3 correction written in that correction's pull request; stage 5 keeping the rest.

## Option chosen

(b).

## Reasons

Each place is edited once, and no correction writes text that a later pull request replaces.

## Reasons for each rejected option

* (a): two pull requests would edit the same sentence, and the first would write wording the second removes.

## Open, and where it goes

* The claim-preservation tables of stage-3 pointers: with the stage-3 plans.
* Confirmation of the map itself: done in stage 2, on 2026-10-03, with its adjustments ([LOG-010](LOG-010-concept-home-map.md)).

**Status (2026-10-06).**

* The claim-preservation tables of stage-3 pointers are in the descriptions of #50, #51, #55 and #57.
* Confirmation of the map: done on 2026-10-03 ([LOG-010](LOG-010-concept-home-map.md)).
