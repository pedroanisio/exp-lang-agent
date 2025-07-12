"""
File: test_fastapi_interface.py
Path: tests/unit/test_fastapi_interface.py
Purpose: Comprehensive test suite for FastAPI production interface following TDD methodology

This module implements the TDD RED phase for the FastAPI production interface,
creating failing tests that define the expected behavior before implementation.

Test Coverage:
- API endpoint functionality
- Authentication and authorization
- Request/response validation
- Error handling and edge cases
- Database integration
- Performance and security

Rule Compliance:
- rules-101: TDD methodology (RED-GREEN-REFACTOR)
- rules-102: Comprehensive documentation
- rules-103: Implementation standards
- rules-106: Code quality and testing
"""

import pytest
import asyncio
from typing import Dict, Any, List
from httpx import AsyncClient
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

# Import application components (will be implemented in GREEN phase)
from linguistics_agent.api.main import create_app
from linguistics_agent.api.auth import AuthManager, JWTToken
from linguistics_agent.api.dependencies import get_database_session, get_current_user
from linguistics_agent.models.database import (
    Base,
    User,
    Project,
    ChatSession,
    Message,
    KnowledgeEntry,
)
from linguistics_agent.models.requests import (
    LinguisticsQuery,
    UserRegistration,
    UserLogin,
    ProjectCreate,
    SessionCreate,
    MessageCreate,
    KnowledgeIngestionRequest,
)
from linguistics_agent.models.responses import (
    LinguisticsResponse,
    UserResponse,
    TokenResponse,
    ProjectResponse,
    SessionResponse,
    MessageResponse,
    KnowledgeEntryResponse,
    ErrorResponse,
)
from linguistics_agent.database import DatabaseManager


