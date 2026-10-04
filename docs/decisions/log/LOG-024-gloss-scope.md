---
id: LOG-024
alias: documentation-currency N7
date: 2026-10-04
status: recorded
formalization: none
---

# Gloss Spanish terms but not identifiers and paths, gloss the phase label in docstrings, and exempt index titles

## Decision

* Under [writing conventions, rule 3](../../writing-conventions.md#3-spanish-inside-english-documents), identifiers and file paths written in code format are names, not Spanish terms, and need no gloss (DC-46).
* The docstring "(Fase 4)" (English: "(Phase 4)"; see [`methodology.md`](../../methodology.md)) of `src/stress_dw/__init__.py:1` is glossed (DC-53).
* Titles in the decision-record index reproduce the titles of accepted records and are exempt; the gloss is in the record (DC-64).

## Linked findings

Item N7 of the documentation-currency register; findings DC-46, DC-53 and DC-64.

## Options considered

* (N7a) As above.
* (N7b) Every Spanish identifier and path glossed.
* (N7c) Titles in the index glossed.

## Option chosen

(N7a). PR groups: PR-a1 (DC-46, DC-64) and PR-c (DC-53).

## Reasons

* Rule 3 governs Spanish terms and quotations read as language; an identifier or a path in code format is read as a name.
* A docstring is versioned text, and the gloss is one parenthesis.
* An index row reproduces the title of an accepted record, which is not rewritten.

## Reasons for each rejected option

* (N7b): it glosses names that are not read as language.
* (N7c): the index row would differ from the record's title.

## Open, and where it goes

* Whether rule 3's text states the exemption of identifiers and paths, and its wording: the plan of PR-a1.
