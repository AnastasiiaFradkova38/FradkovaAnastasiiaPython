import csv
import time
import tracemalloc
from pathlib import Path
from stream_processor.analytics import find_account_by_number
from stream_processor.pipeline import build_pipeline
from stream_processor.readers import generate_test_csv


def read_eager(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def run_eager_lazy_benchmark(data_dir: Path) -> None:
    print("\n" + "=" * 25 + " EAGER VS LAZY BENCHMARK " + "=" * 25)
    print(
        f"{'Records':>10} | {'Eager time':>11} | {'Lazy time':>11} | "
        f"{'Eager peak':>12} | {'Lazy peak':>12} | {'Lazy TTFR':>11}"
    )
    print("-" * 82)

    for size in (10_000, 100_000, 500_000):
        file_path = data_dir / f"bench_{size}.csv"
        if not file_path.exists():
            generate_test_csv(file_path, size)

        tracemalloc.start()
        start = time.perf_counter()
        rows = read_eager(file_path)
        _ = len(rows)
        eager_time = time.perf_counter() - start
        _, eager_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tracemalloc.start()
        start = time.perf_counter()
        pipeline = build_pipeline(file_path)
        first_item = next(pipeline, None)
        ttfr = time.perf_counter() - start
        count = 1 if first_item is not None else 0
        for _ in pipeline:
            count += 1
        lazy_time = time.perf_counter() - start
        _, lazy_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(
            f"{size:>10} | {eager_time:>9.4f} s | {lazy_time:>9.4f} s | "
            f"{eager_peak / (1024 * 1024):>9.2f} MB | "
            f"{lazy_peak / (1024 * 1024):>9.2f} MB | {ttfr:>9.6f} s"
        )


def run_early_termination_benchmark(data_dir: Path) -> None:
    print("\n" + "=" * 18 + " EARLY TERMINATION (1,000,000 records) " + "=" * 18)
    file_path = data_dir / "bench_1000000.csv"
    if not file_path.exists():
        print("Generating 1,000,000 records CSV (one-time)...")
        generate_test_csv(file_path, 1_000_000)

    target_id = 42

    start = time.perf_counter()
    found_lazy = find_account_by_number(build_pipeline(file_path), target_id)
    lazy_time = time.perf_counter() - start

    start = time.perf_counter()
    all_accounts = list(build_pipeline(file_path))
    found_eager = find_account_by_number(all_accounts, target_id)
    eager_time = time.perf_counter() - start

    assert found_lazy == found_eager
    print(f"Found account: {found_lazy}")
    print(f"Lazy search (early termination): {lazy_time:.6f} s")
    print(f"Eager search (full materialization): {eager_time:.6f} s")