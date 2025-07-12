"""
Linguistics analysis routes for the AI Linguistics Agent.

This module provides endpoints for:
- Text analysis and linguistic processing
- EBNF grammar validation
- Grammar structure analysis
- Session-based conversation management
- Project organization

Follows ADR-001 knowledge database architecture and ADR-002 Anthropic API integration.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import get_current_user
from ..dependencies import get_db_session
from ...agent import LinguisticsAgent
from ...database import DatabaseManager
from ...models.database import User, Project, Session, Message
from ...models.requests import (
    TextAnalysisRequest,
    EBNFValidationRequest,
    GrammarAnalysisRequest,
    ProjectCreateRequest,
    SessionCreateRequest,
    MessageCreateRequest,
)
from ...models.responses import (
    TextAnalysisResponse,
    EBNFValidationResponse,
    GrammarAnalysisResponse,
    ProjectResponse,
    SessionResponse,
    MessageResponse,
    ProjectListResponse,
    SessionListResponse,
    MessageListResponse,
)

# Initialize router with prefix and tags
router = APIRouter(prefix="/linguistics", tags=["linguistics"])


@router.post(
    "/analyze",
    response_model=TextAnalysisResponse,
    summary="Analyze text linguistically",
    description="Perform comprehensive linguistic analysis on provided text",
)
async def analyze_text(
    request: TextAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> TextAnalysisResponse:
    """
    Perform linguistic analysis on text using AI agent.
    
    Args:
        request: Text analysis request with text and options
        current_user: Current authenticated user
        db_session: Database session dependency
        
    Returns:
        TextAnalysisResponse with analysis results
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Initialize AI agent
        agent = LinguisticsAgent()
        
        # Perform analysis
        analysis_result = await agent.analyze_text(
            text=request.text,
            analysis_type=request.analysis_type,
            include_grammar=request.include_grammar,
            include_semantics=request.include_semantics,
            include_syntax=request.include_syntax,
        )
        
        # Store analysis in session if session_id provided
        if request.session_id:
            db_manager = DatabaseManager()
            
            # Verify session belongs to user
            session = await db_manager.get_session_by_id(db_session, request.session_id)
            if not session or session.project.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Session not found or access denied"
                )
            
            # Create message records
            user_message = await db_manager.create_message(db_session, {
                "session_id": request.session_id,
                "content": request.text,
                "message_type": "user",
                "metadata": {"analysis_type": request.analysis_type}
            })
            
            assistant_message = await db_manager.create_message(db_session, {
                "session_id": request.session_id,
                "content": analysis_result.analysis,
                "message_type": "assistant",
                "metadata": {
                    "confidence": analysis_result.confidence,
                    "processing_time": analysis_result.processing_time,
                    "analysis_type": request.analysis_type,
                }
            })
        
        return TextAnalysisResponse(
            analysis=analysis_result.analysis,
            confidence=analysis_result.confidence,
            processing_time=analysis_result.processing_time,
            analysis_type=request.analysis_type,
            metadata=analysis_result.metadata,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Text analysis failed: {str(e)}"
        )


@router.post(
    "/validate-ebnf",
    response_model=EBNFValidationResponse,
    summary="Validate EBNF grammar",
    description="Validate Extended Backus-Naur Form grammar syntax",
)
async def validate_ebnf(
    request: EBNFValidationRequest,
    current_user: User = Depends(get_current_user),
) -> EBNFValidationResponse:
    """
    Validate EBNF grammar syntax.
    
    Args:
        request: EBNF validation request with grammar text
        current_user: Current authenticated user
        
    Returns:
        EBNFValidationResponse with validation results
        
    Raises:
        HTTPException: If validation fails
    """
    try:
        # Initialize AI agent
        agent = LinguisticsAgent()
        
        # Validate EBNF grammar
        validation_result = await agent.validate_ebnf(
            grammar=request.grammar,
            strict_mode=request.strict_mode,
        )
        
        return EBNFValidationResponse(
            is_valid=validation_result.is_valid,
            errors=validation_result.errors,
            warnings=validation_result.warnings,
            suggestions=validation_result.suggestions,
            processed_grammar=validation_result.processed_grammar,
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"EBNF validation failed: {str(e)}"
        )


