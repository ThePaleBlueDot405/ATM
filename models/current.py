from models.account import Account
class CurrentAccount(Account):

    def __init__(self, account_number, name, pin, balance=0,Overdraft_Limit=1000):
        super().__init__(name, pin, balance)
        self.account_number = account_number
        self.overdraft_limit = Overdraft_Limit

    def show_details(self):
        super().show_details()
        print(f"Account Type: Savings Account")
        print(f"Overdraft Limit: {self.overdraft_limit}")
   
   
    # We dont need deposite fucntion because its alrday exixt in Account class
    # def deposit(self,deposit):
    #     if deposit <0:
    #         print("invailed amount")
            
    #     self.balance += deposit
    #     print(f"₹{deposit} depositid succsesfully.")
        

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
    

    

