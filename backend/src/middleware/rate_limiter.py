"""
Rate Limiting Middleware
"""

from fastapi import Request, HTTPException, status
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio
from typing import Dict, Tuple


class RateLimiter:
    """Simple in-memory rate limiter"""

    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000
    ):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.minute_requests: Dict[str, list] = defaultdict(list)
        self.hour_requests: Dict[str, list] = defaultdict(list)
        self.lock = asyncio.Lock()

    async def is_allowed(self, client_id: str) -> Tuple[bool, str]:
        """
        Check if request is allowed

        Args:
            client_id: Client identifier (IP address or user ID)

        Returns:
            Tuple of (is_allowed, reason)
        """
        async with self.lock:
            now = datetime.utcnow()

            # Clean old entries
            self._cleanup_old_entries(client_id, now)

            # Check minute limit
            minute_count = len(self.minute_requests[client_id])
            if minute_count >= self.requests_per_minute:
                return False, f"Rate limit exceeded: {self.requests_per_minute} requests per minute"

            # Check hour limit
            hour_count = len(self.hour_requests[client_id])
            if hour_count >= self.requests_per_hour:
                return False, f"Rate limit exceeded: {self.requests_per_hour} requests per hour"

            # Add current request
            self.minute_requests[client_id].append(now)
            self.hour_requests[client_id].append(now)

            return True, ""

    def _cleanup_old_entries(self, client_id: str, now: datetime):
        """Remove old entries outside the time windows"""
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)

        # Clean minute entries
        self.minute_requests[client_id] = [
            req_time for req_time in self.minute_requests[client_id]
            if req_time > minute_ago
        ]

        # Clean hour entries
        self.hour_requests[client_id] = [
            req_time for req_time in self.hour_requests[client_id]
            if req_time > hour_ago
        ]

        # Remove empty entries
        if not self.minute_requests[client_id]:
            del self.minute_requests[client_id]
        if not self.hour_requests[client_id]:
            del self.hour_requests[client_id]

    async def get_rate_limit_info(self, client_id: str) -> Dict:
        """Get current rate limit status for client"""
        async with self.lock:
            now = datetime.utcnow()
            self._cleanup_old_entries(client_id, now)

            return {
                "requests_this_minute": len(self.minute_requests.get(client_id, [])),
                "requests_this_hour": len(self.hour_requests.get(client_id, [])),
                "limit_per_minute": self.requests_per_minute,
                "limit_per_hour": self.requests_per_hour
            }


# Global rate limiter instance
rate_limiter = RateLimiter(
    requests_per_minute=60,
    requests_per_hour=1000
)


async def rate_limit_middleware(request: Request, call_next):
    """Middleware to enforce rate limiting"""

    # Get client identifier (IP address or authenticated user ID)
    client_id = request.client.host if request.client else "unknown"

    # Check if authenticated and use user ID instead
    if hasattr(request.state, "user") and request.state.user:
        client_id = request.state.user.get("id", client_id)

    # Check rate limit
    allowed, reason = await rate_limiter.is_allowed(client_id)

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=reason,
            headers={"Retry-After": "60"}
        )

    # Add rate limit headers to response
    response = await call_next(request)

    rate_info = await rate_limiter.get_rate_limit_info(client_id)
    response.headers["X-RateLimit-Limit-Minute"] = str(rate_info["limit_per_minute"])
    response.headers["X-RateLimit-Remaining-Minute"] = str(
        rate_info["limit_per_minute"] - rate_info["requests_this_minute"]
    )
    response.headers["X-RateLimit-Limit-Hour"] = str(rate_info["limit_per_hour"])
    response.headers["X-RateLimit-Remaining-Hour"] = str(
        rate_info["limit_per_hour"] - rate_info["requests_this_hour"]
    )

    return response
