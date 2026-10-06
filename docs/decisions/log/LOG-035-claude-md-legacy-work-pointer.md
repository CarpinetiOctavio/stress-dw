---
id: LOG-035
alias: documentation-currency N19
date: 2026-10-05
status: recorded
formalization: none
---

# Point CLAUDE.md's line on legacy work to its records in general

## Decision

In `CLAUDE.md`, the line on work executed against the legacy repository ends "the checks in `docs/audit/legacy-audit.md`, and the readings recorded in the decision records (their findings and addenda) and in the documentation-currency register." It replaces the list of readings in ADR-0000 (addendum of 2026-09-29), ADR-0012 (S1–S3) and ADR-0013 (M1–M2). The statement that the work is read-only does not change.

## Linked findings

DC-97 of the [documentation-currency register](../../audit/documentation-currency.md#16-post-closure-audit-and-corrections); related: DC-88 and [LOG-025](LOG-025-claude-md-wording.md), under which the line points to the records of that work.

## Options considered

* (a) A general pointer to the decision records and the register.
* (b) The list extended with the 2026-10-04 addenda of ADR-0000, ADR-0003 and ADR-0005 and with section 5.6.1 of the register.
* (c) No change.

## Option chosen

(a).

## Reasons

* The list omits the read-only readings of the frozen report made in the documentation-currency sweep, the same kind of omission DC-88 corrected.
* A pointer to where readings are recorded stays true when a later phase reads the frozen report again, and it still points to the records of that work, as LOG-025 decided.
* The line names no section of the register, so the working instructions do not single out one reading of the frozen report.

## Reasons for each rejected option

* (b): the next reading of the frozen report would make the list incomplete again.
* (c): the working instructions would understate the work done against the legacy repository.

## Open, and where it goes

* The change to `CLAUDE.md`: PR-f2.

**Status (2026-10-06).**

* The change to `CLAUDE.md`: done in #63.
