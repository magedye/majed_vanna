from app.config import LLM_PROVIDER, LLM_CONFIG, CACHE_TTL_SECONDS, CACHE_ENABLED
from vanna.integrations.openai import OpenAILlmService
from app.utils.cache import make_cache_key, get_cached_response, set_cached_response
from app.utils.logger import setup_logger, log_perf

logger = setup_logger(__name__)


class CachedOpenAILlmService(OpenAILlmService):
    async def send_request(self, request):
        if not CACHE_ENABLED:
            return await super().send_request(request)
        # Extract basic identifiers
        user = getattr(request, "user", None)
        user_id = getattr(user, "id", "anonymous")
        conversation_id = getattr(request, "conversation_id", "none")
        messages = getattr(request, "messages", []) or []
        question = ""
        if messages:
            question = getattr(messages[-1], "content", "") or ""
        # Try to collect schema/semantic context text (last system message heuristic)
        ddl_ctx = ""
        if messages:
            for m in reversed(messages):
                if getattr(m, "role", "") == "system" and getattr(m, "content", ""):
                    ddl_ctx = m.content
                    break

        cache_key = make_cache_key(user_id, question, ddl_ctx, str(conversation_id))
        cached = get_cached_response(cache_key)
        if cached:
            log_perf(logger, "llm.cache_hit", {"user": user_id, "conversation_id": conversation_id})
            return cached

        response = await super().send_request(request)
        try:
            # safety: avoid caching errors/short queries
            if (
                CACHE_ENABLED
                and question
                and len(question.split()) >= 3
                and isinstance(response, dict)
                and response.get("error") is None
            ):
                set_cached_response(cache_key, response, ttl=CACHE_TTL_SECONDS)
                log_perf(logger, "llm.cache_store", {"user": user_id, "conversation_id": conversation_id})
        except Exception:
            pass
        return response


def get_llm():
    cfg=LLM_CONFIG[LLM_PROVIDER]
    if LLM_PROVIDER=="lmstudio":
        return CachedOpenAILlmService(model=cfg["model"], base_url=cfg["base_url"], api_key=cfg["api_key"])
    if LLM_PROVIDER=="openai":
        return CachedOpenAILlmService(model=cfg["model"], api_key=cfg["api_key"])
    if LLM_PROVIDER=="groq":
        return CachedOpenAILlmService(model=cfg["model"], api_key=cfg["api_key"], base_url="https://api.groq.com/openai/v1")
    if LLM_PROVIDER=="gemini":
        return CachedOpenAILlmService(model=cfg["model"], api_key=cfg["api_key"], base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
llm=get_llm()
