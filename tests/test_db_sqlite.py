import os
import pytest
from uuid import uuid4

from vanna.capabilities.sql_runner import RunSqlToolArgs
from vanna.core.tool.models import ToolContext
from vanna.core.user.models import User

from app.agent.db import db_tool
from app.agent.memory import agent_memory


@pytest.mark.asyncio
async def test_sqlite_run_sql_smoke():
    if os.getenv("DB_PROVIDER", "sqlite") != "sqlite":
        pytest.skip("sqlite not active")
    ctx = ToolContext(
        user=User(id="test", username="test"),
        conversation_id="db-test",
        request_id=str(uuid4()),
        agent_memory=agent_memory,
    )
    res = await db_tool.execute(ctx, RunSqlToolArgs(sql="SELECT 1"))
    assert res.success
