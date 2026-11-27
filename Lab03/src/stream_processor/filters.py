from collections.abc import Iterable, Iterator
from bank_manager.models import Account
from stream_processor.models import AccountOperation


def validate_operations(
    rows: Iterable[dict[str, str]],
    stats: dict[str, int] | None = None,
) -> Iterator[AccountOperation]:
    for row in rows:
        try:
            account_number = int(row["account_number"])
            client = row["client"].strip()
            balance = float(row["balance"])
            operation = row["operation"].strip().lower()
            amount = float(row["amount"])
        except (ValueError, TypeError, KeyError):
            if stats is not None:
                stats["invalid"] = stats.get("invalid", 0) + 1
            continue

        if (
            account_number <= 0
            or not client
            or balance < 0
            or amount < 0
            or operation not in ("top_up", "withdraw")
        ):
            if stats is not None:
                stats["invalid"] = stats.get("invalid", 0) + 1
            continue

        if stats is not None:
            stats["valid"] = stats.get("valid", 0) + 1

        yield AccountOperation(
            account_number=account_number,
            client=client,
            balance=balance,
            operation=operation,
            amount=amount,
        )


def filter_by_client(
    accounts: Iterable[Account], client_name: str
) -> Iterator[Account]:
    target = client_name.lower()
    for account in accounts:
        if account.client_name.lower() == target:
            yield account


def filter_by_balance(
    accounts: Iterable[Account], min_balance: float
) -> Iterator[Account]:
    for account in accounts:
        if account.balance >= min_balance:
            yield account