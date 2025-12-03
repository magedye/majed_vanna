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

class FileAuditLogger(AuditLogger):
    def __init__(self,path="audit.log"): self.path=path
    async def log_event(self,e:AuditEvent):
        with open(self.path,"a") as f: f.write(str(e.__dict__)+"\n")

class LLMLog(LlmMiddleware):
    async def before_llm_request(self,r): print("[LLM-REQ]"); return r
    async def after_llm_response(self,r,res): print("[LLM-RESP]"); return res

class Prompt(SystemPromptBuilder):
    async def build_system_prompt(self,u,t,c):
        return f"User:{u.email}\nTimezone:{c.get('timezone')}"

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
