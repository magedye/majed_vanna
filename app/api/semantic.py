from fastapi import APIRouter, HTTPException
from dbt_integration.doc_generator import SemanticDocGenerator

router = APIRouter(prefix="/api/semantic", tags=["Semantic Docs"])
generator = SemanticDocGenerator()


@router.get("/docs")
def get_docs():
    try:
        result = generator.build()
        return {
            "toc": result.get("toc"),
            "content": result.get("content"),
            "outputs": result.get("outputs"),
        }
    except Exception as exc:
        raise HTTPException(500, f"Failed to generate docs: {exc}")


@router.get("/search")
def search_docs(query: str):
    try:
        results = generator.search(query)
        return {"query": query, "results": results}
    except Exception as exc:
        raise HTTPException(500, f"Search failed: {exc}")
