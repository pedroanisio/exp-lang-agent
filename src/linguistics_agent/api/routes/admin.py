"""
Admin routes for knowledge management in the AI Linguistics Agent.

This module provides administrative endpoints for:
- Knowledge ingestion (URL, PDF, raw text)
- Knowledge base management and navigation
- System administration and monitoring
- User management (admin functions)

Follows ADR-001 knowledge database architecture and requires admin role access.
"""

from typing import List, Optional
from uuid import UUID
import asyncio
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import get_current_user, require_admin_role
from ..dependencies import get_db_session
from ...database import DatabaseManager
from ...models.database import User, KnowledgeEntry
from ...models.requests import (
    KnowledgeIngestRequest,
    URLIngestRequest,
    TextIngestRequest,
    KnowledgeSearchRequest,
    UserManagementRequest,
)
from ...models.responses import (
    KnowledgeIngestResponse,
    KnowledgeEntryResponse,
    KnowledgeSearchResponse,
    KnowledgeStatsResponse,
    UserManagementResponse,
    SystemStatsResponse,
)

# Initialize router with prefix and tags
router = APIRouter(prefix="/admin", tags=["administration"])


@router.post(
    "/knowledge/ingest/url",
    response_model=KnowledgeIngestResponse,
    summary="Ingest knowledge from URL",
    description="Extract and process knowledge from web URLs",
)
async def ingest_from_url(
    request: URLIngestRequest,
    current_user: User = Depends(require_admin_role),
    db_session: AsyncSession = Depends(get_db_session),
) -> KnowledgeIngestResponse:
    """
    Ingest knowledge from a URL.
    
    Args:
        request: URL ingestion request with URL and processing options
        current_user: Current authenticated admin user
        db_session: Database session dependency
        
    Returns:
        KnowledgeIngestResponse with ingestion results
        
    Raises:
        HTTPException: If ingestion fails or access denied
    """
    try:
        # Import knowledge ingestion service
        from ...services.knowledge_ingestion import KnowledgeIngestionService
        
        # Initialize ingestion service
        ingestion_service = KnowledgeIngestionService()
        
        # Process URL
        ingestion_result = await ingestion_service.ingest_from_url(
            url=request.url,
            extract_text=request.extract_text,
            extract_links=request.extract_links,
            max_depth=request.max_depth,
            follow_external=request.follow_external,
        )
        
        # Store in knowledge base
        db_manager = DatabaseManager()
        knowledge_entries = []
        
        for content_item in ingestion_result.content_items:
            knowledge_data = {
                "title": content_item.title,
                "content": content_item.content,
                "source_type": "url",
                "source_url": content_item.url,
                "content_type": content_item.content_type,
                "metadata": {
                    "extraction_method": content_item.extraction_method,
                    "word_count": content_item.word_count,
                    "language": content_item.language,
                    "ingested_by": current_user.id,
                    "ingested_at": datetime.utcnow().isoformat(),
                },
            }
            
            entry = await db_manager.create_knowledge_entry(db_session, knowledge_data)
            knowledge_entries.append(entry)
        
        return KnowledgeIngestResponse(
            success=True,
            entries_created=len(knowledge_entries),
            processing_time=ingestion_result.processing_time,
            source_type="url",
            source_identifier=request.url,
            metadata={
                "total_content_items": len(ingestion_result.content_items),
                "total_words": sum(item.word_count for item in ingestion_result.content_items),
                "languages_detected": list(set(item.language for item in ingestion_result.content_items)),
            },
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"URL ingestion failed: {str(e)}"
        )


