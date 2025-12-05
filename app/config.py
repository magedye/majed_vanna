import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PROVIDER = os.getenv("DB_PROVIDER", "sqlite").lower()
DB_SQLITE = os.getenv("SQLITE_DB", str(DATA_DIR / "mydb.db"))
DB_ORACLE_DSN = os.getenv("DB_ORACLE_DSN", "")
ORACLE_USER = os.getenv("ORACLE_USER", "")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "")
ORACLE_DSN = os.getenv("ORACLE_DSN", "")
ORACLE_SCHEMA = os.getenv("ORACLE_SCHEMA", ORACLE_USER)
ORACLE_ENABLE_POOL = os.getenv("ORACLE_ENABLE_POOL", "false").lower() == "true"
ORACLE_POOL_MIN = int(os.getenv("ORACLE_POOL_MIN", 1))
ORACLE_POOL_MAX = int(os.getenv("ORACLE_POOL_MAX", 4))
ORACLE_POOL_INCREMENT = int(os.getenv("ORACLE_POOL_INCREMENT", 1))
ORACLE_TRAIN_OBJECTS = os.getenv("ORACLE_TRAIN_OBJECTS", "TABLES,VIEWS").upper().split(",")
ORACLE_TRAIN_TABLES = os.getenv("ORACLE_TRAIN_TABLES", "ALL").upper().split(",")
DB_MSSQL_CONN = os.getenv("DB_MSSQL_CONN", "")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "lmstudio").lower()
LLM_MAX_PROMPT_CHARS = int(os.getenv("LLM_MAX_PROMPT_CHARS", 12000))
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

if DB_PROVIDER == "oracle":
    has_dsn_string = bool(DB_ORACLE_DSN)
    has_split_creds = bool(ORACLE_USER and ORACLE_PASSWORD and (ORACLE_DSN or ORACLE_SCHEMA))
    if not (has_dsn_string or has_split_creds):
        raise RuntimeError(
            "Oracle configuration requires DB_ORACLE_DSN or ORACLE_USER/ORACLE_PASSWORD/ORACLE_DSN"
        )
if DB_PROVIDER == "mssql" and not DB_MSSQL_CONN:
    raise RuntimeError("DB_MSSQL_CONN is required when DB_PROVIDER=mssql")

if LLM_PROVIDER not in LLM_CONFIG:
    raise RuntimeError(
        f"Unsupported LLM_PROVIDER: {LLM_PROVIDER!r}. "
        f"Available options: {', '.join(sorted(LLM_CONFIG.keys()))}"
    )

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 7777))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
WORKERS = int(os.getenv("WORKERS", 1))

AGENT_MEMORY_MAX_ITEMS = int(os.getenv("AGENT_MEMORY_MAX_ITEMS", 1000))
RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", 60))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", 60))
