---
id: LOG-013
alias: documentation-currency b
date: 2026-10-04
status: recorded
formalization: none
---

# Word care options neutrally and state the OSMI meaning as a candidate premise

## Decision

Texts that describe `care_options` use a neutral wording, one that names the response ("report 'Yes' or 'Not sure' for care options") and not a property of the respondent's situation. The meaning given by the question text of the OSMI 2014 survey for a column of the same name is stated as a candidate premise, not as the meaning of the column.

## Linked findings

Decision b of the [documentation-currency register](../../audit/documentation-currency.md#8-decide-items)'s decision list; findings DC-43 and DC-75 (the `care_options` wording only).

## Options considered

* (b1) Neutral wording, with the meaning of the OSMI text stated as a candidate premise.
* (b2) "Awareness" of care options.
* (b3) Keep "availability" of care options.

## Option chosen

(b1). PR group: PR-b.

## Reasons

* The source gives no description of `care_options` ([dataset provenance, column documentation](../../dataset-provenance.md#column-documentation); ADR-0001, P6). "Available" is how the legacy report reads the column (same table, column "Legacy report reads it as"), not a statement of the source.
* A neutral wording claims only what the variable supports ([writing conventions, rule 5](../../writing-conventions.md#5-names-claim-only-what-the-data-supports)) and covers both levels that indicators 15 and 16 retain, "Yes" and "Not sure".
* The OpenML deposit of the 2014 survey gives a question text for a column named `care_options` (capture listed in the [evidence section of dataset provenance](../../dataset-provenance.md#evidence)). The Data Card has no text to compare it with, so the match is by column name only; its meaning can be stated as a premise, not as a fact.
* The treatment is the one of [LOG-012](LOG-012-explicit-recognition-premise.md): an interpretation stays visible as a premise.

## Reasons for each rejected option

* (b2): it adopts the meaning of the OSMI text as the meaning of the column on a match by name only, a claim the source does not carry.
* (b3): it carries the legacy reading as a fact, and "available" does not describe a "Not sure" response (DC-43).

## Open, and where it goes

* The neutral wording itself, the sentence that states the premise, and where that sentence lives: the plan of PR-b.
* How ADR-0003 `:77` ("the literal scope of Q7.2") is corrected under the convention for accepted decision records: the plan of PR-b.
* The text of Q7.2 (`indicators.md:88`, ADR-0004 `:114`): decision e.
* Indicator names that carry "conversion" or "resource-access" (indicators 12, 13 and 15): decision c.
