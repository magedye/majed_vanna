from fastapi import APIRouter
import requests

router = APIRouter(prefix="/api/system", tags=["UI Memory Ops"])


@router.post("/execute-memory-op")
def execute_memory_op(action: str, force: bool = False):
    if action == "Backup":
        res = requests.post("http://localhost:8000/api/system/backup-memory")
        return res.json()

    if action == "Reset":
        res = requests.delete(
            f"http://localhost:8000/api/system/reset-memory?force={'true' if force else 'false'}"
        )
        return res.json()

    return {"status": "error", "message": "Invalid action"}
