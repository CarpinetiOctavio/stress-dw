---
id: LOG-039
alias: documentation-currency DC-91
date: 2026-10-06
status: recorded
formalization: none
---

# Adopt the reading rule for figures derived from the source file, with this entry as its home

## Decision

The reading rule below is adopted, and this entry is its home. The rule applies from the date of this entry until the order of [ADR-0011](../0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), rule 4, allows the indicator output to be exposed.

1. The repository is read normally.
2. Figures derived from the source file that already sit in the repository are read only where a check or a criterion needs them. A document that refers to them names the file and the category of the figure and does not restate it. Values readable in a capture follow [ADR-0012](../0012-cite-only-frozen-and-versioned-sources-as-evidence.md), with the scope clarified in [LOG-011](LOG-011-adr-0012-scope-of-capture-values.md).
3. No new value about the data is produced before the step of ADR-0011, rule 4, that allows it: checks A5, A6 and A10 (rule 4), A2 ([LOG-036](LOG-036-open-obligations-to-correspondence-phase.md)) and A7 (assigned to the correspondence phase by DC-13; LOG-036) run only after the criteria commit. No indicator value or output and no dump is produced before the indicator output may be exposed. The source file and the database are not inspected by any means, including tools that preview tables, other than through the pipeline, through the tests as [`phase4-closure.md`, section 2](../../audit/phase4-closure.md#2-reproducing-this) prescribes, and through each check once its turn under rule 4 has come.
4. A figure displayed in breach of this rule is added to the declaration of ADR-0011, rule 2, as rule 1 provides for values displayed by a failing assertion.

## Linked findings

DC-91 of the [documentation-currency register](../../audit/documentation-currency.md#57-execution-rules-in-living-documents).

## Options considered

* (a) A dated addendum to ADR-0011.
* (b) This log entry as home.
* (c) A new decision record.
* (d) The criteria document.

## Option chosen

(b).

## Reasons

* No decision record or living document holds the whole rule: ADR-0011, rules 1, 2 and 4, and ADR-0012 hold parts; the [register, section 2.5](../../audit/documentation-currency.md#25-reading-rule-for-this-sweep), states it for the sweep only.
* [`concept-homes.md`](../../concept-homes.md) admits a decision record as a home where the concept is the decision itself; the decision log holds decisions that no decision record carries, each entry keeping its reasoning until a record does ([decision log](README.md)), so the entry that decides the rule is its home on the same ground.
* Register section 2.5 placed A7, with A5, A6 and A10, after the criteria commit for the sweep; this entry carries that placement into the general rule. Check A7 computes a treatment rate by gender from the source file, so a value obtained before the criteria are fixed would be prior knowledge under ADR-0011, rules 1 and 2.
* Item 2 extends the wording of the register, section 2.5, to criteria, which refer to figures through the declaration of ADR-0011, rule 2.

## Reasons for each rejected option

* (a): the addendum convention ([decision-record index, Addenda](../README.md#addenda-to-accepted-decision-records)) applies when a finding that grounded the decision is corrected or qualified, and this rule corrects no finding of ADR-0011.
* (c): disproportionate to a rule that completes an existing decision.
* (d): the document does not exist until its commit, the rule must hold while it is drafted, and the document is not rewritten after its commit (ADR-0011, Consequences).

## Open, and where it goes

* How values are reported once the indicator output may be exposed: defined with the correspondence evidence document ([LOG-021](LOG-021-evidence-document-to-correspondence-phase.md); DC-89).

**Status (2026-10-07).**

* How values are reported once the indicator output may be exposed: set in [LOG-045](LOG-045-correspondence-evidence-document.md).
