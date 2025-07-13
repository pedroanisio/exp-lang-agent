"""
File: rate_limiting.py
Path: src/linguistics_agent/api/middleware/rate_limiting.py
Purpose: Rate limiting middleware for API protection

This module implements rate limiting middleware to protect the API
from abuse and ensure fair usage across all clients.

Rule Compliance:
- rules-101: TDD GREEN phase implementation
- rules-106: Security and performance standards
"""

from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Optional
import time
import asyncio
import logging
from collections import defaultdict, deque

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using sliding window algorithm.

    Implements per-IP rate limiting with configurable limits
    and time windows for different endpoint categories.
    """

    def __init__(
        self,
        app,
        calls_per_minute: int = 60,
        burst_limit: int = 10,
        window_size: int = 60,
    ):
        """
        Initialize rate limiting middleware.

        Args:
            app: FastAPI application
            calls_per_minute: Maximum calls per minute per IP
            burst_limit: Maximum burst calls in short period
            window_size: Time window in seconds
        """
        super().__init__(app)
        self.calls_per_minute = calls_per_minute
        self.burst_limit = burst_limit
        self.window_size = window_size

        # Storage for rate limiting data
        self.request_counts: Dict[str, deque] = defaultdict(deque)
        self.burst_counts: Dict[str, deque] = defaultdict(deque)

        # Cleanup task
        self._cleanup_task = None

    async def dispatch(self, request: Request, call_next):
        """
        Process request with rate limiting.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware or route handler

        Returns:
            HTTP response or rate limit error
        """
        client_ip = self._get_client_ip(request)
        current_time = time.time()

        # Check rate limits
        if not self._check_rate_limit(client_ip, current_time):
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Rate limit exceeded. Please try again later."},
                headers={"Retry-After": "60"},
            )

        # Record the request
        self._record_request(client_ip, current_time)

        # Process the request
        response = await call_next(request)

        # Add rate limit headers
        self._add_rate_limit_headers(response, client_ip, current_time)

        return response

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request."""
        # Check for forwarded headers first
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fallback to direct client IP
        if request.client:
            return request.client.host

        return "unknown"

    def _check_rate_limit(self, client_ip: str, current_time: float) -> bool:
        """
        Check if request is within rate limits.

        Args:
            client_ip: Client IP address
            current_time: Current timestamp

        Returns:
            True if within limits, False otherwise
        """
        # Clean old entries
        self._cleanup_old_entries(client_ip, current_time)

        # Check burst limit (last 10 seconds)
        burst_window = current_time - 10
        burst_count = sum(1 for t in self.burst_counts[client_ip] if t > burst_window)

        if burst_count >= self.burst_limit:
            return False

        # Check per-minute limit
        minute_window = current_time - self.window_size
        minute_count = sum(
            1 for t in self.request_counts[client_ip] if t > minute_window
        )

        if minute_count >= self.calls_per_minute:
            return False

        return True

    def _record_request(self, client_ip: str, current_time: float) -> None:
        """Record a request for rate limiting tracking."""
        self.request_counts[client_ip].append(current_time)
        self.burst_counts[client_ip].append(current_time)

    def _cleanup_old_entries(self, client_ip: str, current_time: float) -> None:
        """Remove old entries outside the time window."""
        # Clean minute window
        minute_cutoff = current_time - self.window_size
        while (
            self.request_counts[client_ip]
            and self.request_counts[client_ip][0] <= minute_cutoff
        ):
            self.request_counts[client_ip].popleft()

        # Clean burst window
        burst_cutoff = current_time - 10
        while (
            self.burst_counts[client_ip]
            and self.burst_counts[client_ip][0] <= burst_cutoff
        ):
            self.burst_counts[client_ip].popleft()

    def _add_rate_limit_headers(
        self, response: Response, client_ip: str, current_time: float
    ) -> None:
        """Add rate limit information to response headers."""
        minute_window = current_time - self.window_size
        remaining = max(0, self.calls_per_minute - len(self.request_counts[client_ip]))

        response.headers["X-RateLimit-Limit"] = str(self.calls_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(
            int(current_time + self.window_size)
        )


# Export middleware
__all__ = ["RateLimitMiddleware"]
