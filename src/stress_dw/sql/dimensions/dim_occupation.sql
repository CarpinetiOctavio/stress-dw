-- Surrogate keys are numbered in natural-key order: deterministic across runs,
-- and carrying no meaning (definitions.md#model-conventions).
INSERT INTO dim_occupation
SELECT ROW_NUMBER() OVER (ORDER BY occupation), occupation
FROM (SELECT DISTINCT occupation FROM staging_response);
