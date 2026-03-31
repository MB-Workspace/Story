"""
Performance Benchmark Script for Project Vajra

Validates processing speed claims from BENCHMARKS.md.
Run with: python -m tests.benchmark
"""
import time
import statistics
from project_vajra.core import VajraSystem


def generate_test_data(num_wallets: int) -> dict:
    """Generate synthetic case data with specified number of wallets.

    Creates wallets with realistic transaction patterns and
    interconnected relationships for benchmarking.
    """
    evidence = []
    for i in range(num_wallets):
        wallet = {
            "source": f"wallet_{i:04d}",
            "type": "crypto_wallet",
            "transactions": [
                f"deposit_{i}",
                f"withdraw_{i + 1}",
                f"transfer_{i + 2}",
            ],
            "behavior": ["fee_evasion", "micro_transactions"]
            if i % 3 == 0
            else ["time_delayed"],
            "related_to": [
                f"wallet_{(i + 1) % num_wallets:04d}",
                f"wallet_{(i + 2) % num_wallets:04d}",
            ],
        }
        evidence.append(wallet)

    return {
        "case_id": f"BENCH-{num_wallets}-WALLETS",
        "evidence": evidence,
    }


def run_benchmark(sizes: list[int] | None = None, iterations: int = 3) -> None:
    """Run benchmark across multiple case sizes.

    Args:
        sizes: List of wallet counts to test.
        iterations: Number of iterations per size for averaging.
    """
    if sizes is None:
        sizes = [100, 500, 1000, 5000]

    print("=" * 70)
    print("PROJECT VAJRA - PERFORMANCE BENCHMARK")
    print("=" * 70)
    print(f"{'Wallets':>8} | {'Avg Time':>10} | {'Min':>8} | {'Max':>8} | {'TPS':>8}")
    print("-" * 70)

    for size in sizes:
        data = generate_test_data(size)
        times = []

        for _ in range(iterations):
            start = time.perf_counter()
            VajraSystem(data).solve_case()
            duration = time.perf_counter() - start
            times.append(duration)

        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        tps = size / avg_time

        print(f"{size:>8} | {avg_time:>9.3f}s | {min_time:>7.3f}s | {max_time:>7.3f}s | {tps:>7.1f}")

    print("=" * 70)


if __name__ == "__main__":
    run_benchmark()
