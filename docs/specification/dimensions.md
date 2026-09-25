# Dimensions

Eight dimensions. Each one obeys the [dimension grain rule](definitions.md#dimension-grain-rule), and its identifiers and stored values follow the [model conventions](definitions.md#model-conventions).

## Row set

A dimension holds one row per distinct natural key present in staging. Every staged record resolves to exactly one row in each of the eight dimensions.

| Dimension | Natural key | Rows (ceiling) |
|-----------|-------------|----------------|
| `dim_time` | (`year`, `month`) | 13 in the audited source file, confirmed by check A8 — not a fixed ceiling like the other rows, since `dim_time`'s natural key has no bounded domain and a later load can add more |
| `dim_gender` | `gender` | 2 |
| `dim_family_history` | `family_history` | 2 |
| `dim_occupation` | `occupation` | 5 |
| `dim_country` | `country` | 35, confirmed by check A8 |
| `dim_isolation` | `days_indoors` | 5 |
| `dim_access` | (`care_options`, `mental_health_interview`) | 9 |
| `dim_symptoms` | (`growing_stress`, `mood_swings`, `coping_struggles`, `social_weakness`) | 54 |

Ceilings are the product of the domain sizes in [`sources.md`](sources.md#value-domains), not expected counts.

## `dim_time`

| Column | Type | Role | Rule |
|--------|------|------|------|
| `time_id` | INT | primary key | surrogate |
| `year` | INT | natural key | year of `Timestamp` |
| `month` | INT | natural key | month of `Timestamp`, 1–12 |
| `month_name` | VARCHAR(9) | derived | English month name |
| `period` | CHAR(7) | derived | `YYYY-MM`, month zero-padded |
| `quarter` | INT | derived | `((month - 1) DIV 3) + 1` |
| `semester` | INT | derived | 1 if `month` ≤ 6, otherwise 2 |

Unique on (`year`, `month`). Months absent from staging have no row; the calendar months between the earliest and the latest staged month that hold no row are listed in the load report (informational, not a failure).

## `dim_gender`, `dim_family_history`, `dim_occupation`

| Table | Columns | Type |
|-------|---------|------|
| `dim_gender` | `gender_id` (primary key, INT); `gender` (natural key, unique) | VARCHAR(10) |
| `dim_family_history` | `family_history_id` (primary key, INT); `family_history` (natural key, unique) | VARCHAR(3) |
| `dim_occupation` | `occupation_id` (primary key, INT); `occupation` (natural key, unique) | VARCHAR(20) |

These dimensions store no column besides the key.

## `dim_country`

| Column | Type | Role | Rule |
|--------|------|------|------|
| `country_id` | INT | primary key | surrogate |
| `country` | VARCHAR(50) | natural key | unique |
| `region` | VARCHAR(40) | derived | the [country-to-region mapping](country-region-mapping.md) |

## `dim_isolation`

| Column | Type | Role | Rule |
|--------|------|------|------|
| `isolation_id` | INT | primary key | surrogate |
| `days_indoors` | VARCHAR(25) | natural key | unique |
| `sort_order` | INT | derived | fixed mapping below |
| `duration_band` | VARCHAR(6) | derived | fixed mapping below |

| `days_indoors` | `sort_order` | `duration_band` |
|----------------|--------------|-----------------|
| `Go out Every day` | 1 | `Low` |
| `1-14 days` | 2 | `Low` |
| `15-30 days` | 3 | `Medium` |
| `31-60 days` | 4 | `High` |
| `More than 2 months` | 5 | `High` |

`duration_band` is a declared grouping of the five levels with no external validation. No indicator is defined on it: isolation [cuts](definitions.md#query-vocabulary) use `days_indoors`, ordered by `sort_order`, and [`symptom_cluster`](definitions.md#symptom_cluster) is defined on `days_indoors` literals, not on `duration_band`.

## `dim_access`

| Column | Type | Role | Rule |
|--------|------|------|------|
| `access_id` | INT | primary key | surrogate |
| `care_options` | VARCHAR(10) | natural key, part 1 | |
| `mental_health_interview` | VARCHAR(5) | natural key, part 2 | |

Unique on (`care_options`, `mental_health_interview`). The dimension does not store `treatment`; `treatment` is a measure of the [fact table](fact-table.md).

## `dim_symptoms`

| Column | Type | Role | Rule |
|--------|------|------|------|
| `symptoms_id` | INT | primary key | surrogate |
| `growing_stress` | VARCHAR(5) | natural key, part 1 | |
| `mood_swings` | VARCHAR(10) | natural key, part 2 | |
| `coping_struggles` | VARCHAR(3) | natural key, part 3 | |
| `social_weakness` | VARCHAR(5) | natural key, part 4 | |

Unique on the four natural-key columns. The dimension stores no derived column, and `days_indoors` is not stored here: it lives only in `dim_isolation`.
