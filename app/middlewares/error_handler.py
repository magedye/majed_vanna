from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class JsonErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            trace_id = getattr(request.state, "trace_id", None)
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "error_code": "internal_error",
                    "message": "An internal error occurred.",
                    "trace_id": trace_id,
                    "detail": str(exc),
                },
            )
