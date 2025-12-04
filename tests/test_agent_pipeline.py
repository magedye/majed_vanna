import pytest
from uuid import uuid4
from vanna.core.user.models import User
from vanna.core.tool.models import ToolContext
from vanna.components import SimpleTextComponent

from app.agent.builder import agent
from app.agent.memory import agent_memory


class StubLLMResponse:
    def __init__(self, content="ok"):
        self.content = content
        self.model = type("m", (), {"name": "stub-model"})


@pytest.mark.asyncio
async def test_agent_send_message_smoke(monkeypatch):
    async def fake_send_request(req):
        return StubLLMResponse("hello")

    llm_service = agent.llm_service
    monkeypatch.setattr(llm_service, "send_request", fake_send_request)

    user = User(id="stub", username="stub")
    conversation_id = f"conv-{uuid4()}"
    async for component in agent.send_message(
        request_context=None, message="hi", conversation_id=conversation_id
    ):
        assert component is not None
        break
