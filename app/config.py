import os
from dotenv import load_dotenv
load_dotenv()

DB_PROVIDER=os.getenv("DB_PROVIDER","sqlite").lower()
DB_SQLITE=os.getenv("SQLITE_DB", r"D:\mydb.db")
DB_ORACLE_DSN=os.getenv("DB_ORACLE_DSN","user/password@host:1521/service")
DB_MSSQL_CONN=os.getenv("DB_MSSQL_CONN","DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=master;UID=sa;PWD=Password123")

LLM_PROVIDER=os.getenv("LLM_PROVIDER","lmstudio").lower()
LLM_CONFIG={
 "lmstudio":{"base_url":os.getenv("LM_STUDIO_URL","http://10.10.10.1:1234/v1"),"model":os.getenv("LM_STUDIO_MODEL","gemma-3n"),"api_key":"lm-studio"},
 "openai":{"api_key":os.getenv("OPENAI_API_KEY","NONE"),"model":os.getenv("OPENAI_MODEL","gpt-4-turbo")},
 "groq":{"api_key":os.getenv("GROQ_API_KEY","NONE"),"model":os.getenv("GROQ_MODEL","mixtral-8x7b-32768")},
 "gemini":{"api_key":os.getenv("GEMINI_API_KEY","NONE"),"model":os.getenv("GEMINI_MODEL","gemini-pro")}
}

HOST=os.getenv("HOST","0.0.0.0")
PORT=int(os.getenv("PORT",8000))
DEBUG=os.getenv("DEBUG","false").lower()=="true"
WORKERS=int(os.getenv("WORKERS",1))

AGENT_MEMORY_MAX_ITEMS=int(os.getenv("AGENT_MEMORY_MAX_ITEMS",1000))
