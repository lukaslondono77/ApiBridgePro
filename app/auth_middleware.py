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
        return await call_next(request)

    # Check if auth is enabled
    auth_enabled = os.getenv("AUTH_ENABLED", "false").lower() in ("true", "1", "yes")

    if not auth_enabled:
        # Auth disabled - allow all requests (development mode)
        return await call_next(request)

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
    return await call_next(request)

