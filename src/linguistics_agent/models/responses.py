"""
File: responses.py
Path: src/linguistics_agent/models/responses.py
Purpose: Response models for linguistics agent outputs
Author: AI Development Team
Created: 2024-12-07
Modified: 2024-12-07
Description: Pydantic models for responses from the linguistics agent
Rule Compliance: rules-101 v1.2, rules-102 v1.2, rules-103 v1.2
"""

from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator


class ResponseStatus(str, Enum):
    """Status of the agent response."""

    SUCCESS = "success"
    PARTIAL = "partial"
    ERROR = "error"
    TIMEOUT = "timeout"


class ToolUsage(BaseModel):
    """Information about tools used during processing."""

    tool_name: str = Field(..., description="Name of the tool used")
    execution_time: float = Field(..., description="Tool execution time in seconds")
    success: bool = Field(..., description="Whether tool execution was successful")
    output_summary: Optional[str] = Field(
        default=None, description="Summary of tool output"
    )


class KnowledgeSource(BaseModel):
    """Information about knowledge sources used in the response."""

    source_id: str = Field(..., description="Unique identifier for the source")
    title: str = Field(..., description="Title of the knowledge source")
    source_type: str = Field(..., description="Type of source (article, paper, etc.)")
    relevance_score: float = Field(
        ..., description="Relevance score (0.0 to 1.0)", ge=0.0, le=1.0
    )
    url: Optional[str] = Field(default=None, description="URL to the source")
    excerpt: Optional[str] = Field(
        default=None, description="Relevant excerpt from the source"
    )


