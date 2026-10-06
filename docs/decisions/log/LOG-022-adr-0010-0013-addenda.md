---
id: LOG-022
alias: documentation-currency N5
date: 2026-10-04
status: recorded
formalization: addenda of 2026-10-04 to ADR-0010 and ADR-0013
---

# Point ADR-0010 and ADR-0013 to ADR-0009's restated findings by addenda

## Decision

Dated addenda to ADR-0010 (`:19`, E1 "judged not to apply to an insert-only load") and to ADR-0013 (`:56`, `:100`, enforcement "which ADR-0009 evidences (E1)") point to ADR-0009's addendum: enforcement on insert rests on the captured documentation, enforcement on delete on E3, and check C5 tests it (`test_acceptance.py:277`). The parts of ADR-0009 that rest on the restated findings, listed in its addendum (`:53`), keep their text; the choice of engine is not weighed again in this phase.

## Linked findings

Item N5 of the [documentation-currency register](../../audit/documentation-currency.md#8-decide-items); finding DC-45.

## Options considered

* (N5a) Addenda to ADR-0010 and ADR-0013; ADR-0009's dependent parts not weighed again.
* (N5b) The same addenda, and ADR-0009's dependent parts weighed again.

## Option chosen

(N5a). PR group: PR-b.

## Reasons

* ADR-0009's addendum already lists the parts that rest on E1 and E2 (`:53`).
* Weighing the engine choice again is a model question, outside the sweep (register, section 2.3, sweep rule 8).

## Reasons for each rejected option

* (N5b): it reopens a model decision from a documentation sweep.

## Open, and where it goes

* The wording of the two addenda: the plan of PR-b.

**Status (2026-10-06).**

* The wording of the two addenda: done in #54.
