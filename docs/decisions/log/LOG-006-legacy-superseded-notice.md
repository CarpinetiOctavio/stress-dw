---
id: LOG-006
alias: documentation-currency N4
date: 2026-10-02
status: recorded
formalization: addendum to ADR-0000 (planned)
---

# Record that the legacy's one permitted change was made, and align the working instructions

## Decision

* A dated addendum to [ADR-0000](../0000-rebuild-from-scratch-instead-of-continuing-legacy.md) records that the one addition its Decision Outcome permits to the legacy repository, a superseded notice, was made: commit `3cf77ce` on `main` of `stress-dw-legacy`, dated 2026-09-20, "docs: add superseded notice (README only; no other files changed)", adding `README.md` (26 lines) and changing no other file. The addendum states that the exception is exhausted: no further change to the legacy repository is permitted. It also states that the notice reflects the state of the project on 2026-09-20 and that `stress-dw` is the current record.
* The legacy line of `CLAUDE.md` is aligned with ADR-0000 and with what happened: the legacy is never modified beyond that notice, added on 2026-09-20; no further change is permitted. It points to the addendum and keeps its `[ADR-0000]` tag.
* Citations of the legacy keep pointing to the tag `legacy-original`, which the notice does not change.

## Linked findings

DC-44 and DC-92 of the documentation-currency register.

## Options considered

* (a) Change `CLAUDE.md` only.
* (b) A dated addendum to ADR-0000, with a pointer to it from `CLAUDE.md`.
* (c) No change; the finding reported only.

## Option chosen

(a), together with (b) because no versioned document records the notice commit. A search of the repository at commit `286c53d` for "3cf77ce" found nothing, and "superseded notice", "superseded" and "notice" occur only in ADR-0000's permission, in unrelated text, and in `LICENSE`.

## Reasons

* ADR-0000 permits one addition to the legacy, a superseded notice; `CLAUDE.md` said the legacy is never modified, with no exception. Both describe the legacy, so the document that guides every working session contradicted the decision record.
* The notice exists: the mirror's `main` holds exactly one commit after the tag (checked with `git ls-remote` and a temporary bare clone, deleted afterwards; the local clone was not fetched into).
* The fact had no versioned home, so the addendum gives it one, and `CLAUDE.md` points to it instead of restating it.

## Reasons for each rejected option

* (c): it leaves a contradiction in the document that guides every working session.
* (b) unconditionally: if a versioned document already recorded the commit, an addendum would be a second home for the same fact.

## Open, and where it goes

* The text of the addendum and its date: written in the correction pull request that carries it (PR-b).
* The change to `CLAUDE.md`: in the same pull request as the addendum (PR-b), so its pointer resolves when it is merged.
* Once the addendum carries every section of the recording standard, this entry is reduced to a pointer ([formalization rule](README.md#formalization-rule)).
