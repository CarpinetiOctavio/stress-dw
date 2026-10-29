-- Check A2 (F1), minimal form, over the rebuilt staging_response: the four
-- columns the legacy Dim_Sintomas stores, and the fifth, days_indoors, that its
-- load selects DISTINCT over without storing (legacy-original,
-- python/03_cargar_dimensiones.py:269-282).
WITH groups AS (
    SELECT
        growing_stress,
        mood_swings,
        coping_struggles,
        social_weakness,
        COUNT(DISTINCT days_indoors) AS days_indoors_values,
        COUNT(*) AS staged_records
    FROM staging_response
    GROUP BY growing_stress, mood_swings, coping_struggles, social_weakness
)
SELECT
    COUNT(*) AS four_column_groups,
    COUNT(*) FILTER (WHERE days_indoors_values > 1) AS groups_with_more_than_one_days_indoors,
    SUM(staged_records) FILTER (WHERE days_indoors_values > 1) AS staged_records_in_those_groups,
    SUM(days_indoors_values) AS five_column_combinations
FROM groups;
