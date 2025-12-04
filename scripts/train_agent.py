"""
Utility script to extract DDL from the active DB and (when supported) feed it
to Vanna training. Currently collects SQLite schema; extends to Oracle if env
credentials are present. The actual training call is attempted only if a
train() API exists on the loaded Vanna object.
"""

import os
import sys
from pathlib import Path
from typing import List

DB_PROVIDER = os.getenv("DB_PROVIDER", "sqlite").lower()
DB_SQLITE = os.getenv("SQLITE_DB", str(Path(__file__).resolve().parent.parent / "app" / "data" / "mydb.db"))
DB_ORACLE_DSN = os.getenv("DB_ORACLE_DSN", "")
ORACLE_USER = os.getenv("ORACLE_USER", "")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "")
ORACLE_DSN = os.getenv("ORACLE_DSN", "")


def fetch_sqlite_ddl(path: str) -> List[str]:
    import sqlite3

    ddl = []
    conn = sqlite3.connect(path)
    try:
        cur = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND sql NOT NULL;")
        ddl = [row[0] for row in cur.fetchall() if row[0]]
    finally:
        conn.close()
    return ddl


def fetch_oracle_ddl(dsn: str, user: str, password: str) -> List[str]:
    try:
        import oracledb
    except Exception as e:
        print("oracledb not installed, skipping Oracle DDL fetch:", e, file=sys.stderr)
        return []

    ddl = []
    try:
        conn = oracledb.connect(user=user, password=password, dsn=dsn)
    except Exception as e:
        print("Oracle connection failed; cannot fetch DDL:", e, file=sys.stderr)
        return []

    try:
        cur = conn.cursor()
        cur.execute("SELECT DBMS_METADATA.GET_DDL('TABLE', table_name) FROM user_tables")
        for row in cur:
            if row and row[0]:
                ddl.append(str(row[0]))
    except Exception as e:
        print("Oracle DDL fetch error:", e, file=sys.stderr)
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()
    return ddl


def load_vanna():
    try:
        import vanna
        return vanna
    except Exception as e:
        print("Unable to import vanna:", e, file=sys.stderr)
        return None


def main():
    ddl_segments: List[str] = []
    if DB_PROVIDER == "sqlite":
        ddl_segments = fetch_sqlite_ddl(DB_SQLITE)
    elif DB_PROVIDER == "oracle":
        dsn = ORACLE_DSN or DB_ORACLE_DSN
        if dsn and ORACLE_USER and ORACLE_PASSWORD:
            ddl_segments = fetch_oracle_ddl(dsn, ORACLE_USER, ORACLE_PASSWORD)
        else:
            print("Oracle creds/DSN not set; skipping DDL fetch.", file=sys.stderr)
    else:
        print(f"Unsupported DB provider for training: {DB_PROVIDER}", file=sys.stderr)

    if not ddl_segments:
        print("No DDL collected; training skipped.")
        return

    vanna_mod = load_vanna()
    if not vanna_mod or not hasattr(vanna_mod, "train"):
        print("vanna.train() not available; printing DDL for manual ingestion.")
        for stmt in ddl_segments:
            print(stmt)
        return

    try:
        vanna_mod.train(ddl="\n\n".join(ddl_segments))
        print(f"Training invoked with {len(ddl_segments)} DDL statements.")
    except Exception as e:
        print("Training failed:", e, file=sys.stderr)
        for stmt in ddl_segments:
            print(stmt)


if __name__ == "__main__":
    main()
