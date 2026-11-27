from collections.abc import Iterator


class AccountNumberIterator:
    def __init__(self, start: int, stop: int) -> None:
        self.current = start
        self.stop = stop

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


class AccountNumberRange:
    def __init__(self, start: int, stop: int) -> None:
        self.start = start
        self.stop = stop

    def __iter__(self) -> AccountNumberIterator:
        return AccountNumberIterator(self.start, self.stop)