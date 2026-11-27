from collections.abc import Iterable
from bank_manager.models import Account


def calculate_statistics(accounts: Iterable[Account]) -> dict:
    count = 0
    total_balance = 0.0
    min_balance: float | None = None
    max_balance: float | None = None

    for acc in accounts:
        count += 1
        total_balance += acc.balance
        if min_balance is None or acc.balance < min_balance:
            min_balance = acc.balance
        if max_balance is None or acc.balance > max_balance:
            max_balance = acc.balance

    average = total_balance / count if count else 0.0
    return {
        "count": count,
        "total_balance": total_balance,
        "average_balance": average,
        "min_balance": min_balance,
        "max_balance": max_balance,
    }


def find_account_by_number(
    accounts: Iterable[Account], target_number: int
) -> Account | None:
    for acc in accounts:
        if acc.number == target_number:
            return acc
    return None