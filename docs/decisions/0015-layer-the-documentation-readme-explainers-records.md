---
status: "accepted"
date: 2026-11-01
decision-makers: Octavio Carpineti
---

# Layer the documentation: a plain README, one-page explainers, and the records as proof

## Context and Problem Statement

The README rewritten in #85 and given its figures in #86 explained its points inline: two long paragraphs on the result, a table pairing each concept with what it changed and its evidence, and a section on what was built. Its strongest points, the two errors found in the course version, the rebuilt warehouse and the two sources joined in one file, were spread across that table, between rows on the method itself. Every claim linked a record directly, so a reader who wanted the reasoning behind a point had to read the record that proves it.

A cold reading of 2026-11-01, by two fresh language-model sessions given the roles of a recruiter and of a hiring manager, is cited as dated corroboration only: it is not versioned, and no statement of this record depends on it ([ADR-0012](0012-cite-only-frozen-and-versioned-sources-as-evidence.md), rule 2).

The repository also did not say why so much work went into a file whose outputs cannot be used as findings.

How should the documentation present the project so that a reader sees its strongest points first, can reach the reasoning behind each in one page, and reaches the proof only when looking for it, without any of these layers becoming a second home of what another holds?

## Decision Drivers

* The repository is a portfolio piece ([ADR-0001](0001-position-as-portfolio-project.md)); its purpose is to show reasoning and judgment.
* One home per concept ([writing conventions, rule 4](../writing-conventions.md#4-introduce-before-use-one-home-per-concept); [`concept-homes.md`](../concept-homes.md)).
* Evidence discipline ([ADR-0012](0012-cite-only-frozen-and-versioned-sources-as-evidence.md)): a claim links the versioned record that carries it.
* Concept transfers already explain the method by analogy ([ADR-0014](0014-explain-the-method-through-declared-concept-transfers.md)).
* Proportion: text is added where it changes what a reader understands ([scope and proportion](../audit/lessons/scope-and-proportion.md), LSN-015).

## Considered Options

* A README whose every claim links its record directly.
* The README with the concept transfers as its only second layer.
* Three layers: a plain README, one-page explainers, and the records.

## Decision Outcome

Chosen option: "Three layers", because it is the only option under which a reader can read each point at the depth sought, while each rule, count and finding keeps one home.

* **README.** Plain, with no identifiers of records, checks or findings in its narrative part. Each point states what was done and its mechanism, and links its explainer. Claims with no explainer link their record directly.
* **Explainer.** A new document type, in [`docs/explainers/`](../explainers/README.md). It explains one point of the README directly, unlike a concept transfer, which explains by analogy. It fits on one page, the standard ADR-0014 sets for concept transfers. It restates no rule and no count; it links them, and it cites the versioned record for every claim. Figures are embedded from their home documents, never copied.
* **Records.** The specification, the decision records and the audit documents are the proof, not the reading path.
* **Evidence chain.** The README cites through the explainer; the explainer cites the record. [Writing conventions, rule 2](../writing-conventions.md#2-voice), is amended to match.
* **First person.** The root README may use the first person in its narrative sections, as before. In addition, `why-and-how.md` and `how-it-was-evaluated.md` each hold one section in the first person, signed with the account identifier `@CarpinetiOctavio`, marked so that the voice check can scope it. Inside it, the first person is allowed; the second person and any address to the reader are not. Everything outside it stays impersonal.

### Consequences

* Good, because the README's first part stays short and names each mechanism.
* Good, because the reasoning behind each point is one link away, and its proof two.
* Good, because the reason the project exists has a home ([why and how](../explainers/why-and-how.md)).
* Bad, because an explainer is one more document to keep current when the record it explains changes.
* Constraint: a later addition to the README or to an explainer passes these rules.

### Confirmation

Each explainer is listed in its index, fits on one page, and links a versioned record for every claim. The voice check exempts the root README and the two marked sections only, and still flags the second person inside them (`tests/test_writing_conventions.py`).

## Pros and Cons of the Options

### A README whose every claim links its record directly

* Good, because nothing is added between the claim and its proof.
* Bad, because the reasoning behind a point is reachable only through the record that proves it.

### The README with the concept transfers as its only second layer

* Good, because no document type is added.
* Bad, because an analogy explains a concept, not what happened in this case; the errors and the two sources have no analogy to carry them.

### Three layers

* Good, because each reader stops at the depth sought.
* Bad, because the explainer must be kept in step with the record it explains.

## More Information

* Related: [ADR-0001](0001-position-as-portfolio-project.md), [ADR-0012](0012-cite-only-frozen-and-versioned-sources-as-evidence.md), [ADR-0014](0014-explain-the-method-through-declared-concept-transfers.md); pull requests #85 and #86.
