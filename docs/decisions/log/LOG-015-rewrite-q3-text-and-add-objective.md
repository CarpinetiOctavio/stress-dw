---
id: LOG-015
alias: documentation-currency d
date: 2026-10-04
status: recorded
formalization: none
---

# Rewrite Q3's text and add its objective by an ADR-0004 addendum

## Decision

Q3's text becomes "Among respondents, what proportion report both growing stress (Growing_Stress = 'Yes') and coping difficulties (Coping_Struggles = 'Yes'), broken down by occupation and country, and how does that proportion differ when countries are grouped by region?" and Q3 gains the objective "Describe how the proportion of respondents reporting both growing stress and coping difficulties differs by occupation (the dataset's five categories, which include Student and Housewife alongside employment categories), by country, and by region, without attributing any difference to a work environment or to resilience." Both are recorded by a dated addendum to ADR-0004, which also qualifies its statements that Q3 needed no rewording (`:26`) and that every question's text matches exactly (`:118`). By ADR-0004's Confirmation (`:125`), the header of Q3 in [`indicators.md`](../../specification/indicators.md) (`:27`) takes the new wording. ADR-0006 `:35`, an accepted decision record, keeps the original text; `indicators.md` is the current definition ([LOG-008](LOG-008-adr-0006-addendum.md)).

## Linked findings

Decision d of the documentation-currency register's decision list; finding DC-38.

## Options considered

* (d1) The starting text and objective, by an ADR-0004 addendum.
* (d2) The current text kept, with no objective.

## Option chosen

(d1). PR group: PR-b.

## Reasons

* Nothing implements "continent": a case-insensitive search for "continent" over `docs/`, `src/` and `tests/` finds only quotations of Q3's text (`indicators.md:27`, ADR-0006 `:35`, ADR-0005 `:21`).
* Indicators 5 and 6 implement the grouping sets {occupation, country} and {occupation, region} (`indicators.md:31–32`); the new text asks for what they compute.
* ADR-0004 gives Q3 no objective (`:40`, "Q3 reviewed, not revised").
* The five occupation categories named in the objective are the specified domain (`sources.md:37`).

## Reasons for each rejected option

* (d2): it keeps a question that asks for a grouping nothing computes, and leaves ADR-0004's statements of an exact match false.

## Open, and where it goes

* The wording of the addendum: the plan of PR-b.
