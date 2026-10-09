# Decision log

Decisions taken during the project that are not, or not only, recorded in a decision record of [`docs/decisions/`](../README.md). Entries are not MADR records: each one holds the reasoning of one decision until a decision record or an addendum carries it in full (formalization rule, below). Method lessons drawn from the same work are kept in [`docs/audit/lessons/`](../../audit/lessons/README.md).

## Recording standard

Every entry is one file, `LOG-NNN-short-title.md`, with this frontmatter:

| Field | Content |
|-------|---------|
| `id` | `LOG-NNN`, three digits, never reused |
| `alias` | the identifier the decision had in the phase that raised it, with the phase named (for example `documentation-currency N1`) |
| `date` | date the decision was taken, `YYYY-MM-DD` |
| `status` | one of the status values below |
| `formalization` | the decision record or addendum that carries the entry, or will carry it, or `none` |

No entry carries a `decision-makers` field: a decision is recorded without saying whose it was ([writing conventions, rule 2](../../writing-conventions.md#2-voice)).

The body has these sections, in this order:

1. **Decision.** What was decided, in one paragraph.
2. **Linked findings.** The findings or items the decision answers, by ID.
3. **Options considered.**
4. **Option chosen.**
5. **Reasons.**
6. **Reasons for each rejected option.**
7. **Open, and where it goes.** What the decision leaves unresolved, and the place or phase that takes it up.

Context is given by pointer to the document that holds it, not restated ([writing conventions, rule 4](../../writing-conventions.md#4-introduce-before-use-one-home-per-concept)).

## Status values

| Status | Meaning |
|--------|---------|
| `recorded` | The decision is taken; this entry holds its reasoning. |
| `formalized` | The target named in `formalization` carries every section of the recording standard; the entry is reduced to a pointer to it. |
| `superseded` | A later entry replaces this one; the body names it. |

## Formalization rule

An entry is reduced to a pointer only when its target carries every section of the recording standard. Otherwise the entry keeps the reasoning and the target points to the entry. Pointers run one way: the reasoning has exactly one home.

## Index

| ID | Title | Status |
|----|-------|--------|
| [LOG-001](LOG-001-safe-test-commands.md) | Document safe test commands while indicator values may not be exposed | recorded |
| [LOG-002](LOG-002-readme-status-sentence.md) | Correct the README status sentence by reference to the data-integration closure record | recorded |
| [LOG-003](LOG-003-minimum-count-addendum.md) | Record by addendum that the minimum-count consideration is a flag, not a rule | recorded |
| [LOG-004](LOG-004-decision-log-and-lessons.md) | Keep decisions in a decision log and method lessons by theme, with an index check | recorded |
| [LOG-005](LOG-005-register-bookkeeping-conventions.md) | Keep the documentation-currency register's bookkeeping by fixed conventions | recorded |
| [LOG-006](LOG-006-legacy-superseded-notice.md) | Record that the legacy's one permitted change was made, and align the working instructions | recorded |
| [LOG-007](LOG-007-home-map-timing.md) | Confirm the home map in stage 2 and write overlapping pointers in stage 3 | recorded |
| [LOG-008](LOG-008-adr-0006-addendum.md) | Point ADR-0006 to the indicator specification by a dated addendum | recorded |
| [LOG-009](LOG-009-addendum-convention-home.md) | State the addendum convention of decision records in the decision-record index | recorded |
| [LOG-010](LOG-010-concept-home-map.md) | Confirm the concept-to-home map and keep it as a living document | recorded |
| [LOG-011](LOG-011-adr-0012-scope-of-capture-values.md) | Read ADR-0012's constraint on capture values by its scope, and apply it to three places | recorded |
| [LOG-012](LOG-012-explicit-recognition-premise.md) | State where explicit recognition is defined that it rests on a premise | recorded |
| [LOG-013](LOG-013-care-options-neutral-wording.md) | Word care options neutrally and state the OSMI meaning as a candidate premise | recorded |
| [LOG-014](LOG-014-indicator-renames-and-residual-identifiers.md) | Rename indicators 9 to 13, 15 and 16 and keep the isolation identifiers as residual | recorded |
| [LOG-015](LOG-015-rewrite-q3-text-and-add-objective.md) | Rewrite Q3's text and add its objective by an ADR-0004 addendum | recorded |
| [LOG-016](LOG-016-objectives-q2-q6-q71-q72.md) | Set the objectives of Q2 and Q7.1 and fix the conditions for those of Q6 and Q7.2 | recorded |
| [LOG-017](LOG-017-response-grain.md) | Describe the fact table at response grain and keep ADR-0007's title | recorded |
| [LOG-018](LOG-018-cluster-literals-addendum.md) | Record by addendum that the cluster's literals are repeated by design | recorded |
| [LOG-019](LOG-019-a6-scope.md) | Align check A6 with the test of hypothesis H1 | recorded |
| [LOG-020](LOG-020-no-file-line-convention.md) | Set no convention for file and line citations in living documents | recorded |
| [LOG-021](LOG-021-evidence-document-to-correspondence-phase.md) | Assign the definition of the correspondence evidence document to the correspondence phase | recorded |
| [LOG-022](LOG-022-adr-0010-0013-addenda.md) | Point ADR-0010 and ADR-0013 to ADR-0009's restated findings by addenda | recorded |
| [LOG-023](LOG-023-disclosure-willingness-reading.md) | Read mental_health_interview as disclosure willingness, without anticipated stigma | recorded |
| [LOG-024](LOG-024-gloss-scope.md) | Gloss Spanish terms but not identifiers and paths, gloss the phase label in docstrings, and exempt index titles | recorded |
| [LOG-025](LOG-025-claude-md-wording.md) | Align the wording of CLAUDE.md in one change | recorded |
| [LOG-026](LOG-026-voice-of-accepted-records.md) | Leave the voice of accepted decision records as written | recorded |
| [LOG-027](LOG-027-see-as-cross-reference.md) | Allow sentence-initial See as a cross-reference convention | recorded |
| [LOG-028](LOG-028-decision-makers-exception.md) | Keep the decision-makers exception without a stated reason | recorded |
| [LOG-029](LOG-029-template-comments.md) | Leave third-party template comments in .gitignore as they are | recorded |
| [LOG-030](LOG-030-rhmcd-20-published-work.md) | Cite the RHMCD-20 deposit as a published work | recorded |
| [LOG-031](LOG-031-cluster-caveat-by-link.md) | State that symptom-cluster outputs carry a link to the caveat | recorded |
| [LOG-032](LOG-032-citing-unversioned-records.md) | Cite log and register identifiers with a notice until those records are versioned | recorded |
| [LOG-033](LOG-033-portfolio-destination-without-scu.md) | Name the portfolio's destination as academic and professional review, without SCU | recorded |
| [LOG-034](LOG-034-readme-review-status-sentence.md) | Remove the README's review-status sentence at the closure of the sweep | recorded |
| [LOG-035](LOG-035-claude-md-legacy-work-pointer.md) | Point CLAUDE.md's line on legacy work to its records in general | recorded |
| [LOG-036](LOG-036-open-obligations-to-correspondence-phase.md) | Assign DC-19 and DC-21 to the correspondence phase, with A2 after the criteria commit | recorded |
| [LOG-037](LOG-037-addendum-pointers-to-log-entries.md) | Point the 2026-10-04 addenda to their log entries by new dated addenda | recorded |
| [LOG-038](LOG-038-status-lines-for-open-items.md) | Record the state of open items by dated status lines | recorded |
| [LOG-039](LOG-039-reading-rule.md) | Adopt the reading rule for figures derived from the source file, with this entry as its home | superseded |
| [LOG-040](LOG-040-h1-column-groups.md) | Fix the two column groups of H1 by the OSMI schema, for the criteria and for check A5 | recorded |
| [LOG-041](LOG-041-a6-osmi-group.md) | Extend check A6 to the OSMI group of LOG-040 | recorded |
| [LOG-042](LOG-042-pilot-order.md) | Draft the criteria for Q4 first, then Q7.2, then the remaining questions | recorded |
| [LOG-043](LOG-043-status-line-on-change.md) | Add a new dated status line when the state of an open item changes | recorded |
| [LOG-044](LOG-044-stage-placement.md) | Place the open items of the correspondence phase before or after the criteria commit | recorded |
| [LOG-045](LOG-045-correspondence-evidence-document.md) | Name, place and structure the correspondence evidence document as the final report of ADR-0011 | recorded |
| [LOG-046](LOG-046-user-of-the-outputs.md) | Derive what each output must allow from its question's objective, with the original purpose in the documentary layer only | recorded |
| [LOG-047](LOG-047-a5-threshold-procedure.md) | Take the thresholds of check A5 from a verified published source, or else fix them as a declared convention | recorded |
| [LOG-048](LOG-048-verifiable-source-checks.md) | Check every claim that rests on a published work against a copy of it, in a register a script verifies | recorded |
| [LOG-049](LOG-049-reading-rule-by-repository-access.md) | Count the repository as known when the criteria are fixed, with this entry as the home of the reading rule | recorded |
| [LOG-050](LOG-050-a5-a6-a10-reading-thresholds.md) | Fix the interpretability bound of A5 and A6, the harmonization of values, and the α of A10's guard, by the scheme of LOG-047 | recorded |
