# Concept transfers

The formal documents state how this repository works. A concept transfer explains why, by a concept from another field that a reader without the domain can picture, demonstrated on the repository's own artifacts ([ADR-0014](../decisions/0014-explain-the-method-through-declared-concept-transfers.md)). Each document fits on one page and has three parts:

1. **The concept**, introduced with a figure, for a reader outside the domain.
2. **The transfer**: where the concept applies here, each claim linked to the versioned section that holds it.
3. **Where it breaks**: the limit of the analogy.

The figures use illustrative data only; none shows an indicator value.

| Transfer | Concept | Applied to | Result |
|----------|---------|------------|--------|
| [Pre-registration](preregistration-and-data-leakage.md) | The target painted before the shots; data leakage | The criteria committed before the indicator output is exposed | Values of the same quantities already in the repository before that commit are listed and declared, so the commit did not precede every value ([evidence, section 3](../audit/correspondence-evidence.md#3-post-commit-exposures)) |
| [Overfitting](overfitting.md) | Two points, four functions; early stopping | One principle instead of a patch per gap; the stopping rule | A stopping rule set in advance ended the process ([LOG-051](../decisions/log/LOG-051-stopping-rule-documentary-audit-readings.md)) |
| [Parsimony](parsimony.md) | The fewest parameters that explain the data | The same principle in METIS, in a rule, a layer and the method | The documentary verdict was removed ([LOG-051](../decisions/log/LOG-051-stopping-rule-documentary-audit-readings.md); [LSN-014 and LSN-015](../audit/lessons/scope-and-proportion.md)) |
| [Boundary cases](boundary-cases.md) | The ticket-office sign read two ways | The two-reader test of the criteria | In the final round, both readers gave the key's verdict on every case; the agreement shows one reading for readers of that family, not for every reader, and key content on which questions differ by reading branch reached the party that drafts fixes before the text was frozen ([criteria, section 0](../audit/correspondence-criteria.md#0-scope)) |
| [Grain](grain-and-cross-sections.md) | Repeated cross-sections against a panel | What one row of the fact table stands for | The grain renamed to response grain ([ADR-0007, addendum of 2026-10-04](../decisions/0007-person-grain-fact-table-and-dimension-grain-rule.md#addendum-2026-10-04)); the first question reworded from how a share "evolves" to how it differs across months ([ADR-0004](../decisions/0004-revise-business-questions.md)) |
| [Proxy](proxy-and-construct-validity.md) | Feeling hot read as fever | `explicit_recognition` read from `growing_stress` | The premise is stated where the condition is defined ([LOG-012](../decisions/log/LOG-012-explicit-recognition-premise.md)); no verdict states validity ([criteria, section 0](../audit/correspondence-criteria.md#0-scope)) |
| [Sets and multisets](sets-and-multisets.md) | Two guests with one name | Deduplication on all 17 source columns | Deduplicating on the 13 modeled columns would merge rows the source keeps apart ([ADR-0008, Findings, G1](../decisions/0008-staging-deduplication-grain.md#findings)); every dropped row is an exact duplicate, checked by C11 |
