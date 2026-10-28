# Proxy: what a column records against what it is read as

## The concept

Asking a person whether they feel hot is a way to screen for fever. The answer is recorded exactly; reading it as fever is a step the answer does not take by itself.

![Two rows. Fever is read from a yes to the question of feeling hot. Explicit recognition of stress is read from growing_stress = 'Yes'. In both, the reading is a premise, not a measurement.](figures/meant-or-recorded.svg)

*The right-hand box is data; the arrow is a premise.*

A measure that stands in for a concept it does not measure directly is a **proxy**. Whether it captures that concept is its **construct validity**. A proxy is not wrong; an unstated proxy is, because the reader takes the arrow for a measurement.

## The transfer

* **The condition is a proxy.** `explicit_recognition` is `growing_stress = 'Yes'`. Its definition states that reading the answer as explicit recognition is a premise, not a fact stated by the source, and links the variable mapping where the premise lives ([LOG-012](../decisions/log/LOG-012-explicit-recognition-premise.md); [definition](../specification/definitions.md#explicit_recognition)).
* **The name was kept and the arrow stated.** Renaming the condition would have left the interpretation in place and two names for one thing; one sentence and one pointer close the gap where the condition is defined ([LOG-012](../decisions/log/LOG-012-explicit-recognition-premise.md#reasons-for-each-rejected-option)).
* **Names claim only what the data support.** The same rule governs every name in the repository ([writing conventions, rule 5](../writing-conventions.md#5-names-claim-only-what-the-data-supports)).
* **No verdict crosses the arrow.** No correspondence verdict states that the data are valid, or makes a finding about people ([criteria document, section 0](../audit/correspondence-criteria.md#0-scope), What no verdict states).

## Where it breaks

* Fever has a thermometer to check the answer against. The source file has no such reference, so the premise can be stated but not tested.
* A screening question is chosen for its purpose; the survey item was not designed for the reading given to it, so its fit to the concept is unknown, not merely imperfect.
