import pytest
from starlette.responses import Response

from app.agent.input_validation import (
    InputValidationMiddleware,
    validate_chat_payload,
    InputValidationError,
)


def test_validate_chat_payload_basic():
    payload = {"message": " hello ", "metadata": {"k": "v"}, "conversation_id": "c1"}
    cleaned = validate_chat_payload(payload)
    assert cleaned["message"] == "hello"
    assert cleaned["metadata"]["k"] == "v"


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"message": ""},
        {"message": None},
        {"message": "a" * 5001},
    ],
)
def test_validate_chat_payload_reject(payload):
    with pytest.raises(InputValidationError):
        validate_chat_payload(payload)


@pytest.mark.asyncio
async def test_middleware_blocks_invalid_body():
    middleware = InputValidationMiddleware(lambda scope: None)

    class DummyReq:
        def __init__(self, body):
            self._body = body
            self.method = "POST"
            self.url = type("u", (), {"path": "/api/vanna/v2/chat_sse"})
            self.client = None

        async def body(self):
            return self._body

    req = DummyReq(b"not-json")
    resp = await middleware.dispatch(req, lambda r: Response("ok"))
    assert isinstance(resp, Response)
    assert resp.status_code == 400
