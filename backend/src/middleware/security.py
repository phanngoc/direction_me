"""
Security Headers and CORS Configuration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.sessions import SessionMiddleware
import secrets


def setup_security_headers(app: FastAPI):
    """Setup security headers middleware"""

    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none'"
        )
        response.headers["Content-Security-Policy"] = csp

        return response


def setup_cors(app: FastAPI, allowed_origins: list = None):
    """
    Setup CORS configuration

    Args:
        app: FastAPI application
        allowed_origins: List of allowed origins (defaults to localhost for development)
    """
    if allowed_origins is None:
        allowed_origins = [
            "http://localhost:3000",
            "http://localhost:8000",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:8000"
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"],
        expose_headers=["X-RateLimit-*"],
        max_age=600  # 10 minutes
    )


def setup_trusted_hosts(app: FastAPI, allowed_hosts: list = None):
    """
    Setup trusted host middleware

    Args:
        app: FastAPI application
        allowed_hosts: List of allowed host names
    """
    if allowed_hosts is None:
        allowed_hosts = [
            "localhost",
            "127.0.0.1",
            "*.localhost"
        ]

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=allowed_hosts
    )


def setup_session_middleware(app: FastAPI, secret_key: str = None):
    """
    Setup session middleware

    Args:
        app: FastAPI application
        secret_key: Secret key for session encryption
    """
    if secret_key is None:
        # Generate a random secret key for development
        # In production, this should be from environment variables
        secret_key = secrets.token_urlsafe(32)

    app.add_middleware(
        SessionMiddleware,
        secret_key=secret_key,
        max_age=3600,  # 1 hour
        same_site="lax",
        https_only=True  # Set to True in production with HTTPS
    )


def configure_security(
    app: FastAPI,
    allowed_origins: list = None,
    allowed_hosts: list = None,
    secret_key: str = None
):
    """
    Configure all security features

    Args:
        app: FastAPI application
        allowed_origins: CORS allowed origins
        allowed_hosts: Trusted host names
        secret_key: Session secret key
    """
    # Setup security headers
    setup_security_headers(app)

    # Setup CORS
    setup_cors(app, allowed_origins)

    # Setup trusted hosts
    setup_trusted_hosts(app, allowed_hosts)

    # Setup session middleware
    setup_session_middleware(app, secret_key)
