-- NOT NULL rationale: see schema.py module docstring
CREATE TABLE dim_access (
    access_id INT PRIMARY KEY,
    care_options VARCHAR(10) NOT NULL,
    mental_health_interview VARCHAR(5) NOT NULL,
    UNIQUE (care_options, mental_health_interview)
);
