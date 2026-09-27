-- Reads `staged_frame`, the cleaned, validated, deduplicated extraction that
-- staging.py registers; the single parameter is the `Timestamp` format.
INSERT INTO staging_response
SELECT
    response_id,
    strptime(response_timestamp, ?),
    gender,
    country,
    occupation,
    family_history,
    treatment,
    days_indoors,
    growing_stress,
    mood_swings,
    coping_struggles,
    social_weakness,
    mental_health_interview,
    care_options
FROM staged_frame
ORDER BY response_id;
