-- NOT NULL rationale: see schema.py module docstring
CREATE TABLE dim_symptoms (
    symptoms_id INT PRIMARY KEY,
    growing_stress VARCHAR(5) NOT NULL,
    mood_swings VARCHAR(10) NOT NULL,
    coping_struggles VARCHAR(3) NOT NULL,
    social_weakness VARCHAR(5) NOT NULL,
    UNIQUE (growing_stress, mood_swings, coping_struggles, social_weakness)
);
