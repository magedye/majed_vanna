import asyncio
import json
import time
from pathlib import Path

from vanna import Agent
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
from app.utils.logger import setup_logger, log_perf, record_perf_sample, get_trace_ids
import app.agent.db as agent_db
from app.config import (
    LLM_MAX_PROMPT_CHARS,
    LLM_CONFIG,
    LLM_PROVIDER,
    LLM_TIMEOUT_MS,
    LLM_MAX_RETRIES,
    LLM_RETRY_BACKOFF_MS,
)
from app.agent.implementation import LocalVanna
from dbt_integration.semantic_adapter import semantic_loader
from dbt_integration.dbt_loader import DbtMetadataProvider
from app.circuit_breaker import CircuitBreaker

class FileAuditLogger(AuditLogger):
    def __init__(self, path: str = "audit.log"):
        self.path = Path(path)

    async def log_event(self, e: AuditEvent):
        """Persist audit events without breaking the main flow on encoding errors."""
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            payload = json.dumps(e.__dict__, ensure_ascii=False, default=str)
            with open(self.path, "a", encoding="utf-8", errors="replace") as f:
                f.write(payload + "\n")
        except Exception:
            try:
                with open(self.path, "a", encoding="utf-8", errors="ignore") as f:
                    f.write(f"{e}\n")
            except Exception:
                # Never allow audit logging failures to bubble up
                pass

perf_logger = setup_logger(__name__)
llm_circuit = CircuitBreaker("llm", failure_threshold=3, reset_timeout=30)
kb_config = {
    "path": "./chroma_db",
    "api_key": "lm-studio",
    "api_base": LLM_CONFIG.get(LLM_PROVIDER, {}).get("base_url", "http://localhost:1234/v1"),
    "model": LLM_CONFIG.get(LLM_PROVIDER, {}).get("model", "gemma-3n"),
}
knowledge_base = LocalVanna(config=kb_config)
dbt_provider = DbtMetadataProvider(
    manifest_path=Path("dbt/target/manifest.json"),
    catalog_path=Path("dbt/target/catalog.json"),
    run_results_path=Path("dbt/target/run_results.json"),
    provider="oracle",
    context_limit=4000,
)
try:
    dbt_provider.load()
except Exception as e:
    print(f"[DBT] load skipped: {e}")


def _collect_schema_text(limit_chars: int = 12000) -> str:
    try:
        df = knowledge_base.get_training_data()
        if df is None or df.empty:
            return ""
        if "type" in df.columns and "text" in df.columns:
            ddls = df[df["type"] == "ddl"]["text"].dropna().tolist()
        elif "sql" in df.columns:
            ddls = df["sql"].dropna().tolist()
        else:
            ddls = df.to_string().splitlines()
        schema = "\n\n".join(ddls)
        if len(schema) > limit_chars:
            schema = schema[:limit_chars]
        return schema
    except Exception as e:
        log_perf(perf_logger, "schema.load.error", {"error": str(e)})
        return ""

class LLMLog(LlmMiddleware):
    async def before_llm_request(self,r):
        if not llm_circuit._can_pass():
            raise RuntimeError("CircuitBreaker[llm] is OPEN")
        r.metadata = r.metadata or {}
        r.metadata["perf_start"] = time.time()

        # Schema injection
        messages = getattr(r, "messages", []) or []
        if messages:
            user_msg = messages[-1]
            content = getattr(user_msg, "content", "") or ""
            schema_text = _collect_schema_text()
            semantic_text = semantic_loader.build_context()
            dbt_text = ""
            try:
                dbt_text = dbt_provider.build_context()
            except Exception:
                dbt_text = ""
            allowed_tables = []
            try:
                allowed_tables = sorted(agent_db._load_allowed_tables())
            except Exception:
                allowed_tables = []
            blocks = []
            if dbt_text:
                blocks.append(f"DBT metadata:\n{dbt_text}")
            if semantic_text:
                blocks.append(semantic_text)
            if schema_text:
                blocks.append(f"Use this schema:\n{schema_text}")
            if allowed_tables:
                blocks.append(
                    "Oracle guardrails:\n"
                    f"- Allowed tables only: {', '.join(allowed_tables)}\n"
                    "- Do NOT use PRAGMA (SQLite-only).\n"
                    "- Use SELECT/DESCRIBE/EXPLAIN; avoid invented table names."
                )
            if content:
                blocks.append(f"Question: {content}")
            user_msg.content = "\n\n".join(blocks)

        # Prompt size logging / limiting (protect system messages; trim oldest history first)
        system_msgs = [m for m in messages if getattr(m, "role", "") == "system"]
        history_msgs = [m for m in messages if getattr(m, "role", "") != "system"]

        total_chars = sum(len(m.content or "") for m in messages if hasattr(m, "content"))
        system_chars = sum(len(m.content or "") for m in system_msgs if hasattr(m, "content"))

        truncated = False
        if total_chars > LLM_MAX_PROMPT_CHARS and history_msgs:
            truncated = True
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
                    break
            history_msgs = list(reversed(kept))
            r.messages = system_msgs + history_msgs

        if truncated:
            # Hard fallback: drop old history to guarantee valid tool JSON
            last_user_msg = next(
                (m for m in reversed(messages) if getattr(m, "role", "") == "user"),
                None,
            )
            fallback_msgs = list(system_msgs)
            if last_user_msg:
                question = getattr(last_user_msg, "content", "") or ""
                schema_text = _collect_schema_text()
                semantic_text = semantic_loader.build_context()
                parts = []
                if semantic_text:
                    parts.append(semantic_text)
                if schema_text:
                    parts.append(f"Use this schema:\n{schema_text}")
                if question:
                    parts.append(f"Question: {question}")
                parts.append(
                    "Respond with a single JSON tool call only. Do not include prose or multiple calls."
                )
                last_user_msg.content = "\n\n".join(parts)
                fallback_msgs.append(last_user_msg)
            r.messages = fallback_msgs
        log_perf(
            perf_logger,
            "llm.prompt_size",
            {
                "messages": len(messages),
                "total_chars": total_chars,
                "system_chars": system_chars,
                "truncated": truncated,
                "limit": LLM_MAX_PROMPT_CHARS,
                "trace_id": get_trace_ids()[0],
            },
        )
        return r
    async def after_llm_response(self,r,res):
        llm_circuit._on_success()
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
                    "trace_id": get_trace_ids()[0],
                },
            )
            record_perf_sample("llm_ms", duration_ms)
        return res

    async def on_llm_error(self, r, exc):
        llm_circuit._on_failure()
        raise exc

    async def run_with_timeout(self, coro):
        last_exc = None
        for attempt in range(LLM_MAX_RETRIES + 1):
            try:
                return await asyncio.wait_for(coro, timeout=LLM_TIMEOUT_MS / 1000)
            except Exception as exc:
                last_exc = exc
                if attempt >= LLM_MAX_RETRIES:
                    llm_circuit._on_failure()
                    raise
                await asyncio.sleep(LLM_RETRY_BACKOFF_MS / 1000)
        if last_exc:
            raise last_exc

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
