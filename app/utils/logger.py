import logging
from collections import deque
from typing import Dict, Any, Deque

PERF_HISTORY = 50
perf_snapshot: Dict[str, Deque[float]] = {
    "llm_ms": deque(maxlen=PERF_HISTORY),
    "sql_ms": deque(maxlen=PERF_HISTORY),
}


def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger


def log_perf(logger: logging.Logger, event: str, data: Dict[str, Any]):
    """Lightweight performance log without sensitive payloads."""
    safe = {k: v for k, v in data.items() if v is not None}
    logger.info(f"{event} | {safe}")


def record_perf_sample(kind: str, duration_ms: float):
    if kind in perf_snapshot:
        perf_snapshot[kind].append(duration_ms)
