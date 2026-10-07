---
id: LOG-041
alias: correspondence criteria, A6 scope
date: 2026-10-06
status: recorded
formalization: none
---

# Extend check A6 to the OSMI group of LOG-040

## Decision

Check A6 compares the distributions of the columns of the OSMI group ([LOG-040](LOG-040-h1-column-groups.md)) with the OSMI 2014 data. This extends the scope that [LOG-019](LOG-019-a6-scope.md) fixed to five columns; LOG-019 stays as written. The scope follows the group by rule, and only while the partition is not frozen (LOG-040): once any result of A5, A6 or A10 exists, a change of the group changes A6 only by a dated post-result amendment.

## Linked findings

Decision g of the [documentation-currency register](../../audit/documentation-currency.md#81-starting-options), section 8.1, through LOG-040; finding DC-12, through LOG-019.

## Options considered

* (a) The eight columns of the OSMI group.
* (b) The five columns of LOG-019 and `care_options`.
* (c) The five columns of LOG-019.

## Option chosen

(a).

## Reasons

* The group and its test coincide by rule, not by a list made by hand.
* The premise that places `care_options` in the OSMI group becomes testable.
* `mental_health_interview`, central to Q7.2, gets a test.

## Reasons for each rejected option

* (b): it leaves `self_employed` and `mental_health_interview` in the group without a test.
* (c): it leaves the `care_options` premise untestable.

## Open, and where it goes

* Running A6: the correspondence phase, after the criteria commit ([LOG-039](LOG-039-reading-rule.md)).
