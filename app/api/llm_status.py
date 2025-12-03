from fastapi import APIRouter
from app.agent.llm import llm

router = APIRouter()

@router.get("/llm")
def llm_status():
    try:
        test = llm.chat(messages=[{"role":"user","content":"ping"}])
        return {"status": "ok", "response": test}
    except Exception as e:
        return {"status": "error", "error": str(e)}
