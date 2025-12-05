import hashlib
import json
from typing import Any

import redis

from app.config import REDIS_HOST, REDIS_PORT, CACHE_TTL_SECONDS, CACHE_ENABLED
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

CACHE_AVAILABLE = False
counters = {"cache_hit": 0, "cache_miss": 0, "cache_failures": 0}

_client = None

if CACHE_ENABLED:
    try:
        _client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        _client.ping()
        CACHE_AVAILABLE = True
    except Exception as exc:
        logger.info("cache.disabled", extra={"extra_data": {"reason": str(exc)}})
        CACHE_AVAILABLE = False
        _client = None


def make_cache_key(user_id: str, question: str, ddl_context: str, conversation_id: str):
    digest = hashlib.sha256(f"{question}{ddl_context}{conversation_id}".encode("utf-8")).hexdigest()
    return f"vanna_cache:{user_id}:{digest}"


def get_cached_response(key: str):
    if not (CACHE_ENABLED and CACHE_AVAILABLE and _client):
        return None
    try:
        raw = _client.get(key)
        if not raw:
            counters["cache_miss"] += 1
            return None
        counters["cache_hit"] += 1
        return json.loads(raw)
    except Exception as exc:
        counters["cache_failures"] += 1
        _auto_disable(exc)
        return None


def set_cached_response(key: str, value: Any, ttl: int = CACHE_TTL_SECONDS):
    if not (CACHE_ENABLED and CACHE_AVAILABLE and _client):
        return None
    try:
        _client.setex(key, ttl, json.dumps(value))
    except Exception as exc:
        counters["cache_failures"] += 1
        _auto_disable(exc)
        return None


def _auto_disable(exc: Exception):
    global CACHE_AVAILABLE
    if CACHE_AVAILABLE:
        CACHE_AVAILABLE = False
        logger.info("cache.auto_disabled", extra={"extra_data": {"reason": str(exc)}})


def cache_stats():
    return {**counters, "enabled": CACHE_ENABLED, "available": CACHE_AVAILABLE}
