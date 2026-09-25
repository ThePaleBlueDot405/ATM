from models.savings import SavingsAccount


account = SavingsAccount(
    "ACC1001",
    "Jitendra",
    "2480",
    2000
)

# account.show_details()

# print("Initial Balance:", account.check_balance())

account.deposit(1000)

print("Balance after deposit:", account.check_balance())

# account. withrawl_amount(500)

# print("Balance after withdrawal:", account.check_balance())