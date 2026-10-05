---
id: LOG-025
alias: documentation-currency N8
date: 2026-10-04
status: recorded
formalization: none
---

# Align the wording of CLAUDE.md in one change

## Decision

`CLAUDE.md` is changed once, in the pull request that aligns its legacy line ([LOG-006](LOG-006-legacy-superseded-notice.md), PR-b):

* "Fase" (English: "Phase"; see [`methodology.md`](../../methodology.md)) is glossed once (DC-63).
* "SCU" is introduced at its first use (DC-74).
* The line on C8, C9 and C10 keeps the restricted command and states why C10 is in it: its tests do not execute the indicators, but a failing assertion would display counts of the derived conditions (DC-87).
* The line on work against the legacy repository points to the records of that work (DC-88).
* The line on evidence follows ADR-0012, rules 2 and 3 (DC-94).
* "Person grain" becomes "response grain" ([LOG-017](LOG-017-response-grain.md)).

The mention of "SCU" in ADR-0002 (`:15`) stays as written.

## Linked findings

Item N8 of the [documentation-currency register](../../audit/documentation-currency.md#8-decide-items); findings DC-63, DC-74, DC-87, DC-88 and DC-94.

## Options considered

* (N8a) One change, in PR-b.
* (N8b) One change per finding.
* (N8c) No change.

## Option chosen

(N8a). PR group: PR-b.

## Reasons

* Each of the five wordings is unglossed or does not match the document that is the home of its rule.
* One change keeps `CLAUDE.md` a summary under one review.

## Reasons for each rejected option

* (N8b): five reviews of one file for one kind of correction.
* (N8c): it leaves the working instructions out of line with their homes.

## Open, and where it goes

* The wording of each line: the plan of PR-b.
