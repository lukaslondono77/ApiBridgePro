#!/usr/bin/env python3
"""
ApiBridge Pro - Python Example: Weather API
Demonstrates multi-provider weather API with failover.
"""
import asyncio
import sys
import os

# Add SDK to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../sdk/python'))
from apibridge_client import ApiBridgeClient


async def get_weather(city: str):
    """Get weather for a city using ApiBridge Pro"""
    async with ApiBridgeClient("http://localhost:8000") as client:
        # Check system health first
        health = await client.health()
        print(f"✅ ApiBridge is {'healthy' if health['ok'] else 'unhealthy'}")
        print(f"   Available connectors: {', '.join(health['connectors'])}\n")
        
        # Get weather
        print(f"🌤️  Fetching weather for {city}...")
        try:
            response = await client.proxy(
                "weather_unified",
                "/weather",
                params={"q": city}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n📊 Weather in {city}:")
                print(f"   Temperature: {data.get('temp_c', 'N/A')}°C")
                print(f"   Humidity: {data.get('humidity', 'N/A')}%")
                print(f"   Provider: {data.get('provider', 'N/A')}")
                
                # Check headers for additional info
                print(f"\n🔍 Request Details:")
                print(f"   Provider used: {response.headers.get('X-ApiBridge-Provider', 'N/A')}")
                print(f"   Latency: {response.headers.get('X-ApiBridge-Latency-Ms', 'N/A')}ms")
                print(f"   Cache: {response.headers.get('X-ApiBridge-Cache', 'N/A')}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"   {response.text}")
        
        except Exception as e:
            print(f"❌ Request failed: {e}")


async def compare_multiple_cities():
    """Compare weather across multiple cities"""
    cities = ["London", "Tokyo", "New York", "Sydney"]
    
    async with ApiBridgeClient("http://localhost:8000") as client:
        print("🌍 Comparing weather across global cities\n")
        
        for city in cities:
            try:
                response = await client.proxy(
                    "weather_unified",
                    "/weather",
                    params={"q": city}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"{city:15} {data.get('temp_c', 'N/A'):>6}°C  "
                          f"{data.get('humidity', 'N/A'):>3}%  "
                          f"({data.get('provider', 'N/A')})")
            except Exception as e:
                print(f"{city:15} Error: {e}")


async def demonstrate_caching():
    """Demonstrate caching performance benefit"""
    async with ApiBridgeClient("http://localhost:8000") as client:
        import time
        
        print("⚡ Demonstrating cache performance\n")
        
        # First request (cache miss)
        start = time.time()
        response1 = await client.proxy("weather_unified", "/weather", params={"q": "Paris"})
        first_duration = (time.time() - start) * 1000
        
        # Second request (cache hit)
        start = time.time()
        response2 = await client.proxy("weather_unified", "/weather", params={"q": "Paris"})
        second_duration = (time.time() - start) * 1000
        
        print(f"First request:  {first_duration:.2f}ms (cache {response1.headers.get('X-ApiBridge-Cache', 'miss')})")
        print(f"Second request: {second_duration:.2f}ms (cache {response2.headers.get('X-ApiBridge-Cache', 'miss')})")
        print(f"\nSpeedup: {first_duration / second_duration:.1f}x faster!")
        print(f"Cost savings: {100 * (1 - 1/(first_duration/second_duration if second_duration else 1)):.0f}% reduction")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ApiBridge Pro Weather Example")
    parser.add_argument("--city", default="London", help="City name")
    parser.add_argument("--compare", action="store_true", help="Compare multiple cities")
    parser.add_argument("--cache-demo", action="store_true", help="Demonstrate caching")
    
    args = parser.parse_args()
    
    if args.compare:
        asyncio.run(compare_multiple_cities())
    elif args.cache_demo:
        asyncio.run(demonstrate_caching())
    else:
        asyncio.run(get_weather(args.city))

