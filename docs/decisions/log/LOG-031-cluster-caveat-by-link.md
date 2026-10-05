---
id: LOG-031
alias: documentation-currency N15
date: 2026-10-04
status: recorded
formalization: none
---

# State that symptom-cluster outputs carry a link to the caveat

## Decision

`patterns.md:43` is reworded so that outputs using `symptom_cluster` carry a link to the caveat in its definition, which is what `indicators.py:24–27` attaches (DC-54).

## Linked findings

Item N15 of the [documentation-currency register](../../audit/documentation-currency.md#8-decide-items); finding DC-54.

## Options considered

* (N15a) `patterns.md:43` reworded to a link.
* (N15b) The code changed to attach the caveat's text.
* (N15c) Kept as written.

## Option chosen

(N15a). PR group: PR-c.

## Reasons

* [Writing conventions, rule 4](../../writing-conventions.md#4-introduce-before-use-one-home-per-concept): caveats travel by link and are never restated; the code already follows it.

## Reasons for each rejected option

* (N15b): it restates the caveat outside its home.
* (N15c): the specification would describe something the code does not do.

## Open, and where it goes

* The wording: the plan of PR-c.
