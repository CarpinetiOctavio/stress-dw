---
id: LOG-048
alias: correspondence criteria, source verification
date: 2026-10-08
status: recorded
formalization: addendum of 2026-10-08 to ADR-0012
---

# Check every claim that rests on a published work against a copy of it, in a register a script verifies

## Decision

A claim of this repository that rests on a published work is recorded in the verification register, [`docs/references/verification.toml`](../../references/verification.toml). The register gives, for the work, its citation, its DOI, the URL and date the copy consulted was obtained, that copy's SHA-256 and its licence; and, for each claim, the printed page, a verbatim quotation and the documents that make the claim. The module `stress_dw.references` checks that a copy has the registered SHA-256 and that each quotation occurs on its page; how it runs is in [`docs/references/README.md`](../../references/README.md). A copy is stored in the repository only when its licence permits redistribution; the first is Kim (2017), under CC BY-NC 3.0. The work stays cited by its bibliographic data ([ADR-0012](../0012-cite-only-frozen-and-versioned-sources-as-evidence.md), addendum of 2026-09-30); the register adds a check, not a second citation.

## Linked findings

None.

## Options considered

* (a) A verification register checked by a script, with a copy stored only when its licence permits redistribution.
* (b) As (a), with the cited pages of every work stored as well, whatever its licence.
* (c) Stored copies of the works, without a register.

## Option chosen

(a).

## Reasons

* A citation shows which work a claim rests on, not that the passage was read. A register of hash, page and quotation, checked by a script, lets anyone holding a copy of the same file repeat the check.
* The copies of Clement et al. (2015) and Schnyder et al. (2017) obtained from Cambridge Core, and of the author manuscript of Andrade et al. (2014) obtained from PMC, gave the same SHA-256 on repeated download on 2026-10-08, so a copy obtained later from the registered URL is the file that was checked.
* Some providers stamp each download, so the hash of such a copy cannot be matched by another reader's copy. The register marks those sources, and for them the check confirms the quotations on any copy, with the differing hash reported as a note.
* The check confirms that a quotation is on that page of that copy. Whether a claim reads the quotation correctly remains a reading, open to review against the quotation, which the register shows beside the claim.
* The rule adds an obligation to the treatment of published works set by ADR-0012's addendum of 2026-09-30, so a dated addendum to ADR-0012 points to this entry, as its addendum of 2026-10-04 does for [LOG-011](LOG-011-adr-0012-scope-of-capture-values.md) ([formalization rule](README.md#formalization-rule)).

## Reasons for each rejected option

* (b): the copies of Cohen (1988), Bergsma (2013), Clement et al. (2015), Schnyder et al. (2017), Corrigan (2004) and Andersen (1995) each print a copyright statement or terms of use, and the author manuscript of Andrade et al. (2014) prints no licence; none permits redistribution, so storing their pages would redistribute them.
* (c): a stored copy without page and quotation does not show which passage supports which claim, and the copyright statements above bar most copies.

## Open, and where it goes

* Seven statements of [`conceptual-framework.md`, section 3](../../conceptual-framework.md#3-literature-basis-for-the-mechanism) differ from their sources' wording: four about Clement et al. (2015), one each about Corrigan (2004), Andersen (1995) and Andrade et al. (2014). Their correction, and their entries, go to a later pull request.
* A correction to the Conclusions of Schnyder et al. (2017) is reported as published in 2018; its text is not yet checked, and the register's entry for that sentence says so.
* Cohen (1988) and Bergsma (2013): the passages on which check A5's thresholds rest enter the register with the correspondence criteria; whether a later copy can match the SHA-256 of the copies consulted, a scan and a reproduction, is not established.

**Status (2026-10-08).**

* The seven statements of `conceptual-framework.md`, section 3, that differed from their sources: corrected, with their register entries.

**Status (2026-10-08).**

* The correction to the Conclusions of Schnyder et al. (2017): checked against the authors' reply (British Journal of Psychiatry, 211(3), 182–183), which gives the clarified sentence; `conceptual-framework.md`, section 3, now states it. A formal correction notice was not found.
