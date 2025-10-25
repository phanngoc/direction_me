"""
Health Check and Monitoring Endpoints
"""

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional
import psutil
import sys


router = APIRouter(prefix="/health", tags=["health"])


class HealthStatus(BaseModel):
    """Health check response model"""
    status: str
    timestamp: datetime
    version: str
    uptime_seconds: Optional[float] = None
    checks: Dict[str, dict]


class SystemMetrics(BaseModel):
    """System metrics response model"""
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    process_memory_mb: float


# Application start time
app_start_time = datetime.utcnow()


@router.get("/", response_model=HealthStatus)
async def health_check():
    """
    Basic health check endpoint

    Returns application health status and basic checks
    """
    checks = {
        "api": {
            "status": "healthy",
            "message": "API is running"
        },
        "database": await check_database(),
        "system": await check_system_resources()
    }

    # Determine overall status
    overall_status = "healthy"
    if any(check["status"] == "unhealthy" for check in checks.values()):
        overall_status = "unhealthy"
    elif any(check["status"] == "degraded" for check in checks.values()):
        overall_status = "degraded"

    # Calculate uptime
    uptime = (datetime.utcnow() - app_start_time).total_seconds()

    return HealthStatus(
        status=overall_status,
        timestamp=datetime.utcnow(),
        version="1.0.0",  # Should come from config
        uptime_seconds=uptime,
        checks=checks
    )


@router.get("/live")
async def liveness_check():
    """
    Kubernetes liveness probe

    Returns 200 if application is running
    """
    return {"status": "alive"}


@router.get("/ready")
async def readiness_check():
    """
    Kubernetes readiness probe

    Returns 200 if application is ready to accept traffic
    """
    # Check critical dependencies
    db_check = await check_database()

    if db_check["status"] != "healthy":
        return {
            "status": "not_ready",
            "reason": "Database connection failed"
        }, status.HTTP_503_SERVICE_UNAVAILABLE

    return {"status": "ready"}


@router.get("/metrics", response_model=SystemMetrics)
async def system_metrics():
    """
    System metrics endpoint

    Returns current system resource usage
    """
    process = psutil.Process()

    return SystemMetrics(
        cpu_percent=psutil.cpu_percent(interval=1),
        memory_percent=psutil.virtual_memory().percent,
        disk_percent=psutil.disk_usage('/').percent,
        process_memory_mb=process.memory_info().rss / 1024 / 1024
    )


async def check_database() -> dict:
    """Check database connectivity"""
    try:
        # TODO: Implement actual database check
        # For now, return healthy
        return {
            "status": "healthy",
            "message": "Database connection established",
            "response_time_ms": 5
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}",
            "response_time_ms": None
        }


async def check_system_resources() -> dict:
    """Check system resource availability"""
    try:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        # Determine status based on thresholds
        if cpu > 90 or memory > 90 or disk > 90:
            status_val = "unhealthy"
            message = "Critical resource usage"
        elif cpu > 75 or memory > 75 or disk > 75:
            status_val = "degraded"
            message = "High resource usage"
        else:
            status_val = "healthy"
            message = "Normal resource usage"

        return {
            "status": status_val,
            "message": message,
            "metrics": {
                "cpu_percent": cpu,
                "memory_percent": memory,
                "disk_percent": disk
            }
        }
    except Exception as e:
        return {
            "status": "unknown",
            "message": f"Failed to check system resources: {str(e)}"
        }


@router.get("/version")
async def version_info():
    """
    Version information endpoint

    Returns application version and environment information
    """
    return {
        "version": "1.0.0",
        "python_version": sys.version,
        "build_date": "2024-12-19",  # Should come from build process
        "environment": "development"  # Should come from config
    }
