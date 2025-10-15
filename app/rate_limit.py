
from .util import TokenBucket

_buckets: dict[str, TokenBucket] = {}

def allow(name: str, capacity: int, refill_per_sec: float) -> bool:
    bucket = _buckets.setdefault(name, TokenBucket(capacity, refill_per_sec))
    return bucket.allow()


