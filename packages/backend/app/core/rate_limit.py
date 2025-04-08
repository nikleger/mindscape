from fastapi import FastAPI, Request, HTTPException
from redis import asyncio as aioredis
import time
from typing import Optional, Tuple
from app.core.config import settings

class RateLimiter:
    """Rate limiting implementation using Redis as backend store."""
    
    def __init__(self, redis_client: aioredis.Redis):
        self.redis = redis_client
        self.enabled = settings.RATE_LIMIT_ENABLED
        self.default_limit = self._parse_rate_limit(settings.RATE_LIMIT_DEFAULT)
        self.login_limit = self._parse_rate_limit(settings.RATE_LIMIT_LOGIN)
    
    def _parse_rate_limit(self, rate_limit: str) -> Tuple[int, int]:
        """Parse rate limit string (e.g., '100/minute') into (count, seconds)."""
        count, period = rate_limit.split('/')
        count = int(count)
        if period == 'second':
            seconds = 1
        elif period == 'minute':
            seconds = 60
        elif period == 'hour':
            seconds = 3600
        else:
            raise ValueError(f"Unsupported rate limit period: {period}")
        return count, seconds
    
    def _get_cache_key(self, request: Request) -> str:
        """Generate a cache key based on the client's IP and endpoint."""
        client_ip = request.client.host if request.client else "unknown"
        endpoint = request.url.path
        return f"rate_limit:{client_ip}:{endpoint}"
    
    async def is_rate_limited(self, request: Request) -> Tuple[bool, Optional[int]]:
        """Check if the request should be rate limited.
        
        Returns:
            Tuple[bool, Optional[int]]: (is_limited, retry_after)
        """
        if not self.enabled:
            return False, None
            
        # Determine which rate limit to use
        if request.url.path.endswith('/login'):
            limit, period = self.login_limit
        else:
            limit, period = self.default_limit
            
        cache_key = self._get_cache_key(request)
        
        # Use Redis to track request count
        current_time = int(time.time())
        window_start = current_time - period
        
        async with self.redis.pipeline() as pipe:
            # Remove old entries
            await pipe.zremrangebyscore(cache_key, 0, window_start)
            # Add current request
            await pipe.zadd(cache_key, {str(current_time): current_time})
            # Get request count in window
            await pipe.zcount(cache_key, window_start, current_time)
            # Set key expiration
            await pipe.expire(cache_key, period)
            # Execute pipeline
            _, _, request_count, _ = await pipe.execute()
            
        if request_count > limit:
            retry_after = period - (current_time - window_start)
            return True, retry_after
            
        return False, None

async def rate_limit_middleware(request: Request, call_next):
    """FastAPI middleware for rate limiting."""
    # Skip rate limiting for non-API routes
    if not request.url.path.startswith("/api"):
        return await call_next(request)
        
    redis = request.app.state.redis
    limiter = RateLimiter(redis)
    
    is_limited, retry_after = await limiter.is_rate_limited(request)
    if is_limited:
        headers = {
            "Retry-After": str(retry_after),
            "X-RateLimit-Reset": str(int(time.time()) + retry_after)
        }
        raise HTTPException(
            status_code=429,
            detail="Too many requests",
            headers=headers
        )
    
    return await call_next(request) 