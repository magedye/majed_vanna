from datetime import datetime

from fastapi import APIRouter

from app.config import DB_PROVIDER, LLM_CONFIG, LLM_PROVIDER, PORT
from app.runtime import state, uptime_seconds

router = APIRouter()


@router.get("/health")
def health_check():
    llm_model = LLM_CONFIG.get(LLM_PROVIDER, {}).get("model")
    runtime_info = {
        "llm_provider": state.get("llm_provider") or LLM_PROVIDER,
        "db_provider": state.get("db_provider") or DB_PROVIDER,
        "port": state.get("port") or str(PORT),
        "sqlite_path": state.get("sqlite_path"),
        "debug": state.get("debug") == "True",
    }
    return {
        "status": "ok",
        "service": "vanna",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": round(uptime_seconds(), 2),
        "llm_model": llm_model,
        **runtime_info,
    }
