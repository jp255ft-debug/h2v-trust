"""Rate limiting dependencies for FastAPI endpoints."""

import time
from typing import Dict, Any, Optional
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import redis
import logging

from config import settings

logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter using Redis for distributed rate limiting."""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis = redis_client
        self.local_cache: Dict[str, Dict[str, Any]] = {}
        
    async def check_rate_limit(
        self,
        request: Request,
        limit: int = 100,
        window: int = 60,  # seconds
        key_prefix: str = "rate_limit"
    ) -> bool:
        """
        Check if request is within rate limit.
        
        Args:
            request: FastAPI request object
            limit: Maximum requests per window
            window: Time window in seconds
            key_prefix: Redis key prefix
            
        Returns:
            True if request is allowed, False if rate limited
        """
        # Get client identifier (IP or API key)
        client_id = self._get_client_identifier(request)
        
        # Generate rate limit key
        key = f"{key_prefix}:{client_id}"
        
        # Use Redis if available, otherwise local cache
        if self.redis:
            return await self._check_redis_rate_limit(key, limit, window)
        else:
            return self._check_local_rate_limit(key, limit, window)
    
    def _get_client_identifier(self, request: Request) -> str:
        """Get unique identifier for rate limiting."""
        # Try to get API key from headers
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return f"api_key:{api_key}"
        
        # Fall back to IP address
        client_host = request.client.host if request.client else "unknown"
        return f"ip:{client_host}"
    
    async def _check_redis_rate_limit(self, key: str, limit: int, window: int) -> bool:
        """Check rate limit using Redis."""
        try:
            # Use Redis pipeline for atomic operations
            pipe = self.redis.pipeline()
            current_time = int(time.time())
            
            # Remove old entries
            pipe.zremrangebyscore(key, 0, current_time - window)
            
            # Count current requests
            pipe.zcard(key)
            
            # Add current request
            pipe.zadd(key, {str(current_time): current_time})
            
            # Set expiration
            pipe.expire(key, window)
            
            results = pipe.execute()
            current_count = results[1]
            
            return current_count <= limit
            
        except redis.RedisError as e:
            logger.error(f"Redis error in rate limiting: {e}")
            # Fall back to local rate limiting
            return self._check_local_rate_limit(key, limit, window)
    
    def _check_local_rate_limit(self, key: str, limit: int, window: int) -> bool:
        """Check rate limit using local cache."""
        current_time = time.time()
        
        # Initialize or clean cache for this key
        if key not in self.local_cache:
            self.local_cache[key] = {
                "timestamps": [],
                "window": window,
            }
        
        cache_entry = self.local_cache[key]
        
        # Remove old timestamps
        cache_entry["timestamps"] = [
            ts for ts in cache_entry["timestamps"]
            if current_time - ts < window
        ]
        
        # Check if limit exceeded
        if len(cache_entry["timestamps"]) >= limit:
            return False
        
        # Add current timestamp
        cache_entry["timestamps"].append(current_time)
        
        # Clean up old cache entries
        self._clean_local_cache()
        
        return True
    
    def _clean_local_cache(self):
        """Clean up old entries from local cache."""
        current_time = time.time()
        keys_to_remove = []
        
        for key, entry in self.local_cache.items():
            # Remove entries older than 2 windows
            entry["timestamps"] = [
                ts for ts in entry["timestamps"]
                if current_time - ts < entry["window"] * 2
            ]
            
            # Remove empty entries
            if not entry["timestamps"]:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.local_cache[key]


class RateLimitChecker:
    """FastAPI dependency for rate limiting."""
    
    def __init__(
        self,
        limit: int = 100,
        window: int = 60,
        key_prefix: str = "rate_limit",
        redis_client: Optional[redis.Redis] = None,
    ):
        self.limit = limit
        self.window = window
        self.key_prefix = key_prefix
        self.rate_limiter = RateLimiter(redis_client)
    
    async def __call__(self, request: Request):
        """Check rate limit for incoming request."""
        is_allowed = await self.rate_limiter.check_rate_limit(
            request=request,
            limit=self.limit,
            window=self.window,
            key_prefix=self.key_prefix,
        )
        
        if not is_allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {self.limit} requests per {self.window} seconds.",
                headers={
                    "Retry-After": str(self.window),
                    "X-RateLimit-Limit": str(self.limit),
                    "X-RateLimit-Window": str(self.window),
                },
            )


class TieredRateLimiter:
    """Tiered rate limiting based on API key or user role."""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.rate_limiter = RateLimiter(redis_client)
        self.tiers = {
            "free": {"limit": 100, "window": 3600},  # 100 requests per hour
            "basic": {"limit": 1000, "window": 3600},  # 1000 requests per hour
            "pro": {"limit": 10000, "window": 3600},  # 10000 requests per hour
            "enterprise": {"limit": 100000, "window": 3600},  # 100000 requests per hour
        }
    
    async def check_tiered_rate_limit(
        self,
        request: Request,
        tier: str = "free",
        endpoint: Optional[str] = None,
    ) -> bool:
        """
        Check tiered rate limit.
        
        Args:
            request: FastAPI request object
            tier: Rate limit tier
            endpoint: Specific endpoint (for granular limits)
            
        Returns:
            True if request is allowed
        """
        # Get tier configuration
        tier_config = self.tiers.get(tier, self.tiers["free"])
        limit = tier_config["limit"]
        window = tier_config["window"]
        
        # Generate key with tier and endpoint
        client_id = self.rate_limiter._get_client_identifier(request)
        key_parts = ["tiered", tier, client_id]
        
        if endpoint:
            key_parts.append(endpoint)
        
        key = ":".join(key_parts)
        
        return await self.rate_limiter.check_rate_limit(
            request=request,
            limit=limit,
            window=window,
            key_prefix=key,
        )


class BurstRateLimiter:
    """Rate limiter with burst allowance."""
    
    def __init__(
        self,
        sustained_limit: int = 100,
        burst_limit: int = 200,
        window: int = 60,
        redis_client: Optional[redis.Redis] = None,
    ):
        self.sustained_limit = sustained_limit
        self.burst_limit = burst_limit
        self.window = window
        self.rate_limiter = RateLimiter(redis_client)
    
    async def check_burst_rate_limit(self, request: Request) -> bool:
        """
        Check rate limit with burst allowance.
        
        Args:
            request: FastAPI request object
            
        Returns:
            True if request is allowed
        """
        client_id = self.rate_limiter._get_client_identifier(request)
        
        # Check burst limit (short window)
        burst_key = f"burst:{client_id}"
        burst_allowed = await self.rate_limiter.check_rate_limit(
            request=request,
            limit=self.burst_limit,
            window=10,  # 10-second window for bursts
            key_prefix=burst_key,
        )
        
        if not burst_allowed:
            return False
        
        # Check sustained limit (longer window)
        sustained_key = f"sustained:{client_id}"
        sustained_allowed = await self.rate_limiter.check_rate_limit(
            request=request,
            limit=self.sustained_limit,
            window=self.window,
            key_prefix=sustained_key,
        )
        
        return sustained_allowed


# Global rate limiter instances
_rate_limiter = RateLimiter()
_tiered_rate_limiter = TieredRateLimiter()


def get_rate_limiter() -> RateLimiter:
    """Get global rate limiter instance."""
    return _rate_limiter


def get_tiered_rate_limiter() -> TieredRateLimiter:
    """Get global tiered rate limiter instance."""
    return _tiered_rate_limiter


# FastAPI dependencies
def rate_limit(limit: int = 100, window: int = 60) -> RateLimitChecker:
    """Create rate limit dependency."""
    return RateLimitChecker(limit=limit, window=window)


def tiered_rate_limit(tier: str = "free") -> RateLimitChecker:
    """Create tiered rate limit dependency."""
    tier_config = _tiered_rate_limiter.tiers.get(tier, _tiered_rate_limiter.tiers["free"])
    return RateLimitChecker(
        limit=tier_config["limit"],
        window=tier_config["window"],
        key_prefix=f"tier:{tier}",
    )
