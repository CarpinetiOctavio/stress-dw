-- Indicator 10: Elevated mood-swings rate by isolation.
-- indicators.md, Q5; pattern A (patterns.md).
-- The single parameter is low_n_threshold.
WITH population AS (
    SELECT
        dim_isolation.days_indoors AS days_indoors,
        dim_isolation.sort_order AS sort_order,
        dim_symptoms.mood_swings AS level
    FROM fact_response
    JOIN dim_isolation USING (isolation_id)
    JOIN dim_symptoms USING (symptoms_id)
),
cells AS (
    SELECT days_indoors, sort_order, COUNT(*) AS denominator,
        COUNT(*) FILTER (WHERE level IN ('Medium', 'High')) / COUNT(*) AS headline_rate
    FROM population GROUP BY ALL
),
levels AS (
    SELECT DISTINCT level FROM population
),
counts AS (
    SELECT days_indoors, sort_order, level, COUNT(*) AS numerator
    FROM population
    GROUP BY ALL
)
SELECT
    cells.days_indoors,
    levels.level,
    COALESCE(counts.numerator, 0) AS numerator,
    cells.denominator,
    COALESCE(counts.numerator, 0) / NULLIF(cells.denominator, 0) AS rate,
    cells.denominator < ? AS low_n,
    cells.headline_rate
FROM cells
CROSS JOIN levels
LEFT JOIN counts USING (days_indoors, sort_order, level)
ORDER BY cells.sort_order, levels.level;
