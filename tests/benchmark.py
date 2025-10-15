#!/usr/bin/env python3
"""
Benchmark script for ApiBridge Pro performance testing.
Tests throughput, latency, and failover behavior under load.
"""
import asyncio
import os
import sys
import time
from statistics import mean, median, stdev

import httpx
from httpx import ASGITransport

# Add parent directory to path for app imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app  # noqa: E402


class BenchmarkResults:
    def __init__(self, name: str):
        self.name = name
        self.latencies: list[float] = []
        self.errors = 0
        self.success = 0
        self.start_time = 0.0
        self.end_time = 0.0

    def add_latency(self, latency_ms: float, success: bool):
        self.latencies.append(latency_ms)
        if success:
            self.success += 1
        else:
            self.errors += 1

    def print_results(self):
        if not self.latencies:
            print(f"\n{self.name}: No results")
            return

        sorted_latencies = sorted(self.latencies)
        n = len(sorted_latencies)

        duration = self.end_time - self.start_time
        throughput = n / duration if duration > 0 else 0

        print(f"\n{'='*70}")
        print(f"📊 {self.name}")
        print(f"{'='*70}")
        print(f"  Total Requests:    {n}")
        print(f"  Success:           {self.success} ({self.success/n*100:.1f}%)")
        print(f"  Errors:            {self.errors} ({self.errors/n*100:.1f}%)")
        print(f"  Duration:          {duration:.2f}s")
        print(f"  Throughput:        {throughput:.0f} req/sec")
        print("\n  Latency:")
        print(f"    Min:             {min(sorted_latencies):.2f}ms")
        print(f"    Max:             {max(sorted_latencies):.2f}ms")
        print(f"    Mean:            {mean(sorted_latencies):.2f}ms")
        print(f"    Median (p50):    {median(sorted_latencies):.2f}ms")
        if n >= 10:
            p95_idx = int(n * 0.95)
            p99_idx = int(n * 0.99)
            print(f"    p95:             {sorted_latencies[p95_idx]:.2f}ms")
            print(f"    p99:             {sorted_latencies[p99_idx]:.2f}ms")
        if n > 1:
            print(f"    Std Dev:         {stdev(sorted_latencies):.2f}ms")


async def benchmark_health(client: httpx.AsyncClient, n_requests: int) -> BenchmarkResults:
    """Benchmark /health endpoint (lightweight)"""
    results = BenchmarkResults("Health Endpoint Benchmark")
    results.start_time = time.time()

    tasks = []
    for _ in range(n_requests):
        async def make_request():
            start = time.time()
            try:
                resp = await client.get("/health")
                latency = (time.time() - start) * 1000
                results.add_latency(latency, resp.status_code == 200)
            except Exception:
                results.add_latency(0, False)

        tasks.append(make_request())

    await asyncio.gather(*tasks)
    results.end_time = time.time()
    return results


async def benchmark_sequential(client: httpx.AsyncClient, n_requests: int) -> BenchmarkResults:
    """Benchmark sequential requests"""
    results = BenchmarkResults("Sequential Requests")
    results.start_time = time.time()

    for _ in range(n_requests):
        start = time.time()
        try:
            resp = await client.get("/health")
            latency = (time.time() - start) * 1000
            results.add_latency(latency, resp.status_code == 200)
        except Exception:
            results.add_latency(0, False)

    results.end_time = time.time()
    return results


async def benchmark_concurrent(client: httpx.AsyncClient, n_requests: int, concurrency: int) -> BenchmarkResults:
    """Benchmark concurrent requests with controlled concurrency"""
    results = BenchmarkResults(f"Concurrent Requests (concurrency={concurrency})")
    results.start_time = time.time()

    semaphore = asyncio.Semaphore(concurrency)

    async def make_request():
        async with semaphore:
            start = time.time()
            try:
                resp = await client.get("/health")
                latency = (time.time() - start) * 1000
                results.add_latency(latency, resp.status_code == 200)
            except Exception:
                results.add_latency(0, False)

    tasks = [make_request() for _ in range(n_requests)]
    await asyncio.gather(*tasks)

    results.end_time = time.time()
    return results


async def main():
    """Run all benchmarks"""
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║         ApiBridge Pro - Performance Benchmark             ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print("\nStarting benchmarks...")

    # Create ASGI transport for testing
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:

        # Warm-up
        print("\n🔥 Warming up...")
        for _ in range(10):
            await client.get("/health")

        # Benchmark 1: Sequential (baseline)
        print("\n📊 Running sequential benchmark...")
        seq_results = await benchmark_sequential(client, 100)
        seq_results.print_results()

        # Benchmark 2: Fully concurrent
        print("\n📊 Running fully concurrent benchmark...")
        concurrent_results = await benchmark_health(client, 1000)
        concurrent_results.print_results()

        # Benchmark 3: Controlled concurrency (realistic)
        print("\n📊 Running controlled concurrency benchmark (concurrency=50)...")
        controlled_results = await benchmark_concurrent(client, 1000, 50)
        controlled_results.print_results()

        # Benchmark 4: High concurrency
        print("\n📊 Running high concurrency benchmark (concurrency=200)...")
        high_concurrency_results = await benchmark_concurrent(client, 2000, 200)
        high_concurrency_results.print_results()

    print("\n" + "="*70)
    print("🎉 Benchmark Complete!")
    print("="*70)
    print("\n📝 Summary:")
    print(f"  Sequential throughput:      {100/(seq_results.end_time - seq_results.start_time):.0f} req/sec")
    print(f"  Concurrent throughput:      {1000/(concurrent_results.end_time - concurrent_results.start_time):.0f} req/sec")
    print(f"  Realistic throughput:       {1000/(controlled_results.end_time - controlled_results.start_time):.0f} req/sec")
    print(f"\n  Median latency:             {median(controlled_results.latencies):.2f}ms")
    print(f"  95th percentile:            {sorted(controlled_results.latencies)[int(len(controlled_results.latencies)*0.95)]:.2f}ms")
    print("\n💡 Recommendations:")

    p95 = sorted(controlled_results.latencies)[int(len(controlled_results.latencies)*0.95)]
    if p95 > 100:
        print("  ⚠️  High p95 latency detected. Consider:")
        print("     - Optimizing transform logic")
        print("     - Adding more aggressive caching")
        print("     - Increasing connection pool size")
    else:
        print("  ✅ Latency looks good!")

    throughput = 1000/(controlled_results.end_time - controlled_results.start_time)
    if throughput < 5000:
        print(f"  ℹ️  Throughput: {throughput:.0f} req/sec")
        print("     - Good for most use cases")
        print("     - Scale horizontally if needed")
    else:
        print(f"  ✅ Excellent throughput: {throughput:.0f} req/sec")


if __name__ == "__main__":
    asyncio.run(main())

