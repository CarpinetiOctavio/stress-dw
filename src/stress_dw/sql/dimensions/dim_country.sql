-- Surrogate keys are numbered in natural-key order: deterministic across runs,
-- and carrying no meaning (definitions.md#model-conventions).
-- `country_region` is the fixed mapping registered by warehouse.py; a staged
-- country absent from it gets a NULL region, which dim_country rejects.
INSERT INTO dim_country
SELECT ROW_NUMBER() OVER (ORDER BY staged.country), staged.country, country_region.region
FROM (SELECT DISTINCT country FROM staging_response) AS staged
LEFT JOIN country_region ON staged.country = country_region.country;
