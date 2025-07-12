"""
File: security.py
Path: src/linguistics_agent/api/middleware/security.py
Purpose: Security headers middleware for FastAPI application

This module implements security headers middleware to enhance API security
by adding appropriate HTTP security headers to all responses.

Features:
- Content Security Policy (CSP)
- X-Frame-Options protection
- X-Content-Type-Options
- X-XSS-Protection
- Strict-Transport-Security (HSTS)
- Referrer-Policy

Rule Compliance:
- rules-101: TDD GREEN phase implementation
- rules-102: Security documentation
- rules-103: Implementation standards
- rules-106: Security best practices
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import logging

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all HTTP responses.

    This middleware enhances API security by adding standard
    security headers that protect against common web vulnerabilities.
    """

    def __init__(self, app, **kwargs):
        """
        Initialize security headers middleware.

        Args:
            app: FastAPI application instance
            **kwargs: Additional configuration options
        """
        super().__init__(app)
        self.config = {
            "csp_policy": kwargs.get("csp_policy", "default-src 'self'"),
            "frame_options": kwargs.get("frame_options", "DENY"),
            "content_type_options": kwargs.get("content_type_options", "nosniff"),
            "xss_protection": kwargs.get("xss_protection", "1; mode=block"),
            "hsts_max_age": kwargs.get("hsts_max_age", 31536000),  # 1 year
            "referrer_policy": kwargs.get(
                "referrer_policy", "strict-origin-when-cross-origin"
            ),
            "permissions_policy": kwargs.get(
                "permissions_policy", "geolocation=(), microphone=(), camera=()"
            ),
        }

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and add security headers to response.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware or route handler

        Returns:
            HTTP response with security headers added
        """
        try:
            # Process the request
            response = await call_next(request)

            # Add security headers
            self._add_security_headers(response, request)

            return response

        except Exception as e:
            logger.error(f"Security middleware error: {e}")
            # Let the error propagate to global exception handlers
            raise

    def _add_security_headers(self, response: Response, request: Request) -> None:
        """
        Add security headers to the response.

        Args:
            response: HTTP response object
            request: HTTP request object
        """
        # Content Security Policy
        response.headers["Content-Security-Policy"] = self.config["csp_policy"]

        # Prevent clickjacking attacks
        response.headers["X-Frame-Options"] = self.config["frame_options"]

        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = self.config["content_type_options"]

        # XSS protection (legacy, but still useful for older browsers)
        response.headers["X-XSS-Protection"] = self.config["xss_protection"]

        # HTTP Strict Transport Security (HSTS) for HTTPS
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = (
                f"max-age={self.config['hsts_max_age']}; includeSubDomains; preload"
            )

        # Referrer policy
        response.headers["Referrer-Policy"] = self.config["referrer_policy"]

        # Permissions policy (formerly Feature Policy)
        response.headers["Permissions-Policy"] = self.config["permissions_policy"]

        # Additional security headers
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "cross-origin"

        # Server information hiding
        response.headers["Server"] = "AI-Linguistics-Agent"

        # Cache control for sensitive endpoints
        if self._is_sensitive_endpoint(request.url.path):
            response.headers["Cache-Control"] = (
                "no-store, no-cache, must-revalidate, private"
            )
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"

    def _is_sensitive_endpoint(self, path: str) -> bool:
        """
        Check if the endpoint path contains sensitive data.

        Args:
            path: Request path

        Returns:
            True if endpoint is sensitive, False otherwise
        """
        sensitive_patterns = [
            "/auth/",
            "/api/v1/auth/",
            "/admin/",
            "/metrics",
            "/health",
        ]

        return any(pattern in path for pattern in sensitive_patterns)


class CSPViolationReportingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle Content Security Policy violation reports.

    This middleware processes CSP violation reports sent by browsers
    when CSP policies are violated.
    """

    def __init__(self, app, report_endpoint: str = "/api/v1/security/csp-report"):
        """
        Initialize CSP violation reporting middleware.

        Args:
            app: FastAPI application instance
            report_endpoint: Endpoint to receive CSP violation reports
        """
        super().__init__(app)
        self.report_endpoint = report_endpoint

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process CSP violation reports.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware or route handler

        Returns:
            HTTP response
        """
        # Check if this is a CSP violation report
        if (
            request.url.path == self.report_endpoint
            and request.method == "POST"
            and request.headers.get("content-type") == "application/csp-report"
        ):

            try:
                # Read and log the violation report
                body = await request.body()
                logger.warning(f"CSP Violation Report: {body.decode('utf-8')}")

                # Return success response
                return Response(status_code=204)

            except Exception as e:
                logger.error(f"Error processing CSP violation report: {e}")
                return Response(status_code=400)

        # Continue with normal request processing
        return await call_next(request)


# Export middleware classes
__all__ = ["SecurityHeadersMiddleware", "CSPViolationReportingMiddleware"]
