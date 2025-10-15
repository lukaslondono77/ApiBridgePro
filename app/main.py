
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

from .admin_ui import router as admin_router
from .budget import BudgetGuard
from .config import CONNECTORS_FILE, DISABLE_DOCS, MODE, REDIS_URL, load_config
from .connectors import build_connector_policies
from .gateway import Gateway, register_model
from .oauth2_manager import close_oauth2_manager
from .observability import get_metrics, info_metric


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
    version="0.1.0",
    default_response_class=ORJSONResponse,
    docs_url=None if DISABLE_DOCS else "/docs",
    redoc_url=None if DISABLE_DOCS else "/redoc",
    openapi_url=None if DISABLE_DOCS else "/openapi.json",
)

CONFIG = load_config(CONNECTORS_FILE)
POLICIES = build_connector_policies(CONFIG)

budget = BudgetGuard(REDIS_URL)
gateway: Gateway | None = None

# Include admin UI router
app.include_router(admin_router)

@app.on_event("startup")
async def startup():
    await budget.init()
    global gateway
    gateway = Gateway(POLICIES, budget)
    # Update metrics info
    info_metric.info({
        'version': '0.1.0',
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

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

