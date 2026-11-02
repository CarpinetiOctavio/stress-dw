# Fan-out

The first of two errors that the audit of the course version found ([ADR-0000](../decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md)).

## What happened

A dimension is a lookup table: each fact row points to one of its rows. The course symptoms dimension stored a flag computed from `Days_Indoors`, a column it did not store, so rows with the same stored values differed only in the flag, and every response matched more than one of them and was counted once per match ([legacy audit, A2](../audit/legacy-audit.md#checks)).

![Top: the legacy Dim_Sintomas stores four symptom columns and a flag that depends on Days_Indoors, which it does not store, so two rows share the same four values with different flags, and one response matches both rows and the join counts it twice. Bottom: the rebuild stores the four columns in dim_symptoms and Days_Indoors in dim_isolation, one response matches one row in each, and the two conditions are computed at query time. Illustrative rows.](../specification/figures/dimension-fan-out.svg)

*The legacy dimension's flag depended on a column it did not store, so records matched more than one row; the rebuild stores only what its key determines.*

## How the rebuild prevents it

Every column a dimension stores depends only on that dimension's key ([dimension grain rule](../specification/definitions.md#dimension-grain-rule)). The flag is split into two conditions computed at query time, [`explicit_recognition`](../specification/definitions.md#explicit_recognition) and [`symptom_cluster`](../specification/definitions.md#symptom_cluster), so no dimension stores a value that depends on another dimension's column ([ADR-0007](../decisions/0007-person-grain-fact-table-and-dimension-grain-rule.md)).

## How it is tested

Check C1 confirms that each dimension holds one row per natural key, and C2 that joining staging to the dimensions multiplies no row ([`acceptance.md`](../specification/acceptance.md)); the test suite runs them when the source file is present ([Phase 4 closure, section 4](../audit/phase4-closure.md#4-acceptance-checks-c1c11)).
