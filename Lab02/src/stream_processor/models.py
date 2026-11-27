from typing import NamedTuple


class AccountOperation(NamedTuple):
    account_number: int
    client: str
    balance: float
    operation: str
    amount: float