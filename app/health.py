import time

# Track provider health based on recent successful latency
# provider_key -> (healthy: bool, avg_latency_ms: float, ts, circuit_breaker)
_health: dict[str, dict] = {}

class CircuitBreaker:
    """
    Circuit breaker pattern to prevent cascading failures.
    States: CLOSED (normal) → OPEN (failing) → HALF_OPEN (testing recovery)
    """
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.last_failure_time = 0.0
        self.last_success_time = time.time()

    def should_attempt(self) -> bool:
        """Check if request should be attempted"""
        now = time.time()

        if self.state == "CLOSED":
            return True

        if self.state == "OPEN":
            # Check if recovery timeout has passed
            if now - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                return True
            return False  # Still in open state, don't attempt

        if self.state == "HALF_OPEN":
            return True  # Allow one test request

        return True

    def record_success(self):
        """Record successful request"""
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_success_time = time.time()

    def record_failure(self):
        """Record failed request"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"  # Open the circuit

    def get_state(self) -> str:
        return self.state

def mark_success(pkey: str, latency_ms: int):
    h = _health.setdefault(pkey, {
        "healthy": True,
        "avg": latency_ms,
        "ts": time.time(),
        "circuit_breaker": CircuitBreaker()
    })
    # exponential moving average
    h["avg"] = int(0.7 * h["avg"] + 0.3 * latency_ms)
    h["healthy"] = True
    h["ts"] = time.time()

    # Record success in circuit breaker
    if "circuit_breaker" in h:
        h["circuit_breaker"].record_success()

def mark_failure(pkey: str):
    h = _health.setdefault(pkey, {
        "healthy": False,
        "avg": 9999,
        "ts": time.time(),
        "circuit_breaker": CircuitBreaker()
    })
    h["healthy"] = False
    h["ts"] = time.time()

    # Record failure in circuit breaker
    if "circuit_breaker" in h:
        h["circuit_breaker"].record_failure()

def should_attempt_provider(pkey: str) -> bool:
    """Check if provider should be attempted (circuit breaker check)"""
    if pkey not in _health:
        return True

    h = _health[pkey]
    if "circuit_breaker" not in h:
        h["circuit_breaker"] = CircuitBreaker()

    return h["circuit_breaker"].should_attempt()

def pick_best(providers: list[dict]) -> list[dict]:
    """
    Return providers sorted by health + latency + weight + circuit breaker state.
    Filters out providers with open circuit breakers.
    """
    # Filter out providers with open circuit breakers
    available_providers = [
        p for p in providers
        if should_attempt_provider(p["__key"])
    ]

    # If all circuit breakers are open, allow half-open attempts
    if not available_providers:
        available_providers = providers

    def key(p):
        pkey = p["__key"]
        h = _health.get(pkey, {"healthy": True, "avg": 9999})

        # Penalty for open circuit breaker
        circuit_penalty = 0
        if "circuit_breaker" in h:
            state = h["circuit_breaker"].get_state()
            if state == "OPEN":
                circuit_penalty = 100000  # Very high penalty
            elif state == "HALF_OPEN":
                circuit_penalty = 50000  # High penalty

        return (0 if h["healthy"] else 1, circuit_penalty + h["avg"] - int(p.get("weight", 1))*10)

    return sorted(available_providers, key=key)


