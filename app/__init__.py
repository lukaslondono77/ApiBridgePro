"""
ApiBridge Pro - Universal API Gateway

A production-ready API gateway that connects to any API through one smart endpoint.
Features include multi-provider routing, privacy firewall, cost guardrails,
and unified schema transformations.

Example:
    ```python
    from apibridgepro import Gateway, ConnectorPolicy, BudgetGuard

    # Create a gateway instance
    gateway = Gateway(policies, budget)
    ```
"""

__version__ = "0.1.2"
__author__ = "Lukas Londono"

# Main components
from apibridgepro.budget import BudgetGuard
from apibridgepro.caching import get as cache_get
from apibridgepro.caching import set as cache_set
from apibridgepro.config import CONNECTORS_FILE, load_config
from apibridgepro.connectors import ConnectorPolicy, build_connector_policies
from apibridgepro.gateway import Gateway, register_model
from apibridgepro.observability import (
    cache_hits,
    cache_misses,
    get_metrics,
    rate_limit_exceeded,
    request_duration,
    requests_total,
)
from apibridgepro.pii_firewall import PIIAction, PIIFirewall, get_firewall
from apibridgepro.rate_limit import allow as rate_limit_allow

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

