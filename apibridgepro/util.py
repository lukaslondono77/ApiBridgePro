import time


# Simple token-bucket structure (fallback if Redis is unavailable)
class TokenBucket:
    def __init__(self, capacity: int, refill_per_sec: float):
        self.capacity = capacity
        self.refill = refill_per_sec
        self.tokens = float(capacity)
        self.last = time.time()

    def allow(self) -> bool:
        now = time.time()
        dt = now - self.last
        self.tokens = min(self.capacity, self.tokens + dt * self.refill)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

def now_ms() -> int:
    return int(time.time() * 1000)


