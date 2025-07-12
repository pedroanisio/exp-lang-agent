"""
File: database.py
Path: src/linguistics_agent/models/database.py
Purpose: SQLAlchemy database models for AI Linguistics Agent
Author: AI Agent
Created: 2025-07-12
Rule Compliance: rules-101 v1.2+ (TDD GREEN), rules-103 v1.2+ (Standards), rules-104 v1.0 (Requirements)

TDD Phase: GREEN - Implement models to make tests pass
ADR Reference: ADR-004 (PostgreSQL State Management)
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    Index,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func


# Base class for all models
Base = declarative_base()


class UserRole(str, Enum):
    """User role enumeration for RBAC."""

    ADMIN = "admin"
    USER = "user"
    READONLY = "readonly"


class MessageType(str, Enum):
    """Message type enumeration for chat messages."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class TimestampMixin:
    """Mixin for automatic timestamp management."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class SoftDeleteMixin:
    """Mixin for soft delete functionality."""

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class User(Base, TimestampMixin):
    """User model for authentication and authorization."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        String(20), default=UserRole.USER, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Profile information
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Authentication tracking
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    login_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    projects: Mapped[List["Project"]] = relationship(
        "Project", back_populates="user", cascade="all, delete-orphan"
    )
    sessions: Mapped[List["Session"]] = relationship(
        "Session", back_populates="user", cascade="all, delete-orphan"
    )
    messages: Mapped[List["Message"]] = relationship(
        "Message", back_populates="user", cascade="all, delete-orphan"
    )

    # Indexes for performance
    __table_args__ = (
        Index("idx_users_email", "email"),
        Index("idx_users_username", "username"),
        Index("idx_users_role", "role"),
        Index("idx_users_active", "is_active"),
        CheckConstraint(
            "role IN ('admin', 'user', 'readonly')", name="check_user_role"
        ),
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"


class Project(Base, TimestampMixin, SoftDeleteMixin):
    """Project model for organizing linguistic analysis work."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Foreign key to user
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Project settings
    settings: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="projects")
    sessions: Mapped[List["Session"]] = relationship(
        "Session", back_populates="project", cascade="all, delete-orphan"
    )

    # Indexes for performance
    __table_args__ = (
        Index("idx_projects_user_id", "user_id"),
        Index("idx_projects_active", "is_active"),
        Index("idx_projects_name", "name"),
        Index("idx_projects_user_active", "user_id", "is_active"),
    )

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name='{self.name}', user_id={self.user_id})>"


class Session(Base, TimestampMixin, SoftDeleteMixin):
    """Chat session model for conversation management."""

    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)

    # Foreign keys
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    project_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True
    )

    # Session metadata
    context: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Session statistics
    message_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_activity: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="sessions")
    project: Mapped[Optional["Project"]] = relationship(
        "Project", back_populates="sessions"
    )
    messages: Mapped[List["Message"]] = relationship(
        "Message",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )

    # Indexes for performance
    __table_args__ = (
        Index("idx_sessions_user_id", "user_id"),
        Index("idx_sessions_project_id", "project_id"),
        Index("idx_sessions_active", "is_active"),
        Index("idx_sessions_last_activity", "last_activity"),
        Index("idx_sessions_user_active", "user_id", "is_active"),
    )

    def __repr__(self) -> str:
        return f"<Session(id={self.id}, title='{self.title}', user_id={self.user_id})>"


class Message(Base, TimestampMixin):
    """Message model for chat conversation storage."""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    message_type: Mapped[MessageType] = mapped_column(String(20), nullable=False)

    # Foreign keys
    session_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Message metadata
    metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # AI response metadata
    model_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    response_time: Mapped[Optional[float]] = mapped_column(nullable=True)

    # Message processing
    processed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    session: Mapped["Session"] = relationship("Session", back_populates="messages")
    user: Mapped["User"] = relationship("User", back_populates="messages")

    # Indexes for performance
    __table_args__ = (
        Index("idx_messages_session_id", "session_id"),
        Index("idx_messages_user_id", "user_id"),
        Index("idx_messages_type", "message_type"),
        Index("idx_messages_created_at", "created_at"),
        Index("idx_messages_session_created", "session_id", "created_at"),
        CheckConstraint(
            "message_type IN ('user', 'assistant', 'system')", name="check_message_type"
        ),
    )

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, type='{self.message_type}', session_id={self.session_id})>"


class KnowledgeEntry(Base, TimestampMixin):
    """Knowledge entry model for storing linguistic knowledge base."""

    __tablename__ = "knowledge_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Source information
    source_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # url, pdf, text, file
    source_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    source_file: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Content classification
    tags: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=list)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)

    # Content metadata
    metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

    # Processing status
    processed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    embedding_generated: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    # Quality metrics
    quality_score: Mapped[Optional[float]] = mapped_column(nullable=True)
    relevance_score: Mapped[Optional[float]] = mapped_column(nullable=True)

    # Usage statistics
    access_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_accessed: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Indexes for performance
    __table_args__ = (
        Index("idx_knowledge_title", "title"),
        Index("idx_knowledge_source_type", "source_type"),
        Index("idx_knowledge_category", "category"),
        Index("idx_knowledge_language", "language"),
        Index("idx_knowledge_processed", "processed"),
        Index("idx_knowledge_embedding", "embedding_generated"),
        Index("idx_knowledge_quality", "quality_score"),
        Index("idx_knowledge_access_count", "access_count"),
        CheckConstraint(
            "source_type IN ('url', 'pdf', 'text', 'file')", name="check_source_type"
        ),
        CheckConstraint(
            "quality_score >= 0 AND quality_score <= 1", name="check_quality_score"
        ),
        CheckConstraint(
            "relevance_score >= 0 AND relevance_score <= 1",
            name="check_relevance_score",
        ),
    )

    def __repr__(self) -> str:
        return f"<KnowledgeEntry(id={self.id}, title='{self.title[:50]}...', source_type='{self.source_type}')>"


class APIKey(Base, TimestampMixin):
    """API key model for external service integration."""

    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    service: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # anthropic, openai, etc.

    # Key data (encrypted)
    key_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    key_preview: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # First/last few chars

    # Usage tracking
    usage_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_used: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Key management
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Indexes for performance
    __table_args__ = (
        Index("idx_api_keys_service", "service"),
        Index("idx_api_keys_active", "is_active"),
        Index("idx_api_keys_expires", "expires_at"),
        UniqueConstraint("name", "service", name="uq_api_key_name_service"),
        CheckConstraint(
            "service IN ('anthropic', 'openai', 'neo4j', 'chromadb')",
            name="check_service_type",
        ),
    )

    def __repr__(self) -> str:
        return f"<APIKey(id={self.id}, name='{self.name}', service='{self.service}')>"


class SystemConfig(Base, TimestampMixin):
    """System configuration model for application settings."""

    __tablename__ = "system_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    value: Mapped[Any] = mapped_column(JSON, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Configuration metadata
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    is_sensitive: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    requires_restart: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    # Version control
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Indexes for performance
    __table_args__ = (
        Index("idx_system_config_key", "key"),
        Index("idx_system_config_category", "category"),
        Index("idx_system_config_sensitive", "is_sensitive"),
    )

    def __repr__(self) -> str:
        return f"<SystemConfig(id={self.id}, key='{self.key}', category='{self.category}')>"


class AuditLog(Base, TimestampMixin):
    """Audit log model for tracking system activities."""

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # User and action information
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)
    resource_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Action details
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    ip_address: Mapped[Optional[str]] = mapped_column(
        String(45), nullable=True
    )  # IPv6 support
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Result information
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Indexes for performance
    __table_args__ = (
        Index("idx_audit_logs_user_id", "user_id"),
        Index("idx_audit_logs_action", "action"),
        Index("idx_audit_logs_resource", "resource_type", "resource_id"),
        Index("idx_audit_logs_created_at", "created_at"),
        Index("idx_audit_logs_success", "success"),
        Index("idx_audit_logs_user_action", "user_id", "action"),
    )

    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action='{self.action}', resource_type='{self.resource_type}')>"


# Create all indexes and constraints
def create_additional_indexes(engine):
    """Create additional performance indexes."""
    # This function can be called after table creation to add custom indexes
    # that might not be easily defined in the model classes
    pass


# Model registry for easy access
MODEL_REGISTRY = {
    "User": User,
    "Project": Project,
    "Session": Session,
    "Message": Message,
    "KnowledgeEntry": KnowledgeEntry,
    "APIKey": APIKey,
    "SystemConfig": SystemConfig,
    "AuditLog": AuditLog,
}

# Export all models and enums
__all__ = [
    "Base",
    "User",
    "Project",
    "Session",
    "Message",
    "KnowledgeEntry",
    "APIKey",
    "SystemConfig",
    "AuditLog",
    "UserRole",
    "MessageType",
    "TimestampMixin",
    "SoftDeleteMixin",
    "MODEL_REGISTRY",
    "create_additional_indexes",
]
