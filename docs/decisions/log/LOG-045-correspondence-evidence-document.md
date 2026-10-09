---
id: LOG-045
alias: documentation-currency l
date: 2026-10-07
status: recorded
formalization: none
---

# Name, place and structure the correspondence evidence document as the final report of ADR-0011

## Decision

The correspondence evidence document is `docs/audit/correspondence-evidence.md`, and it is the final report of [ADR-0011](../0011-preregister-correspondence-criteria-before-exposing-indicator-values.md) (Consequences and Confirmation). Its contents are written after the criteria commit ([LOG-044](LOG-044-stage-placement.md)). Its structure:

1. Reproduction, stated once: the criteria commit's hash; the repository commit of the runs; the SHA-256 of the source file, by link to its home ([`dataset-provenance.md`, Identity of the file](../../dataset-provenance.md#identity-of-the-file)); the canonical serialization (ADR-0011, rule 5); and the result of comparing the two runs.
2. Branch applied: H1 holds, H1 does not hold, or both without resolving between them. The results of A5, A6 and A10 are cited by pointer to [`legacy-audit.md`](../../audit/legacy-audit.md#checks) (concept-homes row 1), not restated, and the rule that maps those results to a branch is cited by link to the criteria document, `docs/audit/correspondence-criteria.md`.
3. Post-commit exposures: any value displayed outside the order of ADR-0011, rule 4 ([LOG-049](LOG-049-reading-rule-by-repository-access.md), item 4).
4. One section per question, Q1 to Q7.2: the criteria applied, by link, with any dated post-exposure amendment; each indicator by number and hash; the verdict on each criterion and on the question, with the branch under which each verdict is read (not applicable where the question crosses no groups, as Q5; both, without resolving between them, for results that involve `Occupation`, [LOG-040](LOG-040-h1-column-groups.md)); the documentary verdict, for Q2 and Q7.1; and design findings, if any ([ADR-0013, Consequences](../0013-keep-star-schema-add-flat-consumption-view.md#consequences)).

Values: the full output of every indicator is published in its canonical serialization, with its hash; each verdict cites the cells it uses; cells flagged by `low_n` are shown, marked, and never omitted from the evidence document. Their display in the reporting layer stays with [LOG-003](LOG-003-minimum-count-addendum.md).

## Linked findings

DC-89 of the [documentation-currency register](../../audit/documentation-currency.md#57-execution-rules-in-living-documents); decision l of its [section 8.1](../../audit/documentation-currency.md#81-starting-options).

## Options considered

* (a) One document that is also the final report of ADR-0011.
* (b) An evidence document and a separate final report.
* (c) The evidence inside the criteria document.

## Option chosen

(a).

## Reasons

* ADR-0011 asks the final report for the criteria commit's hash, one hash per indicator, the reproduction recipe and the comparison of the two runs. ADR-0013, Consequences, uses the evidence document as the condition for a reduction of the star, through per-indicator hashes, and as the place of design findings. One document meets both, and no versioned text separates them (search for "final report" and "evidence document" over the repository, 2026-10-07).
* Fixing the structure, not the contents, before the criteria are written is consistent with LOG-021's reason against its option (l2), which "would fix the contents of the document before the criteria it reports on exist".
* A rule on what is reported, fixed after the values are seen, allows selection; full publication removes the choice.

## Reasons for each rejected option

* (b): two homes for the same per-indicator hashes.
* (c): the criteria document is not rewritten after its commit (ADR-0011, Consequences), and the evidence is written after it.

## Open, and where it goes

* The contents: the correspondence phase, after the criteria commit.
* Whether the full outputs sit inside the document or in a generated file beside it: the correspondence phase.