@router.post(
    "/analyze-grammar",
    response_model=GrammarAnalysisResponse,
    summary="Analyze grammar structure",
    description="Perform detailed analysis of grammar structure and patterns",
)
async def analyze_grammar(
    request: GrammarAnalysisRequest,
    current_user: User = Depends(get_current_user),
) -> GrammarAnalysisResponse:
    """
    Analyze grammar structure and patterns.
    
    Args:
        request: Grammar analysis request
        current_user: Current authenticated user
        
    Returns:
        GrammarAnalysisResponse with analysis results
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Initialize AI agent
        agent = LinguisticsAgent()
        
        # Analyze grammar
        analysis_result = await agent.analyze_grammar(
            grammar=request.grammar,
            analysis_depth=request.analysis_depth,
            include_patterns=request.include_patterns,
        )
        
        return GrammarAnalysisResponse(
            structure=analysis_result.structure,
            patterns=analysis_result.patterns,
            complexity_score=analysis_result.complexity_score,
            recommendations=analysis_result.recommendations,
            metadata=analysis_result.metadata,
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Grammar analysis failed: {str(e)}"
        )


# Project Management Endpoints

@router.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new project",
    description="Create a new linguistics project for organizing sessions",
)
async def create_project(
    request: ProjectCreateRequest,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> ProjectResponse:
    """
    Create a new linguistics project.
    
    Args:
        request: Project creation request
        current_user: Current authenticated user
        db_session: Database session dependency
        
    Returns:
        ProjectResponse with created project details
        
    Raises:
        HTTPException: If creation fails
    """
    try:
        db_manager = DatabaseManager()
        
        project_data = {
            "name": request.name,
            "description": request.description,
            "user_id": current_user.id,
            "metadata": request.metadata or {},
        }
        
        project = await db_manager.create_project(db_session, project_data)
        
        return ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            user_id=project.user_id,
            created_at=project.created_at,
            updated_at=project.updated_at,
            metadata=project.metadata,
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Project creation failed: {str(e)}"
        )


@router.get(
    "/projects",
    response_model=ProjectListResponse,
    summary="List user projects",
    description="Get list of projects for current user",
)
async def list_projects(
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> ProjectListResponse:
    """
    List projects for current user.
    
    Args:
        current_user: Current authenticated user
        db_session: Database session dependency
        
    Returns:
        ProjectListResponse with list of projects
    """
    try:
        db_manager = DatabaseManager()
        projects = await db_manager.get_projects_by_user(db_session, current_user.id)
        
        project_list = [
            ProjectResponse(
                id=project.id,
                name=project.name,
                description=project.description,
                user_id=project.user_id,
                created_at=project.created_at,
                updated_at=project.updated_at,
                metadata=project.metadata,
            )
            for project in projects
        ]
        
        return ProjectListResponse(projects=project_list)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list projects: {str(e)}"
        )


# Session Management Endpoints

@router.post(
    "/sessions",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new session",
    description="Create a new chat session within a project",
)
async def create_session(
    request: SessionCreateRequest,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> SessionResponse:
    """
    Create a new chat session.
    
    Args:
        request: Session creation request
        current_user: Current authenticated user
        db_session: Database session dependency
        
    Returns:
        SessionResponse with created session details
        
    Raises:
        HTTPException: If creation fails or project access denied
    """
    try:
        db_manager = DatabaseManager()
        
        # Verify project belongs to user
        project = await db_manager.get_project_by_id(db_session, request.project_id)
        if not project or project.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Project not found or access denied"
            )
        
        session_data = {
            "title": request.title,
            "project_id": request.project_id,
            "metadata": request.metadata or {},
        }
        
        session = await db_manager.create_session(db_session, session_data)
        
        return SessionResponse(
            id=session.id,
            title=session.title,
            project_id=session.project_id,
            created_at=session.created_at,
            updated_at=session.updated_at,
            metadata=session.metadata,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Session creation failed: {str(e)}"
        )


@router.get(
    "/projects/{project_id}/sessions",
    response_model=SessionListResponse,
    summary="List project sessions",
    description="Get list of sessions for a specific project",
)
async def list_sessions(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> SessionListResponse:
    """
    List sessions for a specific project.
    
    Args:
        project_id: Project UUID
        current_user: Current authenticated user
        db_session: Database session dependency
        
    Returns:
        SessionListResponse with list of sessions
        
    Raises:
        HTTPException: If project not found or access denied
    """
    try:
        db_manager = DatabaseManager()
        
        # Verify project belongs to user
        project = await db_manager.get_project_by_id(db_session, project_id)
        if not project or project.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Project not found or access denied"
            )
        
        sessions = await db_manager.get_sessions_by_project(db_session, project_id)
        
        session_list = [
            SessionResponse(
                id=session.id,
                title=session.title,
                project_id=session.project_id,
                created_at=session.created_at,
                updated_at=session.updated_at,
                metadata=session.metadata,
            )
            for session in sessions
        ]
        
        return SessionListResponse(sessions=session_list)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list sessions: {str(e)}"
        )


# Message Management Endpoints

@router.get(
    "/sessions/{session_id}/messages",
    response_model=MessageListResponse,
    summary="List session messages",
    description="Get list of messages for a specific session",
)
async def list_messages(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db_session),
) -> MessageListResponse:
    """
    List messages for a specific session.
    
    Args:
        session_id: Session UUID
        current_user: Current authenticated user
        db_session: Database session dependency
        
    Returns:
        MessageListResponse with list of messages
        
    Raises:
        HTTPException: If session not found or access denied
    """
    try:
        db_manager = DatabaseManager()
        
        # Verify session belongs to user
        session = await db_manager.get_session_by_id(db_session, session_id)
        if not session or session.project.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Session not found or access denied"
            )
        
        messages = await db_manager.get_messages_by_session(db_session, session_id)
        
        message_list = [
            MessageResponse(
                id=message.id,
                session_id=message.session_id,
                content=message.content,
                message_type=message.message_type,
                created_at=message.created_at,
                metadata=message.metadata,
            )
            for message in messages
        ]
        
        return MessageListResponse(messages=message_list)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list messages: {str(e)}"
        )

