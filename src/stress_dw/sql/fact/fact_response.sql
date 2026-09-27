-- LEFT JOIN, not INNER: a staged record whose natural key has no dimension row
-- gets a NULL foreign key, which fact_response's NOT NULL rejects, aborting the
-- load (invariant I3) instead of dropping the record silently.
INSERT INTO fact_response
SELECT
    staging_response.response_id,
    dim_time.time_id,
    dim_gender.gender_id,
    dim_family_history.family_history_id,
    dim_occupation.occupation_id,
    dim_country.country_id,
    dim_isolation.isolation_id,
    dim_access.access_id,
    dim_symptoms.symptoms_id,
    staging_response.treatment
FROM staging_response
LEFT JOIN dim_time
    ON dim_time.year = year(staging_response.response_timestamp)
    AND dim_time.month = month(staging_response.response_timestamp)
LEFT JOIN dim_gender
    ON dim_gender.gender = staging_response.gender
LEFT JOIN dim_family_history
    ON dim_family_history.family_history = staging_response.family_history
LEFT JOIN dim_occupation
    ON dim_occupation.occupation = staging_response.occupation
LEFT JOIN dim_country
    ON dim_country.country = staging_response.country
LEFT JOIN dim_isolation
    ON dim_isolation.days_indoors = staging_response.days_indoors
LEFT JOIN dim_access
    ON dim_access.care_options = staging_response.care_options
    AND dim_access.mental_health_interview = staging_response.mental_health_interview
LEFT JOIN dim_symptoms
    ON dim_symptoms.growing_stress = staging_response.growing_stress
    AND dim_symptoms.mood_swings = staging_response.mood_swings
    AND dim_symptoms.coping_struggles = staging_response.coping_struggles
    AND dim_symptoms.social_weakness = staging_response.social_weakness
ORDER BY staging_response.response_id;
