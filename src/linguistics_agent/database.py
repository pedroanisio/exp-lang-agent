"""
File: database.py
Path: src/linguistics_agent/database.py
Purpose: Database manager for AI Linguistics Agent
Author: AI Agent
Created: 2025-07-12
Rule Compliance: rules-101 v1.2+ (TDD GREEN), rules-103 v1.2+ (Standards), rules-104 v1.0 (Requirements)

TDD Phase: GREEN - Implement DatabaseManager to make tests pass
ADR Reference: ADR-004 (PostgreSQL State Management)
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any, List, AsyncGenerator
from datetime import datetime

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete, func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from .models.database import (
    Base,
    User,
    Project,
    Session as ChatSession,
    Message,
    KnowledgeEntry,
    APIKey,
    SystemConfig,
    AuditLog,
    UserRole,
    MessageType,
)
from .config import Settings


logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Base exception for database operations."""

    pass


class DatabaseConnectionError(DatabaseError):
    """Exception for database connection issues."""

    pass


class DatabaseIntegrityError(DatabaseError):
    """Exception for database integrity violations."""

    pass


class DatabaseManager:
    """
    Database manager for handling all database operations.

    Provides async database operations with connection pooling,
    transaction management, and CRUD operations for all models.
    """

    def __init__(self, database_url: str, echo: bool = False):
        """
        Initialize database manager.

        Args:
            database_url: Database connection URL
            echo: Whether to echo SQL statements (for debugging)
        """
        self.database_url = database_url
        self.echo = echo
        self.engine: Optional[AsyncEngine] = None
        self.session_factory: Optional[async_sessionmaker] = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize database engine and create tables."""
        try:
            # Create async engine with connection pooling
            self.engine = create_async_engine(
                self.database_url,
                echo=self.echo,
                pool_size=20,
                max_overflow=30,
                pool_pre_ping=True,
                pool_recycle=3600,  # 1 hour
            )

            # Create session factory
            self.session_factory = async_sessionmaker(
                self.engine, class_=AsyncSession, expire_on_commit=False
            )

            # Create all tables
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            self._initialized = True
            logger.info("Database initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise DatabaseConnectionError(f"Database initialization failed: {e}")

    async def close(self) -> None:
        """Close database connections."""
        if self.engine:
            await self.engine.dispose()
            self._initialized = False
            logger.info("Database connections closed")

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get database session with automatic cleanup.

        Yields:
            AsyncSession: Database session
        """
        if not self._initialized:
            raise DatabaseConnectionError("Database not initialized")

        async with self.session_factory() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"Database session error: {e}")
                raise
            finally:
                await session.close()

    # User CRUD operations
    async def create_user(
        self,
        username: str,
        email: str,
        password_hash: str,
        role: UserRole = UserRole.USER,
        **kwargs,
    ) -> User:
        """Create a new user."""
        async with self.get_session() as session:
            try:
                user = User(
                    username=username,
                    email=email,
                    password_hash=password_hash,
                    role=role,
                    **kwargs,
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user
            except IntegrityError as e:
                await session.rollback()
                raise DatabaseIntegrityError(f"User creation failed: {e}")

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        async with self.get_session() as session:
            result = await session.execute(
                select(User).where(User.id == user_id, User.is_active == True)
            )
            return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        async with self.get_session() as session:
            result = await session.execute(
                select(User).where(User.email == email, User.is_active == True)
            )
            return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        async with self.get_session() as session:
            result = await session.execute(
                select(User).where(User.username == username, User.is_active == True)
            )
            return result.scalar_one_or_none()

    async def update_user(
        self, user_id: int, updates: Dict[str, Any]
    ) -> Optional[User]:
        """Update user information."""
        async with self.get_session() as session:
            try:
                # Update user
                await session.execute(
                    update(User)
                    .where(User.id == user_id)
                    .values(**updates, updated_at=datetime.utcnow())
                )
                await session.commit()

                # Return updated user
                return await self.get_user_by_id(user_id)
            except IntegrityError as e:
                await session.rollback()
                raise DatabaseIntegrityError(f"User update failed: {e}")

    async def delete_user(self, user_id: int) -> bool:
        """Soft delete user."""
        async with self.get_session() as session:
            try:
                await session.execute(
                    update(User)
                    .where(User.id == user_id)
                    .values(is_active=False, updated_at=datetime.utcnow())
                )
                await session.commit()
                return True
            except Exception as e:
                await session.rollback()
                logger.error(f"User deletion failed: {e}")
                return False

    # Project CRUD operations
    async def create_project(
        self, name: str, user_id: int, description: Optional[str] = None, **kwargs
    ) -> Project:
        """Create a new project."""
        async with self.get_session() as session:
            try:
                project = Project(
                    name=name, user_id=user_id, description=description, **kwargs
                )
                session.add(project)
                await session.commit()
                await session.refresh(project)
                return project
            except IntegrityError as e:
                await session.rollback()
                raise DatabaseIntegrityError(f"Project creation failed: {e}")

    async def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """Get project by ID."""
        async with self.get_session() as session:
            result = await session.execute(
                select(Project)
                .where(Project.id == project_id, Project.is_active == True)
                .options(selectinload(Project.user))
            )
            return result.scalar_one_or_none()

    async def get_user_projects(self, user_id: int) -> List[Project]:
        """Get all projects for a user."""
        async with self.get_session() as session:
            result = await session.execute(
                select(Project)
                .where(Project.user_id == user_id, Project.is_active == True)
                .order_by(Project.updated_at.desc())
            )
            return result.scalars().all()

    # Session CRUD operations
    async def create_session(
        self, title: str, user_id: int, project_id: Optional[int] = None, **kwargs
    ) -> ChatSession:
        """Create a new chat session."""
        async with self.get_session() as session:
            try:
                chat_session = ChatSession(
                    title=title, user_id=user_id, project_id=project_id, **kwargs
                )
                session.add(chat_session)
                await session.commit()
                await session.refresh(chat_session)
                return chat_session
            except IntegrityError as e:
                await session.rollback()
                raise DatabaseIntegrityError(f"Session creation failed: {e}")

    async def get_session_by_id(self, session_id: int) -> Optional[ChatSession]:
        """Get session by ID."""
        async with self.get_session() as session:
            result = await session.execute(
                select(ChatSession)
                .where(ChatSession.id == session_id, ChatSession.is_active == True)
                .options(
                    selectinload(ChatSession.user),
                    selectinload(ChatSession.project),
                    selectinload(ChatSession.messages),
                )
            )
            return result.scalar_one_or_none()

    async def get_user_sessions(self, user_id: int) -> List[ChatSession]:
        """Get all sessions for a user."""
        async with self.get_session() as session:
            result = await session.execute(
                select(ChatSession)
                .where(ChatSession.user_id == user_id, ChatSession.is_active == True)
                .order_by(
                    ChatSession.last_activity.desc().nullslast(),
                    ChatSession.updated_at.desc(),
                )
            )
            return result.scalars().all()

    # Message CRUD operations
    async def create_message(
        self,
        content: str,
        message_type: MessageType,
        session_id: int,
        user_id: int,
        **kwargs,
    ) -> Message:
        """Create a new message."""
        async with self.get_session() as session:
            try:
                message = Message(
                    content=content,
                    message_type=message_type,
                    session_id=session_id,
                    user_id=user_id,
                    **kwargs,
                )
                session.add(message)

                # Update session message count and last activity
                await session.execute(
                    update(ChatSession)
                    .where(ChatSession.id == session_id)
                    .values(
                        message_count=ChatSession.message_count + 1,
                        last_activity=datetime.utcnow(),
                        updated_at=datetime.utcnow(),
                    )
                )

                await session.commit()
                await session.refresh(message)
                return message
            except IntegrityError as e:
                await session.rollback()
                raise DatabaseIntegrityError(f"Message creation failed: {e}")

    async def get_session_messages(
        self, session_id: int, limit: Optional[int] = None, offset: int = 0
    ) -> List[Message]:
        """Get messages for a session."""
        async with self.get_session() as session:
            query = (
                select(Message)
                .where(Message.session_id == session_id)
                .order_by(Message.created_at)
                .offset(offset)
            )

            if limit:
                query = query.limit(limit)

            result = await session.execute(query)
            return result.scalars().all()

    # Knowledge Entry CRUD operations
    async def create_knowledge_entry(
        self, title: str, content: str, source_type: str, **kwargs
    ) -> KnowledgeEntry:
        """Create a new knowledge entry."""
        async with self.get_session() as session:
            try:
                knowledge_entry = KnowledgeEntry(
                    title=title, content=content, source_type=source_type, **kwargs
                )
                session.add(knowledge_entry)
                await session.commit()
                await session.refresh(knowledge_entry)
                return knowledge_entry
            except IntegrityError as e:
                await session.rollback()
                raise DatabaseIntegrityError(f"Knowledge entry creation failed: {e}")

    async def search_knowledge_entries(
        self, query: str, limit: int = 10, category: Optional[str] = None
    ) -> List[KnowledgeEntry]:
        """Search knowledge entries by content."""
        async with self.get_session() as session:
            # Basic text search (can be enhanced with full-text search)
            search_query = select(KnowledgeEntry).where(
                KnowledgeEntry.processed == True
            )

            if query:
                search_query = search_query.where(
                    KnowledgeEntry.content.ilike(f"%{query}%")
                    | KnowledgeEntry.title.ilike(f"%{query}%")
                )

            if category:
                search_query = search_query.where(KnowledgeEntry.category == category)

            search_query = search_query.order_by(
                KnowledgeEntry.relevance_score.desc().nullslast(),
                KnowledgeEntry.quality_score.desc().nullslast(),
                KnowledgeEntry.access_count.desc(),
            ).limit(limit)

            result = await session.execute(search_query)
            return result.scalars().all()

    # System configuration operations
    async def get_config(self, key: str) -> Optional[Any]:
        """Get system configuration value."""
        async with self.get_session() as session:
            result = await session.execute(
                select(SystemConfig.value).where(SystemConfig.key == key)
            )
            config = result.scalar_one_or_none()
            return config

    async def set_config(
        self, key: str, value: Any, description: Optional[str] = None
    ) -> None:
        """Set system configuration value."""
        async with self.get_session() as session:
            try:
                # Try to update existing config
                result = await session.execute(
                    update(SystemConfig)
                    .where(SystemConfig.key == key)
                    .values(value=value, updated_at=datetime.utcnow())
                )

                if result.rowcount == 0:
                    # Create new config if it doesn't exist
                    config = SystemConfig(
                        key=key,
                        value=value,
                        description=description,
                        category="general",
                    )
                    session.add(config)

                await session.commit()
            except Exception as e:
                await session.rollback()
                raise DatabaseError(f"Config update failed: {e}")

    # Audit logging
    async def log_audit(
        self,
        action: str,
        resource_type: str,
        user_id: Optional[int] = None,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        success: bool = True,
        error_message: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Log audit event."""
        async with self.get_session() as session:
            try:
                audit_log = AuditLog(
                    user_id=user_id,
                    action=action,
                    resource_type=resource_type,
                    resource_id=resource_id,
                    details=details or {},
                    success=success,
                    error_message=error_message,
                    **kwargs,
                )
                session.add(audit_log)
                await session.commit()
            except Exception as e:
                # Don't fail the main operation if audit logging fails
                logger.error(f"Audit logging failed: {e}")

    # Health check and statistics
    async def health_check(self) -> Dict[str, Any]:
        """Perform database health check."""
        try:
            async with self.get_session() as session:
                # Test basic connectivity
                result = await session.execute(select(func.now()))
                db_time = result.scalar()

                # Get basic statistics
                user_count = await session.scalar(select(func.count(User.id)))
                project_count = await session.scalar(select(func.count(Project.id)))
                session_count = await session.scalar(select(func.count(ChatSession.id)))
                message_count = await session.scalar(select(func.count(Message.id)))

                return {
                    "status": "healthy",
                    "database_time": db_time,
                    "statistics": {
                        "users": user_count,
                        "projects": project_count,
                        "sessions": session_count,
                        "messages": message_count,
                    },
                }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def get_database_stats(self) -> Dict[str, Any]:
        """Get detailed database statistics."""
        async with self.get_session() as session:
            stats = {}

            # User statistics
            user_stats = await session.execute(
                select(
                    func.count(User.id).label("total"),
                    func.count(User.id).filter(User.is_active == True).label("active"),
                    func.count(User.id)
                    .filter(User.role == UserRole.ADMIN)
                    .label("admins"),
                )
            )
            stats["users"] = user_stats.first()._asdict()

            # Project statistics
            project_stats = await session.execute(
                select(
                    func.count(Project.id).label("total"),
                    func.count(Project.id)
                    .filter(Project.is_active == True)
                    .label("active"),
                )
            )
            stats["projects"] = project_stats.first()._asdict()

            # Session statistics
            session_stats = await session.execute(
                select(
                    func.count(ChatSession.id).label("total"),
                    func.count(ChatSession.id)
                    .filter(ChatSession.is_active == True)
                    .label("active"),
                    func.avg(ChatSession.message_count).label("avg_messages"),
                )
            )
            stats["sessions"] = session_stats.first()._asdict()

            # Message statistics
            message_stats = await session.execute(
                select(
                    func.count(Message.id).label("total"),
                    func.count(Message.id)
                    .filter(Message.message_type == MessageType.USER)
                    .label("user_messages"),
                    func.count(Message.id)
                    .filter(Message.message_type == MessageType.ASSISTANT)
                    .label("assistant_messages"),
                )
            )
            stats["messages"] = message_stats.first()._asdict()

            # Knowledge statistics
            knowledge_stats = await session.execute(
                select(
                    func.count(KnowledgeEntry.id).label("total"),
                    func.count(KnowledgeEntry.id)
                    .filter(KnowledgeEntry.processed == True)
                    .label("processed"),
                    func.avg(KnowledgeEntry.quality_score).label("avg_quality"),
                )
            )
            stats["knowledge"] = knowledge_stats.first()._asdict()

            return stats


# Global database manager instance
db_manager: Optional[DatabaseManager] = None


async def get_database_manager() -> DatabaseManager:
    """Get the global database manager instance."""
    global db_manager
    if db_manager is None:
        settings = Settings()
        db_manager = DatabaseManager(settings.database_url, echo=settings.debug)
        await db_manager.initialize()
    return db_manager


async def close_database_manager() -> None:
    """Close the global database manager."""
    global db_manager
    if db_manager:
        await db_manager.close()
        db_manager = None


# Export main classes and functions
__all__ = [
    "DatabaseManager",
    "DatabaseError",
    "DatabaseConnectionError",
    "DatabaseIntegrityError",
    "get_database_manager",
    "close_database_manager",
]
