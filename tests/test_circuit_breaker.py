"""
Test circuit breaker functionality
"""
import time

from apibridgepro.health import CircuitBreaker, _health, mark_failure, mark_success, should_attempt_provider


def setup_function():
    """Clear health state before each test"""
    _health.clear()


def test_circuit_breaker_starts_closed():
    """Test that circuit breaker starts in CLOSED state"""
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=10)
    assert cb.get_state() == "CLOSED"
    assert cb.should_attempt() is True


def test_circuit_breaker_opens_after_threshold():
    """Test that circuit breaker opens after failure threshold"""
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=10)

    # Record 2 failures (below threshold)
    cb.record_failure()
    cb.record_failure()
    assert cb.get_state() == "CLOSED"
    assert cb.should_attempt() is True

    # 3rd failure should open circuit
    cb.record_failure()
    assert cb.get_state() == "OPEN"
    assert cb.should_attempt() is False


def test_circuit_breaker_recovers_after_timeout():
    """Test that circuit breaker moves to HALF_OPEN after recovery timeout"""
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=1)  # 1 second timeout

    # Open the circuit
    cb.record_failure()
    cb.record_failure()
    assert cb.get_state() == "OPEN"
    assert cb.should_attempt() is False

    # Wait for recovery timeout
    time.sleep(1.1)

    # Should move to HALF_OPEN and allow one attempt
    assert cb.should_attempt() is True
    assert cb.get_state() == "HALF_OPEN"


def test_circuit_breaker_closes_on_success_after_half_open():
    """Test that successful request in HALF_OPEN closes the circuit"""
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=1)

    # Open the circuit
    cb.record_failure()
    cb.record_failure()
    assert cb.get_state() == "OPEN"

    # Wait for recovery
    time.sleep(1.1)
    assert cb.should_attempt() is True
    assert cb.get_state() == "HALF_OPEN"

    # Successful request should close circuit
    cb.record_success()
    assert cb.get_state() == "CLOSED"
    assert cb.failure_count == 0


def test_circuit_breaker_integration_with_health():
    """Test circuit breaker integration with health tracking"""
    pkey = "test:provider"

    # Mark multiple failures to open circuit
    for _ in range(5):
        mark_failure(pkey)

    # Circuit should be open
    assert should_attempt_provider(pkey) is False

    # Mark success should close circuit
    mark_success(pkey, 100)
    assert should_attempt_provider(pkey) is True


def test_should_attempt_provider_for_unknown():
    """Test that unknown providers are allowed"""
    assert should_attempt_provider("unknown:provider") is True


def test_circuit_breaker_resets_on_success():
    """Test that success resets failure count"""
    cb = CircuitBreaker(failure_threshold=5, recovery_timeout=10)

    # Record some failures
    cb.record_failure()
    cb.record_failure()
    assert cb.failure_count == 2

    # Success should reset
    cb.record_success()
    assert cb.failure_count == 0
    assert cb.get_state() == "CLOSED"

