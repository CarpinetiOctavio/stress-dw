-- Indicator 16: Treatment non-uptake rate under full context.
-- indicators.md, Q7.2; pattern C (patterns.md).
-- The single parameter is low_n_threshold.
-- Uses symptom_cluster: see its validity caveat in definitions.md.
WITH population AS (
    SELECT
        dim_symptoms.growing_stress AS growing_stress,
        (
            dim_symptoms.mood_swings IN ('Medium', 'High')
            AND dim_symptoms.coping_struggles = 'Yes'
            AND dim_isolation.days_indoors
                IN ('15-30 days', '31-60 days', 'More than 2 months')
        ) AS symptom_cluster,
        dim_access.care_options AS care_options,
        dim_access.mental_health_interview AS mental_health_interview,
        fact_response.treatment AS level
    FROM fact_response
    JOIN dim_isolation USING (isolation_id)
    JOIN dim_symptoms USING (symptoms_id)
    JOIN dim_access USING (access_id)
    WHERE (dim_symptoms.growing_stress = 'Yes' OR (
            dim_symptoms.mood_swings IN ('Medium', 'High')
            AND dim_symptoms.coping_struggles = 'Yes'
            AND dim_isolation.days_indoors
                IN ('15-30 days', '31-60 days', 'More than 2 months')
        ))
        AND dim_access.care_options IN ('Yes', 'Not sure')
),
cells AS (
    SELECT growing_stress, symptom_cluster, care_options, mental_health_interview, COUNT(*) AS denominator
    FROM population GROUP BY ALL
),
levels AS (
    SELECT DISTINCT level FROM population
),
counts AS (
    SELECT growing_stress, symptom_cluster, care_options, mental_health_interview, level, COUNT(*) AS numerator
    FROM population
    GROUP BY ALL
)
SELECT
    cells.growing_stress,
    cells.symptom_cluster,
    cells.care_options,
    cells.mental_health_interview,
    levels.level,
    COALESCE(counts.numerator, 0) AS numerator,
    cells.denominator,
    COALESCE(counts.numerator, 0) / NULLIF(cells.denominator, 0) AS rate,
    cells.denominator < ? AS low_n
FROM cells
CROSS JOIN levels
LEFT JOIN counts USING (growing_stress, symptom_cluster, care_options, mental_health_interview, level)
ORDER BY cells.growing_stress, cells.symptom_cluster, cells.care_options, cells.mental_health_interview, levels.level;
