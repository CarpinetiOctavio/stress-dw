-- NOT NULL rationale: see schema.py module docstring
CREATE TABLE dim_family_history (
    family_history_id INT PRIMARY KEY,
    family_history VARCHAR(3) NOT NULL UNIQUE
);
