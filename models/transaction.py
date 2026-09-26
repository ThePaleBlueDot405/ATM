from models.savings import SavingsAccount
from models.current import CurrentAccount
from datetime import datetime


class Transaction:
    # Transaction class is responsible for storing transaction details
    # such as account, transaction type, amount, balance, and time.
    def __init__(self,account, transaction_type, amount, balance_after):
        self.account = account
        self.transaction_type = transaction_type
        self.amount = amount 
        self.balance_after = balance_after
        self.timestamp = datetime.now() 
                 # datetime.now() gets the exact current date and time.
        
    def withrawl(self, amount, account):
      
       return account.withrawl(amount)

    def deposit(self, amount, account):
       return account.deposit(amount)

    def __str__(self): 

          # __str__() controls how the Transaction object is displayed
          # when we use print(transaction).
          
          return (
              f"{self.timestamp.strftime('%d-%m-%Y %I:%M:%S %p')} | "  
              # Convert the datetime into the format we want.

              f"{self.transaction_type} | "

              f"Amount: ₹{self.amount} | "

              f"Balance: ₹{self.balance_after}"
              # Display the balance after the transaction.
           )
            

# Create account objects.
# These objects are not required here in the final project.
# They are written here only to test whether the Transaction class works.

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
transaction = Transaction(
    savings_account,
    "Withdrawal",
    100,
    savings_account.check_balance()
)


print(transaction)


# Because Transaction has a __str__() method,
# print(transaction) automatically calls transaction.__str__().


transaction.withrawl(100, savings_account)

transaction.deposit(20000, savings_account)


transaction.deposit(200, current_account)
transaction.withrawl(20000, current_account)


# Display the final balance of the SavingsAccount.
print("Savings Balance:", savings_account.check_balance())

# Display the final balance of the CurrentAccount.
print("Current Balance:", current_account.check_balance())

print("Overdraft Limit:", current_account.overdraft_limit)