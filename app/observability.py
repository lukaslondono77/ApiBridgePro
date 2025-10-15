"""
Observability - Prometheus metrics and OpenTelemetry traces
"""
import logging
from functools import wraps

from fastapi import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, Info, generate_latest

# Prometheus Metrics
requests_total = Counter(
    'apibridge_requests_total',
    'Total number of requests',
    ['connector', 'method', 'status']
)

request_duration = Histogram(
    'apibridge_request_duration_seconds',
    'Request duration in seconds',
    ['connector', 'method']
)

upstream_requests = Counter(
    'apibridge_upstream_requests_total',
    'Total upstream provider requests',
    ['connector', 'provider', 'status']
)

upstream_duration = Histogram(
    'apibridge_upstream_duration_seconds',
    'Upstream request duration',
    ['connector', 'provider']
)

cache_hits = Counter(
    'apibridge_cache_hits_total',
    'Cache hits',
    ['connector']
)

cache_misses = Counter(
    'apibridge_cache_misses_total',
    'Cache misses',
    ['connector']
)

rate_limit_exceeded = Counter(
    'apibridge_rate_limit_exceeded_total',
    'Rate limit exceeded count',
    ['connector']
)

budget_spent = Gauge(
    'apibridge_budget_spent_usd',
    'Current budget spent in USD',
    ['connector', 'month']
)

provider_health = Gauge(
    'apibridge_provider_health',
    'Provider health status (1=healthy, 0=unhealthy)',
    ['connector', 'provider']
)

schema_drift_detected = Counter(
    'apibridge_schema_drift_total',
    'Schema drift detections',
    ['connector']
)

info_metric = Info('apibridge', 'ApiBridge Pro information')

# Initialize info
info_metric.info({
    'version': '0.1.0',
    'mode': 'live'
})

# OpenTelemetry setup (optional)
try:
    import os

    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

    OTEL_ENABLED = os.getenv("OTEL_ENABLED", "false").lower() in ("true", "1", "yes")

    if OTEL_ENABLED:
        # Create resource
        resource = Resource.create({"service.name": "apibridge-pro"})

        # Set up tracer provider
        provider = TracerProvider(resource=resource)

        # Configure exporter (OTLP or Console)
        otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
        if otlp_endpoint:
            exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        else:
            exporter = ConsoleSpanExporter()

        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)

        tracer = trace.get_tracer(__name__)
    else:
        tracer = None
except ImportError:
    OTEL_ENABLED = False
    tracer = None

logger = logging.getLogger(__name__)

class MetricsCollector:
    """Helper class for collecting metrics"""

    @staticmethod
    def record_request(connector: str, method: str, status: int, duration: float):
        """Record a gateway request"""
        requests_total.labels(connector=connector, method=method, status=status).inc()
        request_duration.labels(connector=connector, method=method).observe(duration)

    @staticmethod
    def record_upstream(connector: str, provider: str, status: int, duration: float):
        """Record an upstream provider request"""
        upstream_requests.labels(connector=connector, provider=provider, status=status).inc()
        upstream_duration.labels(connector=connector, provider=provider).observe(duration)

    @staticmethod
    def record_cache_hit(connector: str):
        """Record a cache hit"""
        cache_hits.labels(connector=connector).inc()

    @staticmethod
    def record_cache_miss(connector: str):
        """Record a cache miss"""
        cache_misses.labels(connector=connector).inc()

    @staticmethod
    def record_rate_limit(connector: str):
        """Record a rate limit exceeded event"""
        rate_limit_exceeded.labels(connector=connector).inc()

    @staticmethod
    def update_budget(connector: str, month: str, amount: float):
        """Update budget gauge"""
        budget_spent.labels(connector=connector, month=month).set(amount)

    @staticmethod
    def update_provider_health(connector: str, provider: str, healthy: bool):
        """Update provider health status"""
        provider_health.labels(connector=connector, provider=provider).set(1 if healthy else 0)

    @staticmethod
    def record_schema_drift(connector: str):
        """Record schema drift detection"""
        schema_drift_detected.labels(connector=connector).inc()

def get_metrics() -> Response:
    """Get Prometheus metrics endpoint response"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

def trace_operation(operation_name: str):
    """Decorator to trace operations with OpenTelemetry"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if tracer and OTEL_ENABLED:
                with tracer.start_as_current_span(operation_name) as span:
                    try:
                        result = await func(*args, **kwargs)
                        span.set_attribute("success", True)
                        return result
                    except Exception as e:
                        span.set_attribute("success", False)
                        span.set_attribute("error", str(e))
                        raise
            else:
                return await func(*args, **kwargs)
        return wrapper
    return decorator


