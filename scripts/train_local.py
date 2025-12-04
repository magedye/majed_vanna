import os
from vanna.legacy.chromadb.chromadb_vector import ChromaDB_VectorStore
from vanna.legacy.openai.openai_chat import OpenAI_Chat
from openai import OpenAI


class LocalVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        # 1. Init ChromaDB locally
        ChromaDB_VectorStore.__init__(self, config={"path": "./chroma_db"})
        # 2. Init LLM (LM Studio)
        client = OpenAI(api_key=config.get("api_key"), base_url=config.get("api_base"))
        OpenAI_Chat.__init__(self, openai_client=client, config={"model": config.get("model")})


# Config for LM Studio
config = {
    "api_key": "lm-studio",
    "api_base": "http://localhost:1234/v1",
    "model": "gemma-3n",
}

vn = LocalVanna(config=config)

# Connect to SQLite
vn.connect_to_sqlite("D:/mydb.db")

# Train
print("Starting Local Training...")
df_ddl = vn.run_sql("SELECT type, sql FROM sqlite_master WHERE sql IS NOT NULL")
for ddl in df_ddl["sql"].to_list():
    print(f"Training on: {ddl[:50]}...")
    vn.train(ddl=ddl)

print("Training Complete. Vector Store path: ./chroma_db")
