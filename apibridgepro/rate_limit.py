import time
from typing import Any

from .util import TokenBucket

# Try Redis for distributed rate limiting
RedisType: type[Any] | None = None
try:
    from redis.asyncio import Redis  # redis>=5 supports asyncio
    RedisType = Redis
except Exception:  # nosec B110
    # Redis is optional - fallback to in-memory storage
    pass

_buckets: dict[str, TokenBucket] = {}
_redis_client: Any = None


async def init_rate_limiter(redis_url: str | None = None) -> None:
    """Initialize Redis client for distributed rate limiting"""
    global _redis_client
    if RedisType and redis_url:
        try:
            _redis_client = RedisType.from_url(redis_url, decode_responses=True)
            await _redis_client.ping()
        except Exception:
            _redis_client = None


async def allow_async(name: str, capacity: int, refill_per_sec: float) -> bool:
    """
    Async version with Redis support for distributed rate limiting.
    Falls back to in-memory if Redis is unavailable.
    """
    # Try Redis first for distributed rate limiting
    if _redis_client:
        try:
            # Use Redis-based token bucket algorithm
            # Key format: "rl:{name}"
            key = f"rl:{name}"
            now = time.time()

            # Get current token count and last update time
            pipe = _redis_client.pipeline()
            pipe.hget(key, "tokens")
            pipe.hget(key, "last")
            pipe.hget(key, "capacity")
            pipe.hget(key, "refill")
            results = await pipe.execute()

            tokens = float(results[0] or capacity)
            last = float(results[1] or now)
            stored_capacity = float(results[2] or capacity)
            stored_refill = float(results[3] or refill_per_sec)

            # If capacity or refill changed, update
            if stored_capacity != capacity or stored_refill != refill_per_sec:
                await _redis_client.hset(key, mapping={
                    "capacity": capacity,
                    "refill": refill_per_sec,
                })

            # Refill tokens based on time elapsed
            dt = now - last
            tokens = min(capacity, tokens + dt * refill_per_sec)

            # Check if request is allowed
            if tokens >= 1:
                tokens -= 1
                await _redis_client.hset(key, mapping={
                    "tokens": tokens,
                    "last": now,
                    "capacity": capacity,
                    "refill": refill_per_sec,
                })
                # Set TTL to auto-cleanup unused buckets (1 hour)
                await _redis_client.expire(key, 3600)
                return True

            # Not enough tokens
            await _redis_client.hset(key, mapping={
                "tokens": tokens,
                "last": now,
                "capacity": capacity,
                "refill": refill_per_sec,
            })
            await _redis_client.expire(key, 3600)
            return False

        except Exception:  # nosec B110
            # Redis failed, fall through to in-memory
            pass

    # Fallback to in-memory token bucket
    bucket = _buckets.setdefault(name, TokenBucket(capacity, refill_per_sec))
    return bucket.allow()


def allow(name: str, capacity: int, refill_per_sec: float) -> bool:
    """
    Synchronous version (in-memory only).
    Use allow_async() for Redis support.
    """
    bucket = _buckets.setdefault(name, TokenBucket(capacity, refill_per_sec))
    return bucket.allow()

