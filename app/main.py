import os
import sys
from pathlib import Path
from typing import Any, Dict
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vanna.servers.fastapi import VannaFastAPIServer
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.api import system_ops, memory_ui_handler, semantic, metrics
from app.agent.builder import agent
from app.agent.input_validation import InputValidationMiddleware, SafeChatHandler
from app.api.error_handlers import register_exception_handlers
from app.api.rate_limit import RateLimitMiddleware
from app.middlewares.error_handler import JsonErrorMiddleware
from app.middlewares.trace_context import TraceContextMiddleware
from app.middlewares.slow_detector import SlowRequestMiddleware
from app.middlewares.security_headers import SecurityHeadersMiddleware
from app.agent.db import close_db
from app.config import (
    HOST,
    DEBUG,
    DB_PROVIDER,
    DB_SQLITE,
    LLM_CONFIG,
    LLM_PROVIDER,
    RATE_LIMIT_MAX_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
    MAX_PAYLOAD_SIZE_BYTES,
)
from app.runtime import update_runtime


class PayloadLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        body = await request.body()
        if len(body) > MAX_PAYLOAD_SIZE_BYTES:
            return JSONResponse(
                status_code=413, content={"detail": "Payload too large"}
            )
        request._body = body
        return await call_next(request)


def start():
    config: Dict[str, Any] = {
        "cors": {
            "enabled": True,
            "allow_origins": ["*"],
            "allow_credentials": False,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        },
        "dev_mode": DEBUG,
        "static_folder": "static",
    }
    server = VannaFastAPIServer(agent=agent, config=config)
    server.chat_handler = SafeChatHandler(agent)
    app = server.create_app()
    app.mount("/charts", StaticFiles(directory="app/static/charts"), name="charts")
    app.add_middleware(PayloadLimitMiddleware)
    app.add_middleware(JsonErrorMiddleware)
    app.add_middleware(TraceContextMiddleware)
    app.add_middleware(SlowRequestMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(InputValidationMiddleware)
    app.add_middleware(
        RateLimitMiddleware,
        max_requests=RATE_LIMIT_MAX_REQUESTS,
        window_seconds=RATE_LIMIT_WINDOW_SECONDS,
    )
    app.include_router(api_router, prefix="/api")
    app.include_router(system_ops.router)
    app.include_router(memory_ui_handler.router)
    app.include_router(semantic.router)
    app.include_router(metrics.router)
    register_exception_handlers(app)

    port = int(os.getenv("APP_PORT", "7777"))

    update_runtime(
        llm_provider=LLM_PROVIDER,
        db_provider=DB_PROVIDER,
        port=str(port),
        debug=str(DEBUG),
        sqlite_path=DB_SQLITE if DB_PROVIDER == "sqlite" else None,
    )

    model_name = LLM_CONFIG.get(LLM_PROVIDER, {}).get("model", "unknown")
    print("Starting Vanna agent")
    print(f"  Environment: {'debug' if DEBUG else 'production'}")
    print(f"  Host/Port: {HOST}:{port}")
    print(f"  LLM Provider: {LLM_PROVIDER} ({model_name})")
    print(f"  DB Provider: {DB_PROVIDER} (sqlite path={DB_SQLITE if DB_PROVIDER == 'sqlite' else 'n/a'})")

    async def lifespan(app):
        try:
            yield
        finally:
            close_db()

    server.create_app = lambda: app
    app.router.lifespan_context = asynccontextmanager(lifespan)
    server.run(host=HOST, port=port)

if __name__=="__main__":
    start()
