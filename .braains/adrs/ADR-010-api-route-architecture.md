# ADR-010: API Route Architecture and Organization Pattern

## Metadata
- **Status**: Proposed
- **Date**: 2025-07-12
- **Deciders**: AI Agent, API Architect
- **Technical Story**: US-003 - FastAPI Production Interface
- **Rule Compliance**: rules-101 v1.2+, rules-102 v1.2+, rules-103 v1.2+
- **Extends**: ADR-003 FastAPI Framework Selection

## Context and Problem Statement

The FastAPI application has evolved into a complex multi-route system with authentication, linguistics analysis, knowledge management, and administrative functions. The current route organization pattern has emerged organically but lacks formal architectural documentation. We need to establish a clear, scalable API route architecture that supports maintainability, testing, and future expansion.

**Current State:**
- Multiple route modules: auth, linguistics, admin, users, health
- Complex middleware stack: security, rate limiting, logging
- Pydantic models for request/response validation
- JWT-based authentication system
- No formal route organization documentation

**Key Requirements:**
- Scalable route organization pattern
- Clear separation of concerns
- Consistent error handling across routes
- Maintainable authentication and authorization
- Support for API versioning
- Comprehensive OpenAPI documentation

## Decision Drivers

- **Maintainability**: Clear organization for easy navigation and updates
- **Scalability**: Support for growing number of endpoints
- **Consistency**: Uniform patterns across all routes
- **Security**: Consistent authentication and authorization
- **Documentation**: Automatic OpenAPI generation
- **Testing**: Easy unit and integration testing
- **Performance**: Efficient request routing and processing

## Considered Options

### Option 1: Flat Route Structure
**Description**: All routes in a single file or minimal organization

### Option 2: Feature-Based Route Organization
**Description**: Routes organized by business feature/domain

### Option 3: Layer-Based Route Organization  
**Description**: Routes organized by technical layer (auth, api, admin)

### Option 4: Hybrid Domain-Layer Organization
**Description**: Combination of domain features with technical layers

## Decision Outcome

**Chosen Option**: Option 4 - Hybrid Domain-Layer Organization

**Rationale:**
1. **Domain Clarity**: Business features clearly separated
2. **Technical Separation**: Cross-cutting concerns properly layered
3. **Scalability**: Easy to add new domains and technical features
4. **Maintainability**: Clear ownership and responsibility boundaries
5. **Testing**: Isolated testing of domains and layers

## Route Architecture Specification

### Directory Structure
```
src/linguistics_agent/api/
├── __init__.py
├── main.py                 # FastAPI app factory
├── dependencies.py         # Shared dependencies
├── middleware/            # Cross-cutting concerns
│   ├── __init__.py
│   ├── security.py        # Security middleware
│   ├── rate_limiting.py   # Rate limiting
│   └── logging.py         # Request/response logging
├── routes/               # Domain-specific routes
│   ├── __init__.py
│   ├── auth.py           # Authentication endpoints
│   ├── linguistics.py    # Core AI linguistics analysis
│   ├── knowledge.py      # Knowledge management
│   ├── projects.py       # Project management
│   ├── sessions.py       # Session management
│   ├── users.py          # User management
│   ├── admin.py          # Administrative functions
│   └── health.py         # Health checks and monitoring
└── auth.py               # Authentication utilities
```

### Route Organization Principles

#### 1. Domain-Driven Route Grouping
```python
# linguistics.py - Core AI functionality
@router.post("/analyze/text")
@router.post("/analyze/grammar") 
@router.post("/analyze/ebnf")

# knowledge.py - Knowledge management
@router.post("/knowledge/ingest")
@router.get("/knowledge/search")
@router.get("/knowledge/graph")

# projects.py - Project management
@router.post("/projects")
@router.get("/projects/{project_id}")
@router.put("/projects/{project_id}")
```

