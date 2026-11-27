from bank_manager.models import Account

accounts = [
    Account(number=1, client_name="Alice", balance=2500.50, account_type="salary"),
    Account(number=2, client_name="Bob", balance=150.00, account_type="current"),
    Account(number=3, client_name="Charlie", balance=10500.00, account_type="deposit"),
    Account(number=4, client_name="Diana", balance=340.25, account_type="salary"),
    Account(number=5, client_name="Eve", balance=50000.00, account_type="deposit"),
]

ACCOUNT_TYPES: tuple[str, ...] = ("salary", "current", "deposit")