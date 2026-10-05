---
id: LOG-019
alias: documentation-currency i
date: 2026-10-04
status: recorded
formalization: none
---

# Align check A6 with the test of hypothesis H1

## Decision

Check A6 compares the distributions of `Timestamp`, `Gender`, `Country`, `family_history` and `treatment` with the OSMI 2014 data, as the test of H1 states (ADR-0001 `:31`). The association part of that test stays in A5 (`legacy-audit.md:13`). The scope is fixed before the check is run; running A6 remains in the correspondence phase (ADR-0011, rule 4).

## Linked findings

Decision i of the [documentation-currency register](../../audit/documentation-currency.md#8-decide-items)'s decision list; finding DC-12.

## Options considered

* (i1) A6 aligned with the five variables of H1's test.
* (i2) A6 kept to `Timestamp`, with the reason recorded.

## Option chosen

(i1). PR group: none carried by DC-12; the plan of stage 3 assigns it.

## Reasons

* A6 serves H1, and H1's test names five variables; A6 compares one (`legacy-audit.md:14`).
* A scope fixed before any result exists cannot be chosen in the light of that result.

## Reasons for each rejected option

* (i2): it checks less than the test the check serves.

## Open, and where it goes

* The wording of A6's row in `legacy-audit.md`: the plan of stage 3.
* Running A6: the correspondence phase.
