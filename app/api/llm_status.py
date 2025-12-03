import asyncio
from datetime import datetime

from fastapi import APIRouter

from app.agent.llm import llm
from app.config import LLM_CONFIG, LLM_PROVIDER
from vanna.core.llm.models import LlmMessage, LlmRequest
from vanna.core.user.models import User

router = APIRouter()


@router.get("/llm")
async def llm_status():
    request = LlmRequest(
        messages=[LlmMessage(role="user", content="ping")],
        user=User(id="health-check"),
        max_tokens=16,
    )
    model_name = LLM_CONFIG.get(LLM_PROVIDER, {}).get("model")
    start_time = datetime.utcnow()
    try:
        response = await asyncio.wait_for(llm.send_request(request), timeout=3)
        duration = (datetime.utcnow() - start_time).total_seconds()
        return {
            "status": "ok",
            "provider": LLM_PROVIDER,
            "model": model_name,
            "response": response.content,
            "duration_seconds": round(duration, 3),
        }
    except asyncio.TimeoutError:
        return {
            "status": "error",
            "error": "LLM request timed out",
            "provider": LLM_PROVIDER,
        }
    except Exception as exc:
        return {
            "status": "error",
            "error": str(exc),
            "provider": LLM_PROVIDER,
        }
