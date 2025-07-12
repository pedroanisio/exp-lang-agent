"""
File: test_database_models.py
Path: tests/unit/test_database_models.py
Purpose: Unit tests for database models (TDD RED phase)
Author: AI Agent
Created: 2025-07-12
Rule Compliance: rules-101 v1.2+ (TDD), rules-103 v1.2+ (Standards)

TDD Phase: RED - Write failing tests first
These tests will fail until we implement the database models
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func
from typing import AsyncGenerator

# Import models that don't exist yet (will cause import errors - RED phase)
from linguistics_agent.models.database import (
    Base,
    User,
    Project,
    Session as ChatSession,
    Message,
    KnowledgeEntry,
    UserRole,
    MessageType,
)
from linguistics_agent.database import DatabaseManager


class TestDatabaseModels:
    """Test suite for database models following TDD methodology."""

    @pytest.fixture
    async def db_engine(self):
        """Create test database engine."""
        # Use in-memory SQLite for testing
        engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield engine

        # Cleanup
        await engine.dispose()

    @pytest.fixture
    async def db_session(self, db_engine) -> AsyncGenerator[AsyncSession, None]:
        """Create test database session."""
        async_session = sessionmaker(
            db_engine, class_=AsyncSession, expire_on_commit=False
        )

        async with async_session() as session:
            yield session

    @pytest.mark.asyncio
    async def test_user_model_creation(self, db_session: AsyncSession):
        """Test User model creation and validation."""
        # This test will fail until User model is implemented
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password_123",
            role=UserRole.USER,
            is_active=True,
        )

        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.role == UserRole.USER
        assert user.is_active is True
        assert user.created_at is not None
        assert user.updated_at is not None

    @pytest.mark.asyncio
    async def test_user_model_validation(self, db_session: AsyncSession):
        """Test User model field validation."""
        # Test email uniqueness constraint
        user1 = User(
            username="user1",
            email="duplicate@example.com",
            password_hash="hash1",
            role=UserRole.USER,
        )

        user2 = User(
            username="user2",
            email="duplicate@example.com",  # Duplicate email
            password_hash="hash2",
            role=UserRole.USER,
        )

        db_session.add(user1)
        await db_session.commit()

        db_session.add(user2)
        with pytest.raises(Exception):  # Should raise integrity error
            await db_session.commit()

    @pytest.mark.asyncio
    async def test_user_role_enum(self):
        """Test UserRole enum values."""
        assert UserRole.ADMIN == "admin"
        assert UserRole.USER == "user"
        assert UserRole.READONLY == "readonly"

    @pytest.mark.asyncio
    async def test_project_model_creation(self, db_session: AsyncSession):
        """Test Project model creation and user relationship."""
        # Create user first
        user = User(
            username="projectowner",
            email="owner@example.com",
            password_hash="hashed_password",
            role=UserRole.USER,
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Create project
        project = Project(
            name="Test Linguistics Project",
            description="A project for testing linguistic analysis",
            user_id=user.id,
            is_active=True,
        )

        db_session.add(project)
        await db_session.commit()
        await db_session.refresh(project)

        assert project.id is not None
        assert project.name == "Test Linguistics Project"
        assert project.user_id == user.id
        assert project.is_active is True
        assert project.created_at is not None

    @pytest.mark.asyncio
    async def test_chat_session_model_creation(self, db_session: AsyncSession):
        """Test ChatSession model creation and relationships."""
        # Create user and project
        user = User(
            username="sessionuser",
            email="session@example.com",
            password_hash="hashed_password",
            role=UserRole.USER,
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        project = Project(
            name="Session Project",
            description="Project for session testing",
            user_id=user.id,
        )
        db_session.add(project)
        await db_session.commit()
        await db_session.refresh(project)

        # Create chat session
        chat_session = ChatSession(
            title="Test Chat Session",
            user_id=user.id,
            project_id=project.id,
            is_active=True,
        )

        db_session.add(chat_session)
        await db_session.commit()
        await db_session.refresh(chat_session)

        assert chat_session.id is not None
        assert chat_session.title == "Test Chat Session"
        assert chat_session.user_id == user.id
        assert chat_session.project_id == project.id
        assert chat_session.is_active is True

    @pytest.mark.asyncio
    async def test_message_model_creation(self, db_session: AsyncSession):
        """Test Message model creation and session relationship."""
        # Create user, project, and session
        user = User(
            username="messageuser",
            email="message@example.com",
            password_hash="hashed_password",
            role=UserRole.USER,
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        project = Project(
            name="Message Project",
            description="Project for message testing",
            user_id=user.id,
        )
        db_session.add(project)
        await db_session.commit()
        await db_session.refresh(project)

        chat_session = ChatSession(
            title="Message Session", user_id=user.id, project_id=project.id
        )
        db_session.add(chat_session)
        await db_session.commit()
        await db_session.refresh(chat_session)

        # Create message
        message = Message(
            content="What is the syntax of this EBNF grammar?",
            message_type=MessageType.USER,
            session_id=chat_session.id,
            user_id=user.id,
        )

        db_session.add(message)
        await db_session.commit()
        await db_session.refresh(message)

        assert message.id is not None
        assert message.content == "What is the syntax of this EBNF grammar?"
        assert message.message_type == MessageType.USER
        assert message.session_id == chat_session.id
        assert message.user_id == user.id
        assert message.created_at is not None

    @pytest.mark.asyncio
    async def test_message_type_enum(self):
        """Test MessageType enum values."""
        assert MessageType.USER == "user"
        assert MessageType.ASSISTANT == "assistant"
        assert MessageType.SYSTEM == "system"

    @pytest.mark.asyncio
    async def test_knowledge_entry_model_creation(self, db_session: AsyncSession):
        """Test KnowledgeEntry model creation."""
        knowledge_entry = KnowledgeEntry(
            title="EBNF Grammar Rules",
            content="Extended Backus-Naur Form (EBNF) is a notation...",
            source_type="article",
            source_url="https://example.com/ebnf-guide",
            tags=["ebnf", "grammar", "parsing"],
            metadata={"author": "John Doe", "year": 2023},
        )

        db_session.add(knowledge_entry)
        await db_session.commit()
        await db_session.refresh(knowledge_entry)

        assert knowledge_entry.id is not None
        assert knowledge_entry.title == "EBNF Grammar Rules"
        assert knowledge_entry.source_type == "article"
        assert "ebnf" in knowledge_entry.tags
        assert knowledge_entry.metadata["author"] == "John Doe"

    @pytest.mark.asyncio
    async def test_user_projects_relationship(self, db_session: AsyncSession):
        """Test User-Project relationship."""
        user = User(
            username="multiproject",
            email="multi@example.com",
            password_hash="hashed_password",
            role=UserRole.USER,
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Create multiple projects for the user
        project1 = Project(
            name="Project 1", description="First project", user_id=user.id
        )
        project2 = Project(
            name="Project 2", description="Second project", user_id=user.id
        )

        db_session.add_all([project1, project2])
        await db_session.commit()

        # Test relationship
        result = await db_session.execute(
            select(Project).where(Project.user_id == user.id)
        )
        user_projects = result.scalars().all()

        assert len(user_projects) == 2
        assert any(p.name == "Project 1" for p in user_projects)
        assert any(p.name == "Project 2" for p in user_projects)

    @pytest.mark.asyncio
    async def test_session_messages_relationship(self, db_session: AsyncSession):
        """Test ChatSession-Message relationship."""
        # Create user, project, and session
        user = User(
            username="chatuser",
            email="chat@example.com",
            password_hash="hashed_password",
            role=UserRole.USER,
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        project = Project(
            name="Chat Project", description="Project for chat testing", user_id=user.id
        )
        db_session.add(project)
        await db_session.commit()
        await db_session.refresh(project)

        chat_session = ChatSession(
            title="Chat with Messages", user_id=user.id, project_id=project.id
        )
        db_session.add(chat_session)
        await db_session.commit()
        await db_session.refresh(chat_session)

        # Create multiple messages
        message1 = Message(
            content="Hello, can you help with EBNF?",
            message_type=MessageType.USER,
            session_id=chat_session.id,
            user_id=user.id,
        )
        message2 = Message(
            content="Of course! I'd be happy to help with EBNF grammar.",
            message_type=MessageType.ASSISTANT,
            session_id=chat_session.id,
            user_id=user.id,
        )

        db_session.add_all([message1, message2])
        await db_session.commit()

        # Test relationship
        result = await db_session.execute(
            select(Message)
            .where(Message.session_id == chat_session.id)
            .order_by(Message.created_at)
        )
        session_messages = result.scalars().all()

        assert len(session_messages) == 2
        assert session_messages[0].message_type == MessageType.USER
        assert session_messages[1].message_type == MessageType.ASSISTANT

    @pytest.mark.asyncio
    async def test_database_manager_connection(self):
        """Test DatabaseManager connection and session management."""
        # This will fail until DatabaseManager is implemented
        db_manager = DatabaseManager("sqlite+aiosqlite:///:memory:")

        await db_manager.initialize()

        async with db_manager.get_session() as session:
            assert isinstance(session, AsyncSession)

        await db_manager.close()

    @pytest.mark.asyncio
    async def test_database_manager_crud_operations(self):
        """Test DatabaseManager CRUD operations."""
        db_manager = DatabaseManager("sqlite+aiosqlite:///:memory:")
        await db_manager.initialize()

        # Test user creation
        user_data = {
            "username": "cruduser",
            "email": "crud@example.com",
            "password_hash": "hashed_password",
            "role": UserRole.USER,
        }

        user = await db_manager.create_user(**user_data)
        assert user.id is not None
        assert user.username == "cruduser"

        # Test user retrieval
        retrieved_user = await db_manager.get_user_by_id(user.id)
        assert retrieved_user.username == "cruduser"

        # Test user update
        updated_user = await db_manager.update_user(
            user.id, {"username": "updateduser"}
        )
        assert updated_user.username == "updateduser"

        # Test user deletion
        await db_manager.delete_user(user.id)
        deleted_user = await db_manager.get_user_by_id(user.id)
        assert deleted_user is None

        await db_manager.close()

    @pytest.mark.asyncio
    async def test_database_indexes_and_constraints(self, db_session: AsyncSession):
        """Test database indexes and constraints."""
        # Test unique constraint on email
        user1 = User(
            username="user1",
            email="unique@example.com",
            password_hash="hash1",
            role=UserRole.USER,
        )

        db_session.add(user1)
        await db_session.commit()

        # Try to create another user with same email
        user2 = User(
            username="user2",
            email="unique@example.com",  # Same email
            password_hash="hash2",
            role=UserRole.USER,
        )

        db_session.add(user2)
        with pytest.raises(Exception):  # Should raise integrity error
            await db_session.commit()

    @pytest.mark.asyncio
    async def test_soft_delete_functionality(self, db_session: AsyncSession):
        """Test soft delete functionality for projects and sessions."""
        user = User(
            username="softdeleteuser",
            email="softdelete@example.com",
            password_hash="hashed_password",
            role=UserRole.USER,
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        project = Project(
            name="Soft Delete Project",
            description="Project to test soft delete",
            user_id=user.id,
            is_active=True,
        )
        db_session.add(project)
        await db_session.commit()
        await db_session.refresh(project)

        # Soft delete project
        project.is_active = False
        project.deleted_at = datetime.utcnow()
        await db_session.commit()

        # Verify soft delete
        result = await db_session.execute(
            select(Project).where(Project.id == project.id, Project.is_active == True)
        )
        active_project = result.scalar_one_or_none()
        assert active_project is None

        # Verify project still exists in database
        result = await db_session.execute(
            select(Project).where(Project.id == project.id)
        )
        deleted_project = result.scalar_one_or_none()
        assert deleted_project is not None
        assert deleted_project.is_active is False
        assert deleted_project.deleted_at is not None

    @pytest.mark.asyncio
    async def test_timestamp_auto_update(self, db_session: AsyncSession):
        """Test automatic timestamp updates."""
        user = User(
            username="timestampuser",
            email="timestamp@example.com",
            password_hash="hashed_password",
            role=UserRole.USER,
        )

        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        original_created_at = user.created_at
        original_updated_at = user.updated_at

        # Wait a moment and update
        await asyncio.sleep(0.1)
        user.username = "updatedtimestamp"
        await db_session.commit()
        await db_session.refresh(user)

        # Verify timestamps
        assert user.created_at == original_created_at  # Should not change
        assert user.updated_at > original_updated_at  # Should be updated

    @pytest.mark.asyncio
    async def test_json_field_storage(self, db_session: AsyncSession):
        """Test JSON field storage and retrieval."""
        knowledge_entry = KnowledgeEntry(
            title="JSON Test Entry",
            content="Content with JSON metadata",
            source_type="test",
            tags=["json", "test"],
            metadata={
                "complex_data": {
                    "nested": {"value": 123},
                    "array": [1, 2, 3],
                    "boolean": True,
                },
                "simple_string": "test",
            },
        )

        db_session.add(knowledge_entry)
        await db_session.commit()
        await db_session.refresh(knowledge_entry)

        # Verify JSON storage and retrieval
        assert knowledge_entry.metadata["complex_data"]["nested"]["value"] == 123
        assert knowledge_entry.metadata["complex_data"]["array"] == [1, 2, 3]
        assert knowledge_entry.metadata["complex_data"]["boolean"] is True
        assert knowledge_entry.metadata["simple_string"] == "test"

    @pytest.mark.asyncio
    async def test_database_performance_indexes(self, db_session: AsyncSession):
        """Test that performance indexes are working."""
        # Create test data
        user = User(
            username="perfuser",
            email="perf@example.com",
            password_hash="hashed_password",
            role=UserRole.USER,
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Create multiple projects and sessions
        for i in range(10):
            project = Project(
                name=f"Project {i}", description=f"Description {i}", user_id=user.id
            )
            db_session.add(project)

        await db_session.commit()

        # Test query performance (should use indexes)
        start_time = datetime.utcnow()
        result = await db_session.execute(
            select(Project).where(Project.user_id == user.id)
        )
        projects = result.scalars().all()
        end_time = datetime.utcnow()

        # Verify results and performance
        assert len(projects) == 10
        query_time = (end_time - start_time).total_seconds()
        assert query_time < 1.0  # Should be fast with proper indexes
