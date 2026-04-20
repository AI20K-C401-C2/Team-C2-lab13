from __future__ import annotations

import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Start each request with a clean logging context so IDs do not leak across requests.
        clear_contextvars()

        # Reuse an upstream request ID when present; otherwise generate a lab-friendly fallback.
        incoming_request_id = request.headers.get("x-request-id")
        correlation_id = incoming_request_id.strip() if incoming_request_id and incoming_request_id.strip() else f"req-{uuid.uuid4().hex[:8]}"
        
        # Bind once here so every downstream log line inherits the same correlation ID.
        bind_contextvars(correlation_id=correlation_id)
        
        request.state.correlation_id = correlation_id
        
        start = time.perf_counter()
        response = await call_next(request)
        
        # Mirror tracing metadata back to callers so they can debug requests from the edge.
        response.headers["x-request-id"] = correlation_id
        response.headers["x-response-time-ms"] = str(int((time.perf_counter() - start) * 1000))
        
        return response
