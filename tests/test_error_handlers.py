import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from app.api.error_handlers import register_exception_handlers


def create_app():
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/boom")
    async def boom():
        raise HTTPException(status_code=500, detail="secret")

    @app.get("/bad")
    async def bad():
        raise HTTPException(status_code=400, detail="bad")

    return app


def test_error_handler_500_masks_detail():
    app = create_app()
    client = TestClient(app)
    res = client.get("/boom")
    assert res.status_code == 500
    assert res.json()["detail"] in {"Internal server error. Please try again later.", "An error occurred."}


def test_error_handler_400_passthrough():
    app = create_app()
    client = TestClient(app)
    res = client.get("/bad")
    assert res.status_code == 400
    assert res.json()["detail"] == "bad"
