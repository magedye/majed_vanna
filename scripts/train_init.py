"""
Initial training script to populate Vanna with current DB schema.
- Fetches DDL from SQLite or Oracle (if creds provided).
- Invokes vanna.train(ddl=...) when available; otherwise prints DDL.
"""

import os
import sys
from pathlib import Path
from typing import List

from app.config import (
    DB_PROVIDER,
    DB_SQLITE,
    DB_ORACLE_DSN,
    ORACLE_USER,
    ORACLE_PASSWORD,
    ORACLE_DSN,
)


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
        import vanna.legacy as vn

        return vn
    except Exception as e:
        print("Unable to import vanna.legacy:", e, file=sys.stderr)
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
