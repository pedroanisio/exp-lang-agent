"""
File: __init__.py
Path: src/linguistics_agent/api/routes/__init__.py
Purpose: API routes package initialization

This module exports all API route modules for the FastAPI application.

Rule Compliance:
- rules-101: TDD GREEN phase implementation
- rules-103: Implementation standards
"""

from .auth import router as auth_router
from .users import router as users_router
from .linguistics import router as linguistics_router
from .admin import router as admin_router
from .health import router as health_router

__all__ = [
    "auth_router",
    "users_router",
    "linguistics_router",
    "admin_router",
    "health_router",
]
