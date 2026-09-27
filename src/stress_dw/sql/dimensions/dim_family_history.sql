-- Surrogate keys are numbered in natural-key order: deterministic across runs,
-- and carrying no meaning (definitions.md#model-conventions).
INSERT INTO dim_family_history
SELECT ROW_NUMBER() OVER (ORDER BY family_history), family_history
FROM (SELECT DISTINCT family_history FROM staging_response);
