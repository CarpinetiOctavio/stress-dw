---
id: LOG-004
alias: documentation-currency N16
date: 2026-10-02
status: recorded
formalization: none
---

# Keep decisions in a decision log and method lessons by theme, with an index check

## Decision

* Decisions taken during the project are recorded in `docs/decisions/log/`, one file per decision, named `LOG-NNN-short-title.md`, with the frontmatter, sections and status values of the [recording standard](README.md#recording-standard). Entries carry no `decision-makers` field. The alias names the phase that raised the decision. [`docs/decisions/README.md`](../README.md) links the log once, with a sentence stating that log entries are not MADR records.
* Method lessons are recorded in `docs/audit/lessons/`, one file per theme, each lesson with an `LSN-NNN` identifier in its heading, and the format in [`lessons/README.md`](../../audit/lessons/README.md).
* The documentation-currency register keeps its method, scope, encountered figures, concept-to-home map, the list of decision items as pointers, and what was not swept. Its decision records and its method lessons become pointers to this log and to the lesson files; neither enters the versioned register in full.
* The prefixes `LOG-` and `LSN-` are added to the identifier section of `docs/decisions/README.md`, in the same change as finding DC-24.
* Formalization follows the [formalization rule](README.md#formalization-rule).
* An index check, `tests/test_record_indexes.py`, taking the repository root as a parameter, is created in the same pull request as the log and the lesson files, before the register is versioned. It checks that every log and lesson file has an index row and every row a file, that titles equal the files' first headings, and that statuses equal the frontmatter; and the decision-record index of `docs/decisions/README.md` against its files. This check extends the scope of the documentation-currency sweep; it is adopted to prevent the indexes from drifting after the sweep closes.

## Linked findings

Item N16 of the documentation-currency register (whether its decision records and method lessons enter the versioned register in full); findings DC-23 and DC-24.

## Options considered

* Home of decision records: (a) the register's own section; (b) an unversioned file listing the critical decisions; (c) one file, `docs/decisions/decision-log.md`; (d) a subfolder of `docs/decisions/` whose name states its status; (e) a subfolder `docs/decisions/log/`, one file per decision, status as a field.
* Home of method lessons: (f) a section of the register; (g) files per phase; (h) files per theme in `docs/audit/lessons/`.
* Drift control: (i) none; (j) an automated index check.

## Option chosen

(e), (h) and (j).

## Reasons

* The register is the audit of one phase; decisions of later phases have no place in it. A log under `docs/decisions/` gives decision records one home across phases.
* One file per decision keeps a history per entry and stable links. Status as a field does not go stale once entries are formalized, as a status in a folder name would.
* Files outside the `NNNN` pattern stay out of the decision-record index and out of the voice check's source of names, which reads only top-level `NNNN` files; the voice check still scans them, which enforces the impersonal form.
* The same lesson recurs across phases, so themes are a stable unit; identifiers in headings keep pointers valid when wording changes.
* No automated check covered any index before this decision; an index that is not checked drifts.

## Reasons for each rejected option

* (a): it ties decisions of every phase to the audit of one phase, and the register's versioned form would carry long reasoning outside its subject.
* (b): an unversioned file is not part of the record, and a list beside the register would be a second home.
* (c): a single file has no history per entry and grows without a stable unit.
* (d): a status in a folder name goes stale once entries are formalized.
* (f): lessons recur across phases and do not belong to one phase's audit.
* (g): the same lesson would be split across phases.
* (i): indexes drift without a check.

## Open, and where it goes

* The test module itself: drafted with the plan of the correction stage, in the same pull request as the log and the lesson files, placed before the register is versioned. Besides the index checks above, it checks that every finding identifier cited by a log entry resolves to a finding row of the register once the register is versioned, that every `LSN-` identifier cited by the register resolves to a lesson, and that every `LOG-` identifier cited by a lesson resolves to a log entry.
* Links from log entries to register findings: added when the register is versioned; until then entries cite findings by identifier only.
* Order (decided 2026-10-03): the records pull request (log, lessons, index check) goes right after PR-N1 and PR-N2, before PR-a1 and PR-b, since PR-a1 adds the `LOG-` and `LSN-` prefixes to the identifier section and the addenda of PR-b may point to their log entries.
* The index check also checks that every home cited in `docs/concept-homes.md` resolves, file and anchor ([LOG-010](LOG-010-concept-home-map.md)); a row whose home reads "open" is a declared gap, not a broken home.
* The `LOG-` and `LSN-` prefixes in the identifier section of `docs/decisions/README.md`: the same change as DC-24.
* The register's pointers to log entries and lessons: written when the register is versioned.
* PR-e: the pull request that versions the register at `docs/audit/documentation-currency.md`, rewrites its links from draft to final paths (sections 7, 11 and 12 of the register) and adds the links from log entries to findings; it is merged before stage 4 of the documentation-currency sweep.
