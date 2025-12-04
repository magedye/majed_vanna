from vanna import Agent
import time

from vanna.core.system_prompt import SystemPromptBuilder
from vanna.core.middleware import LlmMiddleware
from vanna.core.audit import AuditLogger, AuditEvent
from vanna.core.observability import ObservabilityProvider, Span

from app.agent.llm import llm
from app.agent.tools import tool_registry
from app.agent.memory import agent_memory
from app.agent.security import user_resolver
from app.agent.filters import conversation_filters
from app.agent.hooks import lifecycle_hooks
from app.agent.enrichers import context_enrichers
from app.agent.workflow import workflow_handler
from app.utils.logger import setup_logger, log_perf, record_perf_sample
from app.config import LLM_MAX_PROMPT_CHARS
from app.config import LLM_MAX_PROMPT_CHARS

class FileAuditLogger(AuditLogger):
    def __init__(self,path="audit.log"): self.path=path
    async def log_event(self,e:AuditEvent):
        with open(self.path,"a") as f: f.write(str(e.__dict__)+"\n")

perf_logger = setup_logger(__name__)

class LLMLog(LlmMiddleware):
    async def before_llm_request(self,r):
        r.metadata = r.metadata or {}
        r.metadata["perf_start"] = time.time()

        # Prompt size logging / limiting (protect system messages; trim oldest history first)
        messages = getattr(r, "messages", []) or []
        system_msgs = [m for m in messages if getattr(m, "role", "") == "system"]
        history_msgs = [m for m in messages if getattr(m, "role", "") != "system"]

        total_chars = sum(len(m.content or "") for m in messages if hasattr(m, "content"))
        system_chars = sum(len(m.content or "") for m in system_msgs if hasattr(m, "content"))

        truncated = False
        if total_chars > LLM_MAX_PROMPT_CHARS and history_msgs:
            budget = max(LLM_MAX_PROMPT_CHARS - system_chars, 0)
            kept = []
            # keep most recent history first, trimming from the oldest
            for m in reversed(history_msgs):
                content = getattr(m, "content", "") or ""
                if not content:
                    kept.append(m)
                    continue
                if len(content) <= budget:
                    budget -= len(content)
                    kept.append(m)
                else:
                    m.content = content[-budget:] if budget > 0 else ""
                    budget = 0
                    kept.append(m)
                    truncated = True
                    break
            history_msgs = list(reversed(kept))
            r.messages = system_msgs + history_msgs
        log_perf(
            perf_logger,
            "llm.prompt_size",
            {
                "messages": len(messages),
                "total_chars": total_chars,
                "system_chars": system_chars,
                "truncated": truncated,
                "limit": LLM_MAX_PROMPT_CHARS,
            },
        )
        return r
    async def after_llm_response(self,r,res):
        start = (r.metadata or {}).pop("perf_start", None)
        if start:
            duration_ms = round((time.time() - start) * 1000, 2)
            log_perf(
                perf_logger,
                "llm.roundtrip",
                {
                    "duration_ms": duration_ms,
                    "model": getattr(getattr(res, "model", None), "name", None)
                    or getattr(r, "model", None),
                    "request_id": getattr(r, "request_id", None),
                    "conversation_id": getattr(r, "conversation_id", None),
                },
            )
            record_perf_sample("llm_ms", duration_ms)
        return res

class Prompt(SystemPromptBuilder):
    async def build_system_prompt(self, user, tools, conversation=None):
        tz = user.metadata.get("timezone", "UTC")
        email = getattr(user, "email", "unknown")
        return f"User:{email}\nTimezone:{tz}"

class DummyObservability(ObservabilityProvider):
    async def record_metric(
        self, name, value, unit="", tags=None
    ):
        return None

    async def create_span(self, name, attributes=None):
        return Span(name=name, attributes=attributes or {})

    async def end_span(self, span: Span) -> None:
        span.end()


observability = DummyObservability()

agent=Agent(
 llm_service=llm,
 tool_registry=tool_registry,
 user_resolver=user_resolver,
 agent_memory=agent_memory,
 workflow_handler=workflow_handler,
 llm_middlewares=[LLMLog()],
 lifecycle_hooks=lifecycle_hooks,
 context_enrichers=context_enrichers,
 conversation_filters=conversation_filters,
 system_prompt_builder=Prompt(),
 observability_provider=observability,
 audit_logger=FileAuditLogger()
)
