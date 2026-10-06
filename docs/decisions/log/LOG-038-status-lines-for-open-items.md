---
id: LOG-038
alias: documentation-currency closure, state of open items
date: 2026-10-05
status: recorded
formalization: none
---

# Record the state of open items by dated status lines

## Decision

Each log entry whose "Open, and where it goes" section lists items receives, at the end of that section, one dated status line per item: done, with the pull request that did it; the correspondence phase; or a later phase named by a recorded decision (the planned README rewrite, the reporting layer). The items themselves stay as written.

## Linked findings

DC-102 of the [documentation-currency register](../../audit/documentation-currency.md#16-post-closure-audit-and-corrections).

## Options considered

* (a) Dated status lines, the items kept as written.
* (b) The sections rewritten in the present tense.

## Option chosen

(a).

## Reasons

* Items whose work is done are still written as future work ("the plan of PR-b" and similar).
* A status line states what happened and when, and keeps what each entry expected when it was recorded.

## Reasons for each rejected option

* (b): it erases what each entry expected when it was recorded.

## Open, and where it goes

* The status lines, each with its pull request found in the repository history: PR-f3.

**Status (2026-10-06).**

* The status lines: done in #64, except those of LOG-037 and this entry, added with the closure of the sweep ([register, section 16](../../audit/documentation-currency.md#16-post-closure-audit-and-corrections)).
