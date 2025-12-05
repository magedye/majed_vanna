import json
import logging
from collections import deque
from contextvars import ContextVar
from typing import Dict, Any, Deque

from uuid import uuid4

PERF_HISTORY = 50
perf_snapshot: Dict[str, Deque[float]] = {
    "llm_ms": deque(maxlen=PERF_HISTORY),
    "sql_ms": deque(maxlen=PERF_HISTORY),
}

trace_id_ctx: ContextVar[str | None] = ContextVar("trace_id", default=None)
span_id_ctx: ContextVar[str | None] = ContextVar("span_id", default=None)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base = {
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "time": self.formatTime(record, self.datefmt),
            "trace_id": trace_id_ctx.get(),
            "span_id": span_id_ctx.get(),
        }
        extra_data = getattr(record, "extra_data", None)
        if isinstance(extra_data, dict):
            for k, v in extra_data.items():
                try:
                    json.dumps(v)
                    base[k] = v
                except TypeError:
                    base[k] = str(v)
        return json.dumps(base, ensure_ascii=False)


def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = JsonFormatter()
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    logger.propagate = False
    return logger


def log_perf(logger: logging.Logger, event: str, data: Dict[str, Any]):
    """Lightweight performance log without sensitive payloads."""
    safe = {k: v for k, v in data.items() if v is not None}
    logger.info(event, extra={"extra_data": {"event": event, **safe}})


def record_perf_sample(kind: str, duration_ms: float):
    if kind in perf_snapshot:
        perf_snapshot[kind].append(duration_ms)


def set_trace_context(trace_id: str | None = None, span_id: str | None = None):
    if trace_id is None:
        trace_id = str(uuid4())
    if span_id is None:
        span_id = str(uuid4())
    trace_id_ctx.set(trace_id)
    span_id_ctx.set(span_id)
    return trace_id, span_id


def get_trace_ids():
    return trace_id_ctx.get(), span_id_ctx.get()
