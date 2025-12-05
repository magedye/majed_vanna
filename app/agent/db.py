import time
from uuid import uuid4

import pandas as pd
import asyncio

from vanna.capabilities.sql_runner import RunSqlToolArgs, SqlRunner
from vanna.core.tool import ToolResult
from vanna.core.tool.models import ToolContext
from vanna.core.user.models import User
from vanna.integrations.local import LocalFileSystem
from vanna.integrations.mssql import MSSQLRunner
from vanna.integrations.sqlite import SqliteRunner
from vanna.components import (
    UiComponent,
    NotificationComponent,
    ComponentType,
    SimpleTextComponent,
)
from vanna.tools import RunSqlTool, VisualizeDataTool

from app.agent.memory import agent_memory
from app.circuit_breaker import CircuitBreaker
from app.config import (
    DB_MSSQL_CONN,
    DB_ORACLE_DSN,
    DB_PROVIDER,
    DB_SQLITE,
    ORACLE_USER,
    ORACLE_PASSWORD,
    ORACLE_DSN,
    ORACLE_SCHEMA,
    ORACLE_ENABLE_POOL,
    ORACLE_POOL_MIN,
    ORACLE_POOL_MAX,
    ORACLE_POOL_INCREMENT,
    ORACLE_TRAIN_OBJECTS,
    ORACLE_TRAIN_TABLES,
)
from app.agent.sql_validation import validate_sql, SQLValidationError
from app.utils.logger import setup_logger, log_perf, record_perf_sample
from app.config import (
    DB_QUERY_TIMEOUT_MS,
    DB_MAX_RETRIES,
    DB_RETRY_BACKOFF_MS,
)


_oracle_connection_factory = None
_oracle_pool = None
db_circuit = CircuitBreaker("db", failure_threshold=3, reset_timeout=30)


def _build_oracle_runner():
    """Initialize Oracle runner with optional pooling and shared connection factory."""
    global _oracle_connection_factory
    global _oracle_pool
    try:
        import oracledb
    except Exception as e:
        print("DB init error: oracledb not available", e)
        _oracle_connection_factory = None
        return None

    user = ORACLE_USER
    password = ORACLE_PASSWORD
    dsn = DB_ORACLE_DSN or ORACLE_DSN

    if not (user and password and dsn):
        print("DB init error: oracle credentials are incomplete")
        _oracle_connection_factory = None
        return None

    pool = None
    if ORACLE_ENABLE_POOL:
        try:
            pool = oracledb.SessionPool(
                user=user,
                password=password,
                dsn=dsn,
                min=ORACLE_POOL_MIN,
                max=ORACLE_POOL_MAX,
                increment=ORACLE_POOL_INCREMENT,
                threaded=True,
                getmode=oracledb.SPOOL_ATTRVAL_WAIT,
            )
            _oracle_pool = pool
        except Exception as e:
            print("DB init error: oracle pool failed", e)
            _oracle_connection_factory = None
            return None

    def _get_connection():
        if pool:
            return pool.acquire()
        return oracledb.connect(user=user, password=password, dsn=dsn)

    _oracle_connection_factory = _get_connection

    class PoolingOracleRunner(SqlRunner):
        async def run_sql(self, args: RunSqlToolArgs, context: ToolContext) -> pd.DataFrame:
            if not db_circuit._can_pass():
                raise RuntimeError("CircuitBreaker[db] is OPEN")
            sql = args.sql.rstrip()
            if sql.endswith(";"):
                sql = sql[:-1]
            for attempt in range(DB_MAX_RETRIES + 1):
                try:
                    async def _do_query():
                        conn = await db_circuit.call_async(lambda: _oracle_connection_factory())
                        try:
                            cur = conn.cursor()
                            try:
                                cur.execute(sql)
                                rows = cur.fetchall()
                                cols = [d[0] for d in cur.description] if cur.description else []
                                return pd.DataFrame(rows, columns=cols)
                            finally:
                                cur.close()
                        finally:
                            conn.close()

                    return await asyncio.wait_for(
                        _do_query(),
                        timeout=DB_QUERY_TIMEOUT_MS / 1000,
                    )
                except Exception as exc:
                    if attempt >= DB_MAX_RETRIES:
                        raise
                    await asyncio.sleep(DB_RETRY_BACKOFF_MS / 1000)

    return PoolingOracleRunner()


def get_sql_runner():
    try:
        if DB_PROVIDER == "sqlite":
            return SqliteRunner(database_path=DB_SQLITE)
        if DB_PROVIDER == "oracle":
            runner = _build_oracle_runner()
            if runner:
                return runner
            return None
        if DB_PROVIDER == "mssql":
            return MSSQLRunner(odbc_conn_str=DB_MSSQL_CONN)
    except Exception as e:
        print("DB init error:", e)
    return None


sql_runner = get_sql_runner()
perf_logger = setup_logger(__name__)
_allowed_tables_cache = None


def _extract_tables(sql: str):
    import re

    candidates = re.findall(
        r"\bfrom\s+([\w\.\"]+)|\bjoin\s+([\w\.\"]+)", sql, flags=re.IGNORECASE
    )
    tables = []
    for a, b in candidates:
        name = a or b
        name = name.replace('"', "").split(".")[-1]
        if name:
            tables.append(name.lower())
    return set(tables)


