class Account:
    def __init__(self, name, pin, balance=0):
        self.name = name
        self.pin = pin
        self.balance = balance
# Function to cheak balance
    def check_balance(self):
        return self.balance
    
    def show_details(self):
            print(f"Account Holder: {self.name}")
            print(f"Account Number: {self.account_number}")
            print(f"Account Balance: {self.balance}")
# Function to deposite balance
    def deposit(self, amount):
        if amount <= 0:
            print("Invalid amount")
            return
        self.balance += amount
        print(f"₹{amount} depositid succsesfully.")
        
    def withrawl_amount(self, withdrawal_amount):
        self.withdrawal_amount = withdrawal_amount
        if withdrawal_amount <= self.balance:
          self.balance -= withdrawal_amount
        return self.balance
    
