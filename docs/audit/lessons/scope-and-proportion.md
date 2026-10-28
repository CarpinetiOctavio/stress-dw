# Scope and proportion

Format: [lessons index](README.md#format).

The repository's axis is transparency: where its method held is shown by its records, and where it overreached is recorded here as plainly. Both lessons concern effort out of proportion to what it could change.

## LSN-014 — A rule outgrew its weight

* **What happened.** The documentary verdict of Q2 and Q7.1 changed no correspondence verdict, yet its rule was fixed after each audit reading: it grew from 344 to 886 words, and each reading still found new gaps, one of them on a sentence a fix had added. It was removed in the end.
* **How it was detected.** By a stopping rule set before the third audit reading; the fourth reading found a gap, which ended the process.
* **Rule.** See [LOG-051](../../decisions/log/LOG-051-stopping-rule-documentary-audit-readings.md).
* **Pointers.** LOG-051; the addenda to LOG-016, LOG-045 and ADR-0004; [criteria document, section 0](../correspondence-criteria.md#0-scope); [overfitting](../../concept-transfers/overfitting.md).

## LSN-015 — The process outgrew the object

* **What happened.** From the first log entry of the criteria work (LOG-039, 2026-10-06) to the criteria commit (2026-10-26), ten pull requests (#66 to #75) and thirteen log entries (LOG-039 to LOG-051) went into fixing one document of 662 lines, including the rewrites of a rule whose verdict changed no correspondence verdict (LSN-014).
* **How it was detected.** By LSN-014, and by counting the pull requests and log entries of the phase when it closed.
* **Rule.** Before a rule, check or document is added, the verdict or result it can change is named; one that changes none is not added.
* **Pointers.** [ADR-0011](../../decisions/0011-preregister-correspondence-criteria-before-exposing-indicator-values.md); LOG-051; [parsimony](../../concept-transfers/parsimony.md).
