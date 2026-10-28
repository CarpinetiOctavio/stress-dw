# Pre-registration: the target is painted before the shots

## The concept

A marksman who fires at a barn wall and then paints a target around the holes always hits the centre. The hits say nothing about aim, because the result could not have failed.

![Left: a target painted first, with shots scattered around it, some missing. Right: the same shots, with the target painted around them afterwards, so every shot hits.](figures/target-before-or-after.svg)

*The same nine shots. Only the target drawn first can be missed.*

Machine learning names the same failure **data leakage**: when test data reach the model during fitting, the test score measures memory, not generalization. The remedy in both cases is order: the target, or the test set, is fixed and sealed before the shots are fired.

## The transfer

The correspondence criteria are the target; the indicator values are the shots.

* **The target is painted first.** The criteria were committed to `main` before any indicator value was exposed, and the commit's hash is the evidence of that order ([ADR-0011](../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md#decision-outcome), rule 1). A criterion fitted to output already seen could not fail ([ADR-0011](../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md#decision-drivers)).
* **The test set stays sealed while the code runs.** The tests that execute the indicators report pass or fail only, by a command that suppresses assertion messages ([`CLAUDE.md`](../../CLAUDE.md#hard-rules)). Running is allowed; showing is not.
* **What leaked already is declared.** Part of the data was known before the criteria were written: published distributions, counts of the derived conditions, the number of cells. The criteria document lists it, so that a reader can judge whether a criterion bent to it ([criteria document, section 1](../audit/correspondence-criteria.md#1-declaration-of-prior-knowledge)).
* **The same rule protects the test of the text.** The answer key of the two-reader test was withheld from the party that drafted fixes, so that no fix could encode the key's reading. The two times key content reached that party are declared ([criteria document, section 0](../audit/correspondence-criteria.md#0-scope), Two-reader test).

## Where it breaks

* No model is trained here. What transfers is a principle of reasoning, a rule set after the results cannot vouch for them, not the technique.
* A commit records the order of publication, not of observation: history cannot show what was seen outside the repository ([ADR-0011](../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md#consequences)).
* A leaked test set can be replaced; prior knowledge can only be declared, not removed ([ADR-0011](../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md#consequences)).
