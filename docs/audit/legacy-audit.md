# Legacy audit

Evidence behind [ADR-0000](decisions/0000-rebuild-from-scratch-instead-of-continuing-legacy.md) and [ADR-0001](decisions/0001-position-as-portfolio-project.md). Each check records its method and result. Nothing here modifies the legacy repository; all checks are read-only.

## Checks

| ID | Check | Method | Result |
|----|-------|--------|--------|
| A1 | The legacy input is the Kaggle file | Compare SHA-256 of the legacy raw file and a fresh download | Pending |
| A2 | Fan-out in `Dim_Sintomas` (F1) | Group the four stored source columns and count groups with more than one row; count staged records matching more than one dimension row; compare grain groups with 350,699 fact rows | Pending |
| A3 | Actual foreign-key name for occupation (F4) | Read the fact-table DDL | Pending |
| A4 | Duplicates ignoring `Timestamp` (H2) | Count duplicate rows on the 16 non-timestamp columns; unique-profile counts | Pending |
| A5 | Association between column groups (H1) | Cramér's V between the described columns and the symptom columns; and within each group | Pending |
| A6 | Timestamp distribution against OSMI 2014 (H1) | Compare with the OSMI 2014 data | Pending |
| A7 | Weighted treatment rate by gender (F2) | Compute from staging with explicit numerator and denominator; compare with the unweighted `AVG` used by the Looker Studio chart | Pending |

## Already established

* The legacy ETL cleaned 292,364 records to 290,051 by removing 2,313 exact duplicates across all 17 columns, including `Timestamp` (ETL log and `01_limpiar_datos.py` at tag `legacy-original`).