"""
Test caching functionality
"""
import time

from app.caching import get
from app.caching import set as cache_set


def test_cache_set_and_get():
    """Test basic cache set and get"""
    key = "test:key:1"
    content = b"test content"
    headers = [(b"content-type", b"application/json")]
    status = 200
    ttl = 10

    cache_set(key, content, headers, status, ttl)
    result = get(key)

    assert result is not None
    cached_content, cached_headers, cached_status = result
    assert cached_content == content
    assert cached_headers == headers
    assert cached_status == status


def test_cache_expiration():
    """Test that cache entries expire"""
    key = "test:key:expire"
    content = b"expires soon"
    headers = [(b"content-type", b"text/plain")]
    status = 200
    ttl = 1  # 1 second TTL

    cache_set(key, content, headers, status, ttl)

    # Should be available immediately
    result = get(key)
    assert result is not None

    # Wait for expiration
    time.sleep(1.1)

    # Should be expired
    result = get(key)
    assert result is None


def test_cache_key_uniqueness():
    """Test that different cache keys don't collide"""
    key1 = "connector1:GET:http://api.example.com/resource?id=1"
    key2 = "connector1:GET:http://api.example.com/resource?id=2"
    key3 = "connector2:GET:http://api.example.com/resource?id=1"

    cache_set(key1, b"content1", [], 200, 10)
    cache_set(key2, b"content2", [], 200, 10)
    cache_set(key3, b"content3", [], 200, 10)

    assert get(key1)[0] == b"content1"
    assert get(key2)[0] == b"content2"
    assert get(key3)[0] == b"content3"


def test_cache_miss():
    """Test cache miss returns None"""
    result = get("nonexistent:key")
    assert result is None


