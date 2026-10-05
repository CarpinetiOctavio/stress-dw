-- Indicator 12: Care-options response rate.
-- indicators.md, Q6; pattern A (patterns.md).
-- The single parameter is low_n_threshold.
WITH population AS (
    SELECT
        dim_symptoms.growing_stress AS growing_stress,
        dim_country.country AS country,
        dim_occupation.occupation AS occupation,
        dim_gender.gender AS gender,
        dim_access.care_options AS level
    FROM fact_response
    JOIN dim_gender USING (gender_id)
    JOIN dim_occupation USING (occupation_id)
    JOIN dim_country USING (country_id)
    JOIN dim_symptoms USING (symptoms_id)
    JOIN dim_access USING (access_id)
),
cells AS (
    SELECT growing_stress, country, occupation, gender, COUNT(*) AS denominator
    FROM population GROUP BY ALL
),
levels AS (
    SELECT DISTINCT level FROM population
),
counts AS (
    SELECT growing_stress, country, occupation, gender, level, COUNT(*) AS numerator
    FROM population
    GROUP BY ALL
)
SELECT
    cells.growing_stress,
    cells.country,
    cells.occupation,
    cells.gender,
    levels.level,
    COALESCE(counts.numerator, 0) AS numerator,
    cells.denominator,
    COALESCE(counts.numerator, 0) / NULLIF(cells.denominator, 0) AS rate,
    cells.denominator < ? AS low_n
FROM cells
CROSS JOIN levels
LEFT JOIN counts USING (growing_stress, country, occupation, gender, level)
ORDER BY cells.growing_stress, cells.country, cells.occupation, cells.gender, levels.level;
