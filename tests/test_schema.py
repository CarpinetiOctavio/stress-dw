from collections.abc import Iterator

import duckdb
import pytest

from stress_dw.schema import TABLES, create_schema, ensure_schema, read_ddl

# Columns and types per docs/specification/staging.md, dimensions.md, and
# fact-table.md, as DuckDB reports them: VARCHAR(n) and CHAR(n) are stored as
# VARCHAR, DATETIME as TIMESTAMP. A closed list: matching it exactly also
# satisfies acceptance check C4, since no column outside the specification,
# such as `explicit_recognition` or `symptom_cluster`, can exist.
EXPECTED_COLUMNS: dict[str, list[tuple[str, str]]] = {
    "staging_response": [
        ("response_id", "INTEGER"),
        ("response_timestamp", "TIMESTAMP"),
        ("gender", "VARCHAR"),
        ("country", "VARCHAR"),
        ("occupation", "VARCHAR"),
        ("family_history", "VARCHAR"),
        ("treatment", "VARCHAR"),
        ("days_indoors", "VARCHAR"),
        ("growing_stress", "VARCHAR"),
        ("mood_swings", "VARCHAR"),
        ("coping_struggles", "VARCHAR"),
        ("social_weakness", "VARCHAR"),
        ("mental_health_interview", "VARCHAR"),
        ("care_options", "VARCHAR"),
    ],
    "dim_time": [
        ("time_id", "INTEGER"),
        ("year", "INTEGER"),
        ("month", "INTEGER"),
        ("month_name", "VARCHAR"),
        ("period", "VARCHAR"),
        ("quarter", "INTEGER"),
        ("semester", "INTEGER"),
    ],
    "dim_gender": [("gender_id", "INTEGER"), ("gender", "VARCHAR")],
    "dim_family_history": [
        ("family_history_id", "INTEGER"),
        ("family_history", "VARCHAR"),
    ],
    "dim_occupation": [("occupation_id", "INTEGER"), ("occupation", "VARCHAR")],
    "dim_country": [
        ("country_id", "INTEGER"),
        ("country", "VARCHAR"),
        ("region", "VARCHAR"),
    ],
    "dim_isolation": [
        ("isolation_id", "INTEGER"),
        ("days_indoors", "VARCHAR"),
        ("sort_order", "INTEGER"),
        ("duration_band", "VARCHAR"),
    ],
    "dim_access": [
        ("access_id", "INTEGER"),
        ("care_options", "VARCHAR"),
        ("mental_health_interview", "VARCHAR"),
    ],
    "dim_symptoms": [
        ("symptoms_id", "INTEGER"),
        ("growing_stress", "VARCHAR"),
        ("mood_swings", "VARCHAR"),
        ("coping_struggles", "VARCHAR"),
        ("social_weakness", "VARCHAR"),
    ],
    "fact_response": [
        ("response_id", "INTEGER"),
        ("time_id", "INTEGER"),
        ("gender_id", "INTEGER"),
        ("family_history_id", "INTEGER"),
        ("occupation_id", "INTEGER"),
        ("country_id", "INTEGER"),
        ("isolation_id", "INTEGER"),
        ("access_id", "INTEGER"),
        ("symptoms_id", "INTEGER"),
        ("treatment", "VARCHAR"),
    ],
}

# Natural keys per docs/specification/dimensions.md#row-set.
NATURAL_KEYS: dict[str, list[str]] = {
    "dim_time": ["year", "month"],
    "dim_gender": ["gender"],
    "dim_family_history": ["family_history"],
    "dim_occupation": ["occupation"],
    "dim_country": ["country"],
    "dim_isolation": ["days_indoors"],
    "dim_access": ["care_options", "mental_health_interview"],
    "dim_symptoms": [
        "growing_stress",
        "mood_swings",
        "coping_struggles",
        "social_weakness",
    ],
}

# One valid row per dimension, so a fact row can resolve every foreign key.
ONE_ROW_PER_DIMENSION: dict[str, tuple[int | str, ...]] = {
    "dim_time": (1, 2014, 8, "August", "2014-08", 3, 2),
    "dim_gender": (1, "Female"),
    "dim_family_history": (1, "No"),
    "dim_occupation": (1, "Student"),
    "dim_country": (1, "Brazil", "Latin America and the Caribbean"),
    "dim_isolation": (1, "Go out Every day", 1, "Low"),
    "dim_access": (1, "Yes", "No"),
    "dim_symptoms": (1, "Yes", "Low", "No", "Maybe"),
}

INSERT_FACT = "INSERT INTO fact_response VALUES (?, ?, 1, 1, 1, 1, 1, 1, 1, ?)"


@pytest.fixture
def connection() -> Iterator[duckdb.DuckDBPyConnection]:
    with duckdb.connect() as connection:
        create_schema(connection)
        yield connection


@pytest.fixture
def populated_dimensions(
    connection: duckdb.DuckDBPyConnection,
) -> duckdb.DuckDBPyConnection:
    for dimension, row in ONE_ROW_PER_DIMENSION.items():
        placeholders = ", ".join("?" for _ in row)
        connection.execute(f"INSERT INTO {dimension} VALUES ({placeholders})", row)
    return connection


