import os
import shutil
import time

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/system", tags=["System Management"])

BASE_DIR = os.getcwd()
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")
BACKUP_PATH = os.path.join(BASE_DIR, "backups")

os.makedirs(BACKUP_PATH, exist_ok=True)


@router.post("/backup-memory")
def backup_memory():
    """Creates a timestamped backup of the ChromaDB folder."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    target = os.path.join(BACKUP_PATH, f"chroma_backup_{timestamp}")

    try:
        if not os.path.exists(CHROMA_PATH):
            raise HTTPException(404, "No ChromaDB found to back up.")

        shutil.copytree(CHROMA_PATH, target)
        return {"status": "success", "path": target}

    except Exception as e:
        raise HTTPException(500, f"Backup failed: {str(e)}")


@router.delete("/reset-memory")
def reset_memory(force: bool = False):
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

    # Perform deletion
    try:
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)

        os.makedirs(CHROMA_PATH, exist_ok=True)

        return {
            "status": "success",
            "message": "Memory successfully reset. Restart backend.",
        }

    except PermissionError:
        raise HTTPException(500, "Folder locked. Close terminal & retry.")
    except Exception as e:
        raise HTTPException(500, str(e))
