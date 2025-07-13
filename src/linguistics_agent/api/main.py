"""
File: main.py
Path: src/linguistics_agent/api/main.py
Purpose: FastAPI application factory for production interface

This module implements the FastAPI application factory following TDD methodology.
It creates a production-ready API interface with authentication, validation,
error handling, and comprehensive endpoint coverage.

Features:
- JWT-based authentication
- Request/response validation with Pydantic
- Database integration with async SQLAlchemy
- Error handling and logging
- CORS support
- Rate limiting
- Health checks and metrics
- API documentation

Rule Compliance:
- rules-101: TDD GREEN phase implementation
- rules-102: Comprehensive documentation
- rules-103: Implementation standards
- rules-106: Code quality and security
"""

from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
import time
import logging
from typing import Dict, Any, Optional
import uvicorn

# Import API routes
from .routes.auth_minimal import router as auth_router
from .routes.projects import router as projects_router
from .routes.sessions import router as sessions_router
from .routes.messages import router as messages_router
from .routes.analysis import router as analysis_router
from .routes.knowledge import router as knowledge_router
from .routes.health import router as health_router
from .routes.users import router as users_router
from .routes.admin import router as admin_router
from .routes.linguistics import router as linguistics_router
from .routes.cors_options import router as cors_options_router

# Import middleware
from .middleware.rate_limiting import RateLimitMiddleware
from .middleware.security import SecurityHeadersMiddleware
from .middleware.logging import LoggingMiddleware

# Import dependencies
from .dependencies_test import get_database_session, get_current_user
from .auth import AuthManager

# Import configuration
from ..config import Settings

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.

    Handles:
    - Database connection initialization
    - Background task setup
    - Resource cleanup on shutdown
    """
    logger.info("Starting AI Linguistics Agent API...")

    # Startup
    try:
        # Initialize database connection
        from ..database import DatabaseManager

        db_manager = DatabaseManager()
        await db_manager.initialize()
        app.state.db_manager = db_manager

        logger.info("Database connection initialized")
        logger.info("AI Linguistics Agent API started successfully")

        yield

    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise

    finally:
        # Shutdown
        logger.info("Shutting down AI Linguistics Agent API...")

        if hasattr(app.state, "db_manager"):
            await app.state.db_manager.close()
            logger.info("Database connection closed")

        logger.info("AI Linguistics Agent API shutdown complete")


def create_app(settings: Optional[Settings] = None) -> FastAPI:
    """
    Create and configure FastAPI application.

    Args:
        settings: Optional settings override for testing

    Returns:
        Configured FastAPI application instance

    Features:
    - Authentication and authorization
    - Request/response validation
    - Error handling
    - CORS support
    - Rate limiting
    - Security headers
    - API documentation
    - Health checks
    """
    if settings is None:
        settings = Settings()

    # Create FastAPI application
    app = FastAPI(
        title="AI Linguistics Agent API",
        description="""
        Production-ready API for AI-powered linguistic analysis and EBNF grammar processing.
        
        ## Features
        
        * **Authentication**: JWT-based user authentication and authorization
        * **Project Management**: Create and manage linguistic analysis projects
        * **Chat Sessions**: Interactive conversation management with context
        * **Message Handling**: Real-time message processing and storage
        * **Linguistics Analysis**: Advanced EBNF grammar validation and analysis
        * **Knowledge Management**: Intelligent knowledge ingestion and search
        * **Real-time Processing**: Async operations with WebSocket support
        
        ## Authentication
        
        Most endpoints require authentication. Use the `/auth/login` endpoint to obtain
        a JWT token, then include it in the `Authorization` header as `Bearer <token>`.
        
        ## Rate Limiting
        
        API requests are rate-limited to ensure fair usage and system stability.
        """,
        version="1.0.0",
        contact={
            "name": "AI Linguistics Agent Team",
            "email": "support@linguistics-agent.ai",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Add CORS middleware first (must be before security middleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add security middleware
    app.add_middleware(SecurityHeadersMiddleware)

    # Add trusted host middleware for production security
    if settings.app.env == "production":
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)

    # Add rate limiting middleware
    app.add_middleware(RateLimitMiddleware)

    # Add logging middleware
    app.add_middleware(LoggingMiddleware)

    # Include API routers
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])

    app.include_router(
        projects_router,
        prefix="/api/v1/projects",
        tags=["Projects"],
        dependencies=[Depends(get_current_user)],
    )

    app.include_router(
        sessions_router,
        prefix="/api/v1/sessions",
        tags=["Chat Sessions"],
        dependencies=[Depends(get_current_user)],
    )

    app.include_router(
        messages_router,
        prefix="/api/v1/messages",
        tags=["Messages"],
        dependencies=[Depends(get_current_user)],
    )

    app.include_router(
        analysis_router,
        prefix="/api/v1",
        tags=["Linguistics Analysis"],
        dependencies=[Depends(get_current_user)],
    )

    app.include_router(
        knowledge_router,
        prefix="/api/v1/knowledge",
        tags=["Knowledge Management"],
        dependencies=[Depends(get_current_user)],
    )

    # Add existing routers
    app.include_router(users_router, prefix="/api/v1/users", tags=["User Management"])
    app.include_router(admin_router, prefix="/api/v1/admin", tags=["Administration"])
    app.include_router(linguistics_router, prefix="/api/v1/linguistics", tags=["Linguistics Analysis"])
    app.include_router(health_router, prefix="/api/v1", tags=["Health & Monitoring"])
    
    # Add CORS OPTIONS handlers
    app.include_router(cors_options_router, prefix="/api/v1", tags=["CORS"])

    # Global exception handlers
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions with consistent error format."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
                "status_code": exc.status_code,
                "timestamp": time.time(),
                "path": str(request.url.path),
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions with logging."""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Internal server error",
                "status_code": 500,
                "timestamp": time.time(),
                "path": str(request.url.path),
            },
        )

    # Custom OpenAPI schema
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        # Add security scheme
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    return app


def run_development_server():
    """Run development server with hot reload."""
    settings = Settings()
    app = create_app(settings)

    uvicorn.run(
        "linguistics_agent.api.main:create_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        factory=True,
    )


if __name__ == "__main__":
    run_development_server()


# Create module-level app instance for testing
app = create_app()

