from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api import semantic


def build_app():
    app = FastAPI()
    app.include_router(semantic.router)
    return app


client = TestClient(build_app())


def test_semantic_docs_endpoint():
    res = client.get("/api/semantic/docs")
    assert res.status_code == 200
    body = res.json()
    assert "content" in body
    assert "toc" in body


def test_semantic_search_endpoint():
    res = client.get("/api/semantic/search", params={"query": "semantic"})
    assert res.status_code == 200
    body = res.json()
    assert body.get("query") == "semantic"
    assert "results" in body
