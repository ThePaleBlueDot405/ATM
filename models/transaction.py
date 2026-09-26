from models.savings import SavingsAccount
from models.current import CurrentAccount
from datetime import datetime


class Transaction:
    def __init__(self,account, transaction_type, amount, balance_after):
        self.account = account
        self.transaction_type = transaction_type
        self.amount = amount 
        self.balance_after = balance_after
        self.timestamp = datetime.now() 
                 # to note the exact curre #nt time and date
        
    def withrawl(self, amount, account):
       return account.withrawl(amount)

    def deposit(self, amount, account):
       return account.deposit(amount)
    def __str__(self):

          
          return (
              f"{self.timestamp.strftime('%d-%m-%Y %I:%M:%S %p')} | "  #Convert the datetime into the format I want.
              f"{self.transaction_type} | "
              f"Amount: ₹{self.amount} | "
              f"Balance: ₹{self.balance_after}"
           )

# Create account objects and this is not requred to write here but i have to write this just to check code it works or not


#  -m models.transaction  run this for checking code because if you run the code directly from it wil trugh error we can not run this code directly 

savings_account = SavingsAccount(
    "SBI00020201",
    "Jitendra",
    2480,
    2000
)

current_account = CurrentAccount(
    "PNB005848871",
    "Rahul",
    1234,
    2000
)


# Create Transaction object
transaction = Transaction( savings_account,
    "Withdrawal",
    100,savings_account.check_balance()  )

print(transaction)

transaction.withrawl(100, savings_account)
transaction.deposit(20000,savings_account)

transaction.deposit(20000, current_account)


# 
print( "Savings Balance:", savings_account.check_balance())
print("Current Balance:", current_account.check_balance())
