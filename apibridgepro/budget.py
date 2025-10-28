import time
from typing import Any

# Try Redis (async) — if not available, fallback to in-memory
RedisType: type[Any] | None = None
try:
    from redis.asyncio import Redis  # redis>=5 supports asyncio
    RedisType = Redis
except Exception:  # nosec B110
    # Redis is optional - fallback to in-memory storage
    pass

_in_memory_budgets: dict[str, float] = {}

class BudgetGuard:
    def __init__(self, redis_url: str | None):
        self.redis: Any = None
        self.redis_url = redis_url

    async def init(self):
        if RedisType and self.redis_url:
            try:
                self.redis = RedisType.from_url(self.redis_url, decode_responses=True)
                await self.redis.ping()
            except Exception:
                self.redis = None

    async def add_cost(self, key: str, usd: float, month_key: str | None = None):
        month_key = month_key or time.strftime("%Y-%m")
        full = f"budget:{key}:{month_key}"
        if self.redis:
            await self.redis.incrbyfloat(full, usd)
        else:
            _in_memory_budgets[full] = float(_in_memory_budgets.get(full, 0.0) + usd)

    async def get_cost(self, key: str, month_key: str | None = None) -> float:
        month_key = month_key or time.strftime("%Y-%m")
        full = f"budget:{key}:{month_key}"
        if self.redis:
            val = await self.redis.get(full)
            return float(val or 0.0)
        return float(_in_memory_budgets.get(full, 0.0))