@router.post(
    "/knowledge/ingest/pdf",
    response_model=KnowledgeIngestResponse,
    summary="Ingest knowledge from PDF",
    description="Extract and process knowledge from PDF files",
)
async def ingest_from_pdf(
    file: UploadFile = File(..., description="PDF file to process"),
    extract_text: bool = Form(True, description="Extract text content"),
    extract_metadata: bool = Form(True, description="Extract document metadata"),
    ocr_enabled: bool = Form(False, description="Enable OCR for scanned PDFs"),
    current_user: User = Depends(require_admin_role),
    db_session: AsyncSession = Depends(get_db_session),
) -> KnowledgeIngestResponse:
    """
    Ingest knowledge from a PDF file.
    
    Args:
        file: Uploaded PDF file
        extract_text: Whether to extract text content
        extract_metadata: Whether to extract document metadata
        ocr_enabled: Whether to enable OCR for scanned PDFs
        current_user: Current authenticated admin user
        db_session: Database session dependency
        
    Returns:
        KnowledgeIngestResponse with ingestion results
        
    Raises:
        HTTPException: If ingestion fails or file invalid
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are supported"
            )
        
        # Import knowledge ingestion service
        from ...services.knowledge_ingestion import KnowledgeIngestionService
        
        # Initialize ingestion service
        ingestion_service = KnowledgeIngestionService()
        
        # Read file content
        file_content = await file.read()
        
        # Process PDF
        ingestion_result = await ingestion_service.ingest_from_pdf(
            pdf_content=file_content,
            filename=file.filename,
            extract_text=extract_text,
            extract_metadata=extract_metadata,
            ocr_enabled=ocr_enabled,
        )
        
        # Store in knowledge base
        db_manager = DatabaseManager()
        knowledge_entries = []
        
        for content_item in ingestion_result.content_items:
            knowledge_data = {
                "title": content_item.title or file.filename,
                "content": content_item.content,
                "source_type": "pdf",
                "source_url": None,
                "content_type": content_item.content_type,
                "metadata": {
                    "filename": file.filename,
                    "file_size": len(file_content),
                    "extraction_method": content_item.extraction_method,
                    "word_count": content_item.word_count,
                    "language": content_item.language,
                    "page_count": content_item.metadata.get("page_count"),
                    "ingested_by": current_user.id,
                    "ingested_at": datetime.utcnow().isoformat(),
                },
            }
            
            entry = await db_manager.create_knowledge_entry(db_session, knowledge_data)
            knowledge_entries.append(entry)
        
        return KnowledgeIngestResponse(
            success=True,
            entries_created=len(knowledge_entries),
            processing_time=ingestion_result.processing_time,
            source_type="pdf",
            source_identifier=file.filename,
            metadata={
                "file_size": len(file_content),
                "total_content_items": len(ingestion_result.content_items),
                "total_words": sum(item.word_count for item in ingestion_result.content_items),
                "languages_detected": list(set(item.language for item in ingestion_result.content_items)),
            },
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PDF ingestion failed: {str(e)}"
        )


@router.post(
    "/knowledge/ingest/text",
    response_model=KnowledgeIngestResponse,
    summary="Ingest knowledge from raw text",
    description="Process and store raw text content in knowledge base",
)
async def ingest_from_text(
    request: TextIngestRequest,
    current_user: User = Depends(require_admin_role),
    db_session: AsyncSession = Depends(get_db_session),
) -> KnowledgeIngestResponse:
    """
    Ingest knowledge from raw text.
    
    Args:
        request: Text ingestion request with content and metadata
        current_user: Current authenticated admin user
        db_session: Database session dependency
        
    Returns:
        KnowledgeIngestResponse with ingestion results
        
    Raises:
        HTTPException: If ingestion fails
    """
    try:
        # Import knowledge ingestion service
        from ...services.knowledge_ingestion import KnowledgeIngestionService
        
        # Initialize ingestion service
        ingestion_service = KnowledgeIngestionService()
        
        # Process text
        ingestion_result = await ingestion_service.ingest_from_text(
            text=request.text,
            title=request.title,
            content_type=request.content_type,
            language=request.language,
            chunk_size=request.chunk_size,
        )
        
        # Store in knowledge base
        db_manager = DatabaseManager()
        knowledge_entries = []
        
        for content_item in ingestion_result.content_items:
            knowledge_data = {
                "title": content_item.title,
                "content": content_item.content,
                "source_type": "text",
                "source_url": None,
                "content_type": content_item.content_type,
                "metadata": {
                    "extraction_method": content_item.extraction_method,
                    "word_count": content_item.word_count,
                    "language": content_item.language,
                    "chunk_index": content_item.metadata.get("chunk_index"),
                    "ingested_by": current_user.id,
                    "ingested_at": datetime.utcnow().isoformat(),
                },
            }
            
            entry = await db_manager.create_knowledge_entry(db_session, knowledge_data)
            knowledge_entries.append(entry)
        
        return KnowledgeIngestResponse(
            success=True,
            entries_created=len(knowledge_entries),
            processing_time=ingestion_result.processing_time,
            source_type="text",
            source_identifier=request.title,
            metadata={
                "total_content_items": len(ingestion_result.content_items),
                "total_words": sum(item.word_count for item in ingestion_result.content_items),
                "language": request.language,
            },
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Text ingestion failed: {str(e)}"
        )


@router.get(
    "/knowledge/search",
    response_model=KnowledgeSearchResponse,
    summary="Search knowledge base",
    description="Search and navigate through stored knowledge entries",
)
async def search_knowledge(
    query: str,
    content_type: Optional[str] = None,
    source_type: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(require_admin_role),
    db_session: AsyncSession = Depends(get_db_session),
) -> KnowledgeSearchResponse:
    """
    Search knowledge base entries.
    
    Args:
        query: Search query string
        content_type: Filter by content type
        source_type: Filter by source type
        limit: Maximum number of results
        offset: Pagination offset
        current_user: Current authenticated admin user
        db_session: Database session dependency
        
    Returns:
        KnowledgeSearchResponse with search results
        
    Raises:
        HTTPException: If search fails
    """
    try:
        # Import knowledge search service
        from ...services.knowledge_search import KnowledgeSearchService
        
        # Initialize search service
        search_service = KnowledgeSearchService()
        
        # Perform search
        search_result = await search_service.search_knowledge(
            query=query,
            content_type=content_type,
            source_type=source_type,
            limit=limit,
            offset=offset,
        )
        
        # Convert to response format
        knowledge_entries = [
            KnowledgeEntryResponse(
                id=entry.id,
                title=entry.title,
                content=entry.content[:500] + "..." if len(entry.content) > 500 else entry.content,
                source_type=entry.source_type,
                source_url=entry.source_url,
                content_type=entry.content_type,
                created_at=entry.created_at,
                metadata=entry.metadata,
                relevance_score=entry.relevance_score,
            )
            for entry in search_result.entries
        ]
        
        return KnowledgeSearchResponse(
            entries=knowledge_entries,
            total_count=search_result.total_count,
            query=query,
            processing_time=search_result.processing_time,
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Knowledge search failed: {str(e)}"
        )


@router.get(
    "/knowledge/stats",
    response_model=KnowledgeStatsResponse,
    summary="Get knowledge base statistics",
    description="Get comprehensive statistics about the knowledge base",
)
async def get_knowledge_stats(
    current_user: User = Depends(require_admin_role),
    db_session: AsyncSession = Depends(get_db_session),
) -> KnowledgeStatsResponse:
    """
    Get knowledge base statistics.
    
    Args:
        current_user: Current authenticated admin user
        db_session: Database session dependency
        
    Returns:
        KnowledgeStatsResponse with statistics
        
    Raises:
        HTTPException: If stats retrieval fails
    """
    try:
        db_manager = DatabaseManager()
        
        # Get knowledge statistics
        stats = await db_manager.get_knowledge_stats(db_session)
        
        return KnowledgeStatsResponse(
            total_entries=stats["total_entries"],
            entries_by_type=stats["entries_by_type"],
            entries_by_source=stats["entries_by_source"],
            total_words=stats["total_words"],
            languages=stats["languages"],
            recent_ingestions=stats["recent_ingestions"],
            storage_size=stats["storage_size"],
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get knowledge stats: {str(e)}"
        )


@router.get(
    "/users",
    response_model=List[UserManagementResponse],
    summary="List all users",
    description="Get list of all users for administration",
)
async def list_users(
    current_user: User = Depends(require_admin_role),
    db_session: AsyncSession = Depends(get_db_session),
) -> List[UserManagementResponse]:
    """
    List all users for administration.
    
    Args:
        current_user: Current authenticated admin user
        db_session: Database session dependency
        
    Returns:
        List of UserManagementResponse with user details
        
    Raises:
        HTTPException: If user listing fails
    """
    try:
        db_manager = DatabaseManager()
        users = await db_manager.get_all_users(db_session)
        
        return [
            UserManagementResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                role=user.role,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
                last_login=user.metadata.get("last_login") if user.metadata else None,
                project_count=len(user.projects) if user.projects else 0,
            )
            for user in users
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list users: {str(e)}"
        )


@router.get(
    "/system/stats",
    response_model=SystemStatsResponse,
    summary="Get system statistics",
    description="Get comprehensive system statistics and health metrics",
)
async def get_system_stats(
    current_user: User = Depends(require_admin_role),
    db_session: AsyncSession = Depends(get_db_session),
) -> SystemStatsResponse:
    """
    Get system statistics and health metrics.
    
    Args:
        current_user: Current authenticated admin user
        db_session: Database session dependency
        
    Returns:
        SystemStatsResponse with system metrics
        
    Raises:
        HTTPException: If stats retrieval fails
    """
    try:
        db_manager = DatabaseManager()
        
        # Get system statistics
        system_stats = await db_manager.get_system_stats(db_session)
        
        return SystemStatsResponse(
            total_users=system_stats["total_users"],
            active_users=system_stats["active_users"],
            total_projects=system_stats["total_projects"],
            total_sessions=system_stats["total_sessions"],
            total_messages=system_stats["total_messages"],
            knowledge_entries=system_stats["knowledge_entries"],
            api_calls_today=system_stats["api_calls_today"],
            storage_usage=system_stats["storage_usage"],
            uptime=system_stats["uptime"],
            health_status=system_stats["health_status"],
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get system stats: {str(e)}"
        )

