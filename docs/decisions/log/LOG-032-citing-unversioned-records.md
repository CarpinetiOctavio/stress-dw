---
id: LOG-032
alias: documentation-currency stage 3, citation of unversioned records
date: 2026-10-04
status: recorded
formalization: none
---

# Cite log and register identifiers with a notice until those records are versioned

## Decision

* Until the decision log and the documentation-currency register are in the repository, pull-request descriptions and commit messages cite `LOG-` and `DC-` identifiers followed by one fixed sentence: "LOG and DC identifiers refer to the decision log and the documentation-currency register, which enter the repository in later pull requests (the records PR and PR-e)."
* The sentence names only records not yet versioned: after the records pull request is merged it refers to the register alone, and after PR-e it is no longer used.
* Pull request #47 (commit `4b623e0`) predates this decision and cites LOG-001, DC-86 and DC-16 without the sentence. Neither its description nor its commit is changed; those identifiers resolve once the records pull request and PR-e are merged.

## Linked findings

None. Related: [LOG-001](LOG-001-safe-test-commands.md) (reasons for each rejected option, option (a)) and [LOG-004](LOG-004-decision-log-and-lessons.md) (order of the records pull request).

## Options considered

* Citation: (1) identifiers with the sentence; (2) no identifiers; (3) the records pull request moved before PR-N2.
* Scope of the sentence: pull-request descriptions only; descriptions and commit messages.
* Pull request #47: its description edited; left as it is and recorded here.

## Option chosen

(1), in descriptions and commit messages; pull request #47 left as it is and recorded here.

## Reasons

* An identifier with the sentence names a record and states when it enters the repository; it is not cited as evidence of a versioned artifact ([ADR-0012](../0012-cite-only-frozen-and-versioned-sources-as-evidence.md), rule 1).
* Once the log and the register are versioned, every identifier cited this way resolves to a file.
* A commit message is permanent history; the same sentence keeps it as documented as the pull request.

## Reasons for each rejected option

* (2): it loses the link between a change and the decision that grounds it.
* (3): it changes the order decided on 2026-10-03 (LOG-004), under which the records pull request follows PR-N1 and PR-N2.
* Descriptions only: the commit, the permanent record, would carry less than the pull request.
* Editing #47's description: its commit cannot change, so the two would differ, and the description is the text reviewed before the merge.

## Open, and where it goes

Nothing; the sentence stops being used when PR-e is merged.

**Status (2026-10-06).**

* PR-e was merged as #58; the sentence is no longer used.
