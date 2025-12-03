from fastapi import APIRouter
from app.agent.db import test_connections

router = APIRouter()


@router.get("/db")
@router.get("/db-status")
async def db_status():
    return await test_connections()
