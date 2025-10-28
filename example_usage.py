"""
ApiBridge Pro - Library Usage Example

This script demonstrates how to use ApiBridge Pro as a Python library.
"""

import asyncio
from apibridgepro import (
    Gateway,
    BudgetGuard,
    load_config,
    build_connector_policies,
    get_metrics,
)


async def main():
    """Main example function"""
    
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║         ApiBridge Pro - Library Usage Example                    ║")
    print("╚═══════════════════════════════════════════════════════════════════╝\n")
    
    # Step 1: Load configuration
    print("📋 Step 1: Loading configuration...")
    try:
        config = load_config("connectors.yaml")
        print(f"   ✅ Loaded {len(config)} connectors from connectors.yaml")
        
        # Show available connectors
        print(f"   📦 Available connectors:")
        for name in config.keys():
            print(f"      - {name}")
        print()
    except FileNotFoundError:
        print("   ❌ Error: connectors.yaml not found!")
        print("   💡 Make sure connectors.yaml exists in the current directory")
        return
    except Exception as e:
        print(f"   ❌ Error loading config: {e}")
        return
    
    # Step 2: Build connector policies
    print("🔧 Step 2: Building connector policies...")
    try:
        policies = build_connector_policies(config)
        print(f"   ✅ Built {len(policies)} connector policies")
        print()
    except Exception as e:
        print(f"   ❌ Error building policies: {e}")
        return
    
    # Step 3: Initialize budget guard
    print("💰 Step 3: Initializing budget guard...")
    try:
        budget = BudgetGuard(redis_url=None)  # Use in-memory storage
        await budget.init()
        print("   ✅ Budget guard initialized (in-memory mode)")
        print()
    except Exception as e:
        print(f"   ❌ Error initializing budget: {e}")
        return
    
    # Step 4: Create gateway instance
    print("🚀 Step 4: Creating gateway instance...")
    try:
        gateway = Gateway(policies, budget)
        print("   ✅ Gateway created successfully!")
        print()
    except Exception as e:
        print(f"   ❌ Error creating gateway: {e}")
        return
    
    # Step 5: Check metrics
    print("📊 Step 5: Checking metrics...")
    try:
        metrics = get_metrics()
        print(f"   ✅ Metrics available: {len(metrics)} metric types")
        print(f"   📈 Sample metrics:")
        for metric_name in list(metrics.keys())[:5]:
            print(f"      - {metric_name}")
        print()
    except Exception as e:
        print(f"   ⚠️  Metrics check skipped: {e}")
        print()
    
    # Step 6: Show gateway info
    print("ℹ️  Gateway Information:")
    print(f"   - Version: 0.1.0")
    print(f"   - Connectors: {len(policies)}")
    print(f"   - Budget Guard: {'✅ Active' if budget else '❌ Inactive'}")
    print()
    
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                         ✅ SUCCESS!                               ║")
    print("╚═══════════════════════════════════════════════════════════════════╝\n")
    
    print("💡 Next steps:")
    print("   - Use the gateway in your FastAPI app:")
    print("     from app import app")
    print("     uvicorn.run(app, host='0.0.0.0', port=8000)")
    print()
    print("   - Or use components individually:")
    print("     from app import Gateway, BudgetGuard, build_connector_policies")
    print()


if __name__ == "__main__":
    asyncio.run(main())

