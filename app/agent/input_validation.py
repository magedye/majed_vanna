import json
import re
import uuid
from typing import Any, Dict, Optional

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from vanna.servers.base.chat_handler import ChatHandler
from vanna.servers.base.models import ChatRequest, ChatStreamChunk


class InputValidationError(ValueError):
    """Raised when chat input fails basic validation."""


MAX_MESSAGE_LENGTH = 4000
MAX_METADATA_ITEMS = 20
MAX_METADATA_KEY_LEN = 50
MAX_METADATA_VALUE_LEN = 500
MAX_ID_LENGTH = 64
SAFE_ID_PATTERN = re.compile(r"^[A-Za-z0-9._:-]+$")
CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b-\x0c\x0e-\x1f]")
CHAT_ENDPOINTS = {"/api/vanna/v2/chat_sse", "/api/vanna/v2/chat_poll"}


def sanitize_text(value: str, field: str = "message") -> str:
    if not isinstance(value, str):
        raise InputValidationError(f"{field} must be a string")
    cleaned = CONTROL_CHARS.sub(" ", value)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def _validate_id(value: Optional[Any], field: str) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise InputValidationError(f"{field} must be a string")
    candidate = value.strip()
    if not candidate:
        return None
    if len(candidate) > MAX_ID_LENGTH or not SAFE_ID_PATTERN.match(candidate):
        raise InputValidationError(f"{field} contains invalid characters")
    return candidate


def _validate_metadata(metadata: Any) -> Dict[str, Any]:
    if metadata is None:
        return {}
    if not isinstance(metadata, dict):
        raise InputValidationError("metadata must be an object")
    if len(metadata) > MAX_METADATA_ITEMS:
        raise InputValidationError("metadata has too many fields")

    sanitized: Dict[str, Any] = {}
    for raw_key, raw_value in metadata.items():
        if not isinstance(raw_key, str):
            raise InputValidationError("metadata keys must be strings")
        key = sanitize_text(raw_key, field="metadata key")
        if not key:
            raise InputValidationError("metadata keys cannot be empty")
        if len(key) > MAX_METADATA_KEY_LEN:
            raise InputValidationError("metadata key is too long")

        if isinstance(raw_value, str):
            value = sanitize_text(raw_value, field=f"metadata.{key}")
            if len(value) > MAX_METADATA_VALUE_LEN:
                raise InputValidationError("metadata value is too long")
        elif isinstance(raw_value, (int, float, bool)) or raw_value is None:
            value = raw_value
        else:
            raise InputValidationError("metadata values must be strings or numbers")

        sanitized[key] = value

    return sanitized


def validate_chat_payload(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise InputValidationError("payload must be a JSON object")
    if "message" not in payload:
        raise InputValidationError("message is required")

    message = sanitize_text(payload.get("message", ""), field="message")
    if not message:
        raise InputValidationError("message cannot be empty")
    if len(message) > MAX_MESSAGE_LENGTH:
        raise InputValidationError(f"message exceeds {MAX_MESSAGE_LENGTH} characters")

    conversation_id = _validate_id(payload.get("conversation_id"), "conversation_id")
    request_id = _validate_id(payload.get("request_id"), "request_id")
    metadata = _validate_metadata(payload.get("metadata", {}))

    sanitized = dict(payload)
    sanitized.update(
        {
            "message": message,
            "conversation_id": conversation_id,
            "request_id": request_id,
            "metadata": metadata,
        }
    )
    return sanitized


class InputValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "POST" and request.url.path in CHAT_ENDPOINTS:
            try:
                raw_body = await request.body()
                if not raw_body:
                    return JSONResponse({"detail": "Request body is required"}, status_code=400)
                payload = json.loads(raw_body)
            except json.JSONDecodeError:
                return JSONResponse({"detail": "Invalid JSON payload"}, status_code=400)
            except Exception:
                return JSONResponse({"detail": "Unable to read request body"}, status_code=400)

            try:
                sanitized = validate_chat_payload(payload)
            except InputValidationError as exc:
                return JSONResponse({"detail": str(exc)}, status_code=400)

            request._body = json.dumps(sanitized).encode("utf-8")

        return await call_next(request)


class SafeChatHandler(ChatHandler):
    async def handle_stream(self, request: ChatRequest):
        sanitized = validate_chat_payload(
            {
                "message": request.message,
                "conversation_id": request.conversation_id,
                "request_id": request.request_id,
                "metadata": request.metadata,
            }
        )

        request.message = sanitized["message"]
        request.metadata = sanitized.get("metadata", {})
        request.conversation_id = sanitized.get("conversation_id")
        request.request_id = sanitized.get("request_id")

        conversation_id = request.conversation_id or self._generate_conversation_id()
        request_id = request.request_id or str(uuid.uuid4())

        async for component in self.agent.send_message(
            request_context=request.request_context,
            message=request.message,
            conversation_id=conversation_id,
        ):
            yield ChatStreamChunk.from_component(component, conversation_id, request_id)
