"""
Log Sanitizer - Remove sensitive data from log messages
"""
import re
from typing import Any

# Patterns to detect and sanitize sensitive data
SENSITIVE_PATTERNS = [
    (r'\b[A-Za-z0-9_-]{20,}\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b', 'REDACTED_JWT'),  # JWT tokens
    (r'\bsk-[A-Za-z0-9]{32,}\b', 'REDACTED_OPENAI_KEY'),  # OpenAI keys
    (r'\bghp_[A-Za-z0-9]{36}\b', 'REDACTED_GITHUB_TOKEN'),  # GitHub tokens
    (r'\bxoxb-[A-Za-z0-9-]{100,}\b', 'REDACTED_SLACK_TOKEN'),  # Slack tokens
    (r'\b[A-Za-z0-9_-]{32,}\b', None),  # Long strings (potential tokens/keys)
]

# Headers that should never be logged
SENSITIVE_HEADERS = {
    'authorization', 'x-api-key', 'api-key', 'x-auth-token',
    'cookie', 'set-cookie', 'x-forwarded-for', 'x-real-ip',
    'x-request-id', 'x-trace-id',
}


def sanitize_string(message: str) -> str:
    """Remove sensitive patterns from log messages"""
    sanitized = message

    # Remove JWT tokens, API keys, etc.
    for pattern, replacement in SENSITIVE_PATTERNS:
        if replacement:
            sanitized = re.sub(pattern, replacement, sanitized)
        else:
            # For long strings, only redact if they look like tokens (in specific contexts)
            pass

    return sanitized


def sanitize_headers(headers: dict[str, str] | Any) -> dict[str, str]:
    """Remove sensitive headers from logging"""
    if not isinstance(headers, dict):
        return {}

    sanitized = {}
    for key, value in headers.items():
        key_lower = key.lower()
        if key_lower in SENSITIVE_HEADERS or 'key' in key_lower or 'token' in key_lower or 'secret' in key_lower:
            sanitized[key] = 'REDACTED'
        else:
            sanitized[key] = value

    return sanitized


def sanitize_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Recursively sanitize dictionary values"""
    sanitized = {}
    for key, value in data.items():
        key_lower = str(key).lower()

        # Check if key indicates sensitive data
        sensitive_keywords = ['password', 'secret', 'key', 'token', 'auth', 'credential']
        if any(sensitive in key_lower for sensitive in sensitive_keywords):
            sanitized[key] = 'REDACTED'
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value)
        elif isinstance(value, str):
            # Sanitize string values
            sanitized[key] = sanitize_string(value)
        else:
            sanitized[key] = value

    return sanitized


def sanitize_log_record(record: Any) -> None:
    """
    Sanitize logging.LogRecord to remove sensitive data.
    Call this from a logging filter.
    """
    # Sanitize the main message
    if hasattr(record, 'msg') and isinstance(record.msg, str):
        record.msg = sanitize_string(record.msg)

    # Sanitize args if present
    if hasattr(record, 'args') and record.args:
        if isinstance(record.args, tuple):
            record.args = tuple(
                sanitize_string(str(arg)) if isinstance(arg, str) else arg
                for arg in record.args
            )
        elif isinstance(record.args, dict):
            record.args = sanitize_dict(record.args)

