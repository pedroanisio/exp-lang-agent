"""
File: dependencies.py
Path: src/linguistics_agent/api/dependencies.py
Purpose: FastAPI dependencies for database sessions and authentication

This module provides dependency injection functions for FastAPI endpoints,
handling database session management and user authentication.

Features:
- Database session dependency with proper cleanup
- User authentication dependency
- Role-based authorization dependencies
- Request context management

Rule Compliance:
- rules-101: TDD GREEN phase implementation
- rules-102: Dependency documentation
- rules-103: Implementation standards
- rules-106: Security and resource management
"""

from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from ..database import DatabaseManager
from ..models.database import User
from .auth import get_current_user_from_token, TokenData

logger = logging.getLogger(__name__)


async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to provide database session for API endpoints.

    Yields:
        AsyncSession: Database session with automatic cleanup

    This dependency ensures proper database session management
    with automatic cleanup and error handling.
    """
    from ..config import Settings
    settings = Settings()
    db_manager = DatabaseManager(settings.database.postgresql_url)

    try:
        # Initialize database manager if not already done
        if not db_manager.engine:
            await db_manager.initialize()

        # Create session
        async with db_manager.get_session() as session:
            yield session

    except Exception as e:
        logger.error(f"Database session error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error",
        )


async def get_current_user(
    token_data: TokenData = Depends(get_current_user_from_token),
    db_session: AsyncSession = Depends(get_database_session),
) -> User:
    """
    Dependency to get current authenticated user.

    Args:
        token_data: Validated token data from JWT
        db_session: Database session

    Returns:
        Current authenticated user

    Raises:
        HTTPException: If user not found or inactive
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Query user from database
        stmt = select(User).where(
            User.username == token_data.username, User.is_active == True
        )
        result = await db_session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            logger.warning(f"User not found or inactive: {token_data.username}")
            raise credentials_exception

        # Verify user ID matches token
        if user.id != token_data.user_id:
            logger.warning(
                f"User ID mismatch: token={token_data.user_id}, db={user.id}"
            )
            raise credentials_exception

        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving current user: {e}")
        raise credentials_exception


async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to ensure current user has admin role.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user if admin

    Raises:
        HTTPException: If user is not admin
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )

    return current_user


async def get_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to ensure current user is active.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user if active

    Raises:
        HTTPException: If user is not active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
        )

    return current_user


class RoleChecker:
    """
    Role-based access control dependency.

    Usage:
        @app.get("/admin-only")
        async def admin_endpoint(user: User = Depends(RoleChecker(["admin"]))):
            pass
    """

    def __init__(self, allowed_roles: list[str]):
        """
        Initialize role checker with allowed roles.

        Args:
            allowed_roles: List of roles allowed to access the endpoint
        """
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        """
        Check if current user has required role.

        Args:
            current_user: Current authenticated user

        Returns:
            Current user if authorized

        Raises:
            HTTPException: If user doesn't have required role
        """
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(self.allowed_roles)}",
            )

        return current_user


async def get_request_context(request: Request) -> dict:
    """
    Dependency to provide request context information.

    Args:
        request: FastAPI request object

    Returns:
        Dictionary with request context data
    """
    return {
        "method": request.method,
        "url": str(request.url),
        "path": request.url.path,
        "query_params": dict(request.query_params),
        "headers": dict(request.headers),
        "client_host": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "timestamp": request.state.__dict__.get("start_time"),
    }


async def get_pagination_params(
    page: int = 1, size: int = 10, max_size: int = 100
) -> dict:
    """
    Dependency to provide pagination parameters with validation.

    Args:
        page: Page number (1-based)
        size: Items per page
        max_size: Maximum allowed page size

    Returns:
        Dictionary with validated pagination parameters

    Raises:
        HTTPException: If pagination parameters are invalid
    """
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Page number must be 1 or greater",
        )

    if size < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Page size must be 1 or greater",
        )

    if size > max_size:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Page size cannot exceed {max_size}",
        )

    return {"page": page, "size": size, "offset": (page - 1) * size, "limit": size}


class DatabaseTransactionManager:
    """
    Context manager for database transactions in API endpoints.

    Usage:
        async with DatabaseTransactionManager(db_session) as tx:
            # Perform database operations
            await tx.commit()  # Explicit commit
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initialize transaction manager.

        Args:
            db_session: Database session
        """
        self.db_session = db_session
        self.committed = False

    async def __aenter__(self):
        """Enter transaction context."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit transaction context with automatic rollback on error."""
        if exc_type is not None:
            # Exception occurred, rollback transaction
            await self.db_session.rollback()
            logger.error(f"Transaction rolled back due to error: {exc_val}")
        elif not self.committed:
            # No explicit commit, rollback as safety measure
            await self.db_session.rollback()
            logger.warning("Transaction rolled back - no explicit commit")

    async def commit(self):
        """Commit the transaction."""
        await self.db_session.commit()
        self.committed = True

    async def rollback(self):
        """Rollback the transaction."""
        await self.db_session.rollback()


# Export commonly used dependencies
__all__ = [
    "get_database_session",
    "get_current_user",
    "get_admin_user",
    "get_active_user",
    "RoleChecker",
    "get_request_context",
    "get_pagination_params",
    "DatabaseTransactionManager",
]


# Alias for backward compatibility with routes
get_db_session = get_database_session

