"""
User management routes for the AI Linguistics Agent.

This module provides endpoints for:
- User profile management
- User preferences and settings
- User activity and statistics
- Password management

Follows ADR-005 authentication strategy and user management best practices.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import get_current_user, verify_password, get_password_hash
from ..dependencies import get_db_session
from ...database import DatabaseManager
from ...models.database import User
from ...models.requests import (
    UserProfileUpdateRequest,
    PasswordChangeRequest,
    UserPreferencesRequest,
)
from ...models.responses import (
    UserProfileResponse,
    UserStatsResponse,
    UserPreferencesResponse,
)

# Initialize router with prefix and tags
router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/me",
    response_model=UserProfileResponse,
    summary="Get current user profile",
    description="Get detailed profile information for the current user",
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
) -> UserProfileResponse:
    """
    Get current user profile information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserProfileResponse with detailed user information
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
        metadata=current_user.metadata,
    )


@router.put(
    "/me",
    response_model=UserProfileResponse,
    summary="Update user profile",
    description="Update current user profile information",
)
async def update_user_profile(
    profile_data: UserProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> UserProfileResponse:
    """
    Update current user profile.
    
    Args:
        profile_data: Updated profile information
        current_user: Current authenticated user
        db_session: Database session dependency
        
    Returns:
        UserProfileResponse with updated user information
        
    Raises:
        HTTPException: If update fails
    """
    try:
        db_manager = DatabaseManager()
        
        # Prepare update data (only include non-None values)
        update_data = {}
        if profile_data.username is not None:
            update_data["username"] = profile_data.username
        if profile_data.full_name is not None:
            update_data["full_name"] = profile_data.full_name
        if profile_data.metadata is not None:
            # Merge with existing metadata
            existing_metadata = current_user.metadata or {}
            existing_metadata.update(profile_data.metadata)
            update_data["metadata"] = existing_metadata
        
        # Update user in database
        updated_user = await db_manager.update_user(
            db_session, current_user.id, update_data
        )
        
        return UserProfileResponse(
            id=updated_user.id,
            email=updated_user.email,
            username=updated_user.username,
            full_name=updated_user.full_name,
            role=updated_user.role,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
            metadata=updated_user.metadata,
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profile update failed: {str(e)}"
        )


@router.post(
    "/me/change-password",
    status_code=status.HTTP_200_OK,
    summary="Change user password",
    description="Change current user password",
)
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> dict:
    """
    Change current user password.
    
    Args:
        password_data: Password change request with current and new passwords
        current_user: Current authenticated user
        db_session: Database session dependency
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If password change fails or current password is incorrect
    """
    try:
        # Verify current password
        if not verify_password(password_data.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Hash new password
        new_hashed_password = get_password_hash(password_data.new_password)
        
        # Update password in database
        db_manager = DatabaseManager()
        await db_manager.update_user(
            db_session, 
            current_user.id, 
            {"hashed_password": new_hashed_password}
        )
        
        return {
            "message": "Password changed successfully",
            "user_id": current_user.id,
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password change failed: {str(e)}"
        )


@router.get(
    "/me/stats",
    response_model=UserStatsResponse,
    summary="Get user statistics",
    description="Get usage statistics for the current user",
)
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> UserStatsResponse:
    """
    Get user statistics and activity metrics.
    
    Args:
        current_user: Current authenticated user
        db_session: Database session dependency
        
    Returns:
        UserStatsResponse with user activity statistics
        
    Raises:
        HTTPException: If stats retrieval fails
    """
    try:
        db_manager = DatabaseManager()
        
        # Get user statistics
        stats = await db_manager.get_user_stats(db_session, current_user.id)
        
        return UserStatsResponse(
            user_id=current_user.id,
            total_projects=stats["total_projects"],
            total_sessions=stats["total_sessions"],
            total_messages=stats["total_messages"],
            total_analyses=stats["total_analyses"],
            account_age_days=stats["account_age_days"],
            last_activity=stats["last_activity"],
            most_used_features=stats["most_used_features"],
            analysis_types_used=stats["analysis_types_used"],
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user stats: {str(e)}"
        )


@router.get(
    "/me/preferences",
    response_model=UserPreferencesResponse,
    summary="Get user preferences",
    description="Get current user preferences and settings",
)
async def get_user_preferences(
    current_user: User = Depends(get_current_user),
) -> UserPreferencesResponse:
    """
    Get user preferences and settings.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserPreferencesResponse with user preferences
    """
    # Extract preferences from user metadata
    metadata = current_user.metadata or {}
    preferences = metadata.get("preferences", {})
    
    return UserPreferencesResponse(
        user_id=current_user.id,
        theme=preferences.get("theme", "light"),
        language=preferences.get("language", "en"),
        timezone=preferences.get("timezone", "UTC"),
        notifications_enabled=preferences.get("notifications_enabled", True),
        email_notifications=preferences.get("email_notifications", True),
        analysis_defaults=preferences.get("analysis_defaults", {}),
        ui_preferences=preferences.get("ui_preferences", {}),
    )


@router.put(
    "/me/preferences",
    response_model=UserPreferencesResponse,
    summary="Update user preferences",
    description="Update current user preferences and settings",
)
async def update_user_preferences(
    preferences_data: UserPreferencesRequest,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> UserPreferencesResponse:
    """
    Update user preferences and settings.
    
    Args:
        preferences_data: Updated preferences
        current_user: Current authenticated user
        db_session: Database session dependency
        
    Returns:
        UserPreferencesResponse with updated preferences
        
    Raises:
        HTTPException: If update fails
    """
    try:
        # Prepare updated metadata
        metadata = current_user.metadata or {}
        preferences = metadata.get("preferences", {})
        
        # Update preferences with new values (only non-None values)
        if preferences_data.theme is not None:
            preferences["theme"] = preferences_data.theme
        if preferences_data.language is not None:
            preferences["language"] = preferences_data.language
        if preferences_data.timezone is not None:
            preferences["timezone"] = preferences_data.timezone
        if preferences_data.notifications_enabled is not None:
            preferences["notifications_enabled"] = preferences_data.notifications_enabled
        if preferences_data.email_notifications is not None:
            preferences["email_notifications"] = preferences_data.email_notifications
        if preferences_data.analysis_defaults is not None:
            preferences["analysis_defaults"] = preferences_data.analysis_defaults
        if preferences_data.ui_preferences is not None:
            preferences["ui_preferences"] = preferences_data.ui_preferences
        
        # Update metadata
        metadata["preferences"] = preferences
        
        # Update user in database
        db_manager = DatabaseManager()
        await db_manager.update_user(
            db_session, current_user.id, {"metadata": metadata}
        )
        
        return UserPreferencesResponse(
            user_id=current_user.id,
            theme=preferences.get("theme", "light"),
            language=preferences.get("language", "en"),
            timezone=preferences.get("timezone", "UTC"),
            notifications_enabled=preferences.get("notifications_enabled", True),
            email_notifications=preferences.get("email_notifications", True),
            analysis_defaults=preferences.get("analysis_defaults", {}),
            ui_preferences=preferences.get("ui_preferences", {}),
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Preferences update failed: {str(e)}"
        )

