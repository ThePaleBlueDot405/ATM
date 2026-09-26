
# from models.savings import SavingsAccount

# name = input("Enter name: ")
# account_number = input("Enter account number: ")
# pin = input("Enter PIN: ")
# balance = float(input("Enter initial balance: "))
# interest_rate = float(input("Enter interest rate: "))
# min_balance = float(input("Enter minimum balance: "))

# account = SavingsAccount(
#     account_number,
#     name,
#     pin,
#     balance,
#     interest_rate,
#     min_balance
# )
# account.intrest(4)
# # account. withrawl_amount(500)

# # print("Balance after withdrawal:", account.check_balance())


from models.savings import SavingsAccount
from models.current import CurrentAccount
from models.transaction import Transaction


savings_account = SavingsAccount(
    "SAV001",
    "Jitendra",
    2480,
    2000
)

current_account = CurrentAccount(
    "CUR001",
    "Rahul",
    1234,
    2000
)

print("Savings Balance:", savings_account.check_balance())



print("Current Balance:", current_account.check_balance())