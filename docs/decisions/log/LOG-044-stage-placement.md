---
id: LOG-044
alias: correspondence criteria, stage placement
date: 2026-10-06
status: recorded
formalization: none
---

# Place the open items of the correspondence phase before or after the criteria commit

## Decision

Each open item of the correspondence phase is placed by one criterion: an item that produces information about the data goes after the criteria commit of [ADR-0011](../0011-preregister-correspondence-criteria-before-exposing-indicator-values.md); an item that fixes a scope or a rule goes before any result exists. The placements:

* DC-89, the correspondence evidence document: its name, path and structure are fixed before the criteria commit ([LOG-045](LOG-045-correspondence-evidence-document.md)); its contents are written after it. This refines [LOG-021](LOG-021-evidence-document-to-correspondence-phase.md), which assigns the definition to the correspondence phase as a whole.
* DC-19: checks A2 and A3 run after the criteria commit; A2 is already placed there by [LOG-036](LOG-036-open-obligations-to-correspondence-phase.md), and A3, for which LOG-036 sets no order, is placed there by this entry.
* DC-21: the query-time cost is measured after the criteria commit; LOG-036 sets no order for it.
* DC-13: check A7 runs after the criteria commit ([LOG-039](LOG-039-reading-rule.md)).
* The rationale of `dim_access` ([register, section 5.8](../../audit/documentation-currency.md#58-items-of-the-starting-list-not-listed-above), second item): read after the criteria commit, as an item of design coherence, not as a criterion; a design finding may reopen the model ([ADR-0013, Consequences](../0013-keep-star-schema-add-flat-consumption-view.md#consequences)).
* The "design and sufficiency items" of the starting list (register, section 5.8, third item): not carried. The register says "carried forward"; their detail is not versioned, and an item enters only once it is versioned. The register is not edited.

## Linked findings

DC-13, DC-19, DC-21 and DC-89 of the [documentation-currency register](../../audit/documentation-currency.md#57-execution-rules-in-living-documents); the second and third items of its section 5.8.

## Options considered

* (a) Placement by that criterion.
* (b) The correspondence phase as one undivided stage.
* (c) Every item before the criteria commit.

## Option chosen

(a).

## Reasons

* A scope fixed before any result exists cannot be chosen in the light of that result ([LOG-019](LOG-019-a6-scope.md)).
* Information about the data obtained before the criteria are fixed is prior knowledge under ADR-0011, rules 1 and 2.
* LOG-036 sets no order for A3 or for DC-21, and LOG-021 none for the parts of DC-89.

## Reasons for each rejected option

* (b): the order of A3, DC-21 and the parts of DC-89 stays unstated.
* (c): items that produce information about the data would add to the prior knowledge the criteria must declare.

## Open, and where it goes

None.
