# ADR-005: JWT-Based Authentication Strategy

## Metadata
- **Status**: Accepted
- **Date**: 2025-07-12
- **Deciders**: AI Agent, Security Architect
- **Technical Story**: US-003 - FastAPI Production Interface (Authentication)
- **Rule Compliance**: rules-101 v1.2+, rules-102 v1.2+, rules-103 v1.2+

## Context and Problem Statement

The AI Linguistics Agent requires secure authentication and authorization for multi-user access. The system needs to support user registration, login, session management, and role-based access control while maintaining security best practices and integrating seamlessly with the FastAPI framework.

**Key Requirements:**
- Secure user authentication and session management
- Role-based access control (RBAC) for different user types
- Stateless authentication suitable for API-first architecture
- Integration with FastAPI security features
- Support for both web interface and API access
- Token refresh mechanism for long-lived sessions

## Decision Drivers

- **Security**: Industry-standard authentication mechanisms
- **Scalability**: Stateless authentication for horizontal scaling
- **Integration**: Seamless FastAPI integration
- **User Experience**: Smooth login/logout experience
- **API-First**: Support for programmatic API access
- **Standards Compliance**: OAuth 2.0 and JWT standards

## Considered Options

### Option 1: JWT (JSON Web Tokens) with Refresh Tokens
- **Pros**:
  - Stateless authentication (no server-side session storage)
  - Industry standard with excellent library support
  - Self-contained tokens with embedded claims
  - Excellent FastAPI integration
  - Supports both web and API clients
  - Scalable across multiple server instances
- **Cons**:
  - Token revocation complexity
  - Larger token size than session IDs
  - Requires careful secret management

### Option 2: Session-Based Authentication
- **Pros**:
  - Simple implementation and debugging
  - Easy token revocation
  - Smaller session identifiers
- **Cons**:
  - Requires server-side session storage
  - Less scalable for distributed systems
  - Not ideal for API-first architecture

### Option 3: OAuth 2.0 with External Provider
- **Pros**:
  - Delegates authentication to trusted providers
  - Reduces security implementation burden
  - User convenience (single sign-on)
- **Cons**:
  - External dependency on OAuth providers
  - More complex implementation
  - Less control over user management

### Option 4: API Keys Only
- **Pros**:
  - Simple for API-only access
  - Easy to implement and manage
- **Cons**:
  - No user context or roles
  - Not suitable for web interface
  - Limited security features

## Decision Outcome

**Chosen option**: Option 1 - JWT with Refresh Tokens

**Rationale:**
1. **Stateless Design**: Perfect for API-first architecture and horizontal scaling
2. **FastAPI Integration**: Excellent native support and security features
3. **Flexibility**: Supports both web interface and programmatic API access
4. **Standards Compliance**: Industry-standard JWT and OAuth 2.0 patterns
5. **Security**: Robust security with proper implementation
6. **User Experience**: Seamless authentication across different clients

## Positive Consequences

- **Scalability**: Stateless tokens enable horizontal scaling
- **Performance**: No database lookups for token validation
- **Flexibility**: Single authentication system for web and API
- **Security**: Industry-standard security practices
- **Integration**: Seamless FastAPI security integration
- **Standards**: Compliance with JWT and OAuth 2.0 standards

## Negative Consequences

- **Complexity**: More complex than simple session-based auth
- **Token Management**: Requires careful handling of token lifecycle
- **Revocation**: Token blacklisting needed for immediate revocation
- **Secret Management**: Critical dependency on JWT secret security

## Implementation Details

### JWT Token Structure
```python
# JWT payload structure
{
    "sub": "user_id",           # Subject (user identifier)
    "username": "john_doe",     # Username for display
    "email": "john@example.com", # User email
    "role": "user",             # User role for RBAC
    "exp": 1640995200,          # Expiration timestamp
    "iat": 1640991600,          # Issued at timestamp
    "jti": "unique_token_id"    # JWT ID for revocation tracking
}
```

### Authentication Service
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

class AuthService:
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 7
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
```

### FastAPI Security Integration
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """Extract and validate current user from JWT token."""
    token = credentials.credentials
    payload = auth_service.verify_token(token)

    # Verify token type
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    # Get user from database
    user_id = payload.get("sub")
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user

async def get_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Require admin role for protected endpoints."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
```

