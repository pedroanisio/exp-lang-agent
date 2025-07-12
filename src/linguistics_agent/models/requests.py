"""
File: requests.py
Path: src/linguistics_agent/models/requests.py
Purpose: Request models for linguistics agent queries
Author: AI Development Team
Created: 2024-12-07
Modified: 2024-12-07
Description: Pydantic models for incoming requests to the linguistics agent
Rule Compliance: rules-101 v1.2, rules-102 v1.2, rules-103 v1.2
"""

from typing import Any, Dict, List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field, validator


class QueryType(str, Enum):
    """Types of linguistics queries supported by the agent."""

    GENERAL = "general"
    EBNF_VALIDATION = "ebnf_validation"
    GRAMMAR_ANALYSIS = "grammar_analysis"
    ANTLR_OPTIMIZATION = "antlr_optimization"
    LINGUISTIC_ANALYSIS = "linguistic_analysis"
    COMPILER_THEORY = "compiler_theory"
    FORMAL_LANGUAGE = "formal_language"
    SYNTAX_ANALYSIS = "syntax_analysis"
    SEMANTIC_ANALYSIS = "semantic_analysis"


class LinguisticsQuery(BaseModel):
    """
    Model for linguistics queries sent to the agent.

    This model represents a query that can be processed by the LinguisticsAgent,
    including the query text, type, and any additional context or parameters.
    """

    text: str = Field(
        ...,
        description="The main query text to be processed",
        min_length=1,
        max_length=10000,
    )

    query_type: QueryType = Field(
        default=QueryType.GENERAL,
        description="The type of linguistics query being made",
    )

    context: Dict[str, Any] = Field(
        default_factory=dict, description="Additional context information for the query"
    )

    session_id: Optional[str] = Field(
        default=None, description="Session identifier for conversation continuity"
    )

    user_id: Optional[str] = Field(
        default=None, description="User identifier for personalization"
    )

    language: str = Field(
        default="en", description="Language code for the query (ISO 639-1)"
    )

    priority: int = Field(
        default=1, description="Query priority level (1=low, 5=high)", ge=1, le=5
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata for the query"
    )

    @validator("text")
    def validate_text_content(cls, v: str) -> str:
        """Validate that query text is meaningful."""
        if not v.strip():
            raise ValueError("Query text cannot be empty or whitespace only")
        return v.strip()

    @validator("language")
    def validate_language_code(cls, v: str) -> str:
        """Validate language code format."""
        if len(v) != 2 or not v.isalpha():
            raise ValueError("Language must be a 2-letter ISO 639-1 code")
        return v.lower()

    class Config:
        """Pydantic configuration."""

        use_enum_values = True
        validate_assignment = True
        extra = "forbid"
        schema_extra = {
            "example": {
                "text": "Analyze this EBNF grammar for potential optimizations",
                "query_type": "ebnf_validation",
                "context": {
                    "grammar_source": "user_input",
                    "target_language": "python",
                },
                "session_id": "session_123",
                "language": "en",
                "priority": 3,
            }
        }


class EBNFValidationQuery(LinguisticsQuery):
    """Specialized query for EBNF grammar validation."""

    query_type: QueryType = Field(
        default=QueryType.EBNF_VALIDATION,
        description="Fixed query type for EBNF validation",
    )

    grammar_text: str = Field(
        ..., description="EBNF grammar text to validate", min_length=1
    )

    validation_level: str = Field(
        default="strict",
        description="Validation strictness level",
        pattern="^(strict|moderate|lenient)$",
    )


class GrammarAnalysisQuery(LinguisticsQuery):
    """Specialized query for grammar structure analysis."""

    query_type: QueryType = Field(
        default=QueryType.GRAMMAR_ANALYSIS,
        description="Fixed query type for grammar analysis",
    )

    grammar_text: str = Field(..., description="Grammar text to analyze", min_length=1)

    analysis_depth: str = Field(
        default="comprehensive",
        description="Depth of analysis to perform",
        pattern="^(basic|detailed|comprehensive)$",
    )

    include_suggestions: bool = Field(
        default=True, description="Whether to include optimization suggestions"
    )


class KnowledgeIngestionRequest(BaseModel):
    """Request model for knowledge ingestion service."""

    source_type: str = Field(
        ..., description="Type of knowledge source", pattern="^(url|pdf|text|file)$"
    )

    source_content: Union[str, bytes] = Field(
        ..., description="Content to ingest (URL, text, or file data)"
    )

    title: Optional[str] = Field(
        default=None, description="Title for the knowledge item"
    )

    tags: List[str] = Field(
        default_factory=list, description="Tags for categorizing the knowledge"
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata for the knowledge item"
    )

    process_immediately: bool = Field(
        default=True, description="Whether to process the content immediately"
    )

    @validator("tags")
    def validate_tags(cls, v: List[str]) -> List[str]:
        """Validate and normalize tags."""
        return [tag.strip().lower() for tag in v if tag.strip()]

    class Config:
        """Pydantic configuration."""

        validate_assignment = True
        extra = "forbid"
        schema_extra = {
            "example": {
                "source_type": "url",
                "source_content": "https://example.com/linguistics-paper.pdf",
                "title": "Advanced Parsing Techniques",
                "tags": ["parsing", "compiler-theory", "algorithms"],
                "metadata": {"author": "Dr. Smith", "publication_year": 2023},
            }
        }


