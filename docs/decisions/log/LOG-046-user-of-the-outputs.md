---
id: LOG-046
alias: correspondence criteria, user of the outputs
date: 2026-10-07
status: recorded
formalization: none
---

# Derive what each output must allow from its question's objective, with the original purpose in the documentary layer only

## Decision

The output-based correspondence criteria take, as what each output must serve, the determination its question's objective names ([ADR-0004](../0004-revise-business-questions.md)), to the degree the objective claims it (option c). The users stated by the legacy report at the tag `legacy-original`, mental health professionals as end users (pp. 5, 9 and 32), enter only the documentary layer, as the original purpose (option a). The repository's audience, academic and professional review ([LOG-033](LOG-033-portfolio-destination-without-scu.md)), is not a basis for criteria (option b). The criteria document states in its scope that "does not correspond" means that the output does not let the objective's determination be made. Structural criteria that the specification and checks C8 and C9 guarantee are declared unable to fail and do not count toward "corresponds".

## Linked findings

None.

## Options considered

* (a) The users stated by the legacy report.
* (b) The repository's audience.
* (c) The determination each objective names.

## Option chosen

(c) for the output-based criteria; (a) only in the documentary layer.

## Reasons

* [ADR-0011](../0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), rule 3, derives each criterion from the objective of its question; the objectives describe or compare, and that description or comparison is the determination the output must allow.
* No document of this repository states a user of the indicator outputs; its stated audience is academic and professional review (LOG-033).
* Under [ADR-0001](../0001-position-as-portfolio-project.md) (Consequences, Constraint), no test-bench output can feed the decisions the legacy report names (diagnoses, risk patterns, interventions), so an output-based criterion built on them could not pass. A verdict is informative only if its criterion could have gone the other way (ADR-0011, Decision Drivers). As the original purpose, those decisions belong to the documentary layer ([LOG-016](LOG-016-objectives-q2-q6-q71-q72.md)).
* A criterion that the specification or C8 and C9 guarantee could not fail, for the same reason.

## Reasons for each rejected option

* (a), for the output-based criteria: no output could pass under ADR-0001.
* (b): the project would define what counts as serving its own reviewer.

## Open, and where it goes

* The criteria themselves: the criteria document.
