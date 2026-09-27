-- Surrogate keys are numbered in natural-key order: deterministic across runs,
-- and carrying no meaning (definitions.md#model-conventions).
INSERT INTO dim_symptoms
SELECT
    ROW_NUMBER() OVER (
        ORDER BY growing_stress, mood_swings, coping_struggles, social_weakness
    ),
    growing_stress,
    mood_swings,
    coping_struggles,
    social_weakness
FROM (
    SELECT DISTINCT growing_stress, mood_swings, coping_struggles, social_weakness
    FROM staging_response
);
