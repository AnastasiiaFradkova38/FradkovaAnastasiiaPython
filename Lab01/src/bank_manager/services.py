from bank_manager.models import Account
from bank_manager.exceptions import InsufficientFundsError
from dataclasses import replace

def top_up(account: Account, sum: float) -> Account:
    return replace(account, balance=account.balance + sum)

def withdraw(account: Account, sum: float) -> Account | None:
    if account.balance < sum:
        raise InsufficientFundsError(f"Balance too small to withdraw {sum}")
    return replace(account, balance=account.balance - sum)

def check_balance(account: Account) -> float:
    return account.balance

def find_account(accounts: list[Account], number: int) -> Account | None:
    for account in accounts:
        if account.number == number:
            return account
    return None

def calculate_total_sum(accounts: list[Account]) -> float:
    return sum(account.balance for account in accounts)