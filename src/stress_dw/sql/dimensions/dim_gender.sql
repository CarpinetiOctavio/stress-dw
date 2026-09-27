-- Surrogate keys are numbered in natural-key order: deterministic across runs,
-- and carrying no meaning (definitions.md#model-conventions).
INSERT INTO dim_gender
SELECT ROW_NUMBER() OVER (ORDER BY gender), gender
FROM (SELECT DISTINCT gender FROM staging_response);
