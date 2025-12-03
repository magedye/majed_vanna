from uuid import uuid4

from vanna.capabilities.sql_runner import RunSqlToolArgs
from vanna.core.tool.models import ToolContext
from vanna.core.user.models import User
from vanna.integrations.local import LocalFileSystem
from vanna.integrations.mssql import MSSQLRunner
from vanna.integrations.oracle import OracleRunner
from vanna.integrations.sqlite import SqliteRunner
from vanna.tools import RunSqlTool, VisualizeDataTool

from app.agent.memory import agent_memory
from app.config import DB_MSSQL_CONN, DB_ORACLE_DSN, DB_PROVIDER, DB_SQLITE


def get_sql_runner():
    try:
        if DB_PROVIDER == "sqlite":
            return SqliteRunner(database_path=DB_SQLITE)
        if DB_PROVIDER == "oracle":
            return OracleRunner(dsn=DB_ORACLE_DSN)
        if DB_PROVIDER == "mssql":
            return MSSQLRunner(odbc_conn_str=DB_MSSQL_CONN)
    except Exception as e:
        print("DB init error:", e)
    return None


sql_runner = get_sql_runner()
db_tool = RunSqlTool(sql_runner=sql_runner)
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
