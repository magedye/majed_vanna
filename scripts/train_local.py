from app.agent.implementation import LocalVanna

# Config for LM Studio
config = {
    "api_key": "lm-studio",
    "api_base": "http://localhost:1234/v1",
    "model": "gemma-3n",
    "path": "./chroma_db",
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
