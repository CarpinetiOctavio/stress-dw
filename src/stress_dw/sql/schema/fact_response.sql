-- NOT NULL rationale: see schema.py module docstring
CREATE TABLE fact_response (
    response_id INT PRIMARY KEY,
    time_id INT NOT NULL REFERENCES dim_time (time_id),
    gender_id INT NOT NULL REFERENCES dim_gender (gender_id),
    family_history_id INT NOT NULL REFERENCES dim_family_history (family_history_id),
    occupation_id INT NOT NULL REFERENCES dim_occupation (occupation_id),
    country_id INT NOT NULL REFERENCES dim_country (country_id),
    isolation_id INT NOT NULL REFERENCES dim_isolation (isolation_id),
    access_id INT NOT NULL REFERENCES dim_access (access_id),
    symptoms_id INT NOT NULL REFERENCES dim_symptoms (symptoms_id),
    treatment VARCHAR(3) NOT NULL CHECK (treatment IN ('Yes', 'No'))
);
