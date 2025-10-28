"""
Authentication Middleware - API Key validation for gateway requests
"""
import logging
import os
from collections.abc import Callable

from fastapi import Request, Response, status
from fastapi.responses import ORJSONResponse

logger = logging.getLogger(__name__)

# Simple in-memory API key store (can be replaced with DB/Redis)
_API_KEYS: set[str] = set()


def load_api_keys() -> set[str]:
    """
    Load API keys from environment variable.
    Format: comma-separated list
    Example: export VALID_API_KEYS=key1,key2,key3
    """
    keys_str = os.getenv("VALID_API_KEYS", "")
    if keys_str:
        keys = {k.strip() for k in keys_str.split(",") if k.strip()}
        logger.info(f"Loaded {len(keys)} API key(s) from environment")
        return keys
    return set()


def is_valid_api_key(api_key: str) -> bool:
    """Check if API key is valid"""
    if not _API_KEYS:
        _API_KEYS.update(load_api_keys())
    return api_key in _API_KEYS


async def authenticate_request(
    request: Request, call_next: Callable
) -> Response:
    """
    Middleware to authenticate requests to the gateway.

    Checks for X-API-Key header and validates against configured API keys.
    Can be disabled by setting AUTH_ENABLED=false.

    Skip authentication for:
    - Health endpoints (/health, /metrics)
    - Admin endpoints (/admin)
    - Docs endpoints (/docs, /redoc, /openapi.json)
    """
    # Skip auth for public endpoints
    path = request.url.path
    skip_auth_paths = ["/health", "/metrics", "/admin", "/docs", "/redoc", "/openapi.json"]

    if any(path.startswith(p) for p in skip_auth_paths):
        response = await call_next(request)
        return response  # type: ignore[no-any-return]

    # Check if auth is enabled
    auth_enabled = os.getenv("AUTH_ENABLED", "false").lower() in ("true", "1", "yes")

    if not auth_enabled:
        # Auth disabled - allow all requests (development mode)
        response = await call_next(request)
        return response  # type: ignore[no-any-return]

    # Validate API key
    api_key = request.headers.get("X-API-Key") or request.headers.get("Authorization", "").replace("Bearer ", "")

    if not api_key:
        logger.warning(f"Unauthorized request to {path} - no API key provided")
        return ORJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "unauthorized", "message": "API key required. Provide X-API-Key header."}
        )

    if not is_valid_api_key(api_key):
        logger.warning(f"Unauthorized request to {path} - invalid API key")
        return ORJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "unauthorized", "message": "Invalid API key"}
        )

    # Valid API key - proceed
    logger.debug(f"Authenticated request to {path}")
    response = await call_next(request)
    return response  # type: ignore[no-any-return]


async def limit_request_size(
    request: Request, call_next: Callable
) -> Response:
    """
    Middleware to limit request payload size (DoS protection).

    Prevents large payload attacks by limiting request body size.
    Configurable via MAX_REQUEST_SIZE_MB environment variable (default: 10MB).
    """
    max_size_mb = float(os.getenv("MAX_REQUEST_SIZE_MB", "10"))
    max_size_bytes = int(max_size_mb * 1024 * 1024)

    # Check Content-Length header if present
    content_length = request.headers.get("Content-Length")
    if content_length:
        try:
            size = int(content_length)
            if size > max_size_bytes:
                logger.warning(
                    f"Request payload too large: {size} bytes (max: {max_size_bytes})"
                )
                return ORJSONResponse(
                    status_code=413,
                    content={
                        "error": "payload_too_large",
                        "message": f"Request body exceeds maximum size of {max_size_mb}MB",
                        "max_size_mb": max_size_mb,
                    },
                )
        except ValueError:
            pass  # Invalid Content-Length, will check body if needed

    # For methods with body, stream check (FastAPI/Starlette handles this)
    # We'll rely on Starlette's built-in size limits for actual body reading
    response = await call_next(request)
    return response  # type: ignore[no-any-return]

