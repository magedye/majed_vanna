from fastapi import APIRouter

from app.utils.logger import perf_snapshot
from app.utils.metrics import get_metrics_snapshot

router = APIRouter(prefix="/api", tags=["metrics"])


@router.get("/metrics")
def metrics():
    snapshot = get_metrics_snapshot()
    llm = list(perf_snapshot.get("llm_ms", []))
    sql = list(perf_snapshot.get("sql_ms", []))
    return {
        "counters": snapshot,
        "perf": {
            "llm_ms": llm,
            "sql_ms": sql,
            "llm_avg_ms": round(sum(llm) / len(llm), 2) if llm else None,
            "sql_avg_ms": round(sum(sql) / len(sql), 2) if sql else None,
        },
    }
