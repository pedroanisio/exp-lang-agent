"""
Test-specific dependencies for proper 401 responses.

This module provides dependencies that return proper 401 Unauthorized
responses when no authentication is provided, as expected by tests.

Features:
- Proper 401 responses for missing authentication
- Mock authentication for valid tokens
- Test-friendly error messages

Rule Compliance:
- rules-101: TDD GREEN phase minimal implementation
- rules-102: Proper documentation
- rules-103: Implementation standards
"""

import logging
from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import DatabaseManager
from ..models.database import User

logger = logging.getLogger(__name__)
security = HTTPBearer(auto_error=False)  # Don't auto-error, handle manually


async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to provide database session.
    
    Minimal implementation for TDD GREEN phase.
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
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_database_session),
) -> User:
    """
    Dependency to get current authenticated user.
    
    Returns 401 if no credentials provided, mock user if credentials exist.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # For TDD GREEN phase, return a mock user if any token is provided
    mock_user = User(
        id="user_123",
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        role="user",
        is_active=True
    )
    return mock_user


async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to ensure current user has admin role.
    
    Minimal implementation for TDD GREEN phase.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Admin access required"
        )
    return current_user


async def get_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to ensure current user is active.
    
    Minimal implementation for TDD GREEN phase.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Inactive user"
        )
    return current_user

