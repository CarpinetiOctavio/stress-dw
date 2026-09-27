-- Indicator 4: Family-history/stress coexistence rate.
-- indicators.md, Q2; pattern A (patterns.md).
-- The single parameter is low_n_threshold.
WITH population AS (
    SELECT
        dim_gender.gender AS gender,
        dim_time.period AS period,
        dim_symptoms.growing_stress AS level
    FROM fact_response
    JOIN dim_time USING (time_id)
    JOIN dim_gender USING (gender_id)
    JOIN dim_family_history USING (family_history_id)
    JOIN dim_symptoms USING (symptoms_id)
    WHERE dim_family_history.family_history = 'Yes'
),
cells AS (
    SELECT gender, period, COUNT(*) AS denominator
    FROM population GROUP BY ALL
),
levels AS (
    SELECT DISTINCT level FROM population
),
counts AS (
    SELECT gender, period, level, COUNT(*) AS numerator
    FROM population
    GROUP BY ALL
)
SELECT
    cells.gender,
    cells.period,
    levels.level,
    COALESCE(counts.numerator, 0) AS numerator,
    cells.denominator,
    COALESCE(counts.numerator, 0) / NULLIF(cells.denominator, 0) AS rate,
    cells.denominator < ? AS low_n
FROM cells
CROSS JOIN levels
LEFT JOIN counts USING (gender, period, level)
ORDER BY cells.gender, cells.period, levels.level;
