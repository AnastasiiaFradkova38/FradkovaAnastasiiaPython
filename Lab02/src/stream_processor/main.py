from itertools import chain, count, islice, pairwise
from pathlib import Path
from stream_processor.analytics import calculate_statistics, find_account_by_number
from stream_processor.batches import batched
from stream_processor.benchmark import (
    run_early_termination_benchmark,
    run_eager_lazy_benchmark,
)
from stream_processor.iterators import AccountNumberRange
from stream_processor.pipeline import build_pipeline
from stream_processor.readers import generate_test_csv


def main() -> None:
    data_dir = Path("data")
    sample_file = data_dir / "accounts_100k.csv"

    if not sample_file.exists():
        print("Generating 100,000 records dataset...")
        generate_test_csv(sample_file, 100_000)

    custom_range = AccountNumberRange(100, 105)
    print("Custom iterator (pass 1):", list(custom_range))
    print("Custom iterator (pass 2):", list(custom_range))

    infinite_ids = count(start=1000, step=10)
    print("Infinite stream (first 5 via islice):", list(islice(infinite_ids, 5)))

    pipeline = build_pipeline(sample_file, min_balance=15000.0)
    first_five = list(islice(pipeline, 5))
    print("\nFirst 5 accounts with balance >= 15000:")
    for acc in first_five:
        print(f"  ID: {acc.number:6} | Client: {acc.client_name:8} | Balance: {acc.balance:10.2f}")

    diffs = [round(curr.balance - prev.balance, 2) for prev, curr in pairwise(first_five)]
    print("Pairwise balance differences:", diffs)

    val_stats: dict[str, int] = {}
    full_pipeline = build_pipeline(sample_file, validation_stats=val_stats)
    stats = calculate_statistics(full_pipeline)
    print("\nStreaming statistics (100,000 records):")
    print(f"  Valid / Invalid records: {val_stats.get('valid', 0)} / {val_stats.get('invalid', 0)}")
    print(f"  Total balance:   {stats['total_balance']:,.2f}")
    print(f"  Average balance: {stats['average_balance']:,.2f}")
    print(f"  Min / Max:       {stats['min_balance']:.2f} / {stats['max_balance']:.2f}")

    alice_pipeline = build_pipeline(sample_file, client_name="Alice")
    alice_total = sum(acc.balance for acc in alice_pipeline)
    print(f"\nTotal balance for client 'Alice' (generator expression): {alice_total:,.2f}")

    found = find_account_by_number(build_pipeline(sample_file), target_number=777)
    print(f"Search account #777: {found}")

    batch_pipeline = build_pipeline(sample_file, min_balance=18000.0)
    batch_count = sum(1 for _ in batched(batch_pipeline, batch_size=500))
    print(f"Processed batches (size 500) for balance >= 18000: {batch_count}")

    combined = chain(
        islice(build_pipeline(sample_file, client_name="Alice"), 2),
        islice(build_pipeline(sample_file, client_name="Bob"), 2),
    )
    print("Combined stream (chain):", [(a.number, a.client_name) for a in combined])

    run_eager_lazy_benchmark(data_dir)
    run_early_termination_benchmark(data_dir)


if __name__ == "__main__":
    main()