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
