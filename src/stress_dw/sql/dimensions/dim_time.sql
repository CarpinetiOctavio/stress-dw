-- Surrogate keys are numbered in natural-key order: deterministic across runs,
-- and carrying no meaning (definitions.md#model-conventions).
INSERT INTO dim_time
SELECT
    ROW_NUMBER() OVER (ORDER BY year, month),
    year,
    month,
    strftime(make_date(year, month, 1), '%B'),
    printf('%04d-%02d', year, month),
    ((month - 1) // 3) + 1,
    CASE WHEN month <= 6 THEN 1 ELSE 2 END
FROM (
    SELECT DISTINCT
        CAST(year(response_timestamp) AS INT) AS year,
        CAST(month(response_timestamp) AS INT) AS month
    FROM staging_response
);
