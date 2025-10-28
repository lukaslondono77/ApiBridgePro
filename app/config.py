import os
import re
from typing import Any

import yaml

ENV_VAR_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)(?::([^}]*))?\}")

def _expand_env(value: str) -> str:
    def repl(match):
        name, default = match.group(1), match.group(2)
        return os.getenv(name, default or "")
    return ENV_VAR_PATTERN.sub(repl, value)

def load_config(path: str) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    # expand ${ENV} inside YAML
    expanded = _expand_env(raw)
    data = yaml.safe_load(expanded) or {}
    if not isinstance(data, dict):
        raise ValueError("connectors.yaml must define a mapping")
    return data

CONNECTORS_FILE = os.getenv("CONNECTORS_FILE", "connectors.yaml")
MODE = os.getenv("APIBRIDGE_MODE", "live")  # live | record | replay
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DISABLE_DOCS = os.getenv("DISABLE_DOCS", "false").lower() in ("1","true","yes")

# CORS configuration - security critical
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")
ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS if origin.strip()]
# If empty, allow all for development (but warn in production)
# In production, set ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com


