# Concept transfers

The formal documents state how this repository works. A concept transfer explains why, by a concept from another field that a reader without the domain can picture, demonstrated on the repository's own artifacts ([ADR-0014](../decisions/0014-explain-the-method-through-declared-concept-transfers.md)). Each document fits on one page and has three parts:

1. **The concept**, introduced with a figure, for a reader outside the domain.
2. **The transfer**: where the concept applies here, each claim linked to the versioned section that holds it.
3. **Where it breaks**: the limit of the analogy.

The figures use illustrative data only; none shows an indicator value.

| Transfer | Concept | Applied to |
|----------|---------|------------|
| [Pre-registration](preregistration-and-data-leakage.md) | The target painted before the shots; data leakage | The criteria committed before any indicator value is exposed |
| [Overfitting](overfitting.md) | Two points, four functions; early stopping | One principle instead of a patch per gap; the stopping rule |
| [Parsimony](parsimony.md) | The fewest parameters that explain the data | The same principle in METIS, in a rule, a layer and the method |
| [Boundary cases](boundary-cases.md) | The ticket-office sign read two ways | The two-reader test of the criteria |
| [Grain](grain-and-cross-sections.md) | Repeated cross-sections against a panel | What one row of the fact table stands for |
| [Proxy](proxy-and-construct-validity.md) | Feeling hot read as fever | `explicit_recognition` read from `growing_stress` |
| [Sets and multisets](sets-and-multisets.md) | Two guests with one name | Deduplication on all 17 source columns |
