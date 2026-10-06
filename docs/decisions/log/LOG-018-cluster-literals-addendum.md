---
id: LOG-018
alias: documentation-currency h
date: 2026-10-04
status: recorded
formalization: addendum of 2026-10-04 to ADR-0007
---

# Record by addendum that the cluster's literals are repeated by design

## Decision

A dated addendum to ADR-0007 records that its statement "the cluster's threshold is written in one definition" (`:65`) does not describe the code: the three literals of `symptom_cluster` are repeated in the queries of indicators 14, 15 and 16, and the acceptance tests repeat them as an independent check (register, section 5.4.1). No refactor is made. The starting option's "correct the text" is not applied, because an accepted record is not rewritten.

## Linked findings

Decision h of the [documentation-currency register](../../audit/documentation-currency.md#8-decide-items)'s decision list; finding DC-50.

## Options considered

* (h1) An addendum; no refactor.
* (h2) A refactor, so that the literals are written once.
* (h3) ADR-0007's text corrected in place.

## Option chosen

(h1). PR group: PR-b; the addendum is shared with [LOG-017](LOG-017-response-grain.md).

## Reasons

* The repetition in the tests is deliberate: `test_acceptance.py:384` states that its conditions are written "over staging_response's own columns: independent of the indicator SQL".
* The finding is a statement of the record that the code does not match; an addendum corrects the record without changing the code.

## Reasons for each rejected option

* (h2): it changes indicator queries to make a sentence of a record true, while the tests' repetition stays by design.
* (h3): accepted decision records are not rewritten.

## Open, and where it goes

* The wording of the addendum: the plan of PR-b.

**Status (2026-10-06).**

* The wording of the addendum: done in #54.
