# Writing conventions

These rules apply to every document in this repository: `docs/`, the ADRs, and the README. Each rule has one home. A rule that originates in a decision record points to it instead of restating it (rule 4). None of them modifies the legacy repository ([ADR-0000](decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md)).

## 1. Language

The repository is written in English, code and documents alike, with no exception. The legacy repository stays in Spanish, unmodified.

## 2. Voice

Impersonal. A document never says who thought, decided, or noticed something: it says "at the time X was considered...", "this was corrected to...". A person's name appears only in the `decision-makers` field of an ADR's frontmatter and inside URLs.

## 3. Spanish inside English documents

Any Spanish term or quotation carries its translation next to it, marked. A short fragment is written `"..." (English: "...")`; a long quotation is followed by `→ English: "..."`. "Fase N" (English: "Phase N") is glossed once per document, at its first appearance, with a pointer to [`methodology.md`](methodology.md).

## 4. Introduce before use; one home per concept

A concept is a defined term, rule, condition, or caveat that a reader must understand to read a document correctly.

* **Introduce before use.** A concept is introduced and explained before it is used. Where it is introduced elsewhere, its first use in the document links to that introduction.
* **One home.** A concept used in more than one place has exactly one home: a section, or a file of its own when it is used across files. Its definition, its rules, and its caveats are written there and nowhere else.
* **Reference, do not restate.** Every other use links to the home. It does not repeat the definition, the rules, or the caveats.
* **Caveats travel by link.** A caveat that must accompany a concept is named at each use through a link to its home (for example, "validity caveat"). It is therefore never assumed to carry over silently, and never restated.
* **One use, inline.** A concept used in a single place is introduced there and needs no home of its own.
* **Moving a home moves its references.** When a concept is given a home, or its home changes, every reference is updated in the same change.

## 5. Names claim only what the data supports

An indicator, a column, or a heading is named for what its variables can support. A cross-sectional self-report item cannot support a word that implies a process, a cause, a clinical state, or a delay ("develop", "deterioration", "postponement", "diagnosis"). The checklist used to review names and questions is the Constraint in [ADR-0004](decisions/0004-revise-business-questions.md).

## 6. Ambiguous values are never folded silently

Defined once, in the [multi-level self-report rule](specification/definitions.md#multi-level-self-report-rule) of the specification. Documents outside the specification link to it when they need it.

## 7. Evidence discipline

Every statement is backed by a cited source, marked as this project's own interpretation, or marked as pending a check ([conceptual framework, section 1](conceptual-framework.md#1-purpose-and-scope)). Findings and hypotheses use the IDs defined in the [decision records README](decisions/README.md#finding-and-hypothesis-ids).
