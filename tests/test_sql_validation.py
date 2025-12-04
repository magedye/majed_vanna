import pytest

from app.agent.sql_validation import validate_sql, SQLValidationError


def test_sql_validation_allows_select():
    sql = "SELECT 1"
    assert validate_sql(sql) == "SELECT 1"


@pytest.mark.parametrize(
    "sql",
    [
        "DROP TABLE users",
        "SELECT 1; SELECT 2",
        "SELECT 1; DROP TABLE x",
        "SELECT * FROM t -- comment",
    ],
)
def test_sql_validation_blocks(sql):
    with pytest.raises(SQLValidationError):
        validate_sql(sql)
