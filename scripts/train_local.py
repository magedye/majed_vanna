import sys
from pathlib import Path

# Ensure project root on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.agent.implementation import LocalVanna
from app.config import (
    DB_PROVIDER,
    DB_SQLITE,
    DB_ORACLE_DSN,
    ORACLE_USER,
    ORACLE_PASSWORD,
    ORACLE_SCHEMA,
    ORACLE_TRAIN_OBJECTS,
    ORACLE_TRAIN_TABLES,
    LLM_CONFIG,
    LLM_PROVIDER,
)


def _build_vanna():
    llm_settings = LLM_CONFIG.get(LLM_PROVIDER, LLM_CONFIG.get("lmstudio"))
    cfg = {
        "api_key": llm_settings.get("api_key"),
        "api_base": llm_settings.get("base_url"),
        "model": llm_settings.get("model"),
        "path": "./chroma_db",
    }
    return LocalVanna(config=cfg)


def _train_sqlite(vn: LocalVanna):
    vn.connect_to_sqlite(DB_SQLITE)
    print("Starting SQLite training...")
    df_ddl = vn.run_sql("SELECT type, sql FROM sqlite_master WHERE sql IS NOT NULL")
    for ddl in df_ddl["sql"].to_list():
        print(f"Training on: {ddl[:50]}...")
        vn.train(ddl=ddl)
    print("Training Complete. Vector Store path: ./chroma_db")


def _train_oracle(vn: LocalVanna):
    try:
        import oracledb
    except Exception as exc:
        print(f"[ERROR] oracledb not installed: {exc}")
        sys.exit(1)
    dsn = DB_ORACLE_DSN
    schema = (ORACLE_SCHEMA or ORACLE_USER).upper()
    train_objects = []
    for o in ORACLE_TRAIN_OBJECTS:
        if o in {"TABLES", "TABLE"}:
            train_objects.append("TABLE")
        elif o in {"VIEWS", "VIEW"}:
            train_objects.append("VIEW")
        elif o:
            train_objects.append(o)
    if not train_objects:
        train_objects = ["TABLE", "VIEW"]

    train_tables = ORACLE_TRAIN_TABLES

    if not (ORACLE_USER and ORACLE_PASSWORD and dsn):
        print("[ERROR] Oracle credentials are incomplete. Check .env values.")
        sys.exit(1)

    print(f"Connecting to Oracle schema {schema} at {dsn} ...")
    conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=dsn)
    cur = conn.cursor()

    obj_filter = ", ".join(f"'{obj}'" for obj in train_objects or ["TABLE", "VIEW"])
    base_sql = (
        "SELECT object_name, object_type FROM all_objects "
        f"WHERE owner = :owner AND object_type IN ({obj_filter})"
    )
    if train_tables and train_tables != ["ALL"]:
        tables_filter = ", ".join(f"'{t}'" for t in train_tables)
        base_sql += f" AND object_name IN ({tables_filter})"

    cur.execute(base_sql, owner=schema)
    rows = cur.fetchall()
    print(f"Discovered {len(rows)} objects for training.")

    for object_name, object_type in rows:
        ddl_sql = "SELECT DBMS_METADATA.GET_DDL(:obj_type, :obj_name, :owner) FROM DUAL"
        cur.execute(ddl_sql, obj_type=object_type, obj_name=object_name, owner=schema)
        ddl_row = cur.fetchone()
        ddl = ddl_row[0]
        ddl_text = ddl.read() if hasattr(ddl, "read") else str(ddl)
        print(f"Training on {object_type} {object_name}...")
        vn.train(ddl=ddl_text)

    cur.close()
    conn.close()
    print("Oracle training complete. Vector Store path: ./chroma_db")


if __name__ == "__main__":
    vn = _build_vanna()
    if DB_PROVIDER == "oracle":
        _train_oracle(vn)
    else:
        _train_sqlite(vn)
