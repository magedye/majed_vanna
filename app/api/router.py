from fastapi import APIRouter
from app.api.db_status import router as db_router
from app.api.health import router as health_router
from app.api.llm_status import router as llm_router
from app.api.metadata import router as metadata_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(db_router)
api_router.include_router(llm_router)
api_router.include_router(metadata_router)
