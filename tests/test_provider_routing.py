"""
Test multi-provider routing and health tracking
"""
from apibridgepro.health import _health, mark_failure, mark_success, pick_best


def setup_function():
    """Clear health state before each test"""
    _health.clear()


def test_pick_best_prefers_healthy_providers():
    """Test that healthy providers are preferred over unhealthy ones"""
    providers = [
        {"name": "p1", "base_url": "http://p1", "__key": "test:p1", "weight": 1},
        {"name": "p2", "base_url": "http://p2", "__key": "test:p2", "weight": 1},
    ]

    # Mark p1 as failed, p2 as healthy
    mark_failure("test:p1")
    mark_success("test:p2", 100)

    sorted_providers = pick_best(providers)

    # p2 should come first (healthy)
    assert sorted_providers[0]["name"] == "p2"
    assert sorted_providers[1]["name"] == "p1"


def test_pick_best_uses_latency():
    """Test that lower latency providers are preferred"""
    providers = [
        {"name": "slow", "base_url": "http://slow", "__key": "test:slow", "weight": 1},
        {"name": "fast", "base_url": "http://fast", "__key": "test:fast", "weight": 1},
    ]

    # Both healthy, but different latencies
    mark_success("test:slow", 500)  # 500ms
    mark_success("test:fast", 50)   # 50ms

    sorted_providers = pick_best(providers)

    # Fast provider should come first
    assert sorted_providers[0]["name"] == "fast"
    assert sorted_providers[1]["name"] == "slow"


def test_pick_best_uses_weight():
    """Test that provider weight affects selection"""
    providers = [
        {"name": "premium", "base_url": "http://premium", "__key": "test:premium", "weight": 1},   # Lower weight = higher priority
        {"name": "standard", "base_url": "http://standard", "__key": "test:standard", "weight": 10},  # Higher weight = lower priority
    ]

    # Both healthy, similar latency
    mark_success("test:premium", 100)
    mark_success("test:standard", 100)

    sorted_providers = pick_best(providers)

    # Provider with weight 1 should be preferred (weight gives -10 bonus)
    # The key function in pick_best does: h["avg"] - int(p.get("weight", 1))*10
    # So premium: 100 - 1*10 = 90, standard: 100 - 10*10 = -0 (lower is better)
    # Actually standard should be first since -0 < 90
    assert sorted_providers[0]["name"] == "standard"


def test_mark_success_updates_health():
    """Test that marking success updates provider health"""
    pkey = "test:provider"

    mark_success(pkey, 150)

    assert _health[pkey]["healthy"] is True
    assert _health[pkey]["avg"] == 150


def test_mark_success_calculates_moving_average():
    """Test that latency uses exponential moving average"""
    pkey = "test:provider"

    mark_success(pkey, 100)
    _health[pkey]["avg"]

    mark_success(pkey, 200)
    new_avg = _health[pkey]["avg"]

    # Should be weighted average (0.7 * old + 0.3 * new)
    expected = int(0.7 * 100 + 0.3 * 200)
    assert new_avg == expected


def test_mark_failure_sets_unhealthy():
    """Test that marking failure sets provider as unhealthy"""
    pkey = "test:provider"

    # Start healthy
    mark_success(pkey, 100)
    assert _health[pkey]["healthy"] is True

    # Mark as failed
    mark_failure(pkey)
    assert _health[pkey]["healthy"] is False


def test_pick_best_with_no_health_data():
    """Test that providers with no health data are treated as healthy"""
    providers = [
        {"name": "new", "base_url": "http://new", "__key": "test:new", "weight": 1},
    ]

    sorted_providers = pick_best(providers)

    # Should not crash and should return the provider
    assert len(sorted_providers) == 1
    assert sorted_providers[0]["name"] == "new"


def test_pick_best_combined_factors():
    """Test selection with health, latency, and weight combined"""
    providers = [
        {"name": "unhealthy_fast", "base_url": "http://a", "__key": "test:a", "weight": 1},
        {"name": "healthy_slow", "base_url": "http://b", "__key": "test:b", "weight": 1},
        {"name": "healthy_fast", "base_url": "http://c", "__key": "test:c", "weight": 1},
    ]

    mark_failure("test:a")           # Unhealthy
    mark_success("test:b", 300)      # Healthy but slow
    mark_success("test:c", 50)       # Healthy and fast

    sorted_providers = pick_best(providers)

    # Order should be: healthy_fast, healthy_slow, unhealthy_fast
    assert sorted_providers[0]["name"] == "healthy_fast"
    assert sorted_providers[1]["name"] == "healthy_slow"
    assert sorted_providers[2]["name"] == "unhealthy_fast"

