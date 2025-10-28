"""
Test security features - path validation, normalization
"""
from apibridgepro.connectors import ConnectorPolicy


def test_path_traversal_blocked():
    """Test that path traversal attempts are blocked"""
    policy = ConnectorPolicy("test", {
        "base_url": "https://api.example.com",
        "allow_paths": ["^/api/users$"]
    })

    # These should be blocked
    assert policy.path_allowed("/api/users/../admin") is False
    assert policy.path_allowed("/api/../admin/secrets") is False
    assert policy.path_allowed("/../etc/passwd") is False


def test_url_encoding_normalized():
    """Test that URL-encoded paths are normalized"""
    policy = ConnectorPolicy("test", {
        "base_url": "https://api.example.com",
        "allow_paths": ["^/api/users$"]
    })

    # URL-encoded path should match after normalization
    assert policy.path_allowed("/api/users") is True
    assert policy.path_allowed("%2Fapi%2Fusers") is True  # Encoded /api/users

    # But encoded traversal should still be blocked
    assert policy.path_allowed("/api/%2E%2E/admin") is False  # Encoded ../


def test_double_slash_normalized():
    """Test that double slashes are normalized"""
    policy = ConnectorPolicy("test", {
        "base_url": "https://api.example.com",
        "allow_paths": ["^/api/users$"]
    })

    # Double slashes should be normalized to single
    assert policy.path_allowed("/api//users") is True
    assert policy.path_allowed("//api/users") is True
    assert policy.path_allowed("/api/users//") is True


def test_trailing_slash_normalized():
    """Test that trailing slashes are handled correctly"""
    policy = ConnectorPolicy("test", {
        "base_url": "https://api.example.com",
        "allow_paths": ["^/api/users$"]
    })

    # With or without trailing slash should match
    assert policy.path_allowed("/api/users") is True
    assert policy.path_allowed("/api/users/") is True


def test_exact_match_required():
    """Test that exact regex match is required (fullmatch)"""
    policy = ConnectorPolicy("test", {
        "base_url": "https://api.example.com",
        "allow_paths": ["^/api/users$"]  # Exact match
    })

    # Exact match
    assert policy.path_allowed("/api/users") is True

    # Partial matches should fail (fullmatch, not match)
    assert policy.path_allowed("/api/users/123") is False
    assert policy.path_allowed("/api/users/admin") is False
    assert policy.path_allowed("/ api/users") is False


def test_wildcard_paths_work():
    """Test that wildcard regex patterns work correctly"""
    policy = ConnectorPolicy("test", {
        "base_url": "https://api.example.com",
        "allow_paths": ["^/api/users/.*$"]  # Wildcard
    })

    # Should match all paths under /api/users/
    assert policy.path_allowed("/api/users/123") is True
    assert policy.path_allowed("/api/users/abc/profile") is True

    # But not other paths
    assert policy.path_allowed("/api/admin") is False
    assert policy.path_allowed("/api") is False


def test_multiple_allowed_paths():
    """Test that multiple allow_paths work correctly"""
    policy = ConnectorPolicy("test", {
        "base_url": "https://api.example.com",
        "allow_paths": [
            "^/api/users$",
            "^/api/posts$",
            "^/api/comments/.*$"
        ]
    })

    # All allowed paths should work
    assert policy.path_allowed("/api/users") is True
    assert policy.path_allowed("/api/posts") is True
    assert policy.path_allowed("/api/comments/123") is True

    # Disallowed paths should fail
    assert policy.path_allowed("/api/admin") is False
    assert policy.path_allowed("/api/settings") is False


def test_case_sensitive_paths():
    """Test that path matching is case-sensitive"""
    policy = ConnectorPolicy("test", {
        "base_url": "https://api.example.com",
        "allow_paths": ["^/api/users$"]
    })

    # Exact case should match
    assert policy.path_allowed("/api/users") is True

    # Different case should not match
    assert policy.path_allowed("/API/USERS") is False
    assert policy.path_allowed("/Api/Users") is False


def test_empty_path():
    """Test handling of empty or root paths"""
    policy = ConnectorPolicy("test", {
        "base_url": "https://api.example.com",
        "allow_paths": ["^/$", "^/api/.*$"]
    })

    assert policy.path_allowed("/") is True
    # Empty string gets normalized to "/" which matches "^/$"
    assert policy.path_allowed("") is True

