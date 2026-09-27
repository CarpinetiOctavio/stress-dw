-- Indicator 8: Lifetime treatment-seeking (count).
-- indicators.md, Q4; pattern C (patterns.md).
-- The single parameter is low_n_threshold.
WITH population AS (
    SELECT
        dim_gender.gender AS gender,
        dim_symptoms.growing_stress AS growing_stress,
        fact_response.treatment AS level
    FROM fact_response
    JOIN dim_gender USING (gender_id)
    JOIN dim_symptoms USING (symptoms_id)
),
cells AS (
    SELECT gender, growing_stress, COUNT(*) AS denominator
    FROM population GROUP BY ALL
),
levels AS (
    SELECT DISTINCT level FROM population
),
counts AS (
    SELECT gender, growing_stress, level, COUNT(*) AS numerator
    FROM population
    GROUP BY ALL
)
SELECT
    cells.gender,
    cells.growing_stress,
    levels.level,
    COALESCE(counts.numerator, 0) AS numerator,
    cells.denominator,
    COALESCE(counts.numerator, 0) / NULLIF(cells.denominator, 0) AS rate,
    cells.denominator < ? AS low_n
FROM cells
CROSS JOIN levels
LEFT JOIN counts USING (gender, growing_stress, level)
WHERE levels.level = 'Yes'
ORDER BY cells.gender, cells.growing_stress, levels.level;
