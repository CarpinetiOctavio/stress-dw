-- Surrogate keys are numbered in natural-key order: deterministic across runs,
-- and carrying no meaning (definitions.md#model-conventions).
INSERT INTO dim_access
SELECT
    ROW_NUMBER() OVER (ORDER BY care_options, mental_health_interview),
    care_options,
    mental_health_interview
FROM (
    SELECT DISTINCT care_options, mental_health_interview
    FROM staging_response
);