#### 2. Consistent Route Patterns
```python
# RESTful resource patterns
GET    /api/v1/{resource}           # List resources
POST   /api/v1/{resource}           # Create resource
GET    /api/v1/{resource}/{id}      # Get specific resource
PUT    /api/v1/{resource}/{id}      # Update resource
DELETE /api/v1/{resource}/{id}      # Delete resource

# Action-based patterns for AI operations
POST   /api/v1/analyze/{type}       # AI analysis operations
POST   /api/v1/knowledge/{action}   # Knowledge operations
```

#### 3. Authentication and Authorization Layers
```python
# Public endpoints (no auth required)
@router.get("/health")
@router.post("/auth/login")

# Authenticated endpoints (JWT required)
@router.get("/projects", dependencies=[Depends(get_current_user)])

# Admin endpoints (admin role required)
@router.post("/admin/users", dependencies=[Depends(require_admin)])
```

### Route Implementation Pattern

#### Standard Route Structure
```python
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from ..models.requests import CreateProjectRequest
from ..models.responses import ProjectResponse, ErrorResponse
from ..auth import get_current_user, require_admin
from ..dependencies import get_database

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)

@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new project",
    description="Create a new linguistics analysis project"
)
async def create_project(
    request: CreateProjectRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_database)
) -> ProjectResponse:
    """Create a new project with proper error handling."""
    try:
        # Implementation logic
        pass
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
```

### Error Handling Strategy

#### Consistent Error Response Format
```python
class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime
    request_id: str
```

#### Global Exception Handlers
```python
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error="validation_error",
            message="Request validation failed",
            details=exc.errors(),
            timestamp=datetime.utcnow(),
            request_id=request.headers.get("X-Request-ID", "unknown")
        ).dict()
    )
```

### API Versioning Strategy

#### Version-Based URL Structure
```python
# Version 1 API
app.include_router(
    auth_router,
    prefix="/api/v1",
    tags=["authentication"]
)

# Future version support
app.include_router(
    auth_router_v2,
    prefix="/api/v2", 
    tags=["authentication-v2"]
)
```

#### Version-Specific Models
```python
# v1/models/requests.py
class CreateProjectRequestV1(BaseModel):
    name: str
    description: Optional[str] = None

# v2/models/requests.py  
class CreateProjectRequestV2(BaseModel):
    name: str
    description: Optional[str] = None
    tags: List[str] = []
    metadata: Dict[str, Any] = {}
```

## Middleware Architecture

### Security Middleware Stack
```python
# Order matters - applied in reverse order
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(CORSMiddleware)
app.add_middleware(TrustedHostMiddleware)
```

### Custom Middleware Implementation
```python
class RequestLoggingMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app
    
    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "http":
            # Log request details
            start_time = time.time()
            
            # Process request
            await self.app(scope, receive, send)
            
            # Log response details
            process_time = time.time() - start_time
            logger.info(f"Request processed in {process_time:.3f}s")
```

## Testing Strategy

### Route Testing Pattern
```python
class TestProjectRoutes:
    """Test suite for project management routes."""
    
    @pytest.mark.asyncio
    async def test_create_project_success(self, client: AsyncClient, auth_headers: Dict):
        """Test successful project creation."""
        request_data = {
            "name": "Test Project",
            "description": "Test project description"
        }
        
        response = await client.post(
            "/api/v1/projects/",
            json=request_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        assert response.json()["name"] == "Test Project"
    
    @pytest.mark.asyncio
    async def test_create_project_unauthorized(self, client: AsyncClient):
        """Test project creation without authentication."""
        request_data = {"name": "Test Project"}
        
        response = await client.post("/api/v1/projects/", json=request_data)
        
        assert response.status_code == 401
        assert "Unauthorized" in response.json()["message"]
```

### Integration Testing
```python
@pytest.mark.integration
async def test_full_linguistics_workflow(client: AsyncClient, auth_headers: Dict):
    """Test complete linguistics analysis workflow."""
    # Create project
    project_response = await client.post("/api/v1/projects/", ...)
    project_id = project_response.json()["id"]
    
    # Create session
    session_response = await client.post(f"/api/v1/projects/{project_id}/sessions", ...)
    session_id = session_response.json()["id"]
    
    # Perform analysis
    analysis_response = await client.post("/api/v1/analyze/text", ...)
    
    assert analysis_response.status_code == 200
```

