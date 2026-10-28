# Grain: what one row stands for

## The concept

The **unit of observation** is what one record describes. Two surveys can both cover three months and differ in it.

![Left: three months, each with four different respondents, A to L. Right: the same four people, A to D, observed in each of three months and linked across them.](figures/cross-sections-or-panel.svg)

*Repeated cross-sections ask different people each time; a panel follows the same people.*

Only a panel can show how a person changes. Repeated cross-sections compare groups: the month 3 group against the month 1 group, never the same individuals. A question that asks how something "evolves" assumes a panel.

## The transfer

In a warehouse, the unit of observation is the **grain** of the fact table: what one row stands for.

* **A row is a response, not a person.** The fact table holds one row per staged survey response. Its decision record first named that grain "person grain"; it was renamed response grain because no source column identifies a respondent ([ADR-0007](../decisions/0007-person-grain-fact-table-and-dimension-grain-rule.md#addendum-2026-10-04), addendum of 2026-10-04).
* **The first question assumed a panel.** Q1 asked how a monthly proportion "evolves". With different respondents per period that reading is not available, so the question was revised to how the proportion differs across the months represented ([ADR-0004](../decisions/0004-revise-business-questions.md#q1--originally), Q1).
* **Row counts are responses.** The 290,051 staged records are not claimed to be 290,051 people ([ADR-0008](../decisions/0008-staging-deduplication-grain.md#decision-outcome), Scope).

## Where it breaks

* The figure knows who is who. The source file does not: one person could answer twice and nothing would show it. The rows are responses of unknown identity, which is weaker than either picture: even "different people each month" is an assumption.
