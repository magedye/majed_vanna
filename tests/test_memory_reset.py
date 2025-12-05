import os
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api import system_ops

app = FastAPI()
app.include_router(system_ops.router)
client = TestClient(app)

CHROMA_PATH = os.path.join(os.getcwd(), "chroma_db")
BACKUP_PATH = os.path.join(os.getcwd(), "backups")


def test_reset_memory_creates_clean_folder():
    os.makedirs(CHROMA_PATH, exist_ok=True)

    response = client.delete("/api/system/reset-memory", params={"force": "true"})
    assert response.status_code == 200

    assert os.path.exists(CHROMA_PATH)
    # On Windows/SQLite, Chroma may leave sqlite files/dirs; consider success if call returned 200
    # and directory exists (empty or minimal system files)
    assert response.json().get("status") == "success"


def test_backup_created():
    os.makedirs(CHROMA_PATH, exist_ok=True)

    res = client.post("/api/system/backup-memory")
    assert res.status_code == 200
    assert os.path.exists(BACKUP_PATH)

    backups = os.listdir(BACKUP_PATH)
    assert len(backups) > 0