## Documentation Strategy

### OpenAPI Configuration
```python
app = FastAPI(
    title="AI Linguistics Agent API",
    description="Production API for AI-powered linguistic analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "authentication", "description": "User authentication and authorization"},
        {"name": "linguistics", "description": "AI linguistic analysis operations"},
        {"name": "knowledge", "description": "Knowledge base management"},
        {"name": "projects", "description": "Project management"},
        {"name": "admin", "description": "Administrative operations"}
    ]
)
```

### Route Documentation Standards
```python
@router.post(
    "/analyze/text",
    response_model=TextAnalysisResponse,
    summary="Analyze text for linguistic patterns",
    description="""
    Perform comprehensive linguistic analysis on provided text using AI.
    
    **Features:**
    - Syntax analysis and parsing
    - Semantic relationship extraction
    - Grammar pattern recognition
    - EBNF compatibility assessment
    
    **Requirements:**
    - Valid JWT authentication token
    - Text content (max 10,000 characters)
    - Optional analysis parameters
    """,
    responses={
        200: {"description": "Analysis completed successfully"},
        400: {"description": "Invalid text content or parameters"},
        401: {"description": "Authentication required"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Analysis service error"}
    }
)
```

## Performance Considerations

### Route Optimization
```python
# Async route handlers for I/O operations
@router.post("/analyze/text")
async def analyze_text(request: TextAnalysisRequest) -> TextAnalysisResponse:
    async with httpx.AsyncClient() as client:
        # Async AI API call
        response = await client.post(...)
    
    # Async database operations
    async with get_database() as db:
        await db.execute(...)
```

### Caching Strategy
```python
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

@router.get("/knowledge/search")
@cache(expire=300)  # 5-minute cache
async def search_knowledge(query: str) -> SearchResponse:
    # Expensive search operation
    pass
```

## Consequences

### Positive Consequences
- **Maintainability**: Clear organization makes code easy to navigate and modify
- **Scalability**: Easy to add new domains and endpoints
- **Consistency**: Uniform patterns across all routes
- **Testing**: Isolated testing of individual route modules
- **Documentation**: Automatic OpenAPI generation with comprehensive docs
- **Security**: Consistent authentication and authorization patterns

### Negative Consequences
- **Initial Complexity**: More files and structure to understand initially
- **Overhead**: Additional abstraction layers
- **Learning Curve**: Team needs to understand the organization pattern

### Neutral Consequences
- **File Count**: More files but better organization
- **Import Complexity**: More imports but clearer dependencies

## Validation and Success Metrics

### Code Quality Metrics
- Route test coverage: >90%
- API documentation completeness: 100%
- Response time consistency: <2 seconds for 95% of endpoints
- Error handling coverage: 100% of error scenarios

### Maintainability Metrics
- Time to add new endpoint: <30 minutes
- Time to understand route structure: <15 minutes for new developers
- Code duplication: <5% across route modules

### Performance Metrics
- Route resolution time: <10ms
- Middleware processing overhead: <50ms
- Memory usage per route: <10MB

## Links and References

- **Related ADRs**: ADR-003 (FastAPI Framework), ADR-005 (Authentication Strategy)
- **External Documentation**: 
  - FastAPI Routing: https://fastapi.tiangolo.com/tutorial/bigger-applications/
  - OpenAPI Specification: https://swagger.io/specification/
- **Code References**: 
  - Route modules: `src/linguistics_agent/api/routes/`
  - Main app: `src/linguistics_agent/api/main.py`
  - Models: `src/linguistics_agent/models/`

## Notes

### Future Considerations
- GraphQL endpoint for complex queries
- WebSocket support for real-time features
- API rate limiting per user/endpoint
- Advanced caching strategies
- API analytics and monitoring

### Rule Compliance
- **TDD Approach**: Test route organization and patterns
- **Memory Management**: Document route architecture decisions
- **Quality Standards**: Follow FastAPI and REST API best practices

---

**Status**: ✅ Documents current API route architecture
**Impact**: Medium - Affects API development and maintenance
**Review Date**: 2025-08-12

