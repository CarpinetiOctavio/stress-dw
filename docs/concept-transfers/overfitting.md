# Overfitting: one principle instead of a patch per gap

## The concept

Through two points pass a line, a quadratic, a cubic and a polynomial of degree n. All four reproduce the known points with zero error.

![Two fixed points crossed exactly by a line, a quadratic, a cubic and a degree-n polynomial; away from the points the curves with more parameters bend further apart.](figures/two-points-four-functions.svg)

*Each curve is labeled with its number of parameters. The line is fully determined by the two points; the others have parameters to spare, so they bend most away from the points that anchor them.*

What sets them apart is how far off they go one step beyond the known points. Spare parameters are room to fit anything, noise included; choosing them is **overfitting**. Two remedies are standard: prefer the fewest parameters that explain the data, and stop fitting when further steps no longer improve the result on **held-out data**, data the fit has not seen.

## The transfer

The criteria document carried a documentary rule, which compared each question's original wording with its current one. Audit readings by fresh readers found places where it admitted two readings: gaps, the data points here.

* **A patch per gap is the polynomial.** A clause per gap fits the readings already made and can open readings no one tested. Across its rewrites the rule grew from 344 to 886 words, and each audit reading still found two new gaps, one of them on a sentence a fix had added ([LOG-051](../decisions/log/LOG-051-stopping-rule-documentary-audit-readings.md#reasons)).
* **One principle is the line.** On 2026-10-19 the rule was rewritten on one principle instead of a clause per gap ([criteria document, section 0](../audit/correspondence-criteria.md#0-scope), dates of the changes).
* **The stopping rule is early stopping.** A rule set before the third audit reading fixed when fixing ends: one fix after gaps, one last reading, and any gap in it ends the process. The last reading found one, and the documentary verdict was removed ([LOG-051](../decisions/log/LOG-051-stopping-rule-documentary-audit-readings.md#decision)).
* **Fresh readers are the held-out data.** The final test gave the frozen text to readers with no other context ([criteria document, section 0](../audit/correspondence-criteria.md#0-scope), Two-reader test).

## Where it breaks

* A text has no parameter count: the word count is a proxy, used only as a constraint on fixes ([LOG-051](../decisions/log/LOG-051-stopping-rule-documentary-audit-readings.md#reasons), declared limits).
* Two points determine a line; gaps do not determine a principle. A principle is argued from the objective, and the gaps only test it ([ADR-0011](../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md#decision-outcome), rule 3).
* One round of held-out readers can find a failure; finding none supports generalization without proving it.
