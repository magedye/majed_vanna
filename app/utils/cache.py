import hashlib
import json

import redis

from app.config import REDIS_HOST, REDIS_PORT, CACHE_TTL_SECONDS


_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def make_cache_key(user_id: str, question: str, ddl_context: str, conversation_id: str):
    digest = hashlib.sha256(f"{question}{ddl_context}{conversation_id}".encode("utf-8")).hexdigest()
    return f"vanna_cache:{user_id}:{digest}"


def get_cached_response(key: str):
    try:
        raw = _client.get(key)
        if not raw:
            return None
        return json.loads(raw)
    except Exception:
        return None


def set_cached_response(key: str, value, ttl: int = CACHE_TTL_SECONDS):
    try:
        _client.setex(key, ttl, json.dumps(value))
    except Exception:
        return None
