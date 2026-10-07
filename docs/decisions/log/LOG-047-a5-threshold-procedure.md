---
id: LOG-047
alias: correspondence criteria, A5 threshold
date: 2026-10-07
status: recorded
formalization: none
---

# Take the thresholds of check A5 from a verified published source, or else fix them as a declared convention

## Decision

The thresholds for a near-zero association across the two column groups and for structure within a group in check A5 (H1's test, [ADR-0001](../0001-position-as-portfolio-project.md#hypotheses-not-findings)) are taken first from a published, consultable source that tabulates conventions for Cramér's V, verified against its text before it is cited, with the edition and page consulted recorded. Failing such a source, they are a declared convention of this project, marked as interpretation ([writing conventions, rule 7](../../writing-conventions.md#7-evidence-discipline)), with their reasoning recorded. Either way they are fixed before A5 runs, in the rule that maps the outcomes of A5, A6 and A10 to a reading branch (the criteria document).

## Linked findings

None.

## Options considered

* (a) A verified published source; failing it, a declared convention.
* (b) A source cited without verification against its text.
* (c) A threshold set after A5 runs.

## Option chosen

(a).

## Reasons

* A published work is cited by its bibliographic reference ([ADR-0012](../0012-cite-only-frozen-and-versioned-sources-as-evidence.md#addendum-2026-09-30), addendum of 2026-09-30); what is cited from it is checked against its text, and the edition and page make the check repeatable.
* A declared convention states its basis as this project's own; an unverified source would misstate it.

## Reasons for each rejected option

* (b): the basis of the threshold would rest on recall.
* (c): a threshold chosen after the result is known depends on the data ([ADR-0011](../0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), Context).

## Open, and where it goes

* The thresholds and their source or reasoning: the criteria document, before A5 runs.
