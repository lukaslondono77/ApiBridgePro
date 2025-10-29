"""
Simple test to verify apibridge-pro installation works
"""
from apibridgepro import Gateway, BudgetGuard, ConnectorPolicy, app

print("=" * 60)
print("ApiBridge Pro - Installation Test")
print("=" * 60)
print()

# Test imports
print("✅ Successfully imported:")
print(f"   - Gateway: {Gateway}")
print(f"   - BudgetGuard: {BudgetGuard}")
print(f"   - ConnectorPolicy: {ConnectorPolicy}")
print(f"   - FastAPI app: {app}")
print()

# Check app info
print("📦 FastAPI App Info:")
print(f"   - Title: {app.title}")
print(f"   - Version: {app.version}")
print(f"   - Description: {app.description[:50]}...")
print()

# Test basic functionality
print("🧪 Testing basic functionality:")
try:
    # Try to create a BudgetGuard instance
    budget = BudgetGuard(redis_url=None)  # In-memory mode
    print("   ✅ BudgetGuard can be instantiated")
    
    # Check Gateway class
    print(f"   ✅ Gateway class available: {Gateway.__name__}")
    
    print()
    print("=" * 60)
    print("🎉 All tests passed! Package is working correctly.")
    print("=" * 60)
    print()
    print("💡 Next steps:")
    print("   - Configure connectors.yaml")
    print("   - Set up API keys in environment variables")
    print("   - Run: apibridge")
    print()
except Exception as e:
    print(f"   ❌ Error: {e}")
    raise

