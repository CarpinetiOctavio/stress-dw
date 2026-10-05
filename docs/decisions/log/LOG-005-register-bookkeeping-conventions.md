---
id: LOG-005
alias: documentation-currency register conventions
date: 2026-10-02
status: recorded
formalization: none
---

# Keep the documentation-currency register's bookkeeping by fixed conventions

## Decision

The documentation-currency register keeps its findings by these conventions:

* **Primary and secondary class.** Each finding has exactly one primary class and, where one applies, a declared secondary class. Totals are computed by script from the primary class, with a reconciliation table that lists the identifiers in each class.
* **NONE.** A finding that requires no action has the class NONE with a sub-reason: clean, still true, open obligation, or correspondence phase. It is counted in the totals.
* **Verified, no finding.** A clean result of a whole probe carries a finding identifier with class NONE (clean), because the sweep's closure depends on that probe being run again with a clean result. A point verification of a single item carries no identifier and is listed under "Verified, no finding".
* **N identifiers.** DECIDE items found by the sweep carry permanent identifiers N1, N2, and so on, distinct from the letters of the decision list the sweep started from.
* **`PR-` prefixes.** Correction groups are named `PR-a1`, `PR-a2`, `PR-b`, `PR-c`, `PR-d`, `PR-e`, and isolated pull requests `PR-N1`, `PR-N2`; bare letters are kept for decisions.
* **Summaries.** A report that summarizes the register names every finding by its identifier.

## Linked findings

The [register](../../audit/documentation-currency.md#5-findings)'s findings section (legend) and its reconciliation section; findings DC-22 and DC-23.

## Options considered

* Classes: combined classes kept as written; one primary class with a declared secondary.
* Findings that need no action: rows without a class dropped from the findings; NONE with a sub-reason.
* Verifications: every point verification numbered as a finding; probe-level clean results numbered and point verifications listed without an identifier; probe-level clean results moved to the list as well.
* Identifiers of new DECIDE items: letters continued after `l`; permanent N identifiers.
* Correction groups: bare letters (`a1`, `b`, and so on); `PR-` prefixes.
* Summaries: findings grouped without their identifiers; every finding named by its identifier.

## Option chosen

One primary class with a declared secondary; NONE with a sub-reason; probe-level clean results numbered and point verifications listed; permanent N identifiers; `PR-` prefixes; every finding named in summaries.

## Reasons

* Totals counted from a column as written did not match the rows ([LSN-008](../../audit/lessons/bookkeeping-and-namespaces.md#lsn-008--totals-are-computed-from-one-primary-class-per-finding)); one primary class per finding makes them reconcilable.
* A clean probe is evidence the closure check needs; a point verification is not a finding.
* A summary that names every finding lets a reader check it against the register for completeness.
* Distinct identifier forms keep one symbol for one meaning ([LSN-010](../../audit/lessons/bookkeeping-and-namespaces.md#lsn-010--each-namespace-has-its-own-prefix)).

## Reasons for each rejected option

* Combined classes kept as written: totals become ambiguous.
* Rows without a class dropped: the evidence of clean checks is lost.
* Every point verification numbered: verifications become findings, and the totals stop measuring what needs attention.
* Probe-level clean results moved to the list: the closure of the sweep depends on those probes being run again with a clean result, so they stay findings.
* Letters continued after `l`: the letters are the decision list the sweep started from; extending them blurs which items came from the sweep.
* Bare letters for correction groups: they collide with the decision letters ("b" can mean either).
* Findings grouped without identifiers in a summary: they seem to be missing ([LSN-009](../../audit/lessons/bookkeeping-and-namespaces.md#lsn-009--every-finding-identifier-appears-in-a-summary-of-the-register)).

## Open, and where it goes

Nothing.
