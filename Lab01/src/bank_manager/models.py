from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Account:
    number: int
    client_name: str
    balance: float