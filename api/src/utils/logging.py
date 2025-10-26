"""
Request logging middleware for FastAPI.

Logs incoming requests and responses for debugging and monitoring.
"""

import logging
import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logger
logger = logging.getLogger("optimeal")
logger.setLevel(logging.INFO)

# Create console handler with formatting
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log HTTP requests and responses.

    Logs:
    - Request method, path, and client IP
    - Response status code and processing time
    - Request body size
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and log details.

        Args:
            request: Incoming request
            call_next: Next middleware/route handler

        Returns:
            Response from downstream handlers
        """
        # Record start time
        start_time = time.time()

        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        # Log incoming request
        logger.info(
            f"Request: {request.method} {request.url.path} from {client_ip}"
        )

        # Process request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"- Status: {response.status_code} "
            f"- Time: {process_time:.3f}s"
        )

        # Add processing time to response headers
        response.headers["X-Process-Time"] = str(process_time)

        return response