def _load_allowed_tables():
    global _allowed_tables_cache
    if _allowed_tables_cache is not None:
        return _allowed_tables_cache
    tables = set()
    try:
        if DB_PROVIDER == "sqlite" and DB_SQLITE:
            import sqlite3

            conn = sqlite3.connect(DB_SQLITE)
            try:
                cur = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                )
                tables = {row[0].lower() for row in cur.fetchall()}
            finally:
                conn.close()
        if DB_PROVIDER == "oracle" and _oracle_connection_factory:
            conn = _oracle_connection_factory()
            try:
                cur = conn.cursor()
                normalized_obj_types = []
                for o in ORACLE_TRAIN_OBJECTS:
                    if o in {"TABLES", "TABLE"}:
                        normalized_obj_types.append("TABLE")
                    elif o in {"VIEWS", "VIEW"}:
                        normalized_obj_types.append("VIEW")
                    elif o:
                        normalized_obj_types.append(o)
                if not normalized_obj_types:
                    normalized_obj_types = ["TABLE", "VIEW"]
                type_list = ", ".join(f"'{t}'" for t in normalized_obj_types)
                schema = (ORACLE_SCHEMA or ORACLE_USER or "").upper()
                query = (
                    "SELECT object_name FROM all_objects "
                    f"WHERE owner = '{schema}' AND object_type IN ({type_list})"
                )
                train_tables = ORACLE_TRAIN_TABLES
                if train_tables and train_tables != ["ALL"]:
                    table_list = ", ".join(f"'{t}'" for t in train_tables)
                    query += f" AND object_name IN ({table_list})"
                cur.execute(query)
                tables = {row[0].lower() for row in cur.fetchall()}
            finally:
                conn.close()
    except Exception as e:
        log_perf(perf_logger, "schema_guard.error", {"error": str(e)})
    _allowed_tables_cache = tables
    return tables


class SafeRunSqlTool(RunSqlTool):
    """Phase 1.B: wrap RunSqlTool with basic SQL validation before execution."""

    async def execute(self, context: ToolContext, args: RunSqlToolArgs) -> ToolResult:
        start_time = time.time()
        try:
            safe_sql = validate_sql(args.sql)
        except SQLValidationError as exc:
            error_message = f"SQL blocked: {exc}"
            return ToolResult(
                success=False,
                result_for_llm=error_message,
                ui_component=UiComponent(
                    rich_component=NotificationComponent(
                        type=ComponentType.NOTIFICATION, level="error", message=error_message
                    ),
                    simple_component=SimpleTextComponent(text=error_message),
                ),
                error=str(exc),
                metadata={"error_type": "sql_validation"},
            )

        safe_args = RunSqlToolArgs(sql=safe_sql)
        tables = _extract_tables(safe_sql)
        allowed = _load_allowed_tables()
        if tables and allowed:
            invalid = [t for t in tables if t not in allowed]
            if invalid:
                error_message = (
                    f"SQL blocked: referenced tables not allowed ({', '.join(invalid)})"
                )
                return ToolResult(
                    success=False,
                    result_for_llm=error_message,
                    ui_component=UiComponent(
                        rich_component=NotificationComponent(
                            type=ComponentType.NOTIFICATION,
                            level="error",
                            message=error_message,
                        ),
                        simple_component=SimpleTextComponent(text=error_message),
                    ),
                    error=error_message,
                    metadata={"error_type": "sql_validation", "invalid_tables": invalid},
                )
        result = await super().execute(context, safe_args)
        duration_ms = round((time.time() - start_time) * 1000, 2)
        log_perf(
            perf_logger,
            "sql.execution",
            {
                "duration_ms": duration_ms,
                "provider": DB_PROVIDER,
                "request_id": getattr(context, "request_id", None),
                "conversation_id": getattr(context, "conversation_id", None),
                "trace_id": getattr(context, "trace_id", None),
            },
        )
        record_perf_sample("sql_ms", duration_ms)
        return result


# Phase 1.B: Use guarded RunSql tool to enforce SQL Safety Layer pre-checks.
db_tool = SafeRunSqlTool(sql_runner=sql_runner)
visualizer = VisualizeDataTool(file_system=LocalFileSystem())


TEST_QUERIES = {
    "sqlite": "SELECT 1",
    "mssql": "SELECT 1",
    "oracle": "SELECT 1 FROM dual",
}


async def test_connections() -> dict:
    if not sql_runner:
        return {
            "status": "error",
            "provider": DB_PROVIDER,
            "message": "No SQL runner configured; verify DB_PROVIDER and credentials.",
        }

    if agent_memory is None:
        return {
            "status": "error",
            "provider": DB_PROVIDER,
            "message": "Agent memory is unavailable; test cannot run.",
        }

    query = TEST_QUERIES.get(DB_PROVIDER)
    if not query:
        return {
            "status": "error",
            "provider": DB_PROVIDER,
            "message": "Unsupported database provider for diagnostics.",
        }

    context = ToolContext(
        user=User(id="system", username="system"),
        conversation_id="db-status",
        request_id=str(uuid4()),
        agent_memory=agent_memory,
    )

    try:
        await sql_runner.run_sql(
            RunSqlToolArgs(sql=query),
            context,
        )
        return {"status": "ok", "provider": DB_PROVIDER}
    except Exception as exc:
        return {
            "status": "error",
            "provider": DB_PROVIDER,
            "message": str(exc),
        }


def close_db():
    try:
        if _oracle_pool:
            _oracle_pool.close()
    except Exception:
        pass
