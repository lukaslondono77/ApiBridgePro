"""
Integration test for proxy endpoint with mocked upstream
"""

import pytest
import respx
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient, Response

from app.main import app, shutdown, startup


@pytest.fixture
async def test_app():
    """Initialize app with lifespan"""
    await startup()
    yield app
    await shutdown()


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.mark.asyncio
@respx.mock
async def test_weather_unified_with_mocked_upstream(test_app):
    """Test weather_unified connector with mocked providers"""
    # Mock OpenWeatherMap response
    respx.get("https://api.openweathermap.org/data/2.5/weather").mock(
        return_value=Response(200, json={
            "main": {
                "temp": 298.15,  # 25°C in Kelvin
                "humidity": 65
            },
            "name": "Bogota"
        })
    )

    # Mock WeatherAPI response
    respx.get("https://api.weatherapi.com/v1/current.json").mock(
        return_value=Response(200, json={
            "current": {
                "temp_c": 25.0,
                "humidity": 65
            },
            "location": {
                "name": "Bogota"
            }
        })
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/proxy/weather_unified/weather?q=Bogota")

    assert response.status_code == 200
    data = response.json()

    # Should have unified schema
    assert "temp_c" in data
    assert "humidity" in data
    assert "provider" in data
    assert abs(data["temp_c"] - 25.0) < 1.0  # Close to 25°C


@pytest.mark.asyncio
@respx.mock
async def test_github_proxy_with_mock(test_app):
    """Test GitHub proxy with mocked response"""
    respx.get("https://api.github.com/user").mock(
        return_value=Response(200, json={
            "login": "testuser",
            "id": 12345,
            "name": "Test User"
        })
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/proxy/github/user")

    assert response.status_code == 200
    data = response.json()
    assert data["login"] == "testuser"


@pytest.mark.asyncio
@respx.mock
async def test_provider_failover(test_app):
    """Test that failover works when primary provider fails"""
    # First provider (openweather) returns 500
    respx.get("https://api.openweathermap.org/data/2.5/weather").mock(
        return_value=Response(500, json={"error": "Internal Server Error"})
    )

    # Second provider (weatherapi) succeeds
    respx.get("https://api.weatherapi.com/v1/current.json").mock(
        return_value=Response(200, json={
            "current": {
                "temp_c": 25.0,
                "humidity": 60
            },
            "location": {
                "name": "Bogota"
            }
        })
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/proxy/weather_unified/current.json?q=Bogota")

    # Should succeed with fallback provider
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "weatherapi"


@pytest.mark.asyncio
@respx.mock
async def test_all_providers_fail(test_app):
    """Test behavior when all providers fail"""
    # Both providers fail
    respx.get("https://api.openweathermap.org/data/2.5/weather").mock(
        return_value=Response(503, json={"error": "Service Unavailable"})
    )
    respx.get("https://api.weatherapi.com/v1/current.json").mock(
        return_value=Response(503, json={"error": "Service Unavailable"})
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/proxy/weather_unified/weather?q=Bogota")

    # Should return 502 Bad Gateway
    assert response.status_code == 502
    data = response.json()
    assert "detail" in data
    assert "error" in data["detail"].lower()


@pytest.mark.asyncio
async def test_health_endpoint(test_app):
    """Test health endpoint returns correct info"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert "mode" in data
    assert "connectors" in data
    assert isinstance(data["connectors"], list)
    assert "weather_unified" in data["connectors"]


@pytest.mark.asyncio
@respx.mock
async def test_caching_behavior(test_app):
    """Test that GET requests are cached"""
    # Mock response
    call_count = 0

    def mock_handler(request):
        nonlocal call_count
        call_count += 1
        return Response(200, json={"value": call_count})

    respx.get("https://api.github.com/user").mock(side_effect=mock_handler)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # First request
        response1 = await ac.get("/proxy/github/user")
        data1 = response1.json()

        # Second request (should be cached)
        response2 = await ac.get("/proxy/github/user")
        data2 = response2.json()

    # Both should return the same data (cached)
    assert data1 == data2
    assert call_count == 1  # Only called once


@pytest.mark.asyncio
@respx.mock
async def test_rate_limiting(test_app):
    """Test that rate limiting is enforced"""
    # Mock a simple endpoint
    respx.get("https://api.github.com/user").mock(
        return_value=Response(200, json={"login": "test"})
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Make requests up to rate limit
        # GitHub connector has default capacity of 10
        responses = []
        for _i in range(15):
            resp = await ac.get("/proxy/github/user")
            responses.append(resp.status_code)

        # Some requests should be rate limited (429)
        assert 429 in responses


@pytest.mark.asyncio
async def test_unknown_connector_returns_404(test_app):
    """Test that unknown connector returns 404"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/proxy/nonexistent/path")

    assert response.status_code == 404
    data = response.json()
    assert "connector" in data["detail"].lower()


@pytest.mark.asyncio
@respx.mock
async def test_disallowed_path_returns_403(test_app):
    """Test that disallowed paths return 403"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # GitHub connector only allows specific paths
        response = await ac.get("/proxy/github/admin/secret")

    assert response.status_code == 403
    data = response.json()
    assert "not allowed" in data["detail"].lower()

