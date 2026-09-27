-- Indicator 1: Stress-recognition (count).
-- indicators.md, Q1; pattern A (patterns.md).
-- The single parameter is low_n_threshold.
WITH population AS (
    SELECT
        dim_symptoms.growing_stress AS level
    FROM fact_response
    JOIN dim_symptoms USING (symptoms_id)
),
cells AS (
    SELECT COUNT(*) AS denominator
    FROM population
),
levels AS (
    SELECT DISTINCT level FROM population
),
counts AS (
    SELECT level, COUNT(*) AS numerator
    FROM population
    GROUP BY ALL
)
SELECT
    levels.level,
    COALESCE(counts.numerator, 0) AS numerator,
    cells.denominator,
    COALESCE(counts.numerator, 0) / NULLIF(cells.denominator, 0) AS rate,
    cells.denominator < ? AS low_n
FROM cells
CROSS JOIN levels
LEFT JOIN counts USING (level)
ORDER BY levels.level;
