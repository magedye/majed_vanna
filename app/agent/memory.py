from vanna.integrations.chromadb import ChromaAgentMemory
from app.config import AGENT_MEMORY_MAX_ITEMS

try:
    agent_memory=ChromaAgentMemory(collection_name="vanna_memory", persist_directory="./chroma_db")
except Exception:
    from vanna.integrations.local.agent_memory import DemoAgentMemory
    agent_memory=DemoAgentMemory(max_items=AGENT_MEMORY_MAX_ITEMS)
