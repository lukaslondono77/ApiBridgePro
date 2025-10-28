"""
Test budget tracking (in-memory and Redis fallback)
"""

import pytest

from apibridgepro.budget import BudgetGuard


@pytest.mark.asyncio
async def test_budget_in_memory_tracking():
    """Test budget tracking without Redis (in-memory fallback)"""
    guard = BudgetGuard(redis_url=None)
    await guard.init()

    # Add costs
    await guard.add_cost("test_connector", 0.5, "2025-01")
    await guard.add_cost("test_connector", 0.3, "2025-01")
    await guard.add_cost("test_connector", 0.2, "2025-01")

    # Check total
    total = await guard.get_cost("test_connector", "2025-01")
    assert abs(total - 1.0) < 0.001  # Allow small floating point error


@pytest.mark.asyncio
async def test_budget_different_months():
    """Test that budget tracking is per-month"""
    guard = BudgetGuard(redis_url=None)
    await guard.init()

    # Use unique connector name to avoid pollution from other tests
    await guard.add_cost("test_connector_months", 1.0, "2025-01")
    await guard.add_cost("test_connector_months", 2.0, "2025-02")

    jan_cost = await guard.get_cost("test_connector_months", "2025-01")
    feb_cost = await guard.get_cost("test_connector_months", "2025-02")

    assert abs(jan_cost - 1.0) < 0.001
    assert abs(feb_cost - 2.0) < 0.001


@pytest.mark.asyncio
async def test_budget_different_connectors():
    """Test that budget tracking is per-connector"""
    guard = BudgetGuard(redis_url=None)
    await guard.init()

    await guard.add_cost("connector_a", 5.0, "2025-01")
    await guard.add_cost("connector_b", 10.0, "2025-01")

    cost_a = await guard.get_cost("connector_a", "2025-01")
    cost_b = await guard.get_cost("connector_b", "2025-01")

    assert abs(cost_a - 5.0) < 0.001
    assert abs(cost_b - 10.0) < 0.001


@pytest.mark.asyncio
async def test_budget_zero_cost():
    """Test that zero cost is handled correctly"""
    guard = BudgetGuard(redis_url=None)
    await guard.init()

    cost = await guard.get_cost("nonexistent", "2025-01")
    assert cost == 0.0


@pytest.mark.asyncio
async def test_budget_incremental_adds():
    """Test that costs accumulate correctly"""
    guard = BudgetGuard(redis_url=None)
    await guard.init()

    # Simulate 100 micro-transactions
    for _i in range(100):
        await guard.add_cost("api", 0.001, "2025-01")

    total = await guard.get_cost("api", "2025-01")
    assert abs(total - 0.1) < 0.001


@pytest.mark.asyncio
async def test_budget_with_invalid_redis():
    """Test graceful fallback when Redis is unavailable"""
    guard = BudgetGuard(redis_url="redis://invalid:9999/0")
    await guard.init()

    # Should fall back to in-memory without errors
    await guard.add_cost("test", 1.0, "2025-01")
    cost = await guard.get_cost("test", "2025-01")
    assert abs(cost - 1.0) < 0.001

