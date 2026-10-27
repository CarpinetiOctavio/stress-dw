---
id: LOG-051
alias: correspondence criteria, stopping rule for the audit readings
date: 2026-10-23
status: recorded
formalization: an addendum to ADR-0004
---

# Stop the fixes to the documentary rule by a rule set before the third audit reading

## Decision

Pre-test audit readings of the documentary rule of the [correspondence criteria](../../audit/correspondence-criteria.md), section 6, each by a fresh reader, stop under a rule set before the third reading.
- With no gap, convergence is supported.
- With gaps, none induced by a fix, one fix is allowed, followed by a fourth and last reading. The fix may neither lengthen the rule nor change a rule case checked when the rule was rewritten on one principle.
- The process is counterproductive in three cases: a fix-induced gap in the third reading; any gap in the fourth; or a fix that breaks either condition. The documentary verdict is then removed.
- After that removal, the entries of Q2 and Q7.1 set each element of the original question and legacy objective beside the columns it rests on and the versioned records on those columns, and quote the current question and objective, with no status and no verdict.
- A doubtful classification falls on the outcome that does not end the process.

The outcome (2026-10-25):
- The third reading found three gaps, none fix-induced.
- After the one fix, the fourth reading found one, of a form the fix had addressed.
- The documentary verdict is removed; the correspondence verdicts are not affected.

## Linked findings

None by ID; the motivation is under Reasons.

## Options considered

* (a) A rule with both ends, set before the third reading; on counterproductive, the steps, statuses and verdict are removed.
* (b) The same rule, with a reduction that keeps steps 1 to 3 and the element boundaries.
* (c) No rule set in advance: fixes continue until a reading finds no gap.

## Option chosen

(a).

## Reasons

* Across its rewrites before the third reading, the rule grew from 344 to 886 words, measured on whitespace in the working drafts, which are not versioned. Each audit reading still found two new gaps, and one of them rested on a sentence a fix had added. A rule that grows while its gaps do not fall is being fitted to each reading's gaps rather than made determinate (interpretation).
* A rule set before the result it decides is the method of [ADR-0011](../0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), which is cited as precedent and not amended. A rule that stops only on convergence never stops a process that does not converge; the counterproductive end stops fixes that create the gaps they fix.
* Doubtful classifications fall on the outcome that does not end the process: the rule guards against the wish to finish sooner.
* Every gap found arose in steps 1 to 3 or in the element boundaries. The reduction keeps the elements, their columns and the records on them, which a reader needs in order to compare the original question with the current one.
* Declared limits:
  * The rule was set after the audit readings began. The gaps of the first two readings had reached the drafting chat through the gap channel, on constructed references, with no reading of the key. No result of the third existed.
  * The rule was amended once, before the third reading ran.
  * It is therefore pre-registered relative to the third and fourth readings only, which is less strict than ADR-0011, whose rule preceded any value.
  * The "before" rests on time records in the working folder, not on a commit.
  * The word count is a proxy, used only as a constraint on the fix.

## Reasons for each rejected option

* (b): it keeps steps 1 to 3 and the element boundaries, where every gap arose.
* (c): a process that does not converge never reaches its end, and each fix depends on the last reading's gaps.

## Open, and where it goes

None.
