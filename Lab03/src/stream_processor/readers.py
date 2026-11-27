import csv
import random
from collections.abc import Iterable, Iterator
from pathlib import Path


def read_lines(path: Path) -> Iterator[str]:
    with path.open("r", encoding="utf-8") as file:
        yield from file


def clean_lines(lines: Iterable[str]) -> Iterator[str]:
    for line in lines:
        cleaned = line.strip()
        if cleaned:
            yield cleaned

def generate_test_csv(path: Path, count: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    clients = ("Alice", "Bob", "Charlie", "Diana", "Eve", "Taras", "Olena")
    operations = ("top_up", "withdraw")

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["account_number", "client", "balance", "operation", "amount"])
        for i in range(1, count + 1):
            if i % 500 == 0:
                writer.writerow([i, "InvalidClient", "bad_balance", "top_up", "100"])
                continue
            writer.writerow(
                [
                    i,
                    random.choice(clients),
                    round(random.uniform(50.0, 20000.0), 2),
                    random.choice(operations),
                    round(random.uniform(10.0, 5000.0), 2),
                ]
            )