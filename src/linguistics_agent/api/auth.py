"""
File: auth.py
Path: src/linguistics_agent/api/auth.py
Purpose: Authentication and authorization management for FastAPI interface

This module implements JWT-based authentication and authorization following
security best practices and TDD methodology.

Features:
- JWT token creation and validation
- Password hashing and verification
- User authentication and authorization
- Token refresh and expiration handling
- Role-based access control

Rule Compliance:
- rules-101: TDD GREEN phase implementation
- rules-102: Security documentation
- rules-103: Implementation standards
- rules-106: Security best practices
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Union
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import secrets
import logging

from ..config import Settings
from ..models.database import User

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token scheme
security = HTTPBearer()


class JWTToken(BaseModel):
    """JWT token response model."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None


class TokenData(BaseModel):
    """Token payload data model."""

    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None
    exp: Optional[datetime] = None


class AuthManager:
    """
    Authentication manager for JWT-based authentication.

    Handles token creation, validation, password hashing,
    and user authentication operations.
    """

    def __init__(self, settings: Optional[Settings] = None):
        """Initialize authentication manager with settings."""
        self.settings = settings or Settings()
        self.secret_key = self.settings.jwt_secret_key
        self.algorithm = self.settings.jwt_algorithm
        self.access_token_expire_minutes = self.settings.jwt_access_token_expire_minutes
        self.refresh_token_expire_days = self.settings.jwt_refresh_token_expire_days

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against its hash.

        Args:
            plain_password: Plain text password
            hashed_password: Hashed password from database

        Returns:
            True if password matches, False otherwise
        """
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False

    def get_password_hash(self, password: str) -> str:
        """
        Hash a plain password.

        Args:
            password: Plain text password

        Returns:
            Hashed password string
        """
        return pwd_context.hash(password)

    def create_access_token(
        self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token.

        Args:
            data: Token payload data
            expires_delta: Optional custom expiration time

        Returns:
            Encoded JWT token string
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.access_token_expire_minutes
            )

        to_encode.update({"exp": expire})

        try:
            encoded_jwt = jwt.encode(
                to_encode, self.secret_key, algorithm=self.algorithm
            )
            return encoded_jwt
        except Exception as e:
            logger.error(f"Token creation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create access token",
            )

    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """
        Create a JWT refresh token.

        Args:
            data: Token payload data

        Returns:
            Encoded JWT refresh token string
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            days=self.refresh_token_expire_days
        )
        to_encode.update({"exp": expire, "type": "refresh"})

        try:
            encoded_jwt = jwt.encode(
                to_encode, self.secret_key, algorithm=self.algorithm
            )
            return encoded_jwt
        except Exception as e:
            logger.error(f"Refresh token creation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create refresh token",
            )

    def verify_token(self, token: str) -> TokenData:
        """
        Verify and decode a JWT token.

        Args:
            token: JWT token string

        Returns:
            Decoded token data

        Raises:
            HTTPException: If token is invalid or expired
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            username: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            role: str = payload.get("role")
            exp: float = payload.get("exp")

            if username is None:
                raise credentials_exception

            # Check if token is expired
            if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(
                timezone.utc
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            token_data = TokenData(
                username=username,
                user_id=user_id,
                role=role,
                exp=datetime.fromtimestamp(exp, tz=timezone.utc) if exp else None,
            )

            return token_data

        except JWTError as e:
            logger.error(f"JWT verification error: {e}")
            raise credentials_exception
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            raise credentials_exception

    def create_token_response(
        self, user: User, include_refresh: bool = True
    ) -> JWTToken:
        """
        Create a complete token response for a user.

        Args:
            user: User object
            include_refresh: Whether to include refresh token

        Returns:
            JWT token response with access and optional refresh token
        """
        # Create access token
        access_token_data = {
            "sub": user.username,
            "user_id": user.id,
            "role": user.role,
            "email": user.email,
        }

        access_token = self.create_access_token(data=access_token_data)

        # Create refresh token if requested
        refresh_token = None
        if include_refresh:
            refresh_token_data = {
                "sub": user.username,
                "user_id": user.id,
                "type": "refresh",
            }
            refresh_token = self.create_refresh_token(data=refresh_token_data)

        return JWTToken(
            access_token=access_token,
            token_type="bearer",
            expires_in=self.access_token_expire_minutes * 60,
            refresh_token=refresh_token,
        )

    def generate_secure_token(self, length: int = 32) -> str:
        """
        Generate a cryptographically secure random token.

        Args:
            length: Token length in bytes

        Returns:
            Secure random token string
        """
        return secrets.token_urlsafe(length)

    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """
        Validate password strength according to security requirements.

        Args:
            password: Password to validate

        Returns:
            Dictionary with validation results
        """
        result = {"valid": True, "errors": [], "score": 0}

        # Minimum length check
        if len(password) < 8:
            result["valid"] = False
            result["errors"].append("Password must be at least 8 characters long")
        else:
            result["score"] += 1

        # Character variety checks
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

        if not has_upper:
            result["errors"].append(
                "Password must contain at least one uppercase letter"
            )
            result["valid"] = False
        else:
            result["score"] += 1

        if not has_lower:
            result["errors"].append(
                "Password must contain at least one lowercase letter"
            )
            result["valid"] = False
        else:
            result["score"] += 1

        if not has_digit:
            result["errors"].append("Password must contain at least one digit")
            result["valid"] = False
        else:
            result["score"] += 1

        if not has_special:
            result["errors"].append(
                "Password must contain at least one special character"
            )
            result["valid"] = False
        else:
            result["score"] += 1

        # Length bonus
        if len(password) >= 12:
            result["score"] += 1

        return result


# Global auth manager instance
auth_manager = AuthManager()


async def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> TokenData:
    """
    Dependency to get current user from JWT token.

    Args:
        credentials: HTTP authorization credentials

    Returns:
        Current user token data

    Raises:
        HTTPException: If token is invalid
    """
    token = credentials.credentials
    return auth_manager.verify_token(token)


# Export commonly used functions and classes
__all__ = [
    "AuthManager",
    "JWTToken",
    "TokenData",
    "auth_manager",
    "get_current_user_from_token",
    "security",
]
