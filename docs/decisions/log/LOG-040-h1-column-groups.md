---
id: LOG-040
alias: documentation-currency g
date: 2026-10-06
status: recorded
formalization: none
---

# Fix the two column groups of H1 by the OSMI schema, for the criteria and for check A5

## Decision

The two column groups of H1 ([ADR-0001, Hypotheses](../0001-position-as-portfolio-project.md#hypotheses-not-findings)) are fixed for the correspondence criteria and for the checks. The OSMI group is the eight source columns whose names occur in the captured OSMI 2014 schema ([ADR-0001, addendum of 2026-10-06](../0001-position-as-portfolio-project.md#addendum-2026-10-06)): `Timestamp`, `Gender`, `Country`, `self_employed`, `family_history`, `treatment`, `mental_health_interview` and `care_options`. The other group is the remaining nine: the eight symptom columns and `Occupation`.

* `care_options` is placed in the OSMI group on a match by name, a premise ([LOG-013](LOG-013-care-options-neutral-wording.md)); check A6 tests it ([LOG-041](LOG-041-a6-osmi-group.md)).
* `Occupation` is placed in the other group as a premise that no planned check can refute: it is absent from the OSMI schema, and H3 names only the eight symptom columns. Every result that involves `Occupation` is read under both reading branches of [ADR-0011](../0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), rule 4, without resolving between them.
* Check A5 measures association between the two groups and within each.
* The partition is frozen once any result of A5, A6 or A10 exists. A later change is recorded as a dated amendment beside this decision, marked as post-result, the original left unchanged, on the same terms as ADR-0011's Constraint for the criteria document.

## Linked findings

Decision g of the [documentation-currency register](../../audit/documentation-currency.md#81-starting-options), section 8.1; the first item of its [section 5.8](../../audit/documentation-currency.md#58-items-of-the-starting-list-not-listed-above) ("pending g").

## Options considered

* (i) Documented and undocumented columns (ADR-0001, P6).
* (ii) By the OSMI schema.
* (iii) Three groups.

## Option chosen

(ii).

## Reasons

* H1 concerns origin, not documentation; the Data Card describes columns without stating where they come from.
* The OSMI schema is the nearest available indication of origin. It comes from a third-party deposit whose relation to OSMI's own files is not verified ([ADR-0001, addendum of 2026-10-01](../0001-position-as-portfolio-project.md#addendum-2026-10-01)), so it fixes a partition and is not evidence about H1.
* Every column falls in one of the two groups that the two branches of ADR-0011, rule 4, require.
* A premise that no check can test is declared as such and read under both branches.

## Reasons for each rejected option

* (i): it places `care_options` with the symptom columns, while the captured schema lists a column of that name with a question text.
* (iii): ADR-0011, rule 4, provides two branches; a residual group needs an extra reading rule, whose content would be "read under both branches", which (ii) applies to `Occupation` with less text.

## Open, and where it goes

* The rule that maps outcomes of A5, A6 and A10 to "H1 holds" or "H1 does not hold": the criteria document, with the branches, before any of those checks runs.
* `Occupation` stays untested unless a versioned capture of RHMCD-20's schema shows it; not pursued.
