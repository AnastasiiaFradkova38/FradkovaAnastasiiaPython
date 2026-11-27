from collections.abc import Iterator
from pathlib import Path
from bank_manager.models import Account
from stream_processor.filters import (
    filter_by_balance,
    filter_by_client,
    validate_operations,
)
from stream_processor.parsers import parse_csv_rows
from stream_processor.readers import clean_lines, read_lines
from stream_processor.transformations import apply_operations


def build_pipeline(
    path: Path,
    min_balance: float | None = None,
    client_name: str | None = None,
    validation_stats: dict[str, int] | None = None,
) -> Iterator[Account]:
    lines = read_lines(path)
    cleaned = clean_lines(lines)
    rows = parse_csv_rows(cleaned)
    valid_ops = validate_operations(rows, stats=validation_stats)
    processed_accounts = apply_operations(valid_ops)

    stream: Iterator[Account] = processed_accounts
    if client_name is not None:
        stream = filter_by_client(stream, client_name)
    if min_balance is not None:
        stream = filter_by_balance(stream, min_balance)

    return stream