import os
from fastapi.testclient import TestClient
from vanna.servers.fastapi import VannaFastAPIServer
from fastapi.staticfiles import StaticFiles

from app.agent.builder import agent
from app.agent.input_validation import InputValidationMiddleware, SafeChatHandler
from app.api.router import api_router
from app.api import system_ops, memory_ui_handler
from app.api.error_handlers import register_exception_handlers
from app.api.rate_limit import RateLimitMiddleware
from app.config import (
    DEBUG,
    RATE_LIMIT_MAX_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
)


def build_app():
    server = VannaFastAPIServer(agent=agent, config={"dev_mode": DEBUG, "static_folder": "static"})
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
    return app


client = TestClient(build_app())

CHROMA_PATH = os.path.join(os.getcwd(), "chroma_db")
BACKUP_PATH = os.path.join(os.getcwd(), "backups")


def test_reset_memory_creates_clean_folder():
    os.makedirs(CHROMA_PATH, exist_ok=True)

    response = client.delete("/api/system/reset-memory?force=true")
    assert response.status_code == 200

    assert os.path.exists(CHROMA_PATH)
    assert os.listdir(CHROMA_PATH) == []  # must be empty


def test_backup_created():
    os.makedirs(CHROMA_PATH, exist_ok=True)

    res = client.post("/api/system/backup-memory")
    assert res.status_code == 200
    assert os.path.exists(BACKUP_PATH)

    backups = os.listdir(BACKUP_PATH)
    assert len(backups) > 0
