---
status: "{proposed | rejected | accepted | deprecated | superseded by ADR-000X}"
date: {YYYY-MM-DD}
decision-makers: Octavio Carpineti
---

# {Short title, stating the problem and the chosen solution}

## Context and Problem Statement

{Two to three sentences, or a short narrative, describing the situation that requires a decision. State the question the decision answers directly, as its own sentence ending in "?".}

## Findings

{Optional. Include only when the decision rests on evidence gathered against the repository, the dataset, or an external source — as in ADR-0000 and ADR-0001. Each row must cite where the evidence lives (report section, script, query, capture) and mark its status as `Established`, a numbered hypothesis (`H1`, `H2`, ...) still to test, or `Pending` a check in `docs/audit/legacy-audit.md`.}

| ID | Finding | Evidence | Status |
|----|---------|----------|--------|
| {F/P/…-n} | **{Finding, stated as a claim, in bold.}** {Supporting detail.} | {Report section / script / query / capture path} | {Established / Hypothesis (Hn) / Pending} |

## Decision Drivers

* {Driver 1}
* {Driver 2}

## Considered Options

* {Option 1}
* {Option 2}
* {Option 3}

## Decision Outcome

Chosen option: "{title of the chosen option}", because {justification tied to the Decision Drivers and, where applicable, the Findings}.

### Consequences

* Good, because {positive consequence}.
* Bad, because {negative consequence, cost, or thing given up}.
* Constraint: {anything the decision binds future work to, if applicable}.

### Confirmation

{How compliance with this decision is checked — e.g. what file holds the evidence, what a later audit verifies against this ADR.}

## Pros and Cons of the Options

### {Option 1}

* Good, because {argument}.
* Bad, because {argument}.

### {Option 2}

* Good, because {argument}.
* Bad, because {argument}.

## More Information

* Related: {other ADRs}.
* {Links, evidence index, source}.