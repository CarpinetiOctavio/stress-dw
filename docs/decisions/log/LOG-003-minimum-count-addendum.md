---
id: LOG-003
alias: documentation-currency N3
date: 2026-10-02
status: recorded
formalization: addendum of 2026-10-04 to ADR-0003
---

# Record by addendum that the minimum-count consideration is a flag, not a rule

## Decision

A dated addendum to [ADR-0003](../0003-redefine-indicators-14-to-16.md) records that the specification implements the minimum-count consideration as a flag: `low_n`, a parameter of the query layer, with no row suppressed and display left to the reporting layer ([`patterns.md`, Reporting rules](../../specification/patterns.md#reporting-rules)). It is not a rule; the rule for reading flagged cells is set in the correspondence criteria. The addendum corrects the statement that the rule "is set in `docs/specification.md`" and decides no rule.

## Linked findings

DC-42 of the [documentation-currency register](../../audit/documentation-currency.md#5-findings).

## Options considered

* (a) The addendum described above.
* (b) A suppression rule in the specification now.
* (c) No change; the finding reported only.

## Option chosen

(a).

## Reasons

ADR-0003 states, in its Consequences and in its addendum of 2026-09-23, that a minimum-count rule is set in the specification. The specification sets a flag and suppresses nothing. The addendum makes the record true without changing the model.

## Reasons for each rejected option

* (b): a change to the model, outside the scope of a documentation sweep; it contradicts the specification's rule that no row is suppressed; it would fix a reading rule apart from the other preregistered criteria ([ADR-0011](../0011-preregister-correspondence-criteria-before-exposing-indicator-values.md)); and it would force changes to SQL and tests and a new run of C8, C9 and C10 while the sweep is closing.
* (c): it leaves a false statement in a cited, accepted decision record.

## Open, and where it goes

* The rule for reading flagged cells: the correspondence criteria.
* Showing or hiding flagged cells: the reporting layer ([`patterns.md`, Reporting rules](../../specification/patterns.md#reporting-rules); [`phase4-closure.md`, section 6](../../audit/phase4-closure.md#6-explicitly-out-of-scope)).
* Once the addendum carries every section of the recording standard, this entry is reduced to a pointer ([formalization rule](README.md#formalization-rule)).

**Status (2026-10-06).**

* The rule for reading flagged cells: the correspondence phase, in the correspondence criteria.
* Showing or hiding flagged cells: the reporting layer.
* Reduction of this entry to a pointer: not done; [LOG-037](LOG-037-addendum-pointers-to-log-entries.md) rejected full formalization, so this entry keeps the reasoning and the decision record's addendum of 2026-10-06 points to it.
