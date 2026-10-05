---
id: LOG-002
alias: documentation-currency N2
date: 2026-10-02
status: recorded
formalization: none
---

# Correct the README status sentence by reference to the data-integration closure record

## Decision

The first two sentences of the README's Status section ("Specification and audit in progress. There is no runnable pipeline yet.") are replaced by the text below, quoted as Markdown source (its link is relative to the repository root, where the README sits):

```markdown
Data integration is closed for this rebuild as of commit `9f31ab0`; the closure record is in [`phase4-closure.md`](docs/audit/phase4-closure.md#1-status). Documentation review is in progress.
```

The third sentence of the section is kept. The change is made ahead of the README's planned rewrite, by reference to [`phase4-closure.md`, section 1](../../audit/phase4-closure.md#1-status); the Status section is otherwise left to that rewrite.

## Linked findings

DC-17 of the [documentation-currency register](../../audit/documentation-currency.md#5-findings).

## Options considered

* (a) Leave the sentences to the planned rewrite.
* (b) Replace them with one sentence by reference to `phase4-closure.md`, section 1, followed by "Documentation review is in progress."
* (c) Rewrite the Status section now.
* Wording of (b): a first draft, quoted as Markdown source below, and the wording chosen.

```markdown
Data integration is closed and the pipeline runs; its closure record and how to reproduce it are in [`phase4-closure.md`](docs/audit/phase4-closure.md#1-status). Documentation review is in progress.
```

## Option chosen

(b), with the wording given under Decision.

## Reasons

The README stated something false: the pipeline exists and its acceptance checks passed at commit `9f31ab0`. Option (b) is the smallest change that removes the false statement, claims nothing beyond section 1 of the closure record, and leaves the rest of the section to the rewrite.

## Reasons for each rejected option

* (a): a false statement would stay on the repository's first page until the rewrite.
* (c): it would anticipate the planned rewrite.
* The first draft: an undated "the pipeline runs" claims more than section 1, which dates the closure to `9f31ab0` and records no later run; it dropped that bound; and it linked section 1 for reproduction, which is in section 2 and is referenced from the README by [LOG-001](LOG-001-safe-test-commands.md).

## Open, and where it goes

* The rest of the Status section and the Development section: the planned README rewrite.
* "Documentation review is in progress." goes stale when the review closes: the planned README rewrite, or the closure check of the documentation-currency sweep if the rewrite comes later.
