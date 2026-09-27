-- NOT NULL rationale: see schema.py module docstring
CREATE TABLE dim_gender (
    gender_id INT PRIMARY KEY,
    gender VARCHAR(10) NOT NULL UNIQUE
);
