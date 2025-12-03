from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.oracle import OracleRunner
from vanna.integrations.mssql import MSSQLRunner
from vanna.integrations.local import LocalFileSystem
from vanna.tools import RunSqlTool, VisualizeDataTool
from app.config import DB_SQLITE, DB_ORACLE_DSN, DB_MSSQL_CONN, DB_PROVIDER

def get_sql_runner():
    try:
        if DB_PROVIDER=="sqlite": return SqliteRunner(database_path=DB_SQLITE)
        elif DB_PROVIDER=="oracle": return OracleRunner(dsn=DB_ORACLE_DSN)
        elif DB_PROVIDER=="mssql": return MSSQLRunner(odbc_conn_str=DB_MSSQL_CONN)
    except Exception as e:
        print("DB init error:", e)
        return None

sql_runner=get_sql_runner()
db_tool=RunSqlTool(sql_runner=sql_runner)
visualizer=VisualizeDataTool(file_system=LocalFileSystem())
