"""
Test rate limiting functionality
"""
import time

from app.rate_limit import allow
from app.util import TokenBucket


def test_token_bucket_allows_requests():
    """Test that token bucket allows requests within capacity"""
    bucket = TokenBucket(capacity=5, refill_per_sec=1.0)

    # Should allow first 5 requests
    for _ in range(5):
        assert bucket.allow() is True

    # Should deny 6th request
    assert bucket.allow() is False


def test_token_bucket_refills():
    """Test that token bucket refills over time"""
    bucket = TokenBucket(capacity=2, refill_per_sec=10.0)

    # Consume all tokens
    assert bucket.allow() is True
    assert bucket.allow() is True
    assert bucket.allow() is False

    # Wait for refill (0.2 seconds = 2 tokens at 10/sec)
    time.sleep(0.25)

    # Should have tokens again
    assert bucket.allow() is True
    assert bucket.allow() is True


def test_rate_limit_per_connector():
    """Test that rate limits are enforced per connector"""
    # Test connector1
    for _ in range(3):
        assert allow("test:connector1", capacity=3, refill_per_sec=1.0) is True
    assert allow("test:connector1", capacity=3, refill_per_sec=1.0) is False

    # Test connector2 should have its own bucket
    for _ in range(3):
        assert allow("test:connector2", capacity=3, refill_per_sec=1.0) is True
    assert allow("test:connector2", capacity=3, refill_per_sec=1.0) is False


def test_rate_limit_concurrent_behavior():
    """Test rate limit behavior under rapid concurrent-like requests"""
    bucket = TokenBucket(capacity=10, refill_per_sec=5.0)

    # Burst of requests
    allowed = sum(1 for _ in range(15) if bucket.allow())

    # Should allow exactly capacity number
    assert allowed == 10

    # After small delay, should have some tokens
    time.sleep(0.3)  # 0.3 * 5 = 1.5 tokens
    assert bucket.allow() is True


