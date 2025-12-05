from vanna.legacy.chromadb.chromadb_vector import ChromaDB_VectorStore
from vanna.legacy.openai.openai_chat import OpenAI_Chat
from openai import OpenAI
from chromadb.utils import embedding_functions

# Pin a stable embedding function to ensure training and runtime use the same space
EMBED_FN = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


class LocalVanna(ChromaDB_VectorStore, OpenAI_Chat):
    """
    Local Vanna implementation using ChromaDB for vectors and LM Studio (OpenAI-compatible) for LLM.
    """

    def __init__(self, config: dict):
        # Expect config to have: path, api_key, api_base, model
        ChromaDB_VectorStore.__init__(
            self,
            config={
                "path": config.get("path", "./chroma_db"),
                "embedding_function": EMBED_FN,
            },
        )
        client = OpenAI(api_key=config.get("api_key"), base_url=config.get("api_base"))
        OpenAI_Chat.__init__(self, client=client, config={"model": config.get("model")})
