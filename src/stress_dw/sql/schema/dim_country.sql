-- NOT NULL rationale: see schema.py module docstring
CREATE TABLE dim_country (
    country_id INT PRIMARY KEY,
    country VARCHAR(50) NOT NULL UNIQUE,
    region VARCHAR(40) NOT NULL
);
