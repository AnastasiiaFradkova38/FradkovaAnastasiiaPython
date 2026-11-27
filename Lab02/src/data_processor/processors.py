from collections import defaultdict
from bank_manager.models import Account
from collections import Counter

def get_unique_account_types(accounts: list[Account]) -> set[str]:
    return {account.account_type for account in accounts}

def create_account_index(accounts: list[Account]) -> dict[int, Account]:
    return {account.number: account for account in accounts}

def group_accounts_by_type(accounts: list[Account]) -> dict[str, list[Account]]:
    result = defaultdict(list)
    for account in accounts:
        result[account.account_type].append(account)
    return dict(result)

def get_account_type_statistics(accounts: list[Account]) -> Counter:
    return Counter(account.account_type for account in accounts)