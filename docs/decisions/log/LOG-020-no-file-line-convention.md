---
id: LOG-020
alias: documentation-currency k
date: 2026-10-04
status: recorded
formalization: none
---

# Set no convention for file and line citations in living documents

## Decision

No convention for `file:line` citations in living documents is added.

## Linked findings

Decision k of the [documentation-currency register](../../audit/documentation-currency.md#8-decide-items)'s decision list; no finding (register, section 8).

## Options considered

* (k1) No convention.
* (k2) A convention for `file:line` citations.

## Option chosen

(k1).

## Reasons

* The sweep found no `file:line` citation in living documents (probe 3, `file:line` locators; register, sections 2.6 and 2.9). The one citation by line in a decision record, ADR-0000 `:35`, cites legacy script lines at the frozen tag, which does not move.
* A rule for a practice that does not occur widens the scope without correcting anything.

## Reasons for each rejected option

* (k2): it regulates a practice absent from the living documents.

## Open, and where it goes

Nothing.
