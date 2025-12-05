import os
from fastapi import APIRouter
import requests

router = APIRouter(prefix="/api/system", tags=["UI Memory Ops"])


@router.post("/execute-memory-op")
def execute_memory_op(action: str, force: bool = False):
    base = f"http://localhost:{os.getenv('APP_PORT', '7777')}"
    if action == "Backup":
        res = requests.post(f"{base}/api/system/backup-memory")
        return res.json()

    if action == "Reset":
        res = requests.delete(
            f"{base}/api/system/reset-memory?force={'true' if force else 'false'}"
        )
        return res.json()

    return {"status": "error", "message": "Invalid action"}
