---
id: LOG-030
alias: documentation-currency N13
date: 2026-10-04
status: recorded
formalization: none
---

# Cite the RHMCD-20 deposit as a published work

## Decision

The RHMCD-20 deposit, cited by its versioned DOI (ADR-0001 `:33`), is a published work under ADR-0012's paragraph on scope (`:33`): it is cited by its bibliographic data, and no capture is required. Its columns matching "verbatim" remains hypothesis H3, checked by A10.

## Linked findings

Item N13 of the [documentation-currency register](../../audit/documentation-currency.md#8-decide-items); finding DC-79.

## Options considered

* (N13a) A published work.
* (N13b) A page under ADR-0012, rule 2, with a capture.

## Option chosen

(N13a). PR group: PR-d.

## Reasons

* ADR-0012 `:33` states that rule 2 does not govern bibliographic references to published works, a published work being a fixed object identified by its bibliographic data, including its DOI when one exists.

## Reasons for each rejected option

* (N13b): ADR-0012 `:33` places a work identified by a DOI outside rule 2.

## Open, and where it goes

* Whether `legacy-audit.md:18` and `conceptual-framework.md:111` need any change: the plan of PR-d.
* The match of the columns: check A10, in the correspondence phase.
