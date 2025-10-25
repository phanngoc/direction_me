"""
FastAPI main application for MyWay Career Assessment System.
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import structlog

from .database import init_db, close_db, check_db_health
from .api import auth, assessment, results, progress, ikigai, careers
from .middleware.auth import AuthMiddleware
from .middleware.error_handler import ErrorHandlerMiddleware
from .utils.logger import setup_logging

# Setup logging
setup_logging()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting MyWay Career Assessment API")
    await init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down MyWay Career Assessment API")
    await close_db()
    logger.info("Database connections closed")


# Create FastAPI app
app = FastAPI(
    title="MyWay Career Assessment API",
    description="API for career assessment system with IQ, EQ, DQ, AQ evaluation and Ikigai analysis",
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.myway.com"]
)

app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(assessment.router, prefix="/api/v1/assessments", tags=["Assessment"])
app.include_router(results.router, prefix="/api/v1/results", tags=["Results"])
app.include_router(progress.router, prefix="/api/v1/progress", tags=["Progress"])
app.include_router(ikigai.router, tags=["Ikigai"])
app.include_router(careers.router, tags=["Careers"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "MyWay Career Assessment API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    db_healthy = await check_db_health()
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "database": "connected" if db_healthy else "disconnected",
        "version": "1.0.0"
    }


@app.get("/api/v1/")
async def api_info():
    """API information endpoint."""
    return {
        "name": "MyWay Career Assessment API",
        "version": "1.0.0",
        "description": "API for career assessment system with IQ, EQ, DQ, AQ evaluation and Ikigai analysis",
        "docs": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )