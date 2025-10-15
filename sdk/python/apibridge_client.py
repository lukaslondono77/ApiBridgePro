"""
ApiBridge Pro - Official Python Client SDK

Install:
    pip install httpx

Usage:
    from apibridge_client import ApiBridgeClient
    
    async with ApiBridgeClient("https://api.example.com") as client:
        # Get weather
        response = await client.weather_unified.weather(q="London")
        print(response)
        
        # Or use generic proxy
        response = await client.proxy("github", "/user")
        print(response.json())
"""
from typing import Optional, Dict, Any, Union
import httpx
from urllib.parse import urljoin


class ConnectorProxy:
    """Dynamic proxy for a specific connector"""
    def __init__(self, client: 'ApiBridgeClient', connector: str):
        self._client = client
        self._connector = connector
    
    async def request(
        self,
        path: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        json: Optional[Dict] = None,
        **kwargs
    ) -> httpx.Response:
        """Make request to connector"""
        return await self._client.proxy(
            self._connector,
            path,
            method=method,
            params=params,
            json=json,
            **kwargs
        )
    
    def __getattr__(self, path: str):
        """Allow connector.path() syntax"""
        async def method(**kwargs):
            # Determine HTTP method from kwargs
            http_method = kwargs.pop('method', 'GET')
            json_body = kwargs.pop('json', None)
            params = kwargs
            
            return await self.request(f"/{path}", method=http_method, params=params, json=json_body)
        return method


class ApiBridgeClient:
    """
    Official Python client for ApiBridge Pro.
    
    Features:
        - Async/await support
        - Type hints
        - Automatic retries
        - Request/response logging
        - Typed connector access
    
    Example:
        async with ApiBridgeClient("https://api.example.com") as client:
            # Option 1: Generic proxy
            response = await client.proxy("weather_unified", "/weather", params={"q": "London"})
            data = response.json()
            
            # Option 2: Typed connector access
            data = await client.weather_unified.weather(q="London")
            
            # Check health
            health = await client.health()
            print(f"OK: {health['ok']}")
    """
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3
    ):
        """
        Initialize ApiBridge client.
        
        Args:
            base_url: ApiBridge instance URL (e.g., "https://api.example.com")
            api_key: Optional API key for authentication
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries on failure
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            timeout=timeout,
            transport=httpx.AsyncHTTPTransport(retries=max_retries)
        )
        self._connectors: Dict[str, ConnectorProxy] = {}
    
    def __getattr__(self, connector: str) -> ConnectorProxy:
        """
        Get connector proxy for typed access.
        
        Example:
            client.weather_unified.weather(q="London")
        """
        if connector not in self._connectors:
            self._connectors[connector] = ConnectorProxy(self, connector)
        return self._connectors[connector]
    
    async def proxy(
        self,
        connector: str,
        path: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        json: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> httpx.Response:
        """
        Make request through ApiBridge connector.
        
        Args:
            connector: Connector name (e.g., "weather_unified")
            path: API path (e.g., "/weather")
            method: HTTP method
            params: Query parameters
            json: JSON body for POST/PUT
            headers: Additional headers
        
        Returns:
            httpx.Response object
        
        Example:
            response = await client.proxy(
                "weather_unified",
                "/weather",
                params={"q": "London"}
            )
            data = response.json()
        """
        url = f"{self.base_url}/proxy/{connector}/{path.lstrip('/')}"
        
        # Build headers
        req_headers = headers or {}
        if self.api_key:
            req_headers['Authorization'] = f"Bearer {self.api_key}"
        
        return await self.client.request(
            method=method,
            url=url,
            params=params,
            json=json,
            headers=req_headers,
            **kwargs
        )
    
    async def health(self) -> Dict[str, Any]:
        """
        Check ApiBridge health.
        
        Returns:
            Dict with keys: ok, mode, connectors
        """
        response = await self.client.get(f"{self.base_url}/health")
        return response.json()
    
    async def metrics(self) -> str:
        """
        Get Prometheus metrics.
        
        Returns:
            Prometheus-formatted metrics string
        """
        response = await self.client.get(f"{self.base_url}/metrics")
        return response.text
    
    async def admin_stats(self) -> Dict[str, Any]:
        """Get admin dashboard statistics"""
        response = await self.client.get(f"{self.base_url}/admin/health-json")
        return response.json()
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# Synchronous wrapper for non-async code
class ApiBridgeClientSync:
    """Synchronous wrapper around async client"""
    
    def __init__(self, *args, **kwargs):
        import asyncio
        self._client = ApiBridgeClient(*args, **kwargs)
        self._loop = asyncio.new_event_loop()
    
    def proxy(self, *args, **kwargs) -> httpx.Response:
        return self._loop.run_until_complete(
            self._client.proxy(*args, **kwargs)
        )
    
    def health(self) -> Dict[str, Any]:
        return self._loop.run_until_complete(self._client.health())
    
    def close(self):
        self._loop.run_until_complete(self._client.close())
        self._loop.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Async usage
        async with ApiBridgeClient("http://localhost:8000") as client:
            # Check health
            health = await client.health()
            print(f"System healthy: {health['ok']}")
            print(f"Connectors: {health['connectors']}")
            
            # Use typed access
            try:
                weather = await client.weather_unified.weather(q="London")
                print(f"Weather: {weather}")
            except Exception as e:
                print(f"Weather API error: {e}")
    
    asyncio.run(main())

