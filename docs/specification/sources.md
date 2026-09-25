# Source columns and value domains

The source file has 17 columns. Thirteen are modeled; four are not. [`dataset-provenance.md`](../dataset-provenance.md) records what the source does and does not document about them. *Natural key* is used as defined in the [dimension grain rule](definitions.md#dimension-grain-rule).

## Column map

| # | Source column | Destination | Role |
|---|---------------|-------------|------|
| 1 | `Timestamp` | [`dim_time`](dimensions.md#dim_time) | natural key, as (year, month) |
| 2 | `Gender` | [`dim_gender`](dimensions.md#dim_gender-dim_family_history-dim_occupation) | natural key |
| 3 | `Country` | [`dim_country`](dimensions.md#dim_country) | natural key |
| 4 | `Occupation` | [`dim_occupation`](dimensions.md#dim_gender-dim_family_history-dim_occupation) | natural key |
| 5 | `self_employed` | — | not modeled |
| 6 | `family_history` | [`dim_family_history`](dimensions.md#dim_gender-dim_family_history-dim_occupation) | natural key |
| 7 | `treatment` | [`fact_response.treatment`](fact-table.md#columns) | measure |
| 8 | `Days_Indoors` | [`dim_isolation`](dimensions.md#dim_isolation) | natural key |
| 9 | `Growing_Stress` | [`dim_symptoms`](dimensions.md#dim_symptoms) | part of natural key |
| 10 | `Changes_Habits` | — | not modeled |
| 11 | `Mental_Health_History` | — | not modeled |
| 12 | `Mood_Swings` | [`dim_symptoms`](dimensions.md#dim_symptoms) | part of natural key |
| 13 | `Coping_Struggles` | [`dim_symptoms`](dimensions.md#dim_symptoms) | part of natural key |
| 14 | `Work_Interest` | — | not modeled |
| 15 | `Social_Weakness` | [`dim_symptoms`](dimensions.md#dim_symptoms) | part of natural key |
| 16 | `mental_health_interview` | [`dim_access`](dimensions.md#dim_access) | part of natural key |
| 17 | `care_options` | [`dim_access`](dimensions.md#dim_access) | part of natural key |

Modeling one of the four excluded columns is an amendment to this specification.

## Value domains

Domains as documented in the legacy report (correspondence and granularity tables), confirmed against the raw file by check A12 of the [legacy audit](../audit/legacy-audit.md): every value in every modeled column matches what is listed below exactly, with no case or whitespace variants and no NULL, empty, or whitespace-only values found.

| Column | Documented domain |
|--------|-------------------|
| `Gender` | `Male`, `Female` |
| `Country` | the 35 countries of the [country-to-region mapping](country-region-mapping.md), confirmed against the raw file by check A8; the legacy report's "36" was inaccurate |
| `Occupation` | `Business`, `Corporate`, `Housewife`, `Others`, `Student` |
| `family_history` | `Yes`, `No` |
| `treatment` | `Yes`, `No` |
| `Days_Indoors` | `Go out Every day`, `1-14 days`, `15-30 days`, `31-60 days`, `More than 2 months` |
| `Growing_Stress` | `Yes`, `No`, `Maybe` |
| `Mood_Swings` | `Low`, `Medium`, `High` |
| `Coping_Struggles` | `Yes`, `No` |
| `Social_Weakness` | `Yes`, `No`, `Maybe` |
| `mental_health_interview` | `Yes`, `No`, `Maybe` |
| `care_options` | `Yes`, `No`, `Not sure` |
| `Timestamp` | parsed to (year, month); range per the Data Card: 2014-08-27 to 2016-02-01; format confirmed as `%m/%d/%Y %H:%M` by check A12, 0 unparsable values |

The legacy report writes `1-14 days` in one place and `1 - 14 days` (spaces around the hyphen) in an example table. The unspaced form is used throughout this specification.

## Load rule

A NULL, or a value outside its documented domain, in any modeled column aborts the load. No row is dropped, defaulted, or recoded to fit. The rule sustains [invariant I1](fact-table.md#invariants). It belongs to the data-integration phase, "Fase 4" (English: "Phase 4"; see [`methodology.md`](../methodology.md)), which is not yet specified for this rebuild; it moves there when that phase is specified.
