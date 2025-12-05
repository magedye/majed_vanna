import shutil
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"
BACKUP_DIR = BASE_DIR / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def backup_chroma(name: str = "chroma_backup.zip") -> Path:
    target = BACKUP_DIR / name
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        if CHROMA_DIR.exists():
            for path in CHROMA_DIR.rglob("*"):
                if path.is_file():
                    zf.write(path, path.relative_to(BASE_DIR))
    return target


def purge_chroma():
    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)


def refresh_chroma():
    backup_chroma()
    purge_chroma()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ChromaDB maintenance utility")
    parser.add_argument("--backup", action="store_true", help="Create a zip backup of chroma_db")
    parser.add_argument("--purge", action="store_true", help="Delete and recreate chroma_db")
    parser.add_argument("--refresh", action="store_true", help="Backup then purge chroma_db")
    args = parser.parse_args()

    if args.refresh:
        p = backup_chroma()
        purge_chroma()
        print(f"Refreshed. Backup: {p}")
    elif args.backup:
        p = backup_chroma()
        print(f"Backup created: {p}")
    elif args.purge:
        purge_chroma()
        print("Purged chroma_db.")
    else:
        parser.print_help()
