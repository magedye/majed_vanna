import sys
from pathlib import Path
import traceback

try:
    import oracledb
except Exception as e:
    print("[ERROR] Cannot import oracledb. Install using: pip install oracledb")
    print("Details:", e)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import DB_ORACLE_DSN, ORACLE_USER, ORACLE_PASSWORD, ORACLE_SCHEMA


def fail(msg):
    print(f"[ERROR] {msg}")
    sys.exit(1)


def warn(msg):
    print(f"[WARN] {msg}")


def ok(msg):
    print(f"[OK] {msg}")


def check_env():
    print("\n=== Checking Oracle Environment Variables ===")
    if not ORACLE_USER:
        fail("ORACLE_USER is missing.")
    if not ORACLE_PASSWORD:
        fail("ORACLE_PASSWORD is missing.")
    if not DB_ORACLE_DSN:
        fail("DB_ORACLE_DSN is missing.")

    ok(f"Oracle user: {ORACLE_USER}")
    ok(f"Oracle DSN: {DB_ORACLE_DSN}")


def check_dsn_format():
    print("\n=== Validating DSN Format ===")
    if ":" not in DB_ORACLE_DSN or "/" not in DB_ORACLE_DSN:
        fail("Invalid DSN format. Expected host:port/service_name")

    ok("DSN format looks correct.")


def connect_oracle():
    print("\n=== Connecting to Oracle Database ===")

    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=DB_ORACLE_DSN,
        )
        ok("Connection to Oracle successful.")
        return conn
    except Exception:
        fail(f"Cannot connect to Oracle. Details:\n{traceback.format_exc()}")


def test_basic_query(conn):
    print("\n=== Running Basic Query Test (SELECT 1 FROM DUAL) ===")
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM DUAL")
        ok(f"Basic query OK: {cur.fetchone()}")
    except Exception:
        fail(f"Basic query failed. Details:\n{traceback.format_exc()}")


def list_tables(conn):
    print("\n=== Retrieving User Tables ===")

    try:
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM user_tables ORDER BY table_name")
        tables = [r[0] for r in cur.fetchall()]

        if not tables:
            warn("No tables found in the schema. System will run but queries will not be meaningful.")
            return []

        ok(f"Found {len(tables)} table(s).")
        print("Example tables:", tables[:10])

        return tables
    except Exception:
        fail(f"Failed to list tables. Details:\n{traceback.format_exc()}")


def describe_table(conn, table):
    print(f"\n=== Extracting Metadata for Table: {table} ===")

    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT column_name, data_type, nullable
            FROM user_tab_columns
            WHERE table_name = :tbl
            ORDER BY column_id
        """,
            {"tbl": table},
        )

        columns = cur.fetchall()
        if not columns:
            warn(f"No metadata returned for {table}.")
            return

        ok(f"{len(columns)} column(s) found.")
        for col in columns:
            print(f"- {col[0]} ({col[1]}) nullable={col[2]}")

    except Exception:
        fail(f"Failed to extract metadata for {table}. Details:\n{traceback.format_exc()}")


def test_metadata_all_tables(conn):
    print("\n=== Extracting Metadata for All Tables (safe mode) ===")
    tables = list_tables(conn)

    if not tables:
        return

    for table in tables[:5]:  # limits output
        describe_table(conn, table)


def main():
    print("\n============================================")
    print("      ORACLE FULL DIAGNOSTIC TEST")
    print("============================================")

    check_env()
    check_dsn_format()
    conn = connect_oracle()

    test_basic_query(conn)
    test_metadata_all_tables(conn)

    conn.close()
    print("\n============================================")
    ok("Oracle diagnostic test completed successfully.")
    print("============================================")


if __name__ == "__main__":
    main()
