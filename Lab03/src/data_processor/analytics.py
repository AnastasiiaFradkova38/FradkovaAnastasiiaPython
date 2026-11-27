# src/data_processor/analytics.py
from collections.abc import Callable
from bank_manager.models import Account
from data_processor.decorators import measure_time

@measure_time
def calculate_total_sum(accounts: list[Account]) -> float:
    if not accounts:
        return 0.0
    return sum(account.balance for account in accounts)

def find_max_balance_account(accounts: list[Account]) -> Account | None:
    if not accounts:
        return None
    return max(accounts, key=lambda acc: acc.balance)

def sort_accounts_by_balance(accounts: list[Account], reverse: bool = True) -> list[Account]:
    return sorted(accounts, key=lambda acc: acc.balance, reverse=reverse)

def create_min_balance_filter(minimum_balance: float) -> Callable[[Account], bool]:
    def predicate(account: Account) -> bool:
        return account.balance >= minimum_balance
    return predicate

def calculate_average_balance_args(*balances: float) -> float:
    if not balances:
        return 0.0
    return sum(balances) / len(balances)

def create_account_record(**fields) -> dict:
    return dict(fields)

def filter_items(items: list, predicate: Callable) -> list:
    return [item for item in items if predicate(item)]