-- Indicator 14: Lifetime treatment-seeking rate by explicit-recognition level, within the convergent-symptom population.
-- indicators.md, Q7; pattern C (patterns.md).
-- The single parameter is low_n_threshold.
-- Uses symptom_cluster: see its validity caveat in definitions.md.
WITH population AS (
    SELECT
        dim_symptoms.growing_stress AS growing_stress,
        fact_response.treatment AS level
    FROM fact_response
    JOIN dim_isolation USING (isolation_id)
    JOIN dim_symptoms USING (symptoms_id)
    WHERE (
            dim_symptoms.mood_swings IN ('Medium', 'High')
            AND dim_symptoms.coping_struggles = 'Yes'
            AND dim_isolation.days_indoors
                IN ('15-30 days', '31-60 days', 'More than 2 months')
        )
),
cells AS (
    SELECT growing_stress, COUNT(*) AS denominator
    FROM population GROUP BY ALL
),
levels AS (
    SELECT DISTINCT level FROM population
),
counts AS (
    SELECT growing_stress, level, COUNT(*) AS numerator
    FROM population
    GROUP BY ALL
)
SELECT
    cells.growing_stress,
    levels.level,
    COALESCE(counts.numerator, 0) AS numerator,
    cells.denominator,
    COALESCE(counts.numerator, 0) / NULLIF(cells.denominator, 0) AS rate,
    cells.denominator < ? AS low_n
FROM cells
CROSS JOIN levels
LEFT JOIN counts USING (growing_stress, level)
ORDER BY cells.growing_stress, levels.level;
