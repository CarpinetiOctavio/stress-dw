---
id: LOG-011
alias: documentation-currency N14
date: 2026-10-03
status: recorded
formalization: addendum to ADR-0012 (planned)
---

# Read ADR-0012's constraint on capture values by its scope, and apply it to three places

## Decision

* A dated addendum to [ADR-0012](../0012-cite-only-frozen-and-versioned-sources-as-evidence.md) clarifies the scope of its constraint that values readable in a capture "are not restated in any other document": it covers values about the data (counts, ranges, distributions), which are prior knowledge under [ADR-0011](../0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), rule 2; descriptions of what a capture shows stay in its evidence row; and a result computed by a check from the source file has its own provenance, even when it equals a value in a capture. The addendum is a clarification of scope, not an exception.
* Three places are changed accordingly:
  * `dataset-provenance.md:64` states the agreement of the legacy log with the Data Card by pointer to the capture, keeping the qualifier that the Data Card's figures are rounded.
  * `sources.md:47` points to the row of check A12 for the `Timestamp` range.
  * `legacy-audit.md:20` keeps A12's range as the check's own result, computed from the source file, and its clause "matching the Data Card" becomes a pointer to the capture.

## Linked findings

DC-85 of the documentation-currency register.

## Options considered

* (i) Remove every capture value outside the criteria document, by pointers, with the readings above.
* (ii) Keep `dataset-provenance.md:64` as a declared exception, recorded by an addendum to ADR-0012.
* (iii) Treat the three places as debts, by analogy with ADR-0012's constraint on existing citations.

## Option chosen

(i), with the two readings, formalized by the addendum.

## Reasons

* The constraint's text has no exception for a document that uses the values as its own evidence, and no limit to text written after it; the three places predate ADR-0012.
* Its scope follows from its own link to ADR-0011, rule 2: it concerns prior knowledge about the data. Read without that scope, it would also remove the descriptions that ADR-0012's rule 4 asks each evidence row to give.
* A check's result is computed from the source file; equality with a capture does not make it a restatement.
* At `:64` no claim is lost: the agreement and its basis remain, by pointer, and the rounding qualifier keeps the claim from implying an exact match the capture does not show.
* The readings qualify an accepted decision record, so they are formalized by an addendum to it ([formalization rule](README.md#formalization-rule)).

## Reasons for each rejected option

* (ii): an exception for one place where none is needed once the scope is read correctly.
* (iii): the constraint on existing citations concerns pages cited without a capture, not restated values; extending it by analogy would stretch it beyond its text.

## Open, and where it goes

* The three changes: PR-d, stage 3.
* The text of the addendum and its date: PR-b, the pull request of the addenda.
* The values remain declared prior knowledge for the correspondence phase (ADR-0011, rule 2).
