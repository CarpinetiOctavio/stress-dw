-- NOT NULL rationale: see schema.py module docstring
CREATE TABLE dim_isolation (
    isolation_id INT PRIMARY KEY,
    days_indoors VARCHAR(25) NOT NULL UNIQUE,
    sort_order INT NOT NULL,
    duration_band VARCHAR(6) NOT NULL
);
