-- NOT NULL rationale: see schema.py module docstring
CREATE TABLE staging_response (
    response_id INT PRIMARY KEY,
    response_timestamp DATETIME NOT NULL,
    gender VARCHAR(10) NOT NULL,
    country VARCHAR(50) NOT NULL,
    occupation VARCHAR(20) NOT NULL,
    family_history VARCHAR(3) NOT NULL,
    treatment VARCHAR(3) NOT NULL,
    days_indoors VARCHAR(25) NOT NULL,
    growing_stress VARCHAR(5) NOT NULL,
    mood_swings VARCHAR(10) NOT NULL,
    coping_struggles VARCHAR(3) NOT NULL,
    social_weakness VARCHAR(5) NOT NULL,
    mental_health_interview VARCHAR(5) NOT NULL,
    care_options VARCHAR(10) NOT NULL
);
