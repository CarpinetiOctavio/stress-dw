---
id: LOG-010
alias: documentation-currency home map
date: 2026-10-03
status: recorded
formalization: none
---

# Confirm the concept-to-home map and keep it as a living document

## Decision

* The concept-to-home map of the documentation-currency sweep (rows 1 to 37) is confirmed, with the adjustments below.
* The map is split by responsibility. The living part (concept, home, reason) is [`docs/concept-homes.md`](../../concept-homes.md), created in the records pull request and linked once from [writing conventions, rule 4](../../writing-conventions.md#4-introduce-before-use-one-home-per-concept). The sweep's dispositions (the other places of each concept, their classes, and the stage that changes them) stay in section 7 of the documentation-currency register and are frozen with it when the sweep closes.
* The index check of [LOG-004](LOG-004-decision-log-and-lessons.md) also checks that every home cited in `docs/concept-homes.md` resolves.
* Adjustments made at confirmation:
  * The status column of the table in `phase4-closure.md`, section 6, is condensed to links to the audit table, keeping each check's effect; its status had already drifted once (finding DC-14). Written in stage 3, since that table is corrected there ([LOG-007](LOG-007-home-map-timing.md)).
  * `conceptual-framework.md:63` is condensed in stage 5: it keeps the consequence of check A13 for hypothesis H1, with links, and the A13 figures leave. This resolves a conflict between two rows of the map.
  * A new row for values about the data readable in a capture, with each capture's evidence row as home and the scope of [LOG-011](LOG-011-adr-0012-scope-of-capture-values.md).
  * New rows for indicator names and for the reading of `care_options`, marked as depending on the wording of decisions c and b.
  * Restatements added: the result of check A8 in `sources.md:36` and `country-region-mapping.md:24` (pointers, stage 5); the display rule of `low_n` in `phase4-closure.md:73` (kept, with its link).
  * Reasons recorded: ADR-0001's Hypotheses section is the home of H1 and H3 by necessity, since no living document explains them; the kept places of the rows for source columns and dimensions name the rule or use that keeps them.

## Linked findings

The [documentation-currency register](../../audit/documentation-currency.md#5-findings), section 7; findings DC-14, DC-85.

## Options considered

* (a) The map only in the register.
* (b) The map in a new decision record.
* (c) A living file for concept, home and reason, with the sweep's dispositions in the register.
* (d) A copy of the map in this entry.

## Option chosen

(c).

## Reasons

* The map governs future writing: a text that needs a concept points to its home, and a change of home updates the map in the same change ([writing conventions, rule 4](../../writing-conventions.md#4-introduce-before-use-one-home-per-concept)). A living file can follow the documents it describes.
* The rule the map applies is already written in a versioned document, writing conventions, rule 4. Under the [formalization rule](README.md#formalization-rule), a decision covered by a versioned document stays a log entry together with the change to that document.
* The dispositions of the sweep are findings work and belong to the register.

## Reasons for each rejected option

* (a): a sweep artifact, frozen when the sweep closes, would govern future writing and go stale.
* (b): a list of homes changes as documents change; frozen in an accepted decision record it would become a snapshot that needs addenda ([LOG-008](LOG-008-adr-0006-addendum.md) records the same problem for ADR-0006).
* (d): a second home for the same table.

## Open, and where it goes

* The sentence of rule 4 that links `docs/concept-homes.md`: the records pull request.
* Links that `docs/concept-homes.md` cannot carry yet: PR-a1 adds the anchor of the new section on addenda in `docs/decisions/README.md` to row 30; PR-b adds the link to ADR-0000's addendum on the superseded notice to row 23.
* Rows that depend on pending wording (decisions b, c, f, and N6): their homes are fixed; the wording of some places waits for those decisions.
* Homes still open: the general home of the reading rule (finding DC-91, correspondence phase) and the correspondence evidence document (decision l).

**Status (2026-10-06).**

* The sentence of rule 4 that links `docs/concept-homes.md`: done in #49.
* The links of rows 30 and 23: row 30 done in #50, row 23 in #52.
* Rows that depend on pending wording: the wording of decisions b, c, f and N6 was applied in #52 to #56.
* Homes still open: the correspondence phase.