# Authentication Request Models

class UserRegistrationRequest(BaseModel):
    """Request model for user registration."""
    
    email: str = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    full_name: str = Field(..., min_length=1, max_length=100, description="Full name")
    password: str = Field(..., min_length=8, description="Password")
    
    @validator('email')
    def validate_email(cls, v):
        import re
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Invalid email format')
        return v.lower()


class UserLoginRequest(BaseModel):
    """Request model for user login."""
    
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="Password")


# Linguistics Analysis Request Models

class TextAnalysisRequest(BaseModel):
    """Request model for text analysis."""
    
    text: str = Field(..., min_length=1, max_length=50000, description="Text to analyze")
    analysis_type: str = Field(default="comprehensive", description="Type of analysis")
    include_grammar: bool = Field(default=True, description="Include grammar analysis")
    include_semantics: bool = Field(default=True, description="Include semantic analysis")
    include_syntax: bool = Field(default=True, description="Include syntax analysis")
    session_id: Optional[str] = Field(None, description="Session ID for context")


class EBNFValidationRequest(BaseModel):
    """Request model for EBNF grammar validation."""
    
    grammar: str = Field(..., min_length=1, description="EBNF grammar to validate")
    strict_mode: bool = Field(default=False, description="Enable strict validation")


class GrammarAnalysisRequest(BaseModel):
    """Request model for grammar analysis."""
    
    grammar: str = Field(..., min_length=1, description="Grammar to analyze")
    analysis_depth: str = Field(default="standard", description="Depth of analysis")
    include_patterns: bool = Field(default=True, description="Include pattern analysis")


# Project and Session Management Request Models

class ProjectCreateRequest(BaseModel):
    """Request model for creating a new project."""
    
    name: str = Field(..., min_length=1, max_length=100, description="Project name")
    description: Optional[str] = Field(None, max_length=500, description="Project description")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class SessionCreateRequest(BaseModel):
    """Request model for creating a new session."""
    
    title: str = Field(..., min_length=1, max_length=100, description="Session title")
    project_id: str = Field(..., description="Project ID")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class MessageCreateRequest(BaseModel):
    """Request model for creating a new message."""
    
    content: str = Field(..., min_length=1, description="Message content")
    message_type: str = Field(default="user", description="Type of message")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


# Knowledge Management Request Models

class KnowledgeIngestRequest(BaseModel):
    """Base request model for knowledge ingestion."""
    
    source_type: str = Field(..., description="Type of knowledge source")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class URLIngestRequest(BaseModel):
    """Request model for URL knowledge ingestion."""
    
    url: str = Field(..., description="URL to ingest")
    extract_text: bool = Field(default=True, description="Extract text content")
    extract_links: bool = Field(default=False, description="Extract linked content")
    max_depth: int = Field(default=1, ge=1, le=3, description="Maximum crawl depth")
    follow_external: bool = Field(default=False, description="Follow external links")


class TextIngestRequest(BaseModel):
    """Request model for text knowledge ingestion."""
    
    text: str = Field(..., min_length=1, description="Text content to ingest")
    title: str = Field(..., min_length=1, description="Title for the content")
    content_type: str = Field(default="text", description="Type of content")
    language: Optional[str] = Field(None, description="Content language")
    chunk_size: Optional[int] = Field(None, ge=100, le=10000, description="Chunk size for processing")


class KnowledgeSearchRequest(BaseModel):
    """Request model for knowledge search."""
    
    query: str = Field(..., min_length=1, description="Search query")
    content_type: Optional[str] = Field(None, description="Filter by content type")
    source_type: Optional[str] = Field(None, description="Filter by source type")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum results")
    offset: int = Field(default=0, ge=0, description="Pagination offset")


# User Management Request Models

class UserProfileUpdateRequest(BaseModel):
    """Request model for updating user profile."""
    
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Username")
    full_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Full name")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class PasswordChangeRequest(BaseModel):
    """Request model for changing password."""
    
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")


class UserPreferencesRequest(BaseModel):
    """Request model for updating user preferences."""
    
    theme: Optional[str] = Field(None, description="UI theme preference")
    language: Optional[str] = Field(None, description="Language preference")
    timezone: Optional[str] = Field(None, description="Timezone preference")
    notifications_enabled: Optional[bool] = Field(None, description="Enable notifications")
    email_notifications: Optional[bool] = Field(None, description="Enable email notifications")
    analysis_defaults: Optional[Dict[str, Any]] = Field(None, description="Default analysis settings")
    ui_preferences: Optional[Dict[str, Any]] = Field(None, description="UI preferences")


class UserManagementRequest(BaseModel):
    """Request model for user management (admin)."""
    
    user_id: str = Field(..., description="User ID to manage")
    action: str = Field(..., description="Management action")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Action parameters")

