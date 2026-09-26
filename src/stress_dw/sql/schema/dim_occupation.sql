-- NOT NULL rationale: see schema.py module docstring
CREATE TABLE dim_occupation (
    occupation_id INT PRIMARY KEY,
    occupation VARCHAR(20) NOT NULL UNIQUE
);
