import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vanna.servers.fastapi import VannaFastAPIServer
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.api import system_ops, memory_ui_handler
from app.agent.builder import agent
from app.agent.port_guard import find_available_port
from app.agent.input_validation import InputValidationMiddleware, SafeChatHandler
from app.api.error_handlers import register_exception_handlers
from app.api.rate_limit import RateLimitMiddleware
from app.config import (
    HOST,
    PORT,
    DEBUG,
    DB_PROVIDER,
    DB_SQLITE,
    LLM_CONFIG,
    LLM_PROVIDER,
    RATE_LIMIT_MAX_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
)
from app.runtime import update_runtime

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
    app.add_middleware(InputValidationMiddleware)
    app.add_middleware(
        RateLimitMiddleware,
        max_requests=RATE_LIMIT_MAX_REQUESTS,
        window_seconds=RATE_LIMIT_WINDOW_SECONDS,
    )
    app.include_router(api_router, prefix="/api")
    app.include_router(system_ops.router)
    app.include_router(memory_ui_handler.router)
    register_exception_handlers(app)

    port = find_available_port(PORT) if DEBUG else PORT
    if DEBUG:
        print(f"[DEBUG] find_available_port scanned starting at {PORT}, selected {port}")

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

    server.create_app = lambda: app
    server.run(host=HOST, port=port)

if __name__=="__main__":
    start()
