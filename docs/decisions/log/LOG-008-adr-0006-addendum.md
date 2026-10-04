---
id: LOG-008
alias: documentation-currency j
date: 2026-10-02
status: recorded
formalization: addendum to ADR-0006 (planned)
---

# Point ADR-0006 to the indicator specification by a dated addendum

## Decision

A dated addendum to [ADR-0006](../0006-final-questions-and-indicators.md) states that [`indicators.md`](../../specification/indicators.md) is the current definition of every indicator, and records how rows 5 and 6 of its indicator table differ from it: ADR-0006 gives the population as the condition and the cut as occupation × country × region; the specification gives the population as all rows and two grouping sets, {occupation, country} and {occupation, region}. The table itself is not changed.

## Linked findings

DC-40 of the documentation-currency register.

## Options considered

* (a) Correct rows 5 and 6 of the table in place, the plan the sweep started from.
* (b) A dated addendum pointing to `indicators.md` and recording the difference.
* (c) No change; the finding reported only.

## Option chosen

(b).

## Reasons

* ADR-0006 describes itself as a snapshot that needs a manual update whenever the records it consolidates change (its Consequences).
* An addendum keeps the snapshot as history and points one way, to the contract.

## Reasons for each rejected option

* (a): a table of indicator definitions is not clearly an operational description, the only part of an accepted decision record that may be corrected in place; and an in-place change would rewrite an accepted record.
* (c): the record would keep contradicting the specification it consolidates.

## Open, and where it goes

* The text of the addendum and its date: the correction pull request that carries it (PR-b).
* Once the addendum carries every section of the recording standard, this entry is reduced to a pointer ([formalization rule](README.md#formalization-rule)).
