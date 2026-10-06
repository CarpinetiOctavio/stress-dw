---
id: LOG-012
alias: documentation-currency a
date: 2026-10-03
status: recorded
formalization: none
---

# State where explicit recognition is defined that it rests on a premise

## Decision

The definition of [`explicit_recognition`](../../specification/definitions.md#explicit_recognition) gains one sentence: reading `growing_stress = 'Yes'` as explicit recognition is a premise, not a fact stated by the source, and the sentence links to the row of `Growing_Stress` in the [conceptual framework, section 4](../../conceptual-framework.md#4-variable-mapping-to-andersens-behavioral-model), where the premise lives (semantics assumed; mapped to perceived need). The condition and its name do not change.

## Linked findings

Decision a of the [documentation-currency register](../../audit/documentation-currency.md#8-decide-items)'s decision list; no finding of the register carries that letter.

## Options considered

* (a1) Keep the label "explicit recognition" and state its premise where the condition is defined, by one sentence and one pointer.
* (a2) Replace the label with a literal name, for example "growing-stress self-report".

## Option chosen

(a1). PR group: PR-a2.

## Reasons

The gap is the unstated premise at the place where the condition is defined, not the word. One sentence and one pointer close it: a reader of the definition learns that the label is an interpretation and finds its basis.

## Reasons for each rejected option

* (a2): it cascades into the definitions, the indicator names, the SQL comments and the tests; it leaves two names for one condition, because the verbatim question texts (ADR-0004, Confirmation) and the accepted decision records keep "recognition"; and it removes no interpretation, since any reading of the item as perceived need still needs the premise.

## Open, and where it goes

* The wording of the sentence: PR-a2.

**Status (2026-10-06).**

* The wording of the sentence: done in #55.
