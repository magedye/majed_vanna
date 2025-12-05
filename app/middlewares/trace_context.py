import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.logger import set_trace_context, trace_id_ctx, span_id_ctx


class TraceContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        incoming_trace = request.headers.get("X-Trace-Id")
        incoming_span = request.headers.get("X-Span-Id")
        trace_id, span_id = set_trace_context(
            trace_id=incoming_trace or str(uuid.uuid4()),
            span_id=incoming_span or str(uuid.uuid4()),
        )
        request.state.trace_id = trace_id
        request.state.span_id = span_id
        try:
            response = await call_next(request)
        finally:
            trace_id_ctx.set(None)
            span_id_ctx.set(None)
        response.headers["X-Trace-Id"] = trace_id
        response.headers["X-Span-Id"] = span_id
        return response
