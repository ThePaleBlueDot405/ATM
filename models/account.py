class Account:
    def __init__(self, name, pin, balance=0):
        self.name = name
        self.pin = pin
        self.balance = balance

    def check_balance(self):
        return self.balance

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
    
    
a2 = Account("jitendra","2480",2000)

print(a2.withrawl_amount(1000))
        
        
        
        
    
a1=Account("Prabhu", "1234", 5000)



print(a1.check_balance())