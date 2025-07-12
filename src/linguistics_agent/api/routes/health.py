"""
Health check routes for the AI Linguistics Agent.

This module provides endpoints for:
- System health monitoring
- Database connectivity checks
- External service status
- Performance metrics
- Readiness and liveness probes

Follows production monitoring best practices and provides comprehensive health information.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_db_session
from ...database import DatabaseManager
from ...models.responses import (
    HealthCheckResponse,
    DetailedHealthResponse,
    DatabaseHealthResponse,
    ExternalServicesHealthResponse,
)

# Initialize router with prefix and tags
router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "/",
    response_model=HealthCheckResponse,
    summary="Basic health check",
    description="Simple health check endpoint for load balancers",
)
async def health_check() -> HealthCheckResponse:
    """
    Basic health check endpoint.
    
    Returns:
        HealthCheckResponse with basic health status
    """
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0",
        uptime=_get_uptime(),
    )


@router.get(
    "/ready",
    response_model=HealthCheckResponse,
    summary="Readiness probe",
    description="Kubernetes readiness probe endpoint",
)
async def readiness_check(
    db_session: AsyncSession = Depends(get_db_session),
) -> HealthCheckResponse:
    """
    Readiness probe for Kubernetes deployments.
    
    Args:
        db_session: Database session dependency
        
    Returns:
        HealthCheckResponse with readiness status
        
    Raises:
        HTTPException: If system is not ready
    """
    try:
        # Check database connectivity
        db_manager = DatabaseManager()
        await db_manager.health_check(db_session)
        
        return HealthCheckResponse(
            status="ready",
            timestamp=datetime.utcnow(),
            version="1.0.0",
            uptime=_get_uptime(),
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"System not ready: {str(e)}"
        )


@router.get(
    "/live",
    response_model=HealthCheckResponse,
    summary="Liveness probe",
    description="Kubernetes liveness probe endpoint",
)
async def liveness_check() -> HealthCheckResponse:
    """
    Liveness probe for Kubernetes deployments.
    
    Returns:
        HealthCheckResponse with liveness status
    """
    return HealthCheckResponse(
        status="alive",
        timestamp=datetime.utcnow(),
        version="1.0.0",
        uptime=_get_uptime(),
    )


@router.get(
    "/detailed",
    response_model=DetailedHealthResponse,
    summary="Detailed health check",
    description="Comprehensive health check with all system components",
)
async def detailed_health_check(
    db_session: AsyncSession = Depends(get_db_session),
) -> DetailedHealthResponse:
    """
    Detailed health check with all system components.
    
    Args:
        db_session: Database session dependency
        
    Returns:
        DetailedHealthResponse with comprehensive health information
    """
    try:
        # Check database health
        database_health = await _check_database_health(db_session)
        
        # Check external services health
        external_services_health = await _check_external_services_health()
        
        # Determine overall status
        overall_status = "healthy"
        if database_health.status != "healthy" or external_services_health.status != "healthy":
            overall_status = "degraded"
        
        return DetailedHealthResponse(
            status=overall_status,
            timestamp=datetime.utcnow(),
            version="1.0.0",
            uptime=_get_uptime(),
            database=database_health,
            external_services=external_services_health,
            system_metrics=_get_system_metrics(),
        )
        
    except Exception as e:
        return DetailedHealthResponse(
            status="unhealthy",
            timestamp=datetime.utcnow(),
            version="1.0.0",
            uptime=_get_uptime(),
            database=DatabaseHealthResponse(
                status="unknown",
                connection_pool_size=0,
                active_connections=0,
                response_time_ms=0,
                last_check=datetime.utcnow(),
            ),
            external_services=ExternalServicesHealthResponse(
                status="unknown",
                anthropic_api={"status": "unknown", "response_time_ms": 0},
                neo4j={"status": "unknown", "response_time_ms": 0},
                chromadb={"status": "unknown", "response_time_ms": 0},
            ),
            system_metrics={
                "error": str(e),
                "cpu_usage": 0,
                "memory_usage": 0,
                "disk_usage": 0,
            },
        )


async def _check_database_health(db_session: AsyncSession) -> DatabaseHealthResponse:
    """
    Check database health and performance metrics.
    
    Args:
        db_session: Database session dependency
        
    Returns:
        DatabaseHealthResponse with database health information
    """
    try:
        start_time = datetime.utcnow()
        
        # Initialize database manager
        db_manager = DatabaseManager()
        
        # Perform health check
        await db_manager.health_check(db_session)
        
        # Calculate response time
        response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        # Get connection pool information
        engine = db_session.get_bind()
        pool = engine.pool
        
        return DatabaseHealthResponse(
            status="healthy",
            connection_pool_size=pool.size(),
            active_connections=pool.checkedout(),
            response_time_ms=response_time,
            last_check=datetime.utcnow(),
        )
        
    except Exception as e:
        return DatabaseHealthResponse(
            status="unhealthy",
            connection_pool_size=0,
            active_connections=0,
            response_time_ms=0,
            last_check=datetime.utcnow(),
            error=str(e),
        )


async def _check_external_services_health() -> ExternalServicesHealthResponse:
    """
    Check external services health.
    
    Returns:
        ExternalServicesHealthResponse with external services health information
    """
    try:
        # Check Anthropic API
        anthropic_health = await _check_anthropic_health()
        
        # Check Neo4j (placeholder for now)
        neo4j_health = {"status": "not_configured", "response_time_ms": 0}
        
        # Check ChromaDB (placeholder for now)
        chromadb_health = {"status": "not_configured", "response_time_ms": 0}
        
        # Determine overall external services status
        overall_status = "healthy"
        if anthropic_health["status"] != "healthy":
            overall_status = "degraded"
        
        return ExternalServicesHealthResponse(
            status=overall_status,
            anthropic_api=anthropic_health,
            neo4j=neo4j_health,
            chromadb=chromadb_health,
        )
        
    except Exception as e:
        return ExternalServicesHealthResponse(
            status="unhealthy",
            anthropic_api={"status": "unknown", "response_time_ms": 0, "error": str(e)},
            neo4j={"status": "unknown", "response_time_ms": 0},
            chromadb={"status": "unknown", "response_time_ms": 0},
        )


async def _check_anthropic_health() -> Dict[str, Any]:
    """
    Check Anthropic API health.
    
    Returns:
        Dictionary with Anthropic API health information
    """
    try:
        import os
        
        # Check if API key is configured
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return {
                "status": "not_configured",
                "response_time_ms": 0,
                "error": "API key not configured"
            }
        
        # For now, just return configured status
        # In a real implementation, you would make a test API call
        return {
            "status": "configured",
            "response_time_ms": 0,
            "note": "API key configured, actual health check not implemented"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "response_time_ms": 0,
            "error": str(e)
        }


def _get_uptime() -> float:
    """
    Get application uptime in seconds.
    
    Returns:
        Uptime in seconds
    """
    # This is a simplified implementation
    # In a real application, you would track the actual start time
    import psutil
    try:
        return psutil.Process().create_time()
    except:
        return 0.0


def _get_system_metrics() -> Dict[str, Any]:
    """
    Get system performance metrics.
    
    Returns:
        Dictionary with system metrics
    """
    try:
        import psutil
        
        # Get CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # Get memory usage
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        
        # Get disk usage
        disk = psutil.disk_usage('/')
        disk_usage = (disk.used / disk.total) * 100
        
        return {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": disk_usage,
            "memory_total_gb": round(memory.total / (1024**3), 2),
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "disk_total_gb": round(disk.total / (1024**3), 2),
            "disk_free_gb": round(disk.free / (1024**3), 2),
        }
        
    except ImportError:
        # psutil not available
        return {
            "cpu_usage": 0,
            "memory_usage": 0,
            "disk_usage": 0,
            "note": "psutil not available for system metrics"
        }
    except Exception as e:
        return {
            "cpu_usage": 0,
            "memory_usage": 0,
            "disk_usage": 0,
            "error": str(e)
        }