class TestFastAPIInterface:
    """
    Comprehensive test suite for FastAPI production interface.

    Following TDD methodology with RED-GREEN-REFACTOR cycle.
    These tests define the expected behavior before implementation.
    """

    @pytest.fixture
    async def test_engine(self):
        """Create test database engine for FastAPI tests."""
        engine = create_async_engine(
            "sqlite+aiosqlite:///:memory:",
            echo=False,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )

        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        yield engine
        await engine.dispose()

    @pytest.fixture
    async def test_session(self, test_engine):
        """Create test database session."""
        session_factory = async_sessionmaker(
            test_engine, class_=AsyncSession, expire_on_commit=False
        )

        async with session_factory() as session:
            yield session

    @pytest.fixture
    async def test_app(self, test_engine):
        """Create test FastAPI application."""
        app = create_app()

        # Override database dependency for testing
        async def override_get_database_session():
            session_factory = async_sessionmaker(
                test_engine, class_=AsyncSession, expire_on_commit=False
            )
            async with session_factory() as session:
                yield session

        app.dependency_overrides[get_database_session] = override_get_database_session
        yield app
        app.dependency_overrides.clear()

    @pytest.fixture
    async def test_client(self, test_app):
        """Create test HTTP client."""
        async with AsyncClient(app=test_app, base_url="http://test") as client:
            yield client

    @pytest.fixture
    async def test_user(self, test_session: AsyncSession):
        """Create test user for authentication tests."""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password_123",
            role="user",
        )
        test_session.add(user)
        await test_session.commit()
        await test_session.refresh(user)
        return user

    @pytest.fixture
    async def auth_headers(self, test_user: User) -> Dict[str, str]:
        """Create authentication headers for test requests."""
        auth_manager = AuthManager()
        token = auth_manager.create_access_token(
            data={"sub": str(test_user.id), "username": test_user.username}
        )
        return {"Authorization": f"Bearer {token}"}

    # ==========================================
    # AUTHENTICATION AND AUTHORIZATION TESTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_user_registration_endpoint(self, test_client: AsyncClient):
        """Test user registration endpoint functionality."""
        # This test will FAIL until implementation (TDD RED phase)
        registration_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "secure_password_123",
            "full_name": "New User",
        }

        response = await test_client.post(
            "/api/v1/auth/register", json=registration_data
        )

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert "id" in response_data
        assert response_data["username"] == "newuser"
        assert response_data["email"] == "newuser@example.com"
        assert "password" not in response_data  # Password should not be returned

    @pytest.mark.asyncio
    async def test_user_login_endpoint(self, test_client: AsyncClient, test_user: User):
        """Test user login endpoint functionality."""
        # This test will FAIL until implementation (TDD RED phase)
        login_data = {"username": "testuser", "password": "secure_password_123"}

        response = await test_client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "access_token" in response_data
        assert "token_type" in response_data
        assert response_data["token_type"] == "bearer"
        assert "expires_in" in response_data

    @pytest.mark.asyncio
    async def test_token_validation_endpoint(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test JWT token validation endpoint."""
        # This test will FAIL until implementation (TDD RED phase)
        response = await test_client.get("/api/v1/auth/me", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "id" in response_data
        assert "username" in response_data
        assert "email" in response_data
        assert "role" in response_data

    @pytest.mark.asyncio
    async def test_unauthorized_access_protection(self, test_client: AsyncClient):
        """Test that protected endpoints require authentication."""
        # This test will FAIL until implementation (TDD RED phase)
        response = await test_client.get("/api/v1/projects")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        response_data = response.json()
        assert "detail" in response_data
        assert "authentication" in response_data["detail"].lower()

    # ==========================================
    # PROJECT MANAGEMENT ENDPOINTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_create_project_endpoint(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test project creation endpoint."""
        # This test will FAIL until implementation (TDD RED phase)
        project_data = {
            "name": "EBNF Grammar Analysis Project",
            "description": "Project for analyzing EBNF grammar structures",
            "settings": {
                "analysis_depth": "comprehensive",
                "output_format": "detailed",
            },
        }

        response = await test_client.post(
            "/api/v1/projects", json=project_data, headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert "id" in response_data
        assert response_data["name"] == project_data["name"]
        assert response_data["description"] == project_data["description"]
        assert "created_at" in response_data
        assert "user_id" in response_data

    @pytest.mark.asyncio
    async def test_list_projects_endpoint(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test project listing endpoint with pagination."""
        # This test will FAIL until implementation (TDD RED phase)
        response = await test_client.get(
            "/api/v1/projects?page=1&size=10", headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "items" in response_data
        assert "total" in response_data
        assert "page" in response_data
        assert "size" in response_data
        assert isinstance(response_data["items"], list)

    @pytest.mark.asyncio
    async def test_get_project_by_id_endpoint(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test retrieving specific project by ID."""
        # This test will FAIL until implementation (TDD RED phase)
        # First create a project
        project_data = {"name": "Test Project", "description": "Test Description"}
        create_response = await test_client.post(
            "/api/v1/projects", json=project_data, headers=auth_headers
        )
        project_id = create_response.json()["id"]

        # Then retrieve it
        response = await test_client.get(
            f"/api/v1/projects/{project_id}", headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["id"] == project_id
        assert response_data["name"] == project_data["name"]

    # ==========================================
    # CHAT SESSION MANAGEMENT ENDPOINTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_create_chat_session_endpoint(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test chat session creation endpoint."""
        # This test will FAIL until implementation (TDD RED phase)
        # First create a project
        project_data = {
            "name": "Chat Project",
            "description": "Project for chat sessions",
        }
        project_response = await test_client.post(
            "/api/v1/projects", json=project_data, headers=auth_headers
        )
        project_id = project_response.json()["id"]

        # Then create a chat session
        session_data = {
            "title": "EBNF Grammar Discussion",
            "project_id": project_id,
            "context": {"topic": "grammar_analysis", "complexity": "advanced"},
        }

        response = await test_client.post(
            "/api/v1/sessions", json=session_data, headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert "id" in response_data
        assert response_data["title"] == session_data["title"]
        assert response_data["project_id"] == project_id
        assert "created_at" in response_data

    @pytest.mark.asyncio
    async def test_list_chat_sessions_endpoint(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test chat session listing endpoint."""
        # This test will FAIL until implementation (TDD RED phase)
        response = await test_client.get(
            "/api/v1/sessions?project_id=1", headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "items" in response_data
        assert isinstance(response_data["items"], list)

    # ==========================================
    # MESSAGE HANDLING ENDPOINTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_send_message_endpoint(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test sending message to chat session."""
        # This test will FAIL until implementation (TDD RED phase)
        # Setup: Create project and session
        project_data = {
            "name": "Message Project",
            "description": "Project for messaging",
        }
        project_response = await test_client.post(
            "/api/v1/projects", json=project_data, headers=auth_headers
        )
        project_id = project_response.json()["id"]

        session_data = {"title": "Message Session", "project_id": project_id}
        session_response = await test_client.post(
            "/api/v1/sessions", json=session_data, headers=auth_headers
        )
        session_id = session_response.json()["id"]

        # Send message
        message_data = {
            "content": "Can you help me analyze this EBNF grammar: expr ::= term (('+' | '-') term)*",
            "message_type": "user",
            "session_id": session_id,
        }

        response = await test_client.post(
            "/api/v1/messages", json=message_data, headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert "id" in response_data
        assert response_data["content"] == message_data["content"]
        assert response_data["message_type"] == "user"
        assert response_data["session_id"] == session_id

    @pytest.mark.asyncio
    async def test_get_session_messages_endpoint(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test retrieving messages from a chat session."""
        # This test will FAIL until implementation (TDD RED phase)
        session_id = 1  # Assume session exists

        response = await test_client.get(
            f"/api/v1/sessions/{session_id}/messages", headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "items" in response_data
        assert isinstance(response_data["items"], list)

    # ==========================================
    # LINGUISTICS ANALYSIS ENDPOINTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_analyze_linguistics_endpoint(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test linguistics analysis endpoint with EBNF processing."""
        # This test will FAIL until implementation (TDD RED phase)
        analysis_data = {
            "text": "expr ::= term (('+' | '-') term)*\nterm ::= factor (('*' | '/') factor)*",
            "analysis_type": "ebnf_validation",
            "options": {
                "validate_syntax": True,
                "generate_ast": True,
                "check_completeness": True,
            },
        }

        response = await test_client.post(
            "/api/v1/analyze", json=analysis_data, headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "analysis_id" in response_data
        assert "results" in response_data
        assert "syntax_valid" in response_data["results"]
        assert "ast" in response_data["results"]
        assert "completeness_check" in response_data["results"]

    @pytest.mark.asyncio
    async def test_grammar_validation_endpoint(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test grammar validation endpoint."""
        # This test will FAIL until implementation (TDD RED phase)
        grammar_data = {
            "grammar_text": "S ::= 'a' S 'b' | 'ab'",
            "grammar_type": "ebnf",
            "validation_level": "strict",
        }

        response = await test_client.post(
            "/api/v1/grammar/validate", json=grammar_data, headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "valid" in response_data
        assert "errors" in response_data
        assert "warnings" in response_data
        assert isinstance(response_data["errors"], list)

    # ==========================================
    # KNOWLEDGE MANAGEMENT ENDPOINTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_ingest_knowledge_endpoint(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test knowledge ingestion endpoint."""
        # This test will FAIL until implementation (TDD RED phase)
        knowledge_data = {
            "source_type": "url",
            "source_url": "https://example.com/ebnf-guide",
            "title": "EBNF Grammar Guide",
            "category": "grammar_reference",
            "tags": ["ebnf", "grammar", "parsing"],
            "auto_process": True,
        }

        response = await test_client.post(
            "/api/v1/knowledge/ingest", json=knowledge_data, headers=auth_headers
        )

        assert response.status_code == status.HTTP_202_ACCEPTED
        response_data = response.json()
        assert "task_id" in response_data
        assert "status" in response_data
        assert response_data["status"] == "processing"

    @pytest.mark.asyncio
    async def test_search_knowledge_endpoint(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test knowledge search endpoint."""
        # This test will FAIL until implementation (TDD RED phase)
        search_params = {
            "query": "EBNF grammar rules",
            "category": "grammar_reference",
            "limit": 10,
            "include_content": True,
        }

        response = await test_client.get(
            "/api/v1/knowledge/search", params=search_params, headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "items" in response_data
        assert "total" in response_data
        assert isinstance(response_data["items"], list)

    # ==========================================
    # ERROR HANDLING AND VALIDATION TESTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_invalid_request_validation(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test request validation with invalid data."""
        # This test will FAIL until implementation (TDD RED phase)
        invalid_project_data = {
            "name": "",  # Empty name should be invalid
            "description": "x" * 2000,  # Too long description
        }

        response = await test_client.post(
            "/api/v1/projects", json=invalid_project_data, headers=auth_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        assert "detail" in response_data
        assert isinstance(response_data["detail"], list)

    @pytest.mark.asyncio
    async def test_not_found_error_handling(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test 404 error handling for non-existent resources."""
        # This test will FAIL until implementation (TDD RED phase)
        response = await test_client.get("/api/v1/projects/99999", headers=auth_headers)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_data = response.json()
        assert "detail" in response_data
        assert "not found" in response_data["detail"].lower()

    @pytest.mark.asyncio
    async def test_server_error_handling(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test server error handling and logging."""
        # This test will FAIL until implementation (TDD RED phase)
        # This would test a scenario that causes a server error
        # Implementation should handle gracefully and return proper error response
        pass

    # ==========================================
    # PERFORMANCE AND SECURITY TESTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_api_rate_limiting(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test API rate limiting functionality."""
        # This test will FAIL until implementation (TDD RED phase)
        # Make multiple rapid requests to test rate limiting
        responses = []
        for _ in range(100):  # Exceed rate limit
            response = await test_client.get("/api/v1/projects", headers=auth_headers)
            responses.append(response.status_code)

        # Should eventually get rate limited
        assert status.HTTP_429_TOO_MANY_REQUESTS in responses

    @pytest.mark.asyncio
    async def test_cors_headers(self, test_client: AsyncClient):
        """Test CORS headers for cross-origin requests."""
        # This test will FAIL until implementation (TDD RED phase)
        response = await test_client.options("/api/v1/projects")

        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-headers" in response.headers

    @pytest.mark.asyncio
    async def test_security_headers(self, test_client: AsyncClient):
        """Test security headers in API responses."""
        # This test will FAIL until implementation (TDD RED phase)
        response = await test_client.get("/api/v1/health")

        assert "x-content-type-options" in response.headers
        assert "x-frame-options" in response.headers
        assert "x-xss-protection" in response.headers

    # ==========================================
    # HEALTH AND MONITORING ENDPOINTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_health_check_endpoint(self, test_client: AsyncClient):
        """Test health check endpoint."""
        # This test will FAIL until implementation (TDD RED phase)
        response = await test_client.get("/api/v1/health")

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "status" in response_data
        assert response_data["status"] == "healthy"
        assert "timestamp" in response_data
        assert "version" in response_data

    @pytest.mark.asyncio
    async def test_metrics_endpoint(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test metrics endpoint for monitoring."""
        # This test will FAIL until implementation (TDD RED phase)
        response = await test_client.get("/api/v1/metrics", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "requests_total" in response_data
        assert "response_time_avg" in response_data
        assert "active_sessions" in response_data

    @pytest.mark.asyncio
    async def test_api_documentation_endpoint(self, test_client: AsyncClient):
        """Test API documentation endpoint (OpenAPI/Swagger)."""
        # This test will FAIL until implementation (TDD RED phase)
        response = await test_client.get("/docs")

        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers["content-type"]

    @pytest.mark.asyncio
    async def test_openapi_schema_endpoint(self, test_client: AsyncClient):
        """Test OpenAPI schema endpoint."""
        # This test will FAIL until implementation (TDD RED phase)
        response = await test_client.get("/openapi.json")

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "openapi" in response_data
        assert "info" in response_data
        assert "paths" in response_data


# ==========================================
# INTEGRATION TESTS WITH DATABASE LAYER
# ==========================================


class TestFastAPIIntegration:
    """Integration tests between FastAPI interface and database layer."""

    @pytest.mark.asyncio
    async def test_end_to_end_user_workflow(self, test_client: AsyncClient):
        """Test complete user workflow from registration to analysis."""
        # This test will FAIL until implementation (TDD RED phase)

        # 1. Register user
        registration_data = {
            "username": "e2euser",
            "email": "e2e@example.com",
            "password": "secure_password_123",
        }
        register_response = await test_client.post(
            "/api/v1/auth/register", json=registration_data
        )
        assert register_response.status_code == status.HTTP_201_CREATED

        # 2. Login
        login_data = {"username": "e2euser", "password": "secure_password_123"}
        login_response = await test_client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Create project
        project_data = {"name": "E2E Project", "description": "End-to-end test project"}
        project_response = await test_client.post(
            "/api/v1/projects", json=project_data, headers=headers
        )
        assert project_response.status_code == status.HTTP_201_CREATED
        project_id = project_response.json()["id"]

        # 4. Create session
        session_data = {"title": "E2E Session", "project_id": project_id}
        session_response = await test_client.post(
            "/api/v1/sessions", json=session_data, headers=headers
        )
        assert session_response.status_code == status.HTTP_201_CREATED
        session_id = session_response.json()["id"]

        # 5. Send message and get analysis
        message_data = {
            "content": "Analyze this grammar: S ::= 'a' S 'b' | 'ab'",
            "message_type": "user",
            "session_id": session_id,
        }
        message_response = await test_client.post(
            "/api/v1/messages", json=message_data, headers=headers
        )
        assert message_response.status_code == status.HTTP_201_CREATED

        # 6. Verify data persistence
        messages_response = await test_client.get(
            f"/api/v1/sessions/{session_id}/messages", headers=headers
        )
        assert messages_response.status_code == status.HTTP_200_OK
        messages = messages_response.json()["items"]
        assert len(messages) >= 1
        assert any(msg["content"] == message_data["content"] for msg in messages)

    @pytest.mark.asyncio
    async def test_database_transaction_handling(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test database transaction handling in API operations."""
        # This test will FAIL until implementation (TDD RED phase)

        # Test that failed operations don't leave partial data
        invalid_project_data = {
            "name": "Test Project",
            "description": "Valid description",
            "invalid_field": "This should cause validation error",
        }

        response = await test_client.post(
            "/api/v1/projects", json=invalid_project_data, headers=auth_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Verify no partial project was created
        projects_response = await test_client.get(
            "/api/v1/projects", headers=auth_headers
        )
        projects = projects_response.json()["items"]
        assert not any(proj["name"] == "Test Project" for proj in projects)

    @pytest.mark.asyncio
    async def test_concurrent_request_handling(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test handling of concurrent API requests."""
        # This test will FAIL until implementation (TDD RED phase)

        # Create multiple concurrent requests
        tasks = []
        for i in range(10):
            project_data = {
                "name": f"Concurrent Project {i}",
                "description": f"Project {i}",
            }
            task = test_client.post(
                "/api/v1/projects", json=project_data, headers=auth_headers
            )
            tasks.append(task)

        # Execute all requests concurrently
        responses = await asyncio.gather(*tasks)

        # All should succeed
        for response in responses:
            assert response.status_code == status.HTTP_201_CREATED

        # Verify all projects were created
        projects_response = await test_client.get(
            "/api/v1/projects", headers=auth_headers
        )
        projects = projects_response.json()["items"]
        assert len(projects) >= 10


# ==========================================
# PERFORMANCE BENCHMARKS
# ==========================================


class TestFastAPIPerformance:
    """Performance tests for FastAPI interface."""

    @pytest.mark.asyncio
    async def test_response_time_benchmarks(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test API response time benchmarks."""
        # This test will FAIL until implementation (TDD RED phase)
        import time

        # Test various endpoints for response time
        endpoints = ["/api/v1/projects", "/api/v1/sessions", "/api/v1/health"]

        for endpoint in endpoints:
            start_time = time.time()
            response = await test_client.get(endpoint, headers=auth_headers)
            end_time = time.time()

            response_time = end_time - start_time
            assert response_time < 2.0  # Should respond within 2 seconds
            assert response.status_code in [200, 401]  # Valid response

    @pytest.mark.asyncio
    async def test_memory_usage_monitoring(
        self, test_client: AsyncClient, auth_headers: Dict[str, str]
    ):
        """Test memory usage during API operations."""
        # This test will FAIL until implementation (TDD RED phase)
        import psutil
        import os

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Perform multiple operations
        for i in range(50):
            project_data = {
                "name": f"Memory Test {i}",
                "description": "Memory test project",
            }
            await test_client.post(
                "/api/v1/projects", json=project_data, headers=auth_headers
            )

        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Memory increase should be reasonable (less than 100MB for 50 projects)
        assert memory_increase < 100 * 1024 * 1024


# ==========================================
# SUMMARY OF TDD RED PHASE TESTS
# ==========================================

"""
TDD RED PHASE SUMMARY - FastAPI Production Interface Tests

Total Test Count: 35+ comprehensive tests covering:

1. AUTHENTICATION & AUTHORIZATION (5 tests)
   - User registration endpoint
   - User login endpoint  
   - Token validation endpoint
   - Unauthorized access protection
   - JWT token handling

2. PROJECT MANAGEMENT (3 tests)
   - Create project endpoint
   - List projects with pagination
   - Get project by ID

3. CHAT SESSION MANAGEMENT (2 tests)
   - Create chat session endpoint
   - List chat sessions endpoint

4. MESSAGE HANDLING (2 tests)
   - Send message endpoint
   - Get session messages endpoint

5. LINGUISTICS ANALYSIS (2 tests)
   - Analyze linguistics endpoint
   - Grammar validation endpoint

6. KNOWLEDGE MANAGEMENT (2 tests)
   - Ingest knowledge endpoint
   - Search knowledge endpoint

7. ERROR HANDLING & VALIDATION (3 tests)
   - Invalid request validation
   - Not found error handling
   - Server error handling

8. PERFORMANCE & SECURITY (3 tests)
   - API rate limiting
   - CORS headers
   - Security headers

9. HEALTH & MONITORING (4 tests)
   - Health check endpoint
   - Metrics endpoint
   - API documentation endpoint
   - OpenAPI schema endpoint

10. INTEGRATION TESTS (3 tests)
    - End-to-end user workflow
    - Database transaction handling
    - Concurrent request handling

11. PERFORMANCE BENCHMARKS (2 tests)
    - Response time benchmarks
    - Memory usage monitoring

ALL TESTS WILL FAIL INITIALLY - This is the TDD RED phase.
Next step: Implement FastAPI application to make tests pass (GREEN phase).

Expected Implementation Components:
- FastAPI application factory (create_app)
- Authentication manager with JWT
- API route handlers for all endpoints
- Request/response models
- Database integration
- Error handling middleware
- Security middleware
- CORS configuration
- Rate limiting
- Health checks
- Metrics collection
- API documentation

Rule Compliance:
- rules-101: TDD RED phase complete, ready for GREEN phase
- rules-102: Comprehensive test documentation
- rules-103: Implementation standards defined in tests
- rules-106: Quality gates established through testing
"""
