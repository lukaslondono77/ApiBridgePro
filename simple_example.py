"""
Simple ApiBridge Pro Example

A minimal example showing the library's basic functionality.
"""

import asyncio
from apibridgepro import Gateway, BudgetGuard, load_config, build_connector_policies


async def simple_example():
    """Simple example of using ApiBridge Pro"""
    
    print("🚀 ApiBridge Pro - Simple Example\n")
    
    # Load config and create gateway
    config = load_config("connectors.yaml")
    policies = build_connector_policies(config)
    budget = BudgetGuard(redis_url=None)
    await budget.init()
    
    gateway = Gateway(policies, budget)
    
    print(f"✅ Gateway ready with {len(policies)} connectors!")
    print(f"📦 Available connectors: {', '.join(list(policies.keys())[:5])}...")
    print("\n💡 The gateway is ready to proxy requests to these APIs!")
    print("   Example: GET /proxy/coingecko/simple/price?ids=bitcoin")


if __name__ == "__main__":
    asyncio.run(simple_example())

