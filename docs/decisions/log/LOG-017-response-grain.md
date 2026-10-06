---
id: LOG-017
alias: documentation-currency f
date: 2026-10-04
status: recorded
formalization: addendum of 2026-10-04 to ADR-0007
---

# Describe the fact table at response grain and keep ADR-0007's title

## Decision

Living documents describe the grain of `fact_response` as response grain: one row per staged survey response. A dated addendum to ADR-0007 records this. ADR-0007's title and file name stay, and so does the row of the decision-record index that reproduces the title. The line of `CLAUDE.md` that says "person grain" is changed within [LOG-025](LOG-025-claude-md-wording.md).

## Linked findings

Decision f of the [documentation-currency register](../../audit/documentation-currency.md#8-decide-items)'s decision list; finding DC-77.

## Options considered

* (f1) Response grain, by an ADR-0007 addendum; the title kept.
* (f2) "Person grain" kept.

## Option chosen

(f1). PR group: PR-c (DC-77); the ADR-0007 addendum is shared with [LOG-018](LOG-018-cluster-literals-addendum.md) and placed by the plan of stage 3.

## Reasons

* `fact-table.md:22` defines the row as "one row per staged record, that is, one row per survey response", and ADR-0008 records that no respondent identifier exists (DC-77).
* An accepted decision record is not rewritten; its title is part of its text.

## Reasons for each rejected option

* (f2): it names a person-level grain that no identifier supports.

## Open, and where it goes

* The wording of the addendum: the plan of stage 3.

**Status (2026-10-06).**

* The wording of the addendum: done in #54.
