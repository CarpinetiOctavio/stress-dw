---
id: LOG-009
alias: documentation-currency N17
date: 2026-10-02
status: recorded
formalization: none
---

# State the addendum convention of decision records in the decision-record index

## Decision

The convention that accepted decision records are not rewritten and receive dated addenda is stated in [`docs/decisions/README.md`](../README.md), in a short section beside "Deviations from base MADR", in the same change as finding DC-24.

## Linked findings

DC-90 of the [documentation-currency register](../../audit/documentation-currency.md#5-findings).

## Options considered

* (a) `docs/decisions/README.md`.
* (b) The decision-record template.
* (c) The writing conventions.

## Option chosen

(a).

## Reasons

The README already holds the conventions of decision records: their format, the Findings section, and the identifiers.

## Reasons for each rejected option

* (b): a template that states the rule would be a second home; a placeholder heading that points to the README remains possible.
* (c): the writing conventions govern prose, not the lifecycle of decision records.

## Open, and where it goes

* The wording of the section: PR-a1, with DC-24.