class LinguisticsResponse(BaseModel):
    """
    Model for responses from the linguistics agent.

    This model represents the comprehensive response from the LinguisticsAgent,
    including the main content, confidence scores, sources, and metadata.
    """

    content: str = Field(
        ..., description="Main response content from the agent", min_length=1
    )

    status: ResponseStatus = Field(
        default=ResponseStatus.SUCCESS, description="Status of the response"
    )

    confidence: float = Field(
        ...,
        description="Confidence score for the response (0.0 to 1.0)",
        ge=0.0,
        le=1.0,
    )

    sources: List[KnowledgeSource] = Field(
        default_factory=list,
        description="Knowledge sources used in generating the response",
    )

    tools_used: List[ToolUsage] = Field(
        default_factory=list, description="Tools used during response generation"
    )

    context_preserved: bool = Field(
        default=True, description="Whether conversation context was preserved"
    )

    session_id: Optional[str] = Field(
        default=None, description="Session identifier for conversation continuity"
    )

    response_time: float = Field(
        default=0.0, description="Response generation time in seconds", ge=0.0
    )

    token_usage: Dict[str, int] = Field(
        default_factory=dict, description="Token usage statistics"
    )

    error: Optional[str] = Field(
        default=None, description="Error message if status is ERROR"
    )

    suggestions: List[str] = Field(
        default_factory=list, description="Follow-up suggestions for the user"
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional response metadata"
    )

    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Response generation timestamp"
    )

    @validator("confidence")
    def validate_confidence_with_status(cls, v: float, values: Dict[str, Any]) -> float:
        """Validate confidence score based on response status."""
        status = values.get("status")
        if status == ResponseStatus.ERROR and v > 0.1:
            raise ValueError("Error responses should have low confidence scores")
        return v

    @validator("error")
    def validate_error_with_status(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Optional[str]:
        """Validate error message consistency with status."""
        status = values.get("status")
        if status == ResponseStatus.ERROR and not v:
            raise ValueError("Error status requires an error message")
        if status != ResponseStatus.ERROR and v:
            raise ValueError("Non-error status should not have error message")
        return v

    class Config:
        """Pydantic configuration."""

        use_enum_values = True
        validate_assignment = True
        extra = "forbid"
        json_encoders = {datetime: lambda v: v.isoformat()}
        schema_extra = {
            "example": {
                "content": "The EBNF grammar appears to be well-formed with proper syntax...",
                "status": "success",
                "confidence": 0.95,
                "sources": [
                    {
                        "source_id": "src_001",
                        "title": "EBNF Specification Guide",
                        "source_type": "technical_document",
                        "relevance_score": 0.9,
                        "excerpt": "EBNF syntax rules...",
                    }
                ],
                "tools_used": [
                    {
                        "tool_name": "ebnf_validator",
                        "execution_time": 0.15,
                        "success": True,
                        "output_summary": "Grammar validation completed",
                    }
                ],
                "context_preserved": True,
                "response_time": 1.23,
            }
        }


class EBNFValidationResponse(LinguisticsResponse):
    """Specialized response for EBNF validation results."""

    validation_results: Dict[str, Any] = Field(
        default_factory=dict, description="Detailed validation results"
    )

    syntax_errors: List[str] = Field(
        default_factory=list, description="List of syntax errors found"
    )

    warnings: List[str] = Field(
        default_factory=list, description="List of warnings or suggestions"
    )

    is_valid: bool = Field(..., description="Whether the EBNF grammar is valid")


class GrammarAnalysisResponse(LinguisticsResponse):
    """Specialized response for grammar analysis results."""

    analysis_results: Dict[str, Any] = Field(
        default_factory=dict, description="Detailed analysis results"
    )

    complexity_score: float = Field(
        default=0.0, description="Grammar complexity score (0.0 to 1.0)", ge=0.0, le=1.0
    )

    optimization_suggestions: List[str] = Field(
        default_factory=list, description="Suggestions for grammar optimization"
    )

    structure_analysis: Dict[str, Any] = Field(
        default_factory=dict, description="Analysis of grammar structure"
    )


class KnowledgeIngestionResponse(BaseModel):
    """Response model for knowledge ingestion operations."""

    ingestion_id: str = Field(..., description="Unique identifier for the ingestion")
    status: ResponseStatus = Field(..., description="Ingestion status")

    processed_items: int = Field(
        default=0, description="Number of items successfully processed"
    )

    failed_items: int = Field(
        default=0, description="Number of items that failed processing"
    )

    processing_time: float = Field(
        default=0.0, description="Total processing time in seconds"
    )

    knowledge_graph_updates: Dict[str, int] = Field(
        default_factory=dict, description="Statistics about knowledge graph updates"
    )

    vector_embeddings_created: int = Field(
        default=0, description="Number of vector embeddings created"
    )

    errors: List[str] = Field(
        default_factory=list, description="List of errors encountered during processing"
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional processing metadata"
    )

    class Config:
        """Pydantic configuration."""

        use_enum_values = True
        validate_assignment = True
        extra = "forbid"


class SessionInfo(BaseModel):
    """Information about a conversation session."""

    session_id: str = Field(..., description="Unique session identifier")
    created_at: datetime = Field(..., description="Session creation timestamp")
    last_activity: datetime = Field(..., description="Last activity timestamp")

    message_count: int = Field(
        default=0, description="Number of messages in the session"
    )

    context_size: int = Field(
        default=0, description="Size of preserved context in tokens"
    )

    tags: List[str] = Field(
        default_factory=list, description="Tags associated with the session"
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional session metadata"
    )

    class Config:
        """Pydantic configuration."""

        validate_assignment = True
        json_encoders = {datetime: lambda v: v.isoformat()}


# Authentication Response Models

class UserRegistrationResponse(BaseModel):
    """Response model for user registration."""
    
    id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    username: str = Field(..., description="Username")
    full_name: str = Field(..., description="Full name")
    role: str = Field(..., description="User role")
    is_active: bool = Field(..., description="Account active status")
    created_at: datetime = Field(..., description="Account creation timestamp")
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Token type")


class UserLoginResponse(BaseModel):
    """Response model for user login."""
    
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Token type")
    user_id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    username: str = Field(..., description="Username")
    full_name: str = Field(..., description="Full name")
    role: str = Field(..., description="User role")


class UserProfileResponse(BaseModel):
    """Response model for user profile."""
    
    id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    username: str = Field(..., description="Username")
    full_name: str = Field(..., description="Full name")
    role: str = Field(..., description="User role")
    is_active: bool = Field(..., description="Account active status")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class TokenRefreshResponse(BaseModel):
    """Response model for token refresh."""
    
    access_token: str = Field(..., description="New JWT access token")
    token_type: str = Field(..., description="Token type")


# Linguistics Analysis Response Models

class TextAnalysisResponse(BaseModel):
    """Response model for text analysis."""
    
    analysis: str = Field(..., description="Analysis results")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    processing_time: float = Field(..., description="Processing time in seconds")
    analysis_type: str = Field(..., description="Type of analysis performed")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class EBNFValidationResponse(BaseModel):
    """Response model for EBNF validation."""
    
    is_valid: bool = Field(..., description="Whether grammar is valid")
    errors: List[str] = Field(default_factory=list, description="Validation errors")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    processed_grammar: Optional[str] = Field(None, description="Processed grammar")


class GrammarAnalysisResponse(BaseModel):
    """Response model for grammar analysis."""
    
    structure: Dict[str, Any] = Field(..., description="Grammar structure analysis")
    patterns: List[Dict[str, Any]] = Field(..., description="Identified patterns")
    complexity_score: float = Field(..., ge=0.0, description="Complexity score")
    recommendations: List[str] = Field(..., description="Optimization recommendations")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


# Project and Session Management Response Models

class ProjectResponse(BaseModel):
    """Response model for project information."""
    
    id: str = Field(..., description="Project ID")
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    user_id: str = Field(..., description="Owner user ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ProjectListResponse(BaseModel):
    """Response model for project list."""
    
    projects: List[ProjectResponse] = Field(..., description="List of projects")


class SessionResponse(BaseModel):
    """Response model for session information."""
    
    id: str = Field(..., description="Session ID")
    title: str = Field(..., description="Session title")
    project_id: str = Field(..., description="Project ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class SessionListResponse(BaseModel):
    """Response model for session list."""
    
    sessions: List[SessionResponse] = Field(..., description="List of sessions")


class MessageResponse(BaseModel):
    """Response model for message information."""
    
    id: str = Field(..., description="Message ID")
    session_id: str = Field(..., description="Session ID")
    content: str = Field(..., description="Message content")
    message_type: str = Field(..., description="Message type")
    created_at: datetime = Field(..., description="Creation timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class MessageListResponse(BaseModel):
    """Response model for message list."""
    
    messages: List[MessageResponse] = Field(..., description="List of messages")


# Knowledge Management Response Models

class KnowledgeIngestResponse(BaseModel):
    """Response model for knowledge ingestion."""
    
    success: bool = Field(..., description="Whether ingestion was successful")
    entries_created: int = Field(..., description="Number of knowledge entries created")
    processing_time: float = Field(..., description="Processing time in seconds")
    source_type: str = Field(..., description="Type of source ingested")
    source_identifier: str = Field(..., description="Source identifier")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class KnowledgeEntryResponse(BaseModel):
    """Response model for knowledge entry."""
    
    id: str = Field(..., description="Knowledge entry ID")
    title: str = Field(..., description="Entry title")
    content: str = Field(..., description="Entry content")
    source_type: str = Field(..., description="Source type")
    source_url: Optional[str] = Field(None, description="Source URL")
    content_type: str = Field(..., description="Content type")
    created_at: datetime = Field(..., description="Creation timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    relevance_score: Optional[float] = Field(None, description="Relevance score for search")


class KnowledgeSearchResponse(BaseModel):
    """Response model for knowledge search."""
    
    entries: List[KnowledgeEntryResponse] = Field(..., description="Search results")
    total_count: int = Field(..., description="Total number of matching entries")
    query: str = Field(..., description="Search query")
    processing_time: float = Field(..., description="Search processing time")


class KnowledgeStatsResponse(BaseModel):
    """Response model for knowledge base statistics."""
    
    total_entries: int = Field(..., description="Total knowledge entries")
    entries_by_type: Dict[str, int] = Field(..., description="Entries by content type")
    entries_by_source: Dict[str, int] = Field(..., description="Entries by source type")
    total_words: int = Field(..., description="Total word count")
    languages: List[str] = Field(..., description="Languages in knowledge base")
    recent_ingestions: int = Field(..., description="Recent ingestions count")
    storage_size: int = Field(..., description="Storage size in bytes")


# User Management Response Models

class UserStatsResponse(BaseModel):
    """Response model for user statistics."""
    
    user_id: str = Field(..., description="User ID")
    total_projects: int = Field(..., description="Total projects")
    total_sessions: int = Field(..., description="Total sessions")
    total_messages: int = Field(..., description="Total messages")
    total_analyses: int = Field(..., description="Total analyses performed")
    account_age_days: int = Field(..., description="Account age in days")
    last_activity: Optional[datetime] = Field(None, description="Last activity timestamp")
    most_used_features: List[str] = Field(..., description="Most used features")
    analysis_types_used: Dict[str, int] = Field(..., description="Analysis types usage")


class UserPreferencesResponse(BaseModel):
    """Response model for user preferences."""
    
    user_id: str = Field(..., description="User ID")
    theme: str = Field(..., description="UI theme preference")
    language: str = Field(..., description="Language preference")
    timezone: str = Field(..., description="Timezone preference")
    notifications_enabled: bool = Field(..., description="Notifications enabled")
    email_notifications: bool = Field(..., description="Email notifications enabled")
    analysis_defaults: Dict[str, Any] = Field(..., description="Default analysis settings")
    ui_preferences: Dict[str, Any] = Field(..., description="UI preferences")


class UserManagementResponse(BaseModel):
    """Response model for user management."""
    
    id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    username: str = Field(..., description="Username")
    full_name: str = Field(..., description="Full name")
    role: str = Field(..., description="User role")
    is_active: bool = Field(..., description="Account active status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    project_count: int = Field(..., description="Number of projects")


class SystemStatsResponse(BaseModel):
    """Response model for system statistics."""
    
    total_users: int = Field(..., description="Total users")
    active_users: int = Field(..., description="Active users")
    total_projects: int = Field(..., description="Total projects")
    total_sessions: int = Field(..., description="Total sessions")
    total_messages: int = Field(..., description="Total messages")
    knowledge_entries: int = Field(..., description="Knowledge entries")
    api_calls_today: int = Field(..., description="API calls today")
    storage_usage: int = Field(..., description="Storage usage in bytes")
    uptime: float = Field(..., description="System uptime in seconds")
    health_status: str = Field(..., description="Overall health status")


# Health Check Response Models

class HealthCheckResponse(BaseModel):
    """Response model for basic health check."""
    
    status: str = Field(..., description="Health status")
    timestamp: datetime = Field(..., description="Check timestamp")
    version: str = Field(..., description="Application version")
    uptime: float = Field(..., description="Uptime in seconds")


class DatabaseHealthResponse(BaseModel):
    """Response model for database health check."""
    
    status: str = Field(..., description="Database status")
    connection_pool_size: int = Field(..., description="Connection pool size")
    active_connections: int = Field(..., description="Active connections")
    response_time_ms: float = Field(..., description="Response time in milliseconds")
    last_check: datetime = Field(..., description="Last check timestamp")
    error: Optional[str] = Field(None, description="Error message if any")


class ExternalServicesHealthResponse(BaseModel):
    """Response model for external services health check."""
    
    status: str = Field(..., description="Overall external services status")
    anthropic_api: Dict[str, Any] = Field(..., description="Anthropic API status")
    neo4j: Dict[str, Any] = Field(..., description="Neo4j status")
    chromadb: Dict[str, Any] = Field(..., description="ChromaDB status")


class DetailedHealthResponse(BaseModel):
    """Response model for detailed health check."""
    
    status: str = Field(..., description="Overall health status")
    timestamp: datetime = Field(..., description="Check timestamp")
    version: str = Field(..., description="Application version")
    uptime: float = Field(..., description="Uptime in seconds")
    database: DatabaseHealthResponse = Field(..., description="Database health")
    external_services: ExternalServicesHealthResponse = Field(..., description="External services health")
    system_metrics: Dict[str, Any] = Field(..., description="System metrics")

