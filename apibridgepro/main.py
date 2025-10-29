import logging
import os
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

from .admin_ui import router as admin_router
from .auth_middleware import authenticate_request, limit_request_size
from .budget import BudgetGuard
from .config import (
    ALLOWED_ORIGINS,
    CONNECTORS_FILE,
    DISABLE_DOCS,
    MODE,
    REDIS_URL,
    load_config,
)
from .connectors import build_connector_policies
from .gateway import Gateway, register_model
from .logging_config import setup_logging
from .oauth2_manager import close_oauth2_manager
from .observability import get_metrics, info_metric
from .rate_limit import init_rate_limiter

# Configure logging with sanitization (default: enabled)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
SANITIZE_LOGS = os.getenv("SANITIZE_LOGS", "true").lower() in ("true", "1", "yes")
setup_logging(log_level=LOG_LEVEL, sanitize=SANITIZE_LOGS)

logger = logging.getLogger(__name__)


# Example model you can validate against (optional, add more as needed)
class WeatherUnified(BaseModel):
    temp_c: float | int
    humidity: float | int | None = None
    provider: str

# Register models by name to use in connectors.yaml
register_model("WeatherUnified", WeatherUnified)

app = FastAPI(
    title="ApiBridge Pro",
    description="Universal API Gateway with smart routing, PII protection, and observability",
    version="0.1.1",
    default_response_class=ORJSONResponse,
    docs_url=None if DISABLE_DOCS else "/docs",
    redoc_url=None if DISABLE_DOCS else "/redoc",
    openapi_url=None if DISABLE_DOCS else "/openapi.json",
)

# CORS configuration - security critical
# In production, set ALLOWED_ORIGINS environment variable:
# export ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
# For development/local demos, ALLOWED_ORIGINS can be empty (allows all)

# Determine allowed origins
cors_origins = ALLOWED_ORIGINS if ALLOWED_ORIGINS else ["*"]
if not ALLOWED_ORIGINS and MODE == "live":
    logger.warning(
        "⚠️  CORS: ALLOWED_ORIGINS not set - allowing all origins. "
        "This is insecure for production! Set ALLOWED_ORIGINS environment variable."
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["Content-Type", "Authorization", "X-API-Key"],
)

# Security middlewares
# Request size limits - prevents DoS attacks (default: 10MB)
# Set MAX_REQUEST_SIZE_MB=50 to increase limit
app.middleware("http")(limit_request_size)

# Authentication middleware - protects gateway endpoints
# Set AUTH_ENABLED=true and VALID_API_KEYS=key1,key2,key3 to enable
app.middleware("http")(authenticate_request)

# Lazy loading - only load config when needed
CONFIG: dict[str, Any] | None = None
POLICIES: dict[str, Any] | None = None
budget: BudgetGuard | None = None
gateway: Gateway | None = None

def _ensure_config_loaded():
    """Load config lazily if not already loaded"""
    global CONFIG, POLICIES, budget
    if CONFIG is None:
        try:
            CONFIG = load_config(CONNECTORS_FILE)
            POLICIES = build_connector_policies(CONFIG)
            budget = BudgetGuard(REDIS_URL)
        except FileNotFoundError:
            # If connectors.yaml not found, use empty config
            CONFIG = {}
            POLICIES = {}
            budget = BudgetGuard(REDIS_URL)
            logger.warning(f"connectors.yaml not found at {CONNECTORS_FILE}, using empty config")

# Include admin UI router
app.include_router(admin_router)

@app.on_event("startup")
async def startup():
    _ensure_config_loaded()
    assert budget is not None and POLICIES is not None
    await budget.init()
    # Initialize distributed rate limiting (if Redis available)
    await init_rate_limiter(REDIS_URL)
    global gateway
    gateway = Gateway(POLICIES, budget)
    # Update metrics info
    info_metric.info({
        'version': '0.1.1',
        'mode': MODE,
        'connectors': str(len(POLICIES))
    })

@app.on_event("shutdown")
async def shutdown():
    if gateway:
        await gateway.close()
    await close_oauth2_manager()

@app.get("/health")
def health():
    _ensure_config_loaded()
    assert POLICIES is not None
    return {"ok": True, "mode": MODE, "connectors": list(POLICIES.keys())}

@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    return get_metrics()

# Record/Replay toggles (very simple; extend as needed)
_RECORDINGS: dict[str, bytes] = {}
def _rr_key(method: str, url: str, query: str) -> str:
    return f"{method}:{url}?{query}"

@app.api_route("/proxy/{connector}/{full_path:path}", methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS","HEAD"])
async def proxy(connector: str, full_path: str, request: Request):
    _ensure_config_loaded()
    if MODE == "replay":
        key = _rr_key(request.method, f"{connector}/{full_path}", request.url.query)
        if key in _RECORDINGS:
            return ORJSONResponse(content=_RECORDINGS[key])

    assert gateway is not None
    resp = await gateway.proxy(connector, full_path, request)

    if MODE == "record" and resp.media_type and "json" in resp.media_type:
        # capture JSON body only
        key = _rr_key(request.method, f"{connector}/{full_path}", request.url.query)
        _RECORDINGS[key] = resp.body

    return resp

def cli():
    """CLI entry point for apibridge command"""
    import sys

    import uvicorn

    # Parse basic args (can be extended)
    host = "0.0.0.0"  # nosec B104
    port = 8000
    reload = True

    if len(sys.argv) > 1:
        if "--help" in sys.argv or "-h" in sys.argv:
            print("""
ApiBridge Pro - Universal API Gateway

Usage:
    apibridge                  # Start server (default: 0.0.0.0:8000)
    apibridge --port 9000     # Custom port
    apibridge --no-reload     # Disable auto-reload

Environment Variables:
    CONNECTORS_FILE            Path to connectors.yaml (default: connectors.yaml)
    REDIS_URL                  Redis connection URL (default: redis://localhost:6379)
    MODE                       live | record | replay (default: live)
    DISABLE_DOCS               Set to 'true' to disable /docs endpoint
            """)
            sys.exit(0)

        # Simple arg parsing
        args = sys.argv[1:]
        if "--port" in args:
            idx = args.index("--port")
            port = int(args[idx + 1]) if idx + 1 < len(args) else 8000
        if "--host" in args:
            idx = args.index("--host")
            host = args[idx + 1] if idx + 1 < len(args) else "0.0.0.0"  # nosec B104
        if "--no-reload" in args:
            reload = False

    uvicorn.run("apibridgepro.main:app", host=host, port=port, reload=reload)  # nosec B104

if __name__ == "__main__":
    cli()

