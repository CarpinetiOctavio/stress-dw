---
id: LOG-001
alias: documentation-currency N1
date: 2026-10-02
status: recorded
formalization: none
---

# Document safe test commands while indicator values may not be exposed

## Decision

The test commands are written once, in [`phase4-closure.md`, section 2](../../audit/phase4-closure.md#2-reproducing-this), as two commands that together run every test exactly once:

* `uv run pytest -k "not (test_c8_ or test_c9_ or test_c10_)"`, which runs every test except C8, C9 and C10, normally;
* the restricted command of [`CLAUDE.md`](../../../CLAUDE.md), verbatim, which runs C8, C9 and C10 with pass or fail reported per test and no assertion message.

The section states that the pair applies until [ADR-0011](../0011-preregister-correspondence-criteria-before-exposing-indicator-values.md) allows exposure: after the criteria commit, after A5 has been run, and after A6 and A10 have been run or recorded as not obtainable (rule 4). It also states that a failure in C1–C7 or C11 may display counts or values derived from the source file and is reported as a failure only, as for C8–C10. The restricted tests are named "C8, C9 and C10". The test counts previously documented there are kept as dated statements of an unrestricted run at commit `9f31ab0`, never under the new commands. `README.md` replaces its `uv run pytest` line with a one-line reference to that section, with a link to ADR-0011, ahead of the README's planned rewrite and for execution safety only; the condition lapses when ADR-0011 allows exposure.

## Linked findings

DC-86 and DC-16 of the documentation-currency register.

## Options considered

* Procedure: (a) a pull request before the decisions of the sweep were taken, as an exception to the sweep's rule that the repository stays read-only until the register is approved; (b) a decision among the others of the sweep, implemented in its correction stage.
* Command set: (i) plain `uv run pytest`, as documented; (ii) `--ignore=tests/test_acceptance.py` together with the restricted command; (iii) the pair above; (iv) the whole acceptance module under the restricted form.
* Home of the commands: (1) the commands repeated in `README.md` and `phase4-closure.md`; (2) `CLAUDE.md` as the home; (3) `phase4-closure.md`, section 2.
* Earlier test counts: kept under the new commands; deleted; kept as dated statements.
* Name of the restricted tests: "the tests that execute the indicators"; "C8, C9 and C10".

## Option chosen

Procedure (b); command set (iii); home (3); the earlier counts as dated statements; "C8, C9 and C10".

## Reasons

* Command set (iii) runs every test exactly once, with C8, C9 and C10 restricted and every other test run normally, as `CLAUDE.md` requires. Verified by collection only at commit `286c53d`: 158 and 43 tests, 201 in all, with no overlap.
* Home (3) is the existing reproduction section, and ADR-0011 already links it.
* Dated statements keep the record without implying that the safe commands produced those counts.

## Reasons for each rejected option

* (a): traceability comes from isolating the change in its own pull request, not from its timing; an exception to the read-only rule would itself need recording; the pull request would cite a register that was not yet versioned; and the interim working rule (only the two commands are run) covered the risk until the correction stage.
* (i): with the source file present it runs C8, C9 and C10 without the restricted form.
* (ii): it drops C1–C7 and C11, which `CLAUDE.md` says are run normally (51 tests).
* (iv): it hides the diagnostics of load and schema failures, whose messages are not indicator values.
* (1): two homes for one concept ([writing conventions, rule 4](../../writing-conventions.md#4-introduce-before-use-one-home-per-concept)).
* (2): `CLAUDE.md` is an operational summary kept as it is, its wording on C10 is pending (documentation-currency N8), and a public README pointing to working instructions is out of place.
* Counts kept under the new commands: they would imply a result those commands never produced. Counts deleted: the record would be lost.
* "The tests that execute the indicators": C10 does not execute the indicators (finding DC-87).
* A first wording of the lapse condition allowed A5 to be recorded as not obtainable; ADR-0011, rule 4, gives that allowance only to A6 and A10.

## Open, and where it goes

* The wording on C10 in `CLAUDE.md` (DC-87): documentation-currency N8.
* Updating `phase4-closure.md`, section 2, when ADR-0011 allows exposure: the correspondence phase, after its exposure step.
* The README's Development section in full: the planned README rewrite.
