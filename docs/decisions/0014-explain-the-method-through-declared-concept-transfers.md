---
status: "accepted"
date: 2026-10-27
decision-makers: Octavio Carpineti
---

# Explain the method through declared concept transfers, one document each, demonstrated on the repository's own artifacts

## Context and Problem Statement

The formal documents (the specification, the decision records, the criteria document) state what was done and how. A reader outside data warehousing or research methods can follow each rule and still not see why it is there. A concept from another field can show the why at a glance, but an analogy can also oversimplify, and a clear text is not an easy one: where the analogy stops holding is part of the explanation.

How should the reasons behind the method be explained to a reader outside its domain, without restating the formal documents or simplifying them?

## Decision Drivers

* The repository is a portfolio piece ([ADR-0001](0001-position-as-portfolio-project.md)); its purpose is to show reasoning and judgment, which the formal documents hold but do not explain.
* One home per concept ([writing conventions, rule 4](../writing-conventions.md#4-introduce-before-use-one-home-per-concept)): an explanation links the rule it explains instead of restating it.
* Evidence discipline ([ADR-0012](0012-cite-only-frozen-and-versioned-sources-as-evidence.md)): a claim about the project cites a versioned artifact.
* An analogy that hides its limit misleads; its limit has to be stated with it.

## Considered Options

* No analogies; the formal documents stand alone.
* Analogies inside the formal documents, next to the rules they explain.
* Declared concept transfers in their own folder, one document each, each demonstrated on the artifacts it applies to and stating where it breaks.

## Decision Outcome

Chosen option: "Declared concept transfers in their own folder", because it explains the why to a reader outside the domain while leaving the formal documents as the only home of each rule.

* **Home.** [`docs/concept-transfers/`](../concept-transfers/README.md) holds one document per transfer and an index. This record holds the decision and no analogy.
* **Form.** Each document fits on one page: the concept, introduced with a figure for a reader outside the domain; the transfer, each claim linked to the versioned section that holds it; and where it breaks.
* **Content.** Figures use illustrative data only and show no indicator value ([ADR-0011](0011-preregister-correspondence-criteria-before-exposing-indicator-values.md)). An outside work cited by a transfer is registered under [LOG-048](log/LOG-048-verifiable-source-checks.md).
* **Not in the criteria document.** No transfer enters the criteria document; a later document may link a transfer where it explains a mechanism.

### Consequences

* Good, because a reader can reach the why of a rule in one page, and the rule's own text stays in one place.
* Good, because each transfer states its limit, so the analogy invites the reader into the formal document instead of replacing it.
* Bad, because each transfer is one more document to keep current when the rule it explains changes.
* Constraint: a transfer restates no rule; it links it.

### Confirmation

Each document in `docs/concept-transfers/` is listed in its index, has the three parts, and links every claim about the project to a versioned section.

## Pros and Cons of the Options

### No analogies

* Good, because nothing is added.
* Bad, because the reasons stay legible only to readers of the domain.

### Analogies inside the formal documents

* Good, because the explanation sits next to the rule.
* Bad, because the formal documents grow and mix two registers, and the criteria document, fixed by commit, cannot take them.

### Declared concept transfers in their own folder

* Good, because explanation and rule each keep one home.
* Bad, because the reader has to follow a link from the rule to its explanation.

## More Information

* Related: [ADR-0001](0001-position-as-portfolio-project.md), [ADR-0011](0011-preregister-correspondence-criteria-before-exposing-indicator-values.md), [ADR-0012](0012-cite-only-frozen-and-versioned-sources-as-evidence.md).
* The method lessons on scope and proportion are in [`audit/lessons/scope-and-proportion.md`](../audit/lessons/scope-and-proportion.md).
