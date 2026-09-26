---
status: "accepted"
date: 2026-09-25
decision-makers: Octavio Carpineti
---

# Deduplicate staged records on all 17 source columns, not the columns this specification models

## Context and Problem Statement

This decision belongs to the data-integration phase, Fase 4 (English: "Phase 4"; see [`methodology.md`](../methodology.md)), which [`specification.md`](../specification.md) leaves open. The source file has no respondent identifier ([`specification.md`](../specification.md), Open items). [ADR-0007](0007-person-grain-fact-table-and-dimension-grain-rule.md) fixed the fact table's grain at one row per staged record, one row per survey response, but left open what counts as one staged record when multiple raw rows agree on every value the pipeline can observe. Checks A4 and A13 of the [legacy audit](../audit/legacy-audit.md) quantified this without resolving it: 194,641 of 292,364 rows duplicate at least one other row on the 16 non-`Timestamp` columns, from only 97,723 distinct profiles, and no positive mechanism explains why. Which columns, and how strict an agreement across them, define one staged record?

## Findings

Two rows cite evidence already established in [`legacy-audit.md`](../audit/legacy-audit.md) (A4, A13). One row, G1, introduces new evidence generated for this decision: it audits neither the legacy codebase (ADR-0000, `F`) nor the dataset's provenance (ADR-0001, `P`), so it starts its own letter.

| ID | Finding | Evidence | Status |
|----|---------|----------|--------|
| A4 | 194,641 of 292,364 rows are duplicates on the 16 non-`Timestamp` columns; only 97,723 distinct profiles exist across the file. | [`legacy-audit.md`](../audit/legacy-audit.md) | Established |
| A13 | No positive duplication mechanism is established. A complete combinatorial grid and simple batch loading are both ruled out. Duplication is non-uniform: concentrated almost entirely in two countries (United States, United Kingdom), while 17 of 35 countries have no duplicate profiles at all. | [`legacy-audit.md`](../audit/legacy-audit.md) | Established |
| G1 | Deduplicating on the 13 modeled columns (12 non-`Timestamp` plus `Timestamp`) instead of all 17 raw columns collapses 290,051 rows to 259,490 — a further 30,561 rows, distributed across countries in roughly the proportion of the file itself (United States 59.0% of the extra collapse vs. 58.6% of the file; United Kingdom 17.4% vs. 17.6%), unlike A13's country-specific structure. | Computed against the SHA-256-verified extraction used by A1, A4, A8, A12 and A13 (`083f44e9...`) | Established |

## Decision Drivers

* A13 found no positive mechanism behind the duplication, and a structure concentrated in a subset of countries rather than spread evenly — nothing here supports assuming that rows sharing every stored value are the same respondent.
* G1: which columns define "the same row" changes the staging row count by 30,561 (about 10.5% of the file) depending only on which columns this specification currently models, not on anything about the source data. A count that shifts if [`sources.md`](../specification/sources.md) is later amended is unstable for a figure meant to anchor the warehouse's volume.
* [ADR-0007](0007-person-grain-fact-table-and-dimension-grain-rule.md) already fixed the fact grain at one row per staged record, one row per survey response; this decision does not reopen that — it only fixes what counts as one staged record when rows agree on every observable value.
* The source file carries no respondent identifier ([`specification.md`](../specification.md), Open items); any dedup rule is an inference over the columns available, not a verification against a known population.
* A1 already established that the legacy's own 2,313-row exact-duplicate count on all 17 columns matches this project's extraction; that precedent already treats full-column exact duplication as the baseline case for "the same response."

## Considered Options

* Deduplicate on the 13 modeled columns (12 non-`Timestamp` plus `Timestamp`): 259,490 distinct rows. Identity is defined only by what the model stores.
* Deduplicate on all 17 raw columns: 290,051 distinct rows. Identity is defined by everything the source file records, including the four columns this specification does not model.
* Deduplicate on the 16 non-`Timestamp` columns, as A4 and A13 investigated, collapsing further to 97,723 distinct profiles: treats every repeated profile, however far apart in time, as the same respondent.

## Decision Outcome

Chosen option: "Deduplicate on all 17 raw columns", because it keeps the staging row count anchored to the source file's own content rather than to this specification's current modeling scope (G1), and because among the three options it discards the least information when judging whether two rows are the same response — consistent with A13 finding no evidence to justify a more aggressive collapse.

* **Staged record identity.** Two raw rows are the same staged record only if they agree on all 17 source columns, `Timestamp` included. The first occurrence, in source file order, is kept; later exact duplicates are dropped before the four unmodeled columns are discarded.
* **Row count.** 290,051 records reach staging from the 292,364-row source file.
* **Scope.** This decision fixes staging's row count. It does not revisit [ADR-0007](0007-person-grain-fact-table-and-dimension-grain-rule.md)'s fact grain, and it does not claim the 290,051 records are 290,051 distinct people — [ADR-0001](0001-position-as-portfolio-project.md) already forecloses any population claim.

### Consequences

* Good, because the staging row count is unaffected if [`sources.md`](../specification/sources.md) is later amended to model one of the four currently-excluded columns — the count is fixed by the 17-column comparison, independent of what the model stores.
* Good, because it requires no assumption about a duplication mechanism A13 could not establish.
* Bad, because staging must read and compare all 17 raw columns to compute the dedup key, even though four of them are discarded immediately afterward and never reach a dimension or the fact table.
* Bad, because two rows that are genuinely different responses but happen to agree on every stored value, `Timestamp` to the minute included, are still treated as one row — an assumption in the other direction, though A1 shows the legacy project already made the same call for its 2,313 originally-flagged duplicates.
* Constraint: a future amendment to [`sources.md`](../specification/sources.md) that models one of the four currently-excluded columns does not retroactively change the row count fixed by this decision.

### Confirmation

The staging load report states three counts: the raw row count (292,364), the count of rows removed as 17-column exact duplicates, and the count reaching staging (290,051); the three reconcile by construction. Fase 4's acceptance criteria, once specified in `staging.md`, add a check that staging's row count is 290,051 and that every removed row is an exact duplicate on all 17 source columns, nothing narrower.

## Pros and Cons of the Options

### Deduplicate on the 13 modeled columns

* Good, because it never reads or compares a column the model doesn't otherwise use.
* Bad, because the row count depends on this specification's current modeling scope (G1) rather than on the source file alone.
* Bad, because it discards more information than the alternative when judging whether two rows are the same response.

### Deduplicate on all 17 raw columns

* Good, because the row count is a property of the source file, stable under any future change to what `sources.md` models.
* Good, because it uses the most information available to judge whether two rows are the same response.
* Bad, because staging briefly handles four columns the model never stores.

### Deduplicate on the 16 non-`Timestamp` columns (collapse to 97,723 profiles)

* Good, because it collapses the largest share of the duplication A4 found.
* Bad, because A13 found no mechanism to justify treating every repeated profile as the same respondent, and the structure it did find is concentrated in specific countries, not evenly distributed.
* Bad, because it discards `Timestamp`, the one column that could distinguish two genuinely different responses sharing an otherwise identical profile.

## More Information

* Related: [ADR-0007](0007-person-grain-fact-table-and-dimension-grain-rule.md) (fact grain, not reopened here), [ADR-0001](0001-position-as-portfolio-project.md) (no population claim).
* Evidence: [`legacy-audit.md`](../audit/legacy-audit.md) (A4, A13); this ADR's own G1.
* The contract this decision feeds: [`staging.md`](../specification/staging.md).