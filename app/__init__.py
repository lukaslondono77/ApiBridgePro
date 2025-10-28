"""
ApiBridge Pro - Universal API Gateway

A production-ready API gateway that connects to any API through one smart endpoint.
Features include multi-provider routing, privacy firewall, cost guardrails, 
and unified schema transformations.

Example:
    ```python
    from apibridge import Gateway, ConnectorPolicy, BudgetGuard
    
    # Create a gateway instance
    gateway = Gateway(policies, budget)
    ```
"""

__version__ = "0.1.0"
__author__ = "Lukas Londono"

# Main components
from .gateway import Gateway, register_model
from .connectors import ConnectorPolicy, build_connector_policies
from .budget import BudgetGuard
from .config import load_config, CONNECTORS_FILE
from .caching import get as cache_get, set as cache_set
from .rate_limit import allow as rate_limit_allow
from .pii_firewall import PIIFirewall, PIIAction, get_firewall
from .observability import (
    requests_total,
    request_duration,
    cache_hits,
    cache_misses,
    rate_limit_exceeded,
    get_metrics,
)
from .main import app

__all__ = [
    # Core classes
    "Gateway",
    "ConnectorPolicy",
    "BudgetGuard",
    "PIIFirewall",
    "PIIAction",
    # Functions
    "register_model",
    "build_connector_policies",
    "load_config",
    "cache_get",
    "cache_set",
    "rate_limit_allow",
    "get_firewall",
    "get_metrics",
    # FastAPI app
    "app",
    # Constants
    "CONNECTORS_FILE",
    # Metrics (for advanced users)
    "requests_total",
    "request_duration",
    "cache_hits",
    "cache_misses",
    "rate_limit_exceeded",
]

