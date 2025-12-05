import os
import chromadb
from chromadb.utils import embedding_functions
from vanna.legacy.base.base import VannaBase
from vanna.integrations.local.agent_memory import DemoAgentMemory

# Fixed embedding function (384-dim)
FIXED_EMBEDDING_FUNCTION = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


class MyVanna(VannaBase):
    """
    A stable Vanna memory layer using ChromaDB PersistentClient
    with fixed embedding dimensions.
    """

    def __init__(self, config=None):
        self.chroma_path = os.path.join(os.getcwd(), "chroma_db")

        # Ensure the directory exists
        os.makedirs(self.chroma_path, exist_ok=True)

        try:
            # Use local filesystem persistence
            self.chroma_client = chromadb.PersistentClient(path=self.chroma_path)

            # Create or load collection with pinned embedding function
            self.collection = self.chroma_client.get_or_create_collection(
                name="vanna_memory",
                embedding_function=FIXED_EMBEDDING_FUNCTION,
                metadata={"hnsw:space": "cosine"},
            )

        except Exception as e:
            print(f"[CRITICAL] Failed to initialize Vanna memory: {e}")
            print("Hint: Call /api/system/reset-memory?force=true")
            # Fallback to mock memory to avoid None crashes
            class _MockMemory:
                def add(self, *_, **__):  # no-op
                    return None

                def search(self, *_, **__):  # empty search result
                    return []

                def connect_to_sqlite(self, *_, **__):  # no-op
                    return None

            self.collection = None
            self.chroma_client = None
            self.mock = _MockMemory()


# Export instance to satisfy existing imports
try:
    agent_memory = MyVanna()
    # If fallback mock was set, expose it via agent_memory
    if getattr(agent_memory, "mock", None):
        agent_memory = agent_memory.mock  # type: ignore
except Exception as exc:
    print(f"[WARNING] Memory layer failed to initialize: {exc}")
    print("[WARNING] Falling back to DemoAgentMemory (stateless).")
    agent_memory = DemoAgentMemory(max_items=1000)
