# Legacy audit

Evidence behind [ADR-0000](decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md) and [ADR-0001](decisions/0001-position-as-portfolio-project.md). Each check records its method and result. Nothing here modifies the legacy repository; all checks are read-only.

## Checks

| ID | Check | Method | Result |
|----|-------|--------|--------|
| A1 | The legacy input is the Kaggle file (P9) | Compare SHA-256 of the legacy raw file and a fresh download | Pending |
| A2 | Fan-out in `Dim_Sintomas` (F1) | Group the four stored source columns and count groups with more than one row; count staged records matching more than one dimension row; compare grain groups with 350,699 fact rows; confirm the resulting distinct-group count against the report's stated ~259 combinations (Script 3 output), and confirm `Dim_Acceso`'s combinations against its stated 9 as the fan-out-free control | Pending |
| A3 | Actual foreign-key name for occupation (F4) | Read the fact-table DDL | Pending |
| A4 | Duplicates ignoring `Timestamp` (H2) | Count duplicate rows on the 16 non-timestamp columns; unique-profile counts | Pending |
| A5 | Association between column groups (H1) | Cramér's V between the described columns and the symptom columns; and within each group | Pending |
| A6 | Timestamp distribution against OSMI 2014 (H1) | Compare with the OSMI 2014 data | Pending |
| A7 | Weighted treatment rate by gender (F2) | Compute from staging with explicit numerator and denominator; compare with the unweighted `AVG` used by the Looker Studio chart | Pending |
| A8 | `Dim_Tiempo` / `Dim_Pais` coverage (F4) | Group staging by year-month and by country; compare the distinct counts against `Dim_Tiempo` (13 rows loaded) and `Dim_Pais` (35 rows loaded); compare against the calendar range implied by `Timestamp` (19 months, Aug 2014–Feb 2016) and the 36 countries documented as expected | Pending |
| A9 | `indicador_inferido_estres` implementation vs. documented formula | Read the derivation logic in the script that populates `Dim_Sintomas`; compare its boolean structure against the Fase 2 formula (`Growing_Stress = 'Yes' OR (Mood_Swings IN ('Medium','High') AND Coping_Struggles = 'Yes' AND Days_Indoors IN ('15-30 days','31-60 days','More than 2 months'))`); recompute the flag for a sample of staged rows and diff against the loaded value | Pending |
| A10 | Symptom-column match against RHMCD-20 (H3) | Compare marginal distributions of the eight shared symptom columns (`Days_Indoors`, `Growing_Stress`, `Changes_Habits`, `Mental_Health_History`, `Mood_Swings`, `Coping_Struggles`, `Work_Interest`, `Social_Weakness`) against RHMCD-20 (Mendeley, DOI 10.17632/pxjmjyfdh2.1); test for exact or near-exact row-level matches on those columns | Pending |

## Already established

* The legacy ETL cleaned 292,364 records to 290,051 by removing 2,313 exact duplicates across all 17 columns, including `Timestamp` (ETL log and `01_limpiar_datos.py` at tag `legacy-original`).
* Two staging loads of 290,051 records occurred on 9 November 2025 (13:10 and 22:01); the count was unchanged after the second load. The fact table loaded 350,699 aggregated records the same day at 22:07. The repository's two commits are both dated 13 November 2025 (UTC-3) (ETL log at tag `legacy-original`; [ADR-0000](decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md)).