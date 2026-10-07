---
id: LOG-042
alias: correspondence criteria, pilot
date: 2026-10-06
status: recorded
formalization: none
---

# Draft the criteria for Q4 first, then Q7.2, then the remaining questions

## Decision

The correspondence criteria are drafted first for Q4, as a pilot of the criterion template, then for Q7.2, then for the remaining questions.

## Linked findings

None.

## Options considered

* Q5 first.
* Q4 first.
* Q7.2 first.

## Option chosen

Q4 first, then Q7.2, then the remaining questions.

## Reasons

* Q4 crosses the two groups of [LOG-040](LOG-040-h1-column-groups.md) (`Gender` and `treatment` in the OSMI group; `Growing_Stress` in the other), as eight of the nine questions do; it exercises rules 3 and 4 of [ADR-0011](../0011-preregister-correspondence-criteria-before-exposing-indicator-values.md) on the smallest crossing structure (cuts `gender` × `growing_stress`, [`indicators.md`](../../specification/indicators.md)).
* Q4 involves neither premise of LOG-040.
* Q7.2 then tests the components Q4 leaves out: derived conditions and the validity caveat, the population filter, the headline cell, the largest specified cell structure, and the premises.

## Reasons for each rejected option

* Q5: it does not cross the groups, so it leaves the branches untested.
* Q7.2 first: it depends on the most open items at once, so a failure could not be attributed to the template rather than to an open dependency.

## Open, and where it goes

The order of the remaining seven questions is not fixed; it is set when they are drafted, in the criteria document.
