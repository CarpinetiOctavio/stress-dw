-- Indicator 2: Stress-recognition rate.
-- indicators.md, Q1; pattern A (patterns.md).
-- The single parameter is low_n_threshold.
WITH population AS (
    SELECT
        dim_time.period AS period,
        dim_gender.gender AS gender,
        dim_symptoms.growing_stress AS level
    FROM fact_response
    JOIN dim_time USING (time_id)
    JOIN dim_gender USING (gender_id)
    JOIN dim_symptoms USING (symptoms_id)
),
cells AS (
    SELECT period, gender, COUNT(*) AS denominator
    FROM population GROUP BY ALL
),
levels AS (
    SELECT DISTINCT level FROM population
),
counts AS (
    SELECT period, gender, level, COUNT(*) AS numerator
    FROM population
    GROUP BY ALL
)
SELECT
    cells.period,
    cells.gender,
    levels.level,
    COALESCE(counts.numerator, 0) AS numerator,
    cells.denominator,
    COALESCE(counts.numerator, 0) / NULLIF(cells.denominator, 0) AS rate,
    cells.denominator < ? AS low_n
FROM cells
CROSS JOIN levels
LEFT JOIN counts USING (period, gender, level)
ORDER BY cells.period, cells.gender, levels.level;
