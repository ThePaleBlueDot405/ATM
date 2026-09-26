# from datetime import datetime, timedelta

# MAX_FAILED_ATTEMPTS = 3
# LOCKOUT_DURATION = timedelta(minutes=5)

# """define constants:
#     MAX_FAILED_ATTEMPTS = 3
#     LOCKOUT_DURATION = 5 minutes

# define exceptions:
#     AccountNotFoundError
#     AuthenticationError
#     AccountLockedError

# class AuthService:

#     function __init__(accounts):
#         store accounts
#         set current_customer = None

#     function _get_account(account_number):
#         look up account_number in accounts
#         if not found:
#             raise AccountNotFoundError
#         return the account

#     function is_locked(account_number):
#         account = _get_account(account_number)
#         if account has no locked_until, or locked_until is None:
#             return False
#         return (current time is before locked_until)

#     function login(account_number, pin):
#         account = _get_account(account_number)

#         if is_locked(account_number):
#             raise AccountLockedError

#         if pin does NOT match account's stored pin:
#             increase account's failed_attempts by 1

#             if failed_attempts >= MAX_FAILED_ATTEMPTS:
#                 set account.locked_until = now + LOCKOUT_DURATION
#                 raise AccountLockedError
#             else:
#                 raise AuthenticationError (mention attempts remaining)

#         // pin was correct
#         reset account.failed_attempts to 0
#         reset account.locked_until to None
#         set current_customer = account
#         return account

#     function logout():
#         set current_customer = None

#     function change_pin(account_number, old_pin, new_pin):
#         account = _get_account(account_number)

#         if old_pin does NOT match account's stored pin:
#             raise AuthenticationError

#         if new_pin is not exactly 4 digits:
#             raise ValueError

#         set account.pin = new_pin
#         return True"""
        
# class AccountNotFoundError(Exception):
#     pass

# class AuthenticationError(Exception):
#     pass

# class AccountLockedError(Exception):
#     pass


# class AuthService :
#     def __init__(self,accounts,current_coustmer=None):
#         self.account = accounts
        
#     def get_account(account_number, accounts):
#         for account in accounts:
#             if account != account_number:
#                 raise ValueError("tum chnadan nahi chuiyanadan ho user")
#             return account_number
#     def is_locked( self,account_number):
#          account = self.get_account(account_number)
         
          
          
class AccountNotFoundError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class AccountLockedError(Exception):
    pass


class AuthService:
    def __init__(self, accounts, current_customer=None):
        self.accounts = accounts
        self.current_customer = current_customer

    def get_account(self, account_number):
        for account in self.accounts:
            if account == account_number:
                return account

        raise AccountNotFoundError("Account not found")

    def is_locked(self, account_number):
        account = self.get_account(account_number)
        return account["locked"]


# ---------------- TEST DATA ----------------

accounts = {
    "1001": {
        "name": "Prabhu",
        "pin": "1234",
        "locked": False
    },

    "1002": {
        "name": "Rahul",
        "pin": "5678",
        "locked": True
    },

    "1003": {
        "name": "Aman",
        "pin": "9999",
        "locked": False
    }
}


# ---------------- TEST ----------------

auth = AuthService(accounts)

print(auth.get_account("1001"))