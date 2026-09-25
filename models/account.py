class Account:
    def __init__(self, name, pin, balance=0):
        self.name = name
        self.pin = pin
        self.balance = balance
# Function to cheak balance
    def check_balance(self):
        return self.balance
# Function to deposite balance
    def deposit(self, amount):
        if amount <= 0:
            print("Invalid amount")
            return
        self.balance += amount
        print(f"₹{amount} depositid succsesfully.")
        
    def withrawl_amount(self, withrawl):
        self.withrawl = withrawl
        if withrawl <= self.balance:
          self.balance -= withrawl
        return self.balance
    
