---
id: LOG-029
alias: documentation-currency N12
date: 2026-10-04
status: recorded
formalization: none
---

# Leave third-party template comments in .gitignore as they are

## Decision

[Writing conventions, rule 2](../../writing-conventions.md#2-voice) is not applied to the comments of the third-party template copied into `.gitignore` (DC-73).

## Linked findings

Item N12 of the [documentation-currency register](../../audit/documentation-currency.md#8-decide-items); finding DC-73.

## Options considered

* (N12a) Left as they are.
* (N12b) Rewritten.
* (N12c) Removed.

## Option chosen

(N12a).

## Reasons

* The comments are third-party text copied verbatim, not text written in the repository's voice.

## Reasons for each rejected option

* (N12b): it edits third-party text for voice.
* (N12c): it removes the template's explanations for no correction of a claim.

## Open, and where it goes

Nothing.
