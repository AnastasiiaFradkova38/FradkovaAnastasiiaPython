from collections.abc import Iterable, Iterator
from bank_manager.exceptions import InsufficientFundsError
from bank_manager.models import Account
from bank_manager.services import top_up, withdraw
from stream_processor.models import AccountOperation


def apply_operations(
    operations: Iterable[AccountOperation],
) -> Iterator[Account]:
    for op in operations:
        account = Account(
            number=op.account_number,
            client_name=op.client,
            balance=op.balance,
            account_type="current",
        )
        if op.operation == "top_up":
            yield top_up(account, op.amount)
        elif op.operation == "withdraw":
            try:
                updated = withdraw(account, op.amount)
                if updated is not None:
                    yield updated
            except InsufficientFundsError:
                yield account