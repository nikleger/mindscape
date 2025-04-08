from typing import Any, Optional
import json
import secrets
from datetime import datetime, timedelta

from fastapi import Request
from redis import Redis
from starlette.middleware.sessions import SessionMiddleware
from starlette.datastructures import MutableHeaders

from app.core.config import settings

class RedisSessionStore:
    """Redis-backed session store for scalable session management."""
    
    def __init__(self, redis_client: Redis, prefix: str = "session:", expire_seconds: int = None):
        self.redis = redis_client
        self.prefix = prefix
        self.expire_seconds = expire_seconds or settings.SESSION_COOKIE_MAX_AGE
    
    def _get_redis_key(self, session_id: str) -> str:
        return f"{self.prefix}{session_id}"
    
    async def get(self, session_id: str) -> dict:
        """Get session data from Redis."""
        key = self._get_redis_key(session_id)
        data = await self.redis.get(key)
        return json.loads(data) if data else {}
    
    async def set(self, session_id: str, data: dict) -> None:
        """Set session data in Redis with expiration."""
        key = self._get_redis_key(session_id)
        await self.redis.setex(
            key,
            self.expire_seconds,
            json.dumps(data)
        )
    
    async def delete(self, session_id: str) -> None:
        """Delete session data from Redis."""
        key = self._get_redis_key(session_id)
        await self.redis.delete(key)

class RedisSessionMiddleware(SessionMiddleware):
    """Enhanced session middleware with Redis backend and security features."""
    
    def __init__(
        self,
        app,
        store: RedisSessionStore,
        session_cookie: str = "session",
        max_age: int = None,
        path: str = "/",
        same_site: str = "lax",
        https_only: bool = False
    ):
        self.app = app
        self.store = store
        self.session_cookie = session_cookie
        self.max_age = max_age or settings.SESSION_COOKIE_MAX_AGE
        self.path = path
        self.security_flags = f"httponly; samesite={same_site}"
        if https_only:
            self.security_flags += "; secure"
    
    async def __call__(self, scope, receive, send):
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        session_id = None
        session = {}
        
        # Get session ID from cookie
        if "session" in scope:
            session_id = scope["session"].get("session_id")
            if session_id:
                session = await self.store.get(session_id)
        
        scope["session"] = session

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                if scope["session"]:
                    # Store session data in Redis
                    if not session_id:
                        session_id = secrets.token_urlsafe(32)
                    await self.store.set(session_id, scope["session"])
                    
                    # Set secure session cookie
                    headers = MutableHeaders(scope=message)
                    header_value = (
                        f"{self.session_cookie}={session_id}; "
                        f"Path={self.path}; "
                        f"Max-Age={self.max_age}; "
                        f"{self.security_flags}"
                    )
                    headers.append("Set-Cookie", header_value)
                
            await send(message)
        
        await self.app(scope, receive, send_wrapper)

def get_redis_session_middleware(app, redis_client: Redis):
    """Create Redis session middleware with configured settings."""
    store = RedisSessionStore(
        redis_client=redis_client,
        expire_seconds=settings.SESSION_COOKIE_MAX_AGE
    )
    
    return RedisSessionMiddleware(
        app=app,
        store=store,
        session_cookie="session",
        max_age=settings.SESSION_COOKIE_MAX_AGE,
        same_site=settings.SESSION_COOKIE_SAMESITE,
        https_only=settings.SESSION_COOKIE_SECURE
    ) 