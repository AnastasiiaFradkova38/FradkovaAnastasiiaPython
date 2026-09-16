from bank_manager.models import Account
from bank_manager.services import top_up, withdraw, check_balance, find_account, calculate_total_sum

def create_accounts() -> list[Account]:
    return [
        Account(number=1, client_name='Alice', balance=25.5),
        Account(number=2, client_name='Bob', balance=10.0)
    ]

def print_account_info(account: Account) -> None:
    print(f"Name: {account.client_name}, number: {account.number}, balance: {account.balance}")

def main() -> None:
    accounts = create_accounts()
    
    print("INITIAL BALANCES")
    for account in accounts:
        print_account_info(account)
    print()

    print("TOP UP")
    accounts[0] = top_up(accounts[0], 3.0)
    print_account_info(accounts[0])
    print()
    
    print("FAILED WITHDRAWAL")
    withdrawal = withdraw(accounts[0], 100.0)
    if not withdrawal:
        print("Error! Balance cannot be negative.")
        print_account_info(accounts[0])
    print()
    
    print("SUCCESSFUL WITHDRAWAL")
    withdrawal = withdraw(accounts[0], 3.0)
    if withdrawal:
        accounts[0] = withdrawal
        print_account_info(accounts[0])
    print()

    print("ACCOUNT SEARCH")
    target_number = 2
    account = find_account(accounts, target_number)
    if account:
        print(f"Found account {target_number}.")
        print_account_info(account)
    else:
        print(f"Account {target_number} not found.")
    print()
        
    print("TOTAL SUM CALCULATION")
    print(f"Total sum: {calculate_total_sum(accounts):.2f}")

if __name__ == "__main__":
    main()