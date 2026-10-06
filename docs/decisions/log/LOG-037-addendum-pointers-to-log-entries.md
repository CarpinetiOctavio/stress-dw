---
id: LOG-037
alias: documentation-currency N21
date: 2026-10-05
status: recorded
formalization: none
---

# Point the 2026-10-04 addenda to their log entries by new dated addenda

## Decision

Each decision record whose addendum of 2026-10-04 carries a decision of this log receives a new dated addendum of one sentence that names the entries keeping the reasoning: ADR-0000 (LOG-006), ADR-0003 (LOG-003, LOG-013), ADR-0004 (LOG-013, LOG-015, LOG-016), ADR-0006 (LOG-008), ADR-0007 (LOG-017, LOG-018), ADR-0010 (LOG-022), ADR-0012 (LOG-011) and ADR-0013 (LOG-022). The addenda of 2026-10-04 stay as written. The `formalization` field of each of those entries names the addendum of 2026-10-04 that carries it, and the entries stay `recorded`.

## Linked findings

DC-101 and DC-100 of the [documentation-currency register](../../audit/documentation-currency.md#16-post-closure-audit-and-corrections).

## Options considered

* (a) A link appended to each addendum of 2026-10-04.
* (b) The [formalization rule](README.md#formalization-rule) changed so that pointers run only from an entry to its target.
* (c) A new dated addendum to each record.
* (d) Full formalization: each addendum extended to carry every section of the recording standard, and each entry reduced to a pointer.

## Option chosen

(c).

## Reasons

* The formalization rule requires the target of an entry that keeps its reasoning to point to the entry; only ADR-0002's addendum does (LOG-033).
* An accepted decision record is not rewritten, and only operational descriptions, such as a path, a command or a link, are corrected in place ([decision-record index, Addenda](../README.md#addenda-to-accepted-decision-records)). A new addendum adds the pointer without changing accepted text.

## Reasons for each rejected option

* (a): it adds text to an accepted addendum; the convention allows a link to be corrected in place, not added.
* (b): it reverses the rule of [LOG-004](LOG-004-decision-log-and-lessons.md), and a reader of a decision record would have no way to the reasoning of its addendum.
* (d): it repeats in accepted records the reasoning the log already holds.

## Open, and where it goes

* The eight addenda and the `formalization` fields: PR-f3.
