---
id: LOG-049
alias: correspondence criteria, prior knowledge by repository access
date: 2026-10-08
status: recorded
formalization: none
---

# Count the repository as known when the criteria are fixed, with this entry as the home of the reading rule

## Decision

The reading rule below replaces the rule of [LOG-039](LOG-039-reading-rule.md), and this entry is its home. Items 1 and 3 are those of LOG-039, unchanged; items 2 and 4 are rewritten. The rule applies from the date of this entry until the order of [ADR-0011](../0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), rule 4, allows the indicator output to be exposed.

1. The repository is read normally.
2. Everything in the repository at the parent of the criteria commit counts as known when the criteria are fixed. The declaration of ADR-0011, rule 2, states it as access to the repository at that commit, and lists beside it what is known from outside the repository. Figures derived from the source file that sit in the repository are not withheld while the criteria are drafted or checked. A document that refers to them names the file and the category of the figure and does not restate it. Values readable in a capture follow [ADR-0012](../0012-cite-only-frozen-and-versioned-sources-as-evidence.md), with the scope clarified in [LOG-011](LOG-011-adr-0012-scope-of-capture-values.md).
3. No new value about the data is produced before the step of ADR-0011, rule 4, that allows it: checks A5, A6 and A10 (rule 4), A2 ([LOG-036](LOG-036-open-obligations-to-correspondence-phase.md)) and A7 (assigned to the correspondence phase by DC-13; LOG-036) run only after the criteria commit. No indicator value or output and no dump is produced before the indicator output may be exposed. The source file and the database are not inspected by any means, including tools that preview tables, other than through the pipeline, through the tests as [`phase4-closure.md`, section 2](../../audit/phase4-closure.md#2-reproducing-this) prescribes, and through each check once its turn under rule 4 has come.
4. A value displayed in breach of item 3 is added to the declaration of ADR-0011, rule 2, as rule 1 provides for values displayed by a failing assertion.

## Linked findings

None.

## Options considered

* (a) A new entry that replaces LOG-039 and holds the whole rule, with items 2 and 4 rewritten.
* (b) A new entry that amends item 2 only, with LOG-039 kept as the home of the rest.
* (c) A dated addendum to ADR-0011.
* (d) LOG-039 kept as it is.

## Option chosen

(a).

## Reasons

* A statement that a figure already in the repository was not read cannot be checked from the repository, so it gives an outside reader nothing to judge. What can be checked is the repository at the parent of the criteria commit: the option chosen in [ADR-0011, Decision Outcome](../0011-preregister-correspondence-criteria-before-exposing-indicator-values.md#decision-outcome) makes the order of exposure "checkable from the repository history" and turns the prior knowledge "into a declared, inspectable list".
* ADR-0011 did not adopt blind analysis, in part because "masking has little to hide here" ([ADR-0011, Blind analysis](../0011-preregister-correspondence-criteria-before-exposing-indicator-values.md#blind-analysis)).
* The criteria are protected by what does not exist yet, not by what is withheld: indicator values and the results of A5, A6 and A10 do not exist before the commits ADR-0011 orders (item 3; ADR-0011, rules 1 and 4).
* Item 4 of LOG-039 covered figures displayed in breach of its item 2. Under item 2 as rewritten, a figure in the repository is declared by access, so item 4 is limited to values that item 3 does not allow to exist yet.

## Reasons for each rejected option

* (b): the rule would have two homes ([writing conventions, rule 4](../../writing-conventions.md#4-introduce-before-use-one-home-per-concept)).
* (c): the addendum convention ([decision-record index, Addenda](../README.md#addenda-to-accepted-decision-records)) applies when a finding that grounded the decision is corrected or qualified, and this change corrects no finding of ADR-0011.
* (d): item 2 of LOG-039 would keep a restriction whose observance cannot be checked from the repository.

## Open, and where it goes

* The declaration by access, with the items known from outside the repository: the criteria document, section 1.
* How values are reported once the indicator output may be exposed: set in [LOG-045](LOG-045-correspondence-evidence-document.md), as recorded in LOG-039.
