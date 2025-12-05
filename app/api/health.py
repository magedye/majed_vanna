from datetime import datetime

from fastapi import APIRouter

from app.agent.db import test_connections
from app.agent.builder import knowledge_base
from app.config import DB_PROVIDER, LLM_CONFIG, LLM_PROVIDER, PORT
from app.utils.logger import perf_snapshot, get_trace_ids
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


@router.get("/health/ready")
async def readiness_check():
    db_status = await test_connections()
    llm_vals = list(perf_snapshot["llm_ms"])
    llm_avg = round(sum(llm_vals) / len(llm_vals), 2) if llm_vals else None
    vector_ready = False
    try:
        df = knowledge_base.get_training_data()
        vector_ready = bool(df is not None and not df.empty)
    except Exception:
        vector_ready = False
    trace_id, _ = get_trace_ids()
    overall = "ok" if db_status.get("status") == "ok" else "error"
    return {
        "status": overall,
        "service": "vanna",
        "db": db_status,
        "llm": {"status": "ok" if llm_avg else "unknown", "latency_ms": llm_avg},
        "vector_store": {"ready": vector_ready},
        "trace_id": trace_id,
        "uptime_seconds": round(uptime_seconds(), 2),
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/health/perf")
async def perf_check():
    llm_vals = list(perf_snapshot["llm_ms"])
    sql_vals = list(perf_snapshot["sql_ms"])
    llm_avg = round(sum(llm_vals) / len(llm_vals), 2) if llm_vals else 0.0
    sql_avg = round(sum(sql_vals) / len(sql_vals), 2) if sql_vals else 0.0
    return {
        "status": "ok",
        "service": "vanna",
        "llm_recent_ms": llm_vals,
        "sql_recent_ms": sql_vals,
        "llm_avg_ms": llm_avg,
        "sql_avg_ms": sql_avg,
        "timestamp": datetime.utcnow().isoformat(),
    }
