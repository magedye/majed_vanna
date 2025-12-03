from fastapi import APIRouter
from app.agent.db import test_connections

router = APIRouter()

@router.get("/db")
def db_status():
    return test_connections()
