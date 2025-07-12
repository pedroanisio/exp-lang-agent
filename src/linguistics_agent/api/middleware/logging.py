"""
File: logging.py
Path: src/linguistics_agent/api/middleware/logging.py
Purpose: Logging middleware for request/response tracking and monitoring

This module implements comprehensive logging middleware for the FastAPI application,
providing detailed request/response logging, performance monitoring, and error tracking.

Rule Compliance:
- rules-101: TDD GREEN phase implementation
- rules-102: Monitoring and observability documentation
- rules-103: Implementation standards
- rules-106: Security and performance logging
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import time
import logging
import json
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for comprehensive request/response logging and monitoring.

    Features:
    - Request/response logging with timing
    - Unique request ID tracking
    - Error logging and monitoring
    - Performance metrics collection
    - Security event logging
    """

    def __init__(
        self,
        app,
        log_requests: bool = True,
        log_responses: bool = True,
        log_request_body: bool = False,
        log_response_body: bool = False,
        exclude_paths: list = None,
    ):
        """
        Initialize logging middleware.

        Args:
            app: FastAPI application
            log_requests: Whether to log incoming requests
            log_responses: Whether to log outgoing responses
            log_request_body: Whether to log request body (security sensitive)
            log_response_body: Whether to log response body (performance impact)
            exclude_paths: List of paths to exclude from logging
        """
        super().__init__(app)
        self.log_requests = log_requests
        self.log_responses = log_responses
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body
        self.exclude_paths = exclude_paths or ["/health", "/metrics", "/favicon.ico"]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request with comprehensive logging.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware or route handler

        Returns:
            HTTP response with logging metadata
        """
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Skip logging for excluded paths
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        # Record start time
        start_time = time.time()
        request.state.start_time = start_time

        # Log incoming request
        if self.log_requests:
            await self._log_request(request, request_id)

        try:
            # Process the request
            response = await call_next(request)

            # Calculate processing time
            process_time = time.time() - start_time

            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{process_time:.4f}"

            # Log outgoing response
            if self.log_responses:
                await self._log_response(request, response, request_id, process_time)

            # Log performance metrics
            self._log_performance_metrics(request, response, process_time)

            return response

        except Exception as e:
            # Calculate error processing time
            process_time = time.time() - start_time

            # Log error
            self._log_error(request, e, request_id, process_time)

            # Re-raise the exception
            raise

    async def _log_request(self, request: Request, request_id: str) -> None:
        """
        Log incoming request details.

        Args:
            request: HTTP request object
            request_id: Unique request identifier
        """
        # Basic request information
        log_data = {
            "event": "request_received",
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "headers": dict(request.headers),
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("user-agent", ""),
        }

        # Add request body if enabled (be careful with sensitive data)
        if self.log_request_body and request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    # Only log if content type is safe
                    content_type = request.headers.get("content-type", "")
                    if "application/json" in content_type:
                        log_data["request_body"] = body.decode("utf-8")[
                            :1000
                        ]  # Limit size
                    else:
                        log_data["request_body_size"] = len(body)
            except Exception as e:
                log_data["request_body_error"] = str(e)

        # Log the request
        logger.info("Request received", extra={"log_data": log_data})

    async def _log_response(
        self, request: Request, response: Response, request_id: str, process_time: float
    ) -> None:
        """
        Log outgoing response details.

        Args:
            request: HTTP request object
            response: HTTP response object
            request_id: Unique request identifier
            process_time: Request processing time in seconds
        """
        log_data = {
            "event": "response_sent",
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time": round(process_time, 4),
            "response_headers": dict(response.headers),
        }

        # Add response body if enabled (performance impact)
        if self.log_response_body and hasattr(response, "body"):
            try:
                if response.body:
                    log_data["response_body_size"] = len(response.body)
                    # Only log small responses
                    if len(response.body) < 1000:
                        log_data["response_body"] = response.body.decode("utf-8")
            except Exception as e:
                log_data["response_body_error"] = str(e)

        # Determine log level based on status code
        if response.status_code >= 500:
            logger.error(
                "Response sent with server error", extra={"log_data": log_data}
            )
        elif response.status_code >= 400:
            logger.warning(
                "Response sent with client error", extra={"log_data": log_data}
            )
        else:
            logger.info("Response sent successfully", extra={"log_data": log_data})

    def _log_error(
        self, request: Request, error: Exception, request_id: str, process_time: float
    ) -> None:
        """
        Log error details.

        Args:
            request: HTTP request object
            error: Exception that occurred
            request_id: Unique request identifier
            process_time: Request processing time in seconds
        """
        log_data = {
            "event": "request_error",
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "method": request.method,
            "path": request.url.path,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "process_time": round(process_time, 4),
            "client_ip": self._get_client_ip(request),
        }

        logger.error(
            "Request processing error", extra={"log_data": log_data}, exc_info=True
        )

    def _log_performance_metrics(
        self, request: Request, response: Response, process_time: float
    ) -> None:
        """
        Log performance metrics for monitoring.

        Args:
            request: HTTP request object
            response: HTTP response object
            process_time: Request processing time in seconds
        """
        # Log slow requests
        if process_time > 2.0:  # Configurable threshold
            logger.warning(
                f"Slow request detected: {request.method} {request.url.path} "
                f"took {process_time:.4f}s",
                extra={
                    "log_data": {
                        "event": "slow_request",
                        "method": request.method,
                        "path": request.url.path,
                        "process_time": process_time,
                        "status_code": response.status_code,
                    }
                },
            )

        # Log performance metrics (could be sent to monitoring system)
        metrics_data = {
            "event": "performance_metric",
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time": process_time,
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Use a separate logger for metrics
        metrics_logger = logging.getLogger("metrics")
        metrics_logger.info("Performance metric", extra={"metrics_data": metrics_data})

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


class SecurityEventLogger:
    """
    Specialized logger for security events.

    Logs authentication failures, authorization violations,
    suspicious activities, and security-related events.
    """

    def __init__(self):
        """Initialize security event logger."""
        self.logger = logging.getLogger("security")

    def log_authentication_failure(
        self, request: Request, username: str = None, reason: str = None
    ) -> None:
        """
        Log authentication failure event.

        Args:
            request: HTTP request object
            username: Username that failed authentication
            reason: Reason for authentication failure
        """
        event_data = {
            "event": "authentication_failure",
            "timestamp": datetime.utcnow().isoformat(),
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("user-agent", ""),
            "path": request.url.path,
            "username": username,
            "reason": reason,
        }

        self.logger.warning(
            "Authentication failure", extra={"security_event": event_data}
        )

    def log_authorization_violation(
        self, request: Request, user_id: int = None, required_role: str = None
    ) -> None:
        """
        Log authorization violation event.

        Args:
            request: HTTP request object
            user_id: ID of user attempting unauthorized access
            required_role: Role required for the operation
        """
        event_data = {
            "event": "authorization_violation",
            "timestamp": datetime.utcnow().isoformat(),
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("user-agent", ""),
            "path": request.url.path,
            "user_id": user_id,
            "required_role": required_role,
        }

        self.logger.warning(
            "Authorization violation", extra={"security_event": event_data}
        )

    def log_suspicious_activity(
        self, request: Request, activity_type: str, details: dict = None
    ) -> None:
        """
        Log suspicious activity event.

        Args:
            request: HTTP request object
            activity_type: Type of suspicious activity
            details: Additional details about the activity
        """
        event_data = {
            "event": "suspicious_activity",
            "timestamp": datetime.utcnow().isoformat(),
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("user-agent", ""),
            "path": request.url.path,
            "activity_type": activity_type,
            "details": details or {},
        }

        self.logger.error(
            "Suspicious activity detected", extra={"security_event": event_data}
        )

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request."""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        if request.client:
            return request.client.host

        return "unknown"


# Global security event logger instance
security_logger = SecurityEventLogger()

# Export middleware and logger
__all__ = ["LoggingMiddleware", "SecurityEventLogger", "security_logger"]
