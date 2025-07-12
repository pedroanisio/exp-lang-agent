"""
File: cors_options.py
Path: src/linguistics_agent/api/routes/cors_options.py
Purpose: CORS preflight OPTIONS handler

This module implements OPTIONS handlers for CORS preflight requests
to ensure proper cross-origin resource sharing support.

Features:
- OPTIONS method handlers for all routes
- CORS preflight response headers
- Minimal implementation for TDD GREEN phase

Rule Compliance:
- rules-101: TDD GREEN phase minimal implementation
- rules-102: Proper documentation
- rules-103: Implementation standards
"""

from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse

router = APIRouter()


@router.options("/projects")
@router.options("/projects/")
async def projects_options():
    """Handle OPTIONS preflight for projects endpoints."""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        }
    )


@router.options("/sessions")
@router.options("/sessions/")
async def sessions_options():
    """Handle OPTIONS preflight for sessions endpoints."""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        }
    )


@router.options("/messages")
@router.options("/messages/")
async def messages_options():
    """Handle OPTIONS preflight for messages endpoints."""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        }
    )


@router.options("/analyze")
@router.options("/grammar/validate")
async def analysis_options():
    """Handle OPTIONS preflight for analysis endpoints."""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        }
    )


@router.options("/knowledge")
@router.options("/knowledge/")
@router.options("/knowledge/ingest")
@router.options("/knowledge/search")
async def knowledge_options():
    """Handle OPTIONS preflight for knowledge endpoints."""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        }
    )