### Authentication Endpoints
```python
@app.post("/api/v1/auth/register", response_model=UserResponse)
async def register(user_data: UserCreate) -> UserResponse:
    """Register a new user account."""
    # Validate user data
    if await user_service.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    hashed_password = auth_service.hash_password(user_data.password)
    user = await user_service.create_user(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password
    )

    return UserResponse.from_orm(user)

@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(credentials: UserCredentials) -> TokenResponse:
    """Authenticate user and return JWT tokens."""
    # Verify credentials
    user = await user_service.authenticate_user(
        credentials.email, credentials.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Create tokens
    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
        "role": user.role
    }

    access_token = auth_service.create_access_token(token_data)
    refresh_token = auth_service.create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

@app.post("/api/v1/auth/refresh", response_model=TokenResponse)
async def refresh_token(refresh_data: RefreshTokenRequest) -> TokenResponse:
    """Refresh access token using refresh token."""
    payload = auth_service.verify_token(refresh_data.refresh_token)

    # Verify token type
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    # Create new access token
    token_data = {
        "sub": payload.get("sub"),
        "username": payload.get("username"),
        "email": payload.get("email"),
        "role": payload.get("role")
    }

    access_token = auth_service.create_access_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_data.refresh_token,  # Keep existing refresh token
        token_type="bearer"
    )
```

### Role-Based Access Control
```python
from enum import Enum
from functools import wraps

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    READONLY = "readonly"

def require_role(required_role: UserRole):
    """Decorator for role-based access control."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user or current_user.role != required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Role {required_role} required"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Usage in endpoints
@app.post("/api/v1/admin/users")
@require_role(UserRole.ADMIN)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_user)
):
    """Admin-only endpoint for user creation."""
    return await user_service.create_user(user_data)
```

### Token Blacklisting for Revocation
```python
class TokenBlacklistService:
    def __init__(self):
        self.blacklisted_tokens = set()  # In production, use Redis

    async def blacklist_token(self, jti: str):
        """Add token to blacklist."""
        self.blacklisted_tokens.add(jti)
        # In production: await redis.sadd("blacklisted_tokens", jti)

    async def is_token_blacklisted(self, jti: str) -> bool:
        """Check if token is blacklisted."""
        return jti in self.blacklisted_tokens
        # In production: return await redis.sismember("blacklisted_tokens", jti)

# Enhanced token verification
async def verify_token_with_blacklist(token: str) -> dict:
    payload = auth_service.verify_token(token)
    jti = payload.get("jti")

    if await blacklist_service.is_token_blacklisted(jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked"
        )

    return payload
```

## Security Considerations

### Password Security
```python
# Strong password requirements
class PasswordValidator:
    @staticmethod
    def validate_password(password: str) -> bool:
        """Validate password strength."""
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True
```

### Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/auth/login")
@limiter.limit("5/minute")  # Limit login attempts
async def login(request: Request, credentials: UserCredentials):
    """Rate-limited login endpoint."""
    # Login implementation
```

### HTTPS and Security Headers
```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Force HTTPS in production
if settings.ENVIRONMENT == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

# Security headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
```

## Testing Strategy

### Authentication Testing
```python
@pytest.mark.asyncio
async def test_user_registration():
    """Test user registration flow."""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePass123!"
    }

    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_login_flow():
    """Test complete login flow."""
    # Create user
    user = await create_test_user()

    # Login
    credentials = {"email": user.email, "password": "testpass"}
    response = await client.post("/api/v1/auth/login", json=credentials)

    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

@pytest.mark.asyncio
async def test_protected_endpoint():
    """Test protected endpoint access."""
    # Get valid token
    token = await get_test_token()

    # Access protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/api/v1/user/profile", headers=headers)

    assert response.status_code == 200
```

## Compliance and Validation

### Rule Compliance
- **rules-101**: TDD approach with comprehensive authentication testing
- **rules-102**: Documented architectural decision with security rationale
- **rules-103**: Implementation follows security coding standards
- **rules-104**: Addresses authentication requirements across multiple user stories

### Security Requirements
- JWT-based stateless authentication
- Role-based access control (RBAC)
- Secure password hashing with bcrypt
- Token refresh mechanism
- Rate limiting for authentication endpoints
- HTTPS enforcement in production

## Related Decisions

- **ADR-003**: FastAPI Framework Selection (authentication integration)
- **ADR-004**: PostgreSQL State Management (user data storage)
- **ADR-008**: React Web Interface (frontend authentication)

## Notes

- Consider implementing OAuth 2.0 providers in future iterations
- Monitor JWT token size and consider optimization if needed
- Evaluate multi-factor authentication (MFA) for enhanced security
- Plan for token rotation and key management strategies

---

**Decision Status**: ✅ Accepted
**Implementation Status**: Ready for Development
**Next Review**: 2025-08-12 (monthly review)
**Rule Compliance**: ✅ rules-101 v1.2+, rules-102 v1.2+, rules-103 v1.2+
