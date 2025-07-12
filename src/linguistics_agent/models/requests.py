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
