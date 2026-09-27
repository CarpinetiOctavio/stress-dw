-- Indicator 6: Stress/coping-difficulty co-occurrence rate.
-- indicators.md, Q3; pattern B (patterns.md).
-- The single parameter is low_n_threshold.
-- Two grouping sets; region rows are sums over the countries of the region.
SELECT
    CASE
        WHEN GROUPING(dim_country.country) = 0 THEN 'occupation, country'
        ELSE 'occupation, region'
    END AS grouping_set,
    dim_occupation.occupation AS occupation,
    dim_country.country AS country,
    dim_country.region AS region,
    COUNT(*) FILTER (WHERE dim_symptoms.growing_stress = 'Yes' AND dim_symptoms.coping_struggles = 'Yes') AS numerator,
    COUNT(*) AS denominator,
    COUNT(*) FILTER (WHERE dim_symptoms.growing_stress = 'Yes' AND dim_symptoms.coping_struggles = 'Yes')
        / NULLIF(COUNT(*), 0) AS rate,
    COUNT(*) < ? AS low_n
FROM fact_response
    JOIN dim_occupation USING (occupation_id)
    JOIN dim_country USING (country_id)
    JOIN dim_symptoms USING (symptoms_id)
GROUP BY GROUPING SETS (
    (dim_occupation.occupation, dim_country.country),
    (dim_occupation.occupation, dim_country.region)
)
ORDER BY grouping_set, occupation, country, region;
