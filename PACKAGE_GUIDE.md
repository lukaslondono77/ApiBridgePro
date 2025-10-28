# 📦 ApiBridge Pro - Python Package Guide

This guide shows you how to install and use ApiBridge Pro as a Python package, just like any other library (e.g., `from apibridge import ...`).

---

## 🚀 Quick Start

### Option 1: Install from Local Directory

```bash
# In the ApiBridgePro directory
pip install -e .
```

Now you can use it in Python:

```python
from apibridge import Gateway, ConnectorPolicy, BudgetGuard, app

# Use the FastAPI app
from apibridge import app

# Or start the server via CLI
apibridge  # Starts server on http://0.0.0.0:8000
```

### Option 2: Install from GitHub (Development)

```bash
pip install git+https://github.com/lukaslondono77/ApiBridgePro.git
```

### Option 3: Build and Install Distribution Package

```bash
# Build the package
python -m build

# Install the built wheel
pip install dist/apibridge_pro-0.1.0-py3-none-any.whl
```

---

## 📚 Using as a Python Package

### Import Components

```python
from apibridge import (
    Gateway,              # Main gateway class
    ConnectorPolicy,      # Connector configuration
    BudgetGuard,          # Budget management
    PIIFirewall,          # PII protection
    load_config,        # Load YAML configs
    register_model,       # Register Pydantic models
    cache_get,            # Cache operations
    cache_set,
    get_metrics,          # Prometheus metrics
)

# Access the FastAPI app
from apibridge import app
```

### Example: Custom Integration

```python
from apibridge import Gateway, ConnectorPolicy, BudgetGuard, load_config
from apibridge.config import CONNECTORS_FILE
import asyncio

# Load your connectors
config = load_config(CONNECTORS_FILE)
policies = build_connector_policies(config)

# Create budget guard
budget = BudgetGuard("redis://localhost:6379")

# Initialize budget
await budget.init()

# Create gateway
gateway = Gateway(policies, budget)

# Use gateway programmatically
async def my_custom_function():
    # Make a request through the gateway
    from fastapi import Request
    request = Request(...)  # Your request object
    response = await gateway.proxy("coingecko", "simple/price", request)
    return response
```

### Register Custom Models

```python
from apibridge import register_model
from pydantic import BaseModel

class MyCustomModel(BaseModel):
    field1: str
    field2: int

# Register for schema drift detection
register_model("MyCustomModel", MyCustomModel)
```

---

## 🎯 CLI Usage

After installation, you'll have an `apibridge` command:

```bash
# Start server (default: http://0.0.0.0:8000)
apibridge

# Custom port
apibridge --port 9000

# Custom host and port
apibridge --host 127.0.0.1 --port 3000

# Disable auto-reload (production mode)
apibridge --no-reload

# Help
apibridge --help
```

---

## 📦 Publishing to PyPI

### Prerequisites

1. Create accounts on:
   - PyPI: https://pypi.org/account/register/
   - TestPyPI: https://test.pypi.org/account/register/

2. Install build tools:

```bash
pip install build twine
```

### Build the Package

```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build source distribution and wheel
python -m build
```

This creates:
- `dist/apibridge-pro-0.1.0.tar.gz` (source distribution)
- `dist/apibridge_pro-0.1.0-py3-none-any.whl` (wheel)

### Test on TestPyPI First

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ apibridge-pro
```

### Publish to PyPI

```bash
# Upload to real PyPI (permanent!)
twine upload dist/*
```

After publishing, anyone can install with:

```bash
pip install apibridge-pro
```

---

## 🔧 Development Setup

For development with auto-reload:

```bash
# Install in editable mode
pip install -e ".[dev]"

# This installs:
# - apibridge-pro (editable)
# - pytest, pytest-asyncio, etc. (dev dependencies)
```

Then you can edit code and changes are reflected immediately!

---

## 📋 Package Configuration

The package is configured in `pyproject.toml`:

- **Package name**: `apibridge-pro`
- **Import name**: `apibridge` (via `from apibridge import ...`)
- **CLI command**: `apibridge`
- **Version**: `0.1.0`

### Updating Version

To release a new version:

1. Update `version` in `pyproject.toml`:
   ```toml
   version = "0.2.0"
   ```

2. Rebuild and publish:
   ```bash
   python -m build
   twine upload dist/*
   ```

---

## 🎨 Using with FastAPI in Your Own App

```python
from fastapi import FastAPI
from apibridge import Gateway, BudgetGuard, build_connector_policies, load_config

# Your FastAPI app
my_app = FastAPI()

# Initialize ApiBridge components
config = load_config("connectors.yaml")
policies = build_connector_policies(config)
budget = BudgetGuard()
await budget.init()
gateway = Gateway(policies, budget)

# Add ApiBridge as a sub-app or mount routes
@my_app.get("/my-gateway/{connector}/{path:path}")
async def custom_proxy(connector: str, path: str):
    # Use gateway here
    pass
```

---

## 🔐 Environment Variables

The package respects these environment variables:

```bash
export CONNECTORS_FILE="connectors.yaml"  # Path to config
export REDIS_URL="redis://localhost:6379"  # Redis for caching
export MODE="live"  # live | record | replay
export DISABLE_DOCS="false"  # Disable /docs endpoint
```

---

## ✅ Verification

After installation, verify it works:

```python
# Python
python -c "from apibridge import Gateway; print('✅ Import works!')"

# CLI
apibridge --help
```

---

## 📝 Summary

✅ **Local Development**: `pip install -e .`  
✅ **From GitHub**: `pip install git+https://github.com/lukaslondono77/ApiBridgePro.git`  
✅ **From PyPI**: `pip install apibridge-pro` (after publishing)  
✅ **CLI Command**: `apibridge`  
✅ **Python Import**: `from apibridge import Gateway, app, ...`  

Your package is now ready to be used like any other Python library! 🎉

