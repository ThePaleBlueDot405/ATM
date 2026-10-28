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


import sys

# QApplication is the object that runs every PyQt5 program
from PyQt5.QtWidgets import QApplication

from models.savings import SavingsAccount
from models.current import CurrentAccount
from models.transaction import Transaction

# our ATM window (ui/app.py)
from ui.app import ATMWindow


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

# Old console test prints. The UI shows the balance now, so they are commented out.
# print("Savings Balance:", savings_account.check_balance())
# print("Current Balance:", current_account.check_balance())


def main():
    # Put all accounts in one dictionary.
    # key = account number, value = account object
    # The UI uses this dictionary to fill the card list and to find the account.
    accounts = {
        savings_account.account_number: savings_account,
        current_account.account_number: current_account,
    }

    # 1. create the application
    app = QApplication(sys.argv)

    # 2. create our ATM window and give it the accounts
    window = ATMWindow(accounts)

    # 3. show the window on screen
    window.show()

    # 4. start the event loop (keeps the window open and listens to clicks)
    #    sys.exit makes sure the program closes properly when the window is closed
    sys.exit(app.exec_())


# This runs main() only when we start this file directly (python main.py)
if __name__ == "__main__":
    main()