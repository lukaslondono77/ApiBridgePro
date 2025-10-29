#!/usr/bin/env python3
"""
Simple example showing how to use ApiBridge Pro
"""
import asyncio

from apibridgepro import Gateway, BudgetGuard, build_connector_policies, load_config

async def main():
    print("🚀 ApiBridge Pro - Simple Example")
    print("=" * 60)
    print()
    
    try:
        # 1. Load configuration
        print("📄 Step 1: Loading connectors configuration...")
        config = load_config("connectors.yaml")
        print(f"   ✅ Loaded {len(config.get('connectors', {}))} connectors")
        print()
        
        # 2. Build connector policies
        print("🔧 Step 2: Building connector policies...")
        policies = build_connector_policies(config)
        print(f"   ✅ Created {len(policies)} policy/policies")
        print(f"   Available: {list(policies.keys())}")
        print()
        
        # 3. Create budget guard
        print("💰 Step 3: Creating budget guard (in-memory)...")
        budget = BudgetGuard(redis_url=None)
        await budget.init()
        print("   ✅ Budget guard ready")
        print()
        
        # 4. Create gateway
        print("🌐 Step 4: Creating gateway...")
        gateway = Gateway(policies, budget)
        print("   ✅ Gateway initialized")
        print()
        
        print("=" * 60)
        print("🎉 Gateway is ready to use!")
        print("=" * 60)
        print()
        print("💡 To use the gateway:")
        print("   1. Start the server: apibridge")
        print("   2. Or use programmatically via gateway.proxy()")
        print()
        
    except FileNotFoundError:
        print("⚠️  connectors.yaml not found in current directory")
        print("   The gateway can still be created, but needs configuration")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

