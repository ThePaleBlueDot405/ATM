from models.account import Account
class SavingsAccount(Account):

    def __init__(self, account_number, name, pin, balance=0, interest_rate= 0.15, min_balance = 500):
        super().__init__(name, pin, balance)
        self.interest_rate = interest_rate
        self.min_balance = min_balance
        self.account_number = account_number

    def show_details(self):
        super().show_details()
        print(f"Account Type: Savings Account")
        print(f"Minum balnce: {self.min_balance}" )
        
        
    # We dont need deposite fucntion because its alrday exixt in Account class
    # def deposit(self,deposit):
    #     if deposit <0:
    #         print("invailed amount")
            
    #     self.balance += deposit
    #     print(f"₹{deposit} depositid succsesfully.")
        

    def withrawl (self , withrawl):
        if withrawl < 0 :
            raise ValueError("Invalid Amount") 
        if self.balance - withrawl < self.min_balance:
            raise ValueError("Transaction Declined: Available Balance Exceeded")
        
        self.balance= self.balance-withrawl
        return self.balance

    
            

        
        
            
    
                 


