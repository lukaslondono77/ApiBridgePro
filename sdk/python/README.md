# ApiBridge Pro - Python SDK

Official Python client for ApiBridge Pro API Gateway.

## Installation

```bash
pip install httpx  # Required dependency
```

Then copy `apibridge_client.py` to your project.

## Quick Start

```python
import asyncio
from apibridge_client import ApiBridgeClient

async def main():
    async with ApiBridgeClient("http://localhost:8000") as client:
        # Check health
        health = await client.health()
        print(f"System OK: {health['ok']}")
        
        # Make API request
        response = await client.proxy(
            "weather_unified",
            "/weather",
            params={"q": "London"}
        )
        data = response.json()
        print(f"Temperature: {data['temp_c']}°C")

asyncio.run(main())
```

## Typed Connector Access

```python
async with ApiBridgeClient("http://localhost:8000") as client:
    # Instead of:
    response = await client.proxy("github", "/user")
    
    # You can use:
    response = await client.github.user()
    
    # Or with parameters:
    response = await client.weather_unified.weather(q="London")
```

## Features

- ✅ Async/await support
- ✅ Automatic retries (exponential backoff)
- ✅ Type hints throughout
- ✅ Context manager support
- ✅ Typed connector access
- ✅ Error handling

## API Reference

### ApiBridgeClient

**Constructor:**
```python
client = ApiBridgeClient(
    base_url="https://api.example.com",
    api_key="optional_api_key",
    timeout=30.0,
    max_retries=3
)
```

**Methods:**

- `async proxy(connector, path, method="GET", params=None, json=None, headers=None)` - Make proxied request
- `async health()` - Check system health
- `async metrics()` - Get Prometheus metrics
- `async admin_stats()` - Get admin statistics
- `async close()` - Close HTTP client

## Examples

### Weather API

```python
async with ApiBridgeClient("http://localhost:8000") as client:
    weather = await client.proxy(
        "weather_unified",
        "/weather",
        params={"q": "Tokyo"}
    )
    data = weather.json()
    print(f"Temperature in Tokyo: {data['temp_c']}°C")
```

### GitHub API

```python
async with ApiBridgeClient(
    "http://localhost:8000",
    api_key="your_api_key"
) as client:
    user = await client.proxy("github", "/user")
    data = user.json()
    print(f"GitHub user: {data['login']}")
```

### POST Request

```python
async with ApiBridgeClient("http://localhost:8000") as client:
    response = await client.proxy(
        "slack",
        "/chat.postMessage",
        method="POST",
        json={
            "channel": "general",
            "text": "Hello from ApiBridge!"
        }
    )
```

## Synchronous Usage

If you can't use async/await:

```python
from apibridge_client import ApiBridgeClientSync

with ApiBridgeClientSync("http://localhost:8000") as client:
    health = client.health()
    print(f"OK: {health['ok']}")
    
    weather = client.proxy("weather_unified", "/weather", params={"q": "London"})
    print(weather.json())
```

## Error Handling

```python
try:
    response = await client.proxy("github", "/user")
    response.raise_for_status()  # Raise on 4xx/5xx
    data = response.json()
except httpx.HTTPStatusError as e:
    print(f"HTTP error: {e.response.status_code}")
except httpx.TimeoutException:
    print("Request timed out")
except Exception as e:
    print(f"Error: {e}")
```

## License

MIT

