import os
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.logger import setup_logger, log_perf
from app.utils.metrics import increment_counter


SLOW_THRESHOLD_MS = int(os.getenv("SLOW_REQUEST_THRESHOLD_MS", "2000"))
logger = setup_logger(__name__)


class SlowRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        increment_counter("requests_total")
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        if response.status_code >= 500:
            increment_counter("errors_total")
        log_perf(
            logger,
            "http.request",
            {
                "path": request.url.path,
                "method": request.method,
                "status": response.status_code,
                "duration_ms": duration_ms,
            },
        )
        if duration_ms > SLOW_THRESHOLD_MS:
            log_perf(
                logger,
                "http.slow_request",
                {
                    "path": request.url.path,
                    "duration_ms": duration_ms,
                    "threshold_ms": SLOW_THRESHOLD_MS,
                },
            )
        return response
