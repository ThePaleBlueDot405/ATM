# ui/app.py
# PyQt5 window for the ATM project.
#
# This file ONLY draws the screen and the buttons.
# The real banking work (deposit, withdraw, balance) is still done by the
# classes inside the models folder (SavingsAccount, CurrentAccount, Transaction).

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QComboBox,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from models.savings import SavingsAccount
from models.current import CurrentAccount
from models.transaction import Transaction


# ---------------- SETTINGS ----------------
PIN_LENGTH = 4            # PIN must be exactly 4 digits
MAX_PIN_ATTEMPTS = 3      # 3 wrong PINs and the card is blocked
MAX_AMOUNT_DIGITS = 7     # stops the user from typing a huge number

# The ATM is always in exactly one of these states.
# The ENTER button does a different job depending on the state.
STATE_CARD = "card"            # waiting for a card to be selected
STATE_PIN = "pin"              # waiting for the PIN
STATE_MENU = "menu"            # logged in, waiting for a menu choice
STATE_DEPOSIT = "deposit"      # waiting for the deposit amount
STATE_WITHDRAW = "withdraw"    # waiting for the withdraw amount


class ATMWindow(QWidget):

    def __init__(self, accounts):
        super().__init__()

        # accounts is a dictionary: { "SAV001": SavingsAccount, "CUR001": CurrentAccount }
        # It is created in main.py and passed in here.
        self.accounts = accounts

        # The account that is logged in right now (None means nobody)
        self.current_account = None

        # Current state of the ATM (see the STATE_ constants above)
        self.state = STATE_CARD

        # Digits typed on the keypad since the last ENTER / CLEAR
        self.typed = ""

        # How many wrong PINs were typed for each account number
        self.pin_attempts = {}

        # Account numbers of cards that are blocked
        self.blocked_cards = []

        # List of Transaction objects for each account (used by Mini Statement)
        self.history = {}
        for account_number in self.accounts:
            self.history[account_number] = []

        self.setWindowTitle("ATM Machine")
        self.setMinimumWidth(480)

        self.build_ui()
        self.show_welcome()

    # =====================================================
    #                  BUILDING THE WINDOW
    # =====================================================

    def build_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # ---------- card selection (works like inserting a card) ----------
        card_layout = QHBoxLayout()
        card_label = QLabel("Card:")
        self.card_box = QComboBox()

        for account_number, account in self.accounts.items():
            # text shown to the user, and the account number saved as hidden data
            text = account_number + " - " + account.name
            self.card_box.addItem(text, account_number)

        card_layout.addWidget(card_label)
        card_layout.addWidget(self.card_box)
        main_layout.addLayout(card_layout)

        # ---------- ATM screen (two labels stacked on top of each other) ----------
        screen_layout = QVBoxLayout()
        screen_layout.setSpacing(0)

        # big label for messages
        self.message_label = QLabel("")
        self.message_label.setFont(QFont("Courier New", 9))
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.message_label.setMinimumHeight(180)
        self.message_label.setStyleSheet(
            "background-color: black; color: lime; padding: 10px;"
        )

        # small label under it that shows what the user is typing
        self.input_label = QLabel("")
        self.input_label.setFont(QFont("Courier New", 11))
        self.input_label.setMinimumHeight(35)
        self.input_label.setStyleSheet(
            "background-color: black; color: yellow; padding: 5px 10px;"
        )

        screen_layout.addWidget(self.message_label)
        screen_layout.addWidget(self.input_label)
        main_layout.addLayout(screen_layout)

        # ---------- menu buttons (Balance, Deposit, ...) ----------
        menu_layout = QGridLayout()

        self.balance_button = QPushButton("Balance")
        self.deposit_button = QPushButton("Deposit")
        self.withdraw_button = QPushButton("Withdraw")
        self.statement_button = QPushButton("Mini Statement")
        self.exit_button = QPushButton("Exit")

        # connect each button to the function that should run when it is clicked
        self.balance_button.clicked.connect(self.show_balance)
        self.deposit_button.clicked.connect(self.start_deposit)
        self.withdraw_button.clicked.connect(self.start_withdraw)
        self.statement_button.clicked.connect(self.show_statement)
        self.exit_button.clicked.connect(self.exit_pressed)

        # keep them in a list so we can enable / disable all of them together
        self.menu_buttons = [
            self.balance_button,
            self.deposit_button,
            self.withdraw_button,
            self.statement_button,
            self.exit_button,
        ]

        for button in self.menu_buttons:
            button.setMinimumHeight(40)

        # addWidget(widget, row, column)  or  addWidget(widget, row, column, rowSpan, columnSpan)
        menu_layout.addWidget(self.balance_button, 0, 0)
        menu_layout.addWidget(self.deposit_button, 0, 1)
        menu_layout.addWidget(self.withdraw_button, 0, 2)
        menu_layout.addWidget(self.statement_button, 1, 0, 1, 2)   # takes 2 columns
        menu_layout.addWidget(self.exit_button, 1, 2)
        main_layout.addLayout(menu_layout)

        # menu stays disabled until the user logs in with a correct PIN
        self.set_menu_enabled(False)

        # ---------- keypad ----------
        keypad_layout = QGridLayout()

        # buttons 1 to 9 (3 rows x 3 columns)
        number = 1
        for row in range(3):
            for column in range(3):
                key = self.make_key(str(number))
                key.clicked.connect(self.digit_pressed)
                keypad_layout.addWidget(key, row, column)
                number = number + 1

        # bottom row of the keypad: CLEAR, 0, ENTER
        clear_key = self.make_key("CLEAR")
        clear_key.setStyleSheet("background-color: #ffe08a;")
        clear_key.clicked.connect(self.clear_pressed)
        keypad_layout.addWidget(clear_key, 3, 0)

        zero_key = self.make_key("0")
        zero_key.clicked.connect(self.digit_pressed)
        keypad_layout.addWidget(zero_key, 3, 1)

        enter_key = self.make_key("ENTER")
        enter_key.setStyleSheet("background-color: #9be39b;")
        enter_key.clicked.connect(self.enter_pressed)
        keypad_layout.addWidget(enter_key, 3, 2)

        # CANCEL button under the keypad, it takes all 3 columns
        cancel_key = self.make_key("CANCEL")
        cancel_key.setStyleSheet("background-color: #f09090;")
        cancel_key.clicked.connect(self.cancel_pressed)
        keypad_layout.addWidget(cancel_key, 4, 0, 1, 3)

        main_layout.addLayout(keypad_layout)

    def make_key(self, text):
        # Makes one keypad button. Every key has the same size and font.
        key = QPushButton(text)
        key.setMinimumSize(80, 50)
        key.setFont(QFont("Arial", 13))
        return key

    def set_menu_enabled(self, enabled):
        # enabled = True  -> user can click the menu buttons
        # enabled = False -> menu buttons are greyed out
        for button in self.menu_buttons:
            button.setEnabled(enabled)

    # =====================================================
    #                  SCREEN HELPERS
    # =====================================================

    def show_message(self, text):
        # Shows text on the big green screen
        self.message_label.setText(text)

    def refresh_input_label(self):
        # Updates the yellow line under the screen
        if self.state == STATE_PIN:
            # never show the real PIN, only stars
            self.input_label.setText("PIN: " + "*" * len(self.typed))
            return

        if self.state == STATE_DEPOSIT or self.state == STATE_WITHDRAW:
            self.input_label.setText("Amount: Rs. " + self.typed)
            return

        # in all other states there is nothing to type
        self.input_label.setText("")

    def show_welcome(self):
        self.show_message(
            "WELCOME TO THE ATM\n\n"
            "1. Select your card at the top\n"
            "2. Press ENTER"
        )
        self.refresh_input_label()

    def end_session(self, message):
        # Logs the user out and takes the ATM back to the first screen
        self.current_account = None
        self.typed = ""
        self.state = STATE_CARD
        self.card_box.setEnabled(True)
        self.set_menu_enabled(False)
        self.refresh_input_label()
        self.show_message(message)

    # =====================================================
    #                  KEYPAD BUTTONS
    # =====================================================

    def digit_pressed(self):
        # This one function handles buttons 0 to 9.
        # self.sender() tells us which button was clicked.
        button = self.sender()
        digit = button.text()

        # while typing the PIN
        if self.state == STATE_PIN:
            if len(self.typed) >= PIN_LENGTH:
                return
            self.typed = self.typed + digit
            self.refresh_input_label()
            return

        # while typing an amount
        if self.state == STATE_DEPOSIT or self.state == STATE_WITHDRAW:
            if len(self.typed) >= MAX_AMOUNT_DIGITS:
                return
            self.typed = self.typed + digit
            self.refresh_input_label()
            return

        # in any other state the digits do nothing

    def clear_pressed(self):
        # CLEAR removes everything typed so far
        self.typed = ""
        self.refresh_input_label()

    def cancel_pressed(self):
        # CANCEL does a different thing in each state
        if self.state == STATE_PIN:
            self.end_session("Cancelled.\nPlease take your card.")
            return

        if self.state == STATE_DEPOSIT or self.state == STATE_WITHDRAW:
            # go back one step to the menu
            self.state = STATE_MENU
            self.typed = ""
            self.refresh_input_label()
            self.show_message("Cancelled.\nChoose an option below.")
            return

        if self.state == STATE_MENU:
            self.end_session("Thank you!\nPlease take your card.")
            return

        # in STATE_CARD there is nothing to cancel

    def enter_pressed(self):
        # ENTER decides what to do by looking at the current state
        if self.state == STATE_CARD:
            self.check_card()
            return

        if self.state == STATE_PIN:
            self.check_pin()
            return

        if self.state == STATE_DEPOSIT:
            self.do_deposit()
            return

        if self.state == STATE_WITHDRAW:
            self.do_withdraw()
            return

        # in STATE_MENU ENTER does nothing, the user must click a menu button

    # =====================================================
    #                  LOGIN (CARD + PIN)
    # =====================================================

    def check_card(self):
        account_number = self.card_box.currentData()

        if account_number in self.blocked_cards:
            self.show_message("This card is blocked.\nPlease contact your bank.")
            return

        self.current_account = self.accounts[account_number]
        self.typed = ""
        self.state = STATE_PIN
        self.card_box.setEnabled(False)
        self.refresh_input_label()
        self.show_message("Card accepted.\n\nEnter your 4 digit PIN\nand press ENTER.")

    def check_pin(self):
        account = self.current_account
        account_number = account.account_number

        if len(self.typed) != PIN_LENGTH:
            self.show_message("PIN must be 4 digits.\nTry again.")
            return

        # PIN is stored as a number in the model (for example 2480),
        # so we turn it into text before comparing with what was typed.
        if self.typed != str(account.pin):
            attempts = self.pin_attempts.get(account_number, 0) + 1
            self.pin_attempts[account_number] = attempts
            self.typed = ""
            self.refresh_input_label()

            if attempts >= MAX_PIN_ATTEMPTS:
                self.blocked_cards.append(account_number)
                self.end_session("Too many wrong PINs.\nYour card is blocked.")
                return

            attempts_left = MAX_PIN_ATTEMPTS - attempts
            self.show_message("Wrong PIN.\nAttempts left: " + str(attempts_left))
            return

        # PIN is correct
        self.pin_attempts[account_number] = 0
        self.typed = ""
        self.state = STATE_MENU
        self.set_menu_enabled(True)
        self.refresh_input_label()
        self.show_message("Welcome, " + account.name + "!\n\nChoose an option below.")

    # =====================================================
    #                  MENU BUTTONS
    # =====================================================

    def show_balance(self):
        account = self.current_account
        self.state = STATE_MENU
        self.typed = ""
        self.refresh_input_label()

        text = "BALANCE\n\n"
        text = text + "Available: Rs. " + format(account.check_balance(), ",.2f") + "\n"

        # extra information that depends on the account type
        if isinstance(account, SavingsAccount):
            text = text + "Minimum balance: Rs. " + format(account.min_balance, ",.2f")

        if isinstance(account, CurrentAccount):
            text = text + "Overdraft left: Rs. " + format(account.overdraft_limit, ",.2f")

        self.show_message(text)

    def start_deposit(self):
        self.state = STATE_DEPOSIT
        self.typed = ""
        self.refresh_input_label()
        self.show_message("DEPOSIT\n\nType the amount\nand press ENTER.")

    def start_withdraw(self):
        self.state = STATE_WITHDRAW
        self.typed = ""
        self.refresh_input_label()
        self.show_message("WITHDRAW\n\nType the amount\nand press ENTER.")

    def show_statement(self):
        account = self.current_account
        self.state = STATE_MENU
        self.typed = ""
        self.refresh_input_label()

        transactions = self.history[account.account_number]

        if len(transactions) == 0:
            self.show_message("MINI STATEMENT\n\nNo transactions yet.")
            return

        text = "MINI STATEMENT (last 5)\n\n"

        # [-5:] means "only the last 5 items of the list"
        for transaction in transactions[-5:]:
            time_text = transaction.timestamp.strftime("%d/%m %I:%M%p")
            line = (
                time_text
                + "  "
                + transaction.transaction_type.ljust(10)
                + " "
                + str(transaction.amount).rjust(7)
                + "  Bal "
                + format(transaction.balance_after, ",.2f")
            )
            text = text + line + "\n"

        self.show_message(text)

    def exit_pressed(self):
        self.end_session("Thank you!\nPlease take your card.")

    # =====================================================
    #                  DEPOSIT / WITHDRAW
    # =====================================================

    def read_amount(self):
        # Turns the typed digits into a number.
        # Returns None if the amount is not usable.
        if self.typed == "":
            self.show_message("Please type an amount first.")
            return None

        amount = int(self.typed)

        if amount <= 0:
            self.typed = ""
            self.refresh_input_label()
            self.show_message("Amount must be\ngreater than 0.")
            return None

        return amount

    def save_transaction(self, transaction_type, amount):
        # Creates a Transaction object (from models/transaction.py)
        # and stores it so the Mini Statement can show it later.
        account = self.current_account
        transaction = Transaction(
            account,
            transaction_type,
            amount,
            account.check_balance()
        )
        self.history[account.account_number].append(transaction)

    def finish_transaction(self, message):
        # Shared ending for a successful deposit or withdrawal
        account = self.current_account
        self.state = STATE_MENU
        self.typed = ""
        self.refresh_input_label()

        text = message + "\n\nNew balance: Rs. " + format(account.check_balance(), ",.2f")
        self.show_message(text)

    def do_deposit(self):
        amount = self.read_amount()
        if amount is None:
            return

        account = self.current_account
        account.deposit(amount)

        self.save_transaction("Deposit", amount)
        self.finish_transaction("Rs. " + str(amount) + " deposited.")

    def do_withdraw(self):
        amount = self.read_amount()
        if amount is None:
            return

        account = self.current_account

        # CurrentAccount.withrawl() in the model does not stop the user from
        # going past the overdraft limit, so we check it here before calling it.
        if isinstance(account, CurrentAccount):
            allowed = account.balance + account.overdraft_limit
            if amount > allowed:
                self.typed = ""
                self.refresh_input_label()
                self.show_message("Transaction Declined:\nOverdraft limit exceeded.")
                return

        # SavingsAccount.withrawl() raises ValueError when the money is not
        # available, so we catch it and show its message on the screen.
        try:
            account.withrawl(amount)
        except ValueError as error:
            self.typed = ""
            self.refresh_input_label()
            self.show_message(str(error))
            return

        self.save_transaction("Withdrawal", amount)
        self.finish_transaction("Rs. " + str(amount) + " withdrawn.")