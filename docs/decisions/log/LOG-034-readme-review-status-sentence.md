---
id: LOG-034
alias: documentation-currency N18
date: 2026-10-05
status: recorded
formalization: none
---

# Remove the README's review-status sentence at the closure of the sweep

## Decision

The sentence "Documentation review is in progress." is removed from the Status section of `README.md`. The rest of the section is left to the README's planned rewrite.

## Linked findings

DC-96 of the [documentation-currency register](../../audit/documentation-currency.md#16-post-closure-audit-and-corrections); related: DC-17 and [LOG-002](LOG-002-readme-status-sentence.md), whose Open section assigns the sentence to the closure check of the sweep.

## Options considered

* (a) Remove the sentence.
* (b) Replace it with a pointer to the closure of the documentation-currency register.

## Option chosen

(a).

## Reasons

* The sweep was declared closed in section 15 of the register, so the sentence is no longer true.
* Removal is the smallest change that leaves nothing false, the criterion of LOG-002; the Status section is otherwise left to the planned rewrite.

## Reasons for each rejected option

* (b): it places the process of a documentation sweep on the repository's first page, which the planned rewrite decides.

## Open, and where it goes

* The removal: PR-f2.
* The rest of the Status section and the Development section: the planned README rewrite (LOG-002).

**Status (2026-10-06).**

* The removal: done in #63.
* The rest of the Status section and the Development section: the planned README rewrite.
