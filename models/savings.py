from account import Account
class SavingsAccount(Account):

    def __init__(self, account_number, name, pin, balance=0, interest_rate= 0.15, min_balance = 500):
        super().__init__(name, pin, balance)
        self.interest_rate = interest_rate
        self.min_balance = min_balance
        self.account_number = account_number

    def show_details(self):
        print(f"Account Holder: {self.name}")
        print(f"Account Number: {self.account_number}")
        print(f"Account Type: Savings Account")

    def deposit(self,deposit):
        if deposit <0:
            print("invailed amount")
            
        self.balance += deposit
        print(f"₹{deposit} depositid succsesfully.")
        

    def withrawl (self , withrawl):
        if withrawl < 0 :
            raise ValueError("Invalid Amount") 
        elif self.balance - withrawl < self.min_balance:
            raise ValueError("Transaction Declined: Available Balance Exceeded")
        else :
            self.balance= self.balance-withrawl
            return self.balance

    def intrest(self , time):
        if time<0 :
            raise ValueError("Invalid Value")
        else:
            inters = 0
            self.balance = self.balance+ time*12*self.interest_rate*self.balance


        
        
            
    
                 


account = SavingsAccount(
    "ACC1001",
    "Jitendra",
    "2480",
    2000
)

account.show_details()

print("Initial Balance:", account.check_balance())

account.deposit(1000)

print("Balance after deposit:", account.check_balance())

account. withrawl(500)

print("Balance after withdrawal:", account.check_balance())

account.intrest(5)
print("Balance after Intrest:", account.check_balance())


