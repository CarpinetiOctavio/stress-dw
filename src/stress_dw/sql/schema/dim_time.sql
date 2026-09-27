-- NOT NULL rationale: see schema.py module docstring
CREATE TABLE dim_time (
    time_id INT PRIMARY KEY,
    year INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(9) NOT NULL,
    period CHAR(7) NOT NULL,
    quarter INT NOT NULL,
    semester INT NOT NULL,
    UNIQUE (year, month)
);
