
from models.savings import SavingsAccount

name = input("Enter name: ")
account_number = input("Enter account number: ")
pin = input("Enter PIN: ")
balance = float(input("Enter initial balance: "))
interest_rate = float(input("Enter interest rate: "))
min_balance = float(input("Enter minimum balance: "))

account = SavingsAccount(
    account_number,
    name,
    pin,
    balance,
    interest_rate,
    min_balance
)
account.intrest(4)
# account. withrawl_amount(500)

# print("Balance after withdrawal:", account.check_balance())