from account import Account
class CurrentAccount(Account):

    def __init__(self, account_number, name, pin, balance=0,Overdraft_Limit=0):
        super().__init__(name, pin, balance)
        self.account_number = account_number
        self.overdraft_limit = Overdraft_Limit

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
        elif withrawl>self.balance:
            extra = withrawl - self.balance
            self.overdraft_limit= self.overdraft_limit - extra
            self.balance= 0
            return self.overdraft_limit
        else :
            self.balance= self.balance-withrawl
            return self.balance
    

    

account = CurrentAccount(
    "ACC1001",
    "Jitendra",
    "2480",
    2000,
    10000
)

account. withrawl(5000)

print("Balance after withdrawal:", account.check_balance())
print(account.overdraft_limit)

