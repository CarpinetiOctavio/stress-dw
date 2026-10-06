---
id: LOG-036
alias: documentation-currency N20
date: 2026-10-05
status: recorded
formalization: none
---

# Assign DC-19 and DC-21 to the correspondence phase, with A2 after the criteria commit

## Decision

The two open obligations of the documentation-currency register are assigned to the correspondence phase: DC-19, the checks that quantify findings F1 to F4 for ADR-0000's Confirmation (A2 and A3; A7 is already assigned to that phase by DC-13), and DC-21, the query-time cost that ADR-0007 leaves to be checked once the pipeline exists. Check A2 is run only after the criteria commit of [ADR-0011](../0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), as A5, A6 and A10 are under its rule 4. No order is set for A3 or for DC-21.

## Linked findings

DC-99, DC-19 and DC-21 of the [documentation-currency register](../../audit/documentation-currency.md#16-post-closure-audit-and-corrections).

## Options considered

* (a) Both assigned to the correspondence phase, with A2 after the criteria commit.
* (b) Both recorded as open obligations outside any phase, which do not block the correspondence phase.
* (c) No change.

## Option chosen

(a).

## Reasons

* The closure statement of section 15 of the register admits as open only items of the correspondence phase and items that are report only on accepted decision records; DC-19 and DC-21 are neither.
* The fan-out that A2 measures can carry into a legacy indicator compared with a newly computed one ([conceptual framework, section 7](../../conceptual-framework.md#7-threats-to-validity), F1).
* The correspondence phase tests the system as built (ADR-0013, Decision Drivers), which is what a measurement of query-time cost observes.
* A2 counts records of the source file and of the legacy fact table; a count obtained before the criteria are fixed is prior knowledge under ADR-0011, rules 1 and 2. Rule 4 orders A5, A6 and A10 after the criteria commit and names no order for A2, so the order is set here.

## Reasons for each rejected option

* (b): it leaves open items with no phase, against the closure criterion of section 15.
* (c): the obligations stay open with no destination.

## Open, and where it goes

* Running A2 and A3, and measuring the query-time cost: the correspondence phase, A2 after the criteria commit.

**Status (2026-10-06).**

* Running A2 and A3, and measuring the query-time cost: the correspondence phase, A2 after the criteria commit.
