import pytest
from bank_manager.models import Account
from bank_manager.services import top_up, withdraw, check_balance, find_account, calculate_total_sum
from bank_manager.exceptions import InsufficientFundsError

@pytest.fixture
def sample_accounts() -> list[Account]:
    return [
        Account(number=1, client_name="Alice", balance=100.0),
        Account(number=2, client_name="Bob", balance=50.0)
    ]

def test_top_up():
    acc = Account(number=1, client_name="Alice", balance=100.0)
    updated_acc = top_up(acc, 50.0)
    
    assert updated_acc.balance == 150.0
    assert updated_acc.number == 1

def test_withdraw_success():
    acc = Account(number=1, client_name="Alice", balance=100.0)
    updated_acc = withdraw(acc, 40.0)
    
    assert updated_acc is not None
    assert updated_acc.balance == 60.0

def test_withdraw_insufficient_funds():
    acc = Account(number=1, client_name="Alice", balance=100.0)
    
    with pytest.raises(InsufficientFundsError):
        withdraw(acc, 200.0)

def test_check_balance():
    acc = Account(number=1, client_name="Alice", balance=123.45)
    assert check_balance(acc) == 123.45

def test_find_account_success(sample_accounts):
    found = find_account(sample_accounts, 2)
    
    assert found is not None
    assert found.client_name == "Bob"

def test_find_account_not_found(sample_accounts):
    not_found = find_account(sample_accounts, 99)
    assert not_found is None

def test_calculate_total_sum(sample_accounts):
    total = calculate_total_sum(sample_accounts)
    assert total == 150.0