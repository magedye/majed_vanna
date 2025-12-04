from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Phase 1.D: unified error responses with internal logging."""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc: RequestValidationError):
        logger.warning("Request validation failed", extra={"path": str(request.url), "errors": exc.errors()})
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid request payload."},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc: HTTPException):
        logger.info("HTTP error", extra={"path": str(request.url), "status": exc.status_code, "detail": exc.detail})
        safe_detail = exc.detail if exc.status_code < 500 else "An error occurred."
        return JSONResponse(status_code=exc.status_code, content={"detail": safe_detail})

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request, exc: Exception):
        logger.exception("Unhandled error", extra={"path": str(request.url)})
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error. Please try again later."},
        )
