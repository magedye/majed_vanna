import sys
from pathlib import Path

import oracledb

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import DB_ORACLE_DSN, ORACLE_USER, ORACLE_PASSWORD


def main():
    if not (ORACLE_USER and ORACLE_PASSWORD and DB_ORACLE_DSN):
        print("Oracle configuration incomplete. Check ORACLE_USER/ORACLE_PASSWORD/DB_ORACLE_DSN.")
        return
    conn = oracledb.connect(
        user=ORACLE_USER,
        password=ORACLE_PASSWORD,
        dsn=DB_ORACLE_DSN,
    )
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM DUAL")
    print("Oracle OK:", cur.fetchone())
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