def constraints(
    connection: duckdb.DuckDBPyConnection, constraint_type: str
) -> list[tuple[str, list[str], str | None, list[str]]]:
    return connection.execute(
        """
        SELECT table_name, constraint_column_names,
               referenced_table, referenced_column_names
        FROM duckdb_constraints()
        WHERE constraint_type = ?
        """,
        [constraint_type],
    ).fetchall()


def test_every_specified_table_is_created(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    tables = connection.execute(
        "SELECT table_name FROM information_schema.tables"
    ).fetchall()
    assert sorted(name for (name,) in tables) == sorted(EXPECTED_COLUMNS)
    assert sorted(TABLES) == sorted(EXPECTED_COLUMNS)


@pytest.mark.parametrize("table", EXPECTED_COLUMNS)
def test_table_has_exactly_the_specified_columns_and_types(
    connection: duckdb.DuckDBPyConnection, table: str
) -> None:
    columns = connection.execute(
        """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = ?
        ORDER BY ordinal_position
        """,
        [table],
    ).fetchall()
    assert columns == EXPECTED_COLUMNS[table]


def test_every_column_is_not_null(connection: duckdb.DuckDBPyConnection) -> None:
    nullable = connection.execute(
        """
        SELECT table_name, column_name
        FROM information_schema.columns
        WHERE is_nullable = 'YES'
        """
    ).fetchall()
    assert nullable == []


def test_every_table_has_its_surrogate_primary_key(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    primary_keys = {
        table: columns
        for table, columns, _, _ in constraints(connection, "PRIMARY KEY")
    }
    assert primary_keys == {
        table: [columns[0][0]] for table, columns in EXPECTED_COLUMNS.items()
    }


def test_each_dimension_is_unique_on_its_natural_key(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    unique_keys = {
        table: columns for table, columns, _, _ in constraints(connection, "UNIQUE")
    }
    assert unique_keys == NATURAL_KEYS


def test_fact_response_has_the_eight_specified_foreign_keys(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    foreign_keys = sorted(
        (columns, referenced_table, referenced_columns)
        for table, columns, referenced_table, referenced_columns in constraints(
            connection, "FOREIGN KEY"
        )
        if table == "fact_response"
    )
    expected = sorted(
        ([f"{name}_id"], f"dim_{name}", [f"{name}_id"])
        for name in (dimension.removeprefix("dim_") for dimension in NATURAL_KEYS)
    )
    assert foreign_keys == expected


def test_a_fact_row_with_every_foreign_key_resolved_is_accepted(
    populated_dimensions: duckdb.DuckDBPyConnection,
) -> None:
    populated_dimensions.execute(INSERT_FACT, [1, 1, "Yes"])
    count = populated_dimensions.execute(
        "SELECT COUNT(*) FROM fact_response"
    ).fetchone()
    assert count == (1,)


def test_a_fact_row_with_an_unresolved_foreign_key_is_rejected(
    populated_dimensions: duckdb.DuckDBPyConnection,
) -> None:
    with pytest.raises(duckdb.ConstraintException):
        populated_dimensions.execute(INSERT_FACT, [1, 2, "Yes"])


@pytest.mark.parametrize("treatment", ["Maybe", "yes", ""])
def test_a_treatment_other_than_yes_or_no_is_rejected(
    populated_dimensions: duckdb.DuckDBPyConnection, treatment: str
) -> None:
    with pytest.raises(duckdb.ConstraintException):
        populated_dimensions.execute(INSERT_FACT, [1, 1, treatment])


def test_a_null_natural_key_is_rejected(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    with pytest.raises(duckdb.ConstraintException):
        connection.execute("INSERT INTO dim_gender VALUES (1, NULL)")


def test_a_failed_statement_leaves_no_table_behind() -> None:
    with duckdb.connect() as connection:
        connection.execute("CREATE TABLE dim_country (country_id INT)")
        with pytest.raises(duckdb.CatalogException) as raised:
            create_schema(connection)
        tables = connection.execute(
            "SELECT table_name FROM information_schema.tables"
        ).fetchall()
    assert tables == [("dim_country",)]
    assert "while creating table dim_country" in raised.value.__notes__


def test_ensure_schema_creates_only_the_missing_tables() -> None:
    with duckdb.connect() as connection:
        connection.execute(read_ddl("dim_gender"))
        connection.execute("INSERT INTO dim_gender VALUES (1, 'Female')")
        ensure_schema(connection)
        tables = connection.execute(
            "SELECT table_name FROM information_schema.tables"
        ).fetchall()
        kept = connection.execute("SELECT * FROM dim_gender").fetchall()
    assert sorted(name for (name,) in tables) == sorted(TABLES)
    assert kept == [(1, "Female")]


def test_ensure_schema_on_a_complete_schema_changes_nothing(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    ensure_schema(connection)
    count = connection.execute(
        "SELECT COUNT(*) FROM information_schema.tables"
    ).fetchone()
    assert count == (len(TABLES),)
