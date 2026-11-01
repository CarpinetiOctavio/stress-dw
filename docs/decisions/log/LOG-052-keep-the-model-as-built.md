---
id: LOG-052
alias: correspondence phase, revisit of ADR-0013
date: 2026-11-01
status: recorded
formalization: an addendum to ADR-0013
---

# Keep the model as built once the correspondence evidence document is merged

## Decision

The model stays as built. The reduced star that [ADR-0013](../0013-keep-star-schema-add-flat-consumption-view.md) defers is weighed once the [correspondence evidence document](../../audit/correspondence-evidence.md) is merged (#83) and is not adopted. This entry is the follow-up note that ADR-0013, Confirmation, requires when it is revisited.

## Linked findings

M4 to M6 and M8 of [ADR-0013](../0013-keep-star-schema-add-flat-consumption-view.md#findings).

## Options considered

* (a) Keep the model as built.
* (b) Adopt the reduced star, under the conditions of ADR-0013, Consequences.

## Option chosen

(a).

## Reasons

* A reduction preserves every indicator output, so it changes no verdict of the correspondence phase ([ADR-0013, Consequences](../0013-keep-star-schema-add-flat-consumption-view.md#consequences)), and it adds no analytical capability ([ADR-0013, Decision Outcome](../0013-keep-star-schema-add-flat-consumption-view.md#decision-outcome)).
* The evidence document records no design finding: every question reads "none" ([`correspondence-evidence.md`, section 4](../../audit/correspondence-evidence.md#4-questions)). Nothing therefore reopens the model.
* The limit that the evidence document shows is the file, not the form of the schema: one of the nine questions corresponds.

## Reasons for each rejected option

* (b): its cost (ADR-0013, M8: the specification, the DDL and the load, the sixteen indicator queries, checks C1, C5 and C7, E3 repeated against a new DDL, and hashes before and after) is out of proportion to what it would add, which is a better-formed model with the same outputs.

## Open, and where it goes

The flat consumption view stays with the reporting layer, as ADR-0013, Decision Outcome, states; this entry does not change it.
