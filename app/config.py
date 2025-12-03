import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PROVIDER = os.getenv("DB_PROVIDER", "sqlite").lower()
DB_SQLITE = os.getenv("SQLITE_DB", str(DATA_DIR / "mydb.db"))
DB_ORACLE_DSN = os.getenv("DB_ORACLE_DSN", "user/password@host:1521/service")
DB_MSSQL_CONN = os.getenv(
    "DB_MSSQL_CONN",
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=master;UID=sa;PWD=Password123",
)

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "lmstudio").lower()
LLM_CONFIG = {
    "lmstudio": {
        "base_url": os.getenv("LM_STUDIO_URL", "http://10.10.10.1:1234/v1"),
        "model": os.getenv("LM_STUDIO_MODEL", "gemma-3n"),
        "api_key": "lm-studio",
    },
    "openai": {
        "api_key": os.getenv("OPENAI_API_KEY", "NONE"),
        "model": os.getenv("OPENAI_MODEL", "gpt-4-turbo"),
    },
    "groq": {
        "api_key": os.getenv("GROQ_API_KEY", "NONE"),
        "model": os.getenv("GROQ_MODEL", "mixtral-8x7b-32768"),
    },
    "gemini": {
        "api_key": os.getenv("GEMINI_API_KEY", "NONE"),
        "model": os.getenv("GEMINI_MODEL", "gemini-pro"),
    },
}

SUPPORTED_DB_PROVIDERS = {"sqlite", "oracle", "mssql"}
if DB_PROVIDER not in SUPPORTED_DB_PROVIDERS:
    raise RuntimeError(
        f"Unsupported DB_PROVIDER: {DB_PROVIDER!r}. "
        f"Available options: {', '.join(sorted(SUPPORTED_DB_PROVIDERS))}"
    )

if LLM_PROVIDER not in LLM_CONFIG:
    raise RuntimeError(
        f"Unsupported LLM_PROVIDER: {LLM_PROVIDER!r}. "
        f"Available options: {', '.join(sorted(LLM_CONFIG.keys()))}"
    )

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
WORKERS = int(os.getenv("WORKERS", 1))

AGENT_MEMORY_MAX_ITEMS = int(os.getenv("AGENT_MEMORY_MAX_ITEMS", 1000))
