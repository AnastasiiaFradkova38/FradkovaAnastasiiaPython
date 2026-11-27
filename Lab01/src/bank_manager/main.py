import time
from bank_manager.models import Account
from data_processor.data import accounts
from data_processor.processors import (
    get_unique_account_types,
    create_account_index,
    group_accounts_by_type,
    get_account_type_statistics,
)
from data_processor.analytics import (
    calculate_total_sum,
    find_max_balance_account,
    sort_accounts_by_balance,
    create_min_balance_filter,
    calculate_average_balance_args,
    create_account_record,
    filter_items,
)


def print_accounts(title: str, items: list[Account]) -> None:
    print(f"\n{title}")
    print("-" * 65)
    for acc in items:
        print(
            f" ID: {acc.number:2} | Name: {acc.client_name:8} | "
            f"Type: {acc.account_type:8} | Balance: {acc.balance:8.2f}"
        )


def run_benchmark() -> None:
    print("\n" + "=" * 20 + " BENCHMARK (list vs dict) " + "=" * 20)
    sizes: tuple[int, ...] = (1_000, 10_000, 100_000)

    print(f"{'Records':>10} | {'list search O(n)':>18} | {'dict search O(1)':>18}")
    print("-" * 52)

    for size in sizes:
        large_accounts = [
            Account(
                number=i,
                client_name=f"Client_{i}",
                balance=100.0,
                account_type="current",
            )
            for i in range(size)
        ]
        target_id = size - 1

        start_time = time.perf_counter()
        found_linear = None
        for acc in large_accounts:
            if acc.number == target_id:
                found_linear = acc
                break
        linear_time = time.perf_counter() - start_time

        index = create_account_index(large_accounts)
        start_time = time.perf_counter()
        found_dict = index.get(target_id)
        dict_time = time.perf_counter() - start_time

        assert found_linear == found_dict
        print(f"{size:>10} | {linear_time:>14.6f} sec | {dict_time:>14.6f} sec")

    print(
        "\nConclusion: Search via dict-index is significantly faster "
        "and remains almost constant as data grows."
    )


def main() -> None:
    print_accounts("All accounts", accounts)

    unique_types = get_unique_account_types(accounts)
    print(f"\nUnique account types (Set): {unique_types}")

    grouped = group_accounts_by_type(accounts)
    print("\nGrouped accounts by type (defaultdict):")
    for acc_type, group_members in grouped.items():
        print(f" {acc_type} -> {len(group_members)} accounts")

    print("\nAnalytics and Aggregation:")
    total_sum = calculate_total_sum(accounts)
    print(f" Total sum (call wrapped by decorator): {total_sum:.2f}")

    avg_balance = calculate_average_balance_args(*(acc.balance for acc in accounts))
    print(f" Average balance of all accounts: {avg_balance:.2f}")

    best_acc = find_max_balance_account(accounts)
    if best_acc:
        print(
            f"\nAccount with maximum balance: "
            f"{best_acc.client_name} ({best_acc.balance:.2f})"
        )

    sorted_accs = sort_accounts_by_balance(accounts)
    print_accounts("Accounts sorted by balance (descending)", sorted_accs)

    acc_index = create_account_index(accounts)
    search_id = 3
    print(f"\nSearch by ID {search_id} (via dict-index): {acc_index.get(search_id)}")

    min_balance = 2000.0
    is_high_balance = create_min_balance_filter(min_balance)

    high_balance_accs = [acc for acc in accounts if is_high_balance(acc)]
    print_accounts(
        f"Accounts with balance >= {min_balance} (Filtering via Closure)",
        high_balance_accs,
    )

    demo_average = calculate_average_balance_args(150.0, 300.0, 450.0)
    print(f"\nAverage balance via *args (150, 300, 450): {demo_average:.2f}")

    new_record = create_account_record(
        id=10, client_name="Taras", type="deposit", balance=1000
    )
    print(f"Created dict via **kwargs: {new_record}")

    rich_accounts = filter_items(accounts, lambda acc: acc.balance > 10000)
    print_accounts("Accounts with balance > 10000 (Universal Filter)", rich_accounts)

    stats = get_account_type_statistics(accounts)
    print(f"\nAccount type statistics (Counter): {stats}")

    run_benchmark()


if __name__ == "__main__":
    main()