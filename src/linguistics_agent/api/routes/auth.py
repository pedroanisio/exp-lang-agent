"""
Authentication routes for the AI Linguistics Agent.

This module provides JWT-based authentication endpoints including:
- User registration
- User login
- Token refresh
- User profile management

Follows ADR-005 authentication strategy and rules-103 security standards.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import (
    create_access_token,
    verify_password,
    get_password_hash,
    verify_token,
    get_current_user,
)
from ..dependencies import get_db_session
from ...database import DatabaseManager
from ...models.database import User
from ...models.requests import UserRegistrationRequest, UserLoginRequest
from ...models.responses import (
    UserRegistrationResponse,
    UserLoginResponse,
    UserProfileResponse,
    TokenRefreshResponse,
)

# Initialize router with tags (prefix added in main.py)
router = APIRouter(tags=["authentication"])
security = HTTPBearer()


@router.post(
    "/register",
    response_model=UserRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password",
)
async def register_user(
    user_data: UserRegistrationRequest,
    db_session: AsyncSession = Depends(get_db_session),
) -> UserRegistrationResponse:
    """
    Register a new user account.
    
    Args:
        user_data: User registration information
        db_session: Database session dependency
        
    Returns:
        UserRegistrationResponse with user details and access token
        
    Raises:
        HTTPException: If email already exists or validation fails
    """
    try:
        # Initialize database manager
        db_manager = DatabaseManager()
        
        # Check if user already exists
        existing_user = await db_manager.get_user_by_email(db_session, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password and create user
        hashed_password = get_password_hash(user_data.password)
        user_dict = {
            "email": user_data.email,
            "username": user_data.username,
            "full_name": user_data.full_name,
            "hashed_password": hashed_password,
            "is_active": True,
            "role": "user",  # Default role
        }
        
        # Create user in database
        new_user = await db_manager.create_user(db_session, user_dict)
        
        # Generate access token
        access_token = create_access_token(
            data={"sub": str(new_user.id), "email": new_user.email}
        )
        
        return UserRegistrationResponse(
            id=new_user.id,
            email=new_user.email,
            username=new_user.username,
            full_name=new_user.full_name,
            role=new_user.role,
            is_active=new_user.is_active,
            created_at=new_user.created_at,
            access_token=access_token,
            token_type="bearer",
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post(
    "/login",
    response_model=UserLoginResponse,
    summary="User login",
    description="Authenticate user with email and password",
)
async def login_user(
    login_data: UserLoginRequest,
    db_session: AsyncSession = Depends(get_db_session),
) -> UserLoginResponse:
    """
    Authenticate user and return access token.
    
    Args:
        login_data: User login credentials
        db_session: Database session dependency
        
    Returns:
        UserLoginResponse with access token and user details
        
    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        # Initialize database manager
        db_manager = DatabaseManager()
        
        # Get user by email
        user = await db_manager.get_user_by_email(db_session, login_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify password
        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is disabled",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Generate access token
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        return UserLoginResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            role=user.role,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.get(
    "/profile",
    response_model=UserProfileResponse,
    summary="Get user profile",
    description="Get current user profile information",
)
async def get_user_profile(
    current_user: User = Depends(get_current_user),
) -> UserProfileResponse:
    """
    Get current user profile information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserProfileResponse with user profile details
    """
    return UserProfileResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


@router.post(
    "/refresh",
    response_model=TokenRefreshResponse,
    summary="Refresh access token",
    description="Refresh the access token using current valid token",
)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db_session: AsyncSession = Depends(get_db_session),
) -> TokenRefreshResponse:
    """
    Refresh the access token.
    
    Args:
        credentials: HTTP Bearer token credentials
        db_session: Database session dependency
        
    Returns:
        TokenRefreshResponse with new access token
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Verify current token
        token_data = verify_token(credentials.credentials)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database
        db_manager = DatabaseManager()
        user = await db_manager.get_user_by_email(db_session, token_data.email)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Generate new access token
        new_access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        return TokenRefreshResponse(
            access_token=new_access_token,
            token_type="bearer",
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="User logout",
    description="Logout user (client-side token removal)",
)
async def logout_user(
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Logout user.
    
    Note: Since we're using stateless JWT tokens, logout is handled
    client-side by removing the token. This endpoint confirms logout.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Success message
    """
    return {
        "message": "Successfully logged out",
        "user_id": current_user.id,
        "timestamp": datetime.utcnow().isoformat(),
    }

