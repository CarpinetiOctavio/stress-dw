# Verification of commands, counts and locators

Format: [lessons index](README.md#format).

## LSN-005 — Collection counts verify a set of test commands

* **What happened.** A proposed pair of test commands, `--ignore=tests/test_acceptance.py` together with the restricted command of `CLAUDE.md`, would have dropped C1–C7 and C11 (51 tests), which are meant to run normally.
* **How it was detected.** By reading the pair against `CLAUDE.md` and by `pytest --collect-only`.
* **Rule.** Any documented set of test commands is verified by collection only: the counts per command sum to the count of a plain run, with no test in two commands.
* **Pointers.** [LOG-001](../../decisions/log/LOG-001-safe-test-commands.md).

## LSN-006 — A count in a report is computed, not recalled

* **What happened.** A report stated that the documentation-currency sweep had found 15 new decision items; its own list had 14.
* **How it was detected.** When permanent identifiers were assigned to the items.
* **Rule.** Every count stated in a report is computed from the register it summarizes.
* **Pointers.** Decision items N1 and N2 of the documentation-currency register ([LOG-001](../../decisions/log/LOG-001-safe-test-commands.md), [LOG-002](../../decisions/log/LOG-002-readme-status-sentence.md)).

## LSN-007 — Locators are verified at the commit they cite

* **What happened.** Some line numbers in the documentation-currency register were first taken from a numbered listing that started after a file's frontmatter, so they were offset.
* **How it was detected.** Before delivery, by locating each cited line again with a search at the start commit.
* **Rule.** Every `file:line` locator is verified by a search at the commit it refers to before the text that cites it is delivered.
* **Pointers.** Method section of the documentation-currency register.

## LSN-011 — Read ranges are checked against the file's last line

* **What happened.** In stage 1 the documentation-currency sweep read seven decision records (ADR-0001, ADR-0002, ADR-0005, ADR-0006, ADR-0008, ADR-0012, ADR-0013) through line ranges that stopped one line before each file's last line, a line without a final newline; the last line of each was not read by hand. The scripted probes read the files whole.
* **How it was detected.** A later search returned two of those lines; comparing every read range with each file's line count found the other five. All seven were then read: six are consistent with the rest, and ADR-0002 `:68` repeats a statement already recorded as finding DC-27.
* **Rule.** A file read by line range is checked against its line count, including a last line without a final newline, so the range covers the whole file.
* **Pointers.** Revision history of the documentation-currency register.


## LSN-012 — A writing rule that no test checks is checked by hand before a pull request

* **What happened.** Two decision-log drafts (LOG-024, LOG-025) and the log index used "Fase" without the gloss that [writing conventions, rule 3](../../writing-conventions.md#3-spanish-inside-english-documents) requires. The drafts passed the patterns of the voice test, which does not check glosses.
* **How it was detected.** By a check of the drafts at their final paths before the records pull request: links, anchors, voice patterns and the "Fase" gloss.
* **Rule.** Before a pull request, each writing-convention rule that no test covers is checked by hand on the changed files, and the plan names the check.
* **Pointers.** LOG-024, LOG-025; writing conventions, rule 3.
