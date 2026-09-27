-- Surrogate keys are numbered in natural-key order: deterministic across runs,
-- and carrying no meaning (definitions.md#model-conventions).
-- `isolation_levels` is the fixed mapping registered by warehouse.py; a staged
-- level absent from it gets NULLs, which dim_isolation rejects.
INSERT INTO dim_isolation
SELECT
    ROW_NUMBER() OVER (ORDER BY staged.days_indoors),
    staged.days_indoors,
    isolation_levels.sort_order,
    isolation_levels.duration_band
FROM (SELECT DISTINCT days_indoors FROM staging_response) AS staged
LEFT JOIN isolation_levels ON staged.days_indoors = isolation_levels.days_indoors;
