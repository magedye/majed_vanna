import os
import shutil
import time

import chromadb
from chromadb.config import Settings
from fastapi import APIRouter, HTTPException, Request

from app.utils.logger import setup_logger, get_trace_ids

router = APIRouter(prefix="/api/system", tags=["System Management"])

BASE_DIR = os.getcwd()
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")
BACKUP_PATH = os.path.join(BASE_DIR, "backups")

os.makedirs(BACKUP_PATH, exist_ok=True)

logger = setup_logger(__name__)


def _require_admin(request: Request):
    email = request.cookies.get("vanna_email") or request.headers.get("vanna_email")
    if email != "admin@example.com":
        raise HTTPException(status_code=403, detail="Forbidden")
    return email


@router.post("/backup-memory")
def backup_memory(request: Request):
    user = _require_admin(request)
    """Creates a timestamped backup of the ChromaDB folder."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    target = os.path.join(BACKUP_PATH, f"chroma_backup_{timestamp}")

    try:
        if not os.path.exists(CHROMA_PATH):
            raise HTTPException(404, "No ChromaDB found to back up.")

        shutil.copytree(CHROMA_PATH, target)
        trace_id, _ = get_trace_ids()
        logger.info("backup.success", extra={"extra_data": {"trace_id": trace_id, "user": user, "path": target}})
        return {"status": "success", "path": target, "trace_id": trace_id, "user": user}

    except Exception as e:
        trace_id, _ = get_trace_ids()
        logger.info("backup.failure", extra={"extra_data": {"trace_id": trace_id, "user": user, "error": str(e)}})
        raise HTTPException(500, f"Backup failed: {str(e)}")


@router.delete("/reset-memory")
def reset_memory(request: Request, force: bool = False):
    user = _require_admin(request)
    """
    Reset local memory safely.
    Requires: /api/system/reset-memory?force=true
    """
    if not force:
        return {
            "status": "warning",
            "message": "Pass force=true to confirm (this deletes memory permanently).",
        }

    # Attempt auto-backup
    if os.path.exists(CHROMA_PATH):
        try:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            backup_target = os.path.join(BACKUP_PATH, f"pre_reset_{timestamp}")
            shutil.copytree(CHROMA_PATH, backup_target)
        except Exception as e:
            print(f"[WARNING] Pre-reset backup failed: {e}")

    # Perform reset via Chroma client to avoid file-lock issues; if reset disabled, drop collections
    try:
        client = chromadb.PersistentClient(
            path=CHROMA_PATH, settings=Settings(anonymized_telemetry=False)
        )
        try:
            client.reset()
        except Exception:
            # If reset is disabled, delete collections individually
            for col in client.list_collections():
                client.delete_collection(col.name)
        os.makedirs(CHROMA_PATH, exist_ok=True)
        trace_id, _ = get_trace_ids()
        logger.info("reset.success", extra={"extra_data": {"trace_id": trace_id, "user": user}})
        return {
            "status": "success",
            "message": "Memory successfully reset. Restart backend.",
            "trace_id": trace_id,
            "user": user,
        }

    except PermissionError as e:
        trace_id, _ = get_trace_ids()
        logger.info("reset.failure", extra={"extra_data": {"trace_id": trace_id, "user": user, "error": str(e)}})
        raise HTTPException(500, "Folder locked. Close terminal & retry.")
    except Exception as e:
        trace_id, _ = get_trace_ids()
        logger.info("reset.failure", extra={"extra_data": {"trace_id": trace_id, "user": user, "error": str(e)}})
        raise HTTPException(500, str(e))
