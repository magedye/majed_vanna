"""
Seed the local SQLite database with a sample table for training/testing.
Creates table `sales_data` and inserts a few dummy rows if not present.
"""

import os
import sqlite3
from pathlib import Path

from app.config import DB_SQLITE, DB_PROVIDER, DATA_DIR


def ensure_sqlite():
    if DB_PROVIDER != "sqlite":
        raise SystemExit("DB_PROVIDER is not sqlite; seed_db.py only supports sqlite.")
    Path(DB_SQLITE).parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_SQLITE)


def seed(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sales_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            region TEXT,
            amount REAL,
            sale_date TEXT
        )
        """
    )
    cur.execute("SELECT COUNT(*) FROM sales_data")
    count = cur.fetchone()[0]
    if count == 0:
        rows = [
            ("Widget", "North", 1200.50, "2025-01-01"),
            ("Widget", "South", 980.00, "2025-01-02"),
            ("Gadget", "East", 1430.75, "2025-01-03"),
            ("Gadget", "West", 1110.20, "2025-01-04"),
            ("Doohickey", "North", 875.00, "2025-01-05"),
        ]
        cur.executemany(
            "INSERT INTO sales_data (product, region, amount, sale_date) VALUES (?, ?, ?, ?)",
            rows,
        )
    conn.commit()
    cur.close()


def main():
    conn = ensure_sqlite()
    try:
        seed(conn)
        print(f"Seeded sqlite at {DB_SQLITE}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
