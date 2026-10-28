# ui/new_account_dialog.py
# A small pop-up form used to open a new account.
#
# This file only collects and checks what the user typed.
# It does NOT create the account. It stores the checked values in
# self.account_data and ui/app.py creates the real account object from them.

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
)
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp


PIN_LENGTH = 4              # same rule as PIN_LENGTH in ui/app.py
MIN_SAVINGS_DEPOSIT = 500   # same as the default min_balance in SavingsAccount


class NewAccountDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Open New Account")
        self.setMinimumWidth(360)

        # Stays None until the user presses Create with correct data.
        # After that it holds: {"name": ..., "type": ..., "pin": ..., "deposit": ...}
        self.account_data = None

        self.build_form()

    def build_form(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # This validator only lets the user type the digits 0 to 9.
        digits_only = QRegExpValidator(QRegExp("[0-9]*"))

        # ---------- input fields ----------
        form_layout = QFormLayout()

        # account holder name
        self.name_input = QLineEdit()
        self.name_input.setMaxLength(30)

        # account type (Savings or Current)
        self.type_box = QComboBox()
        self.type_box.addItem("Savings")
        self.type_box.addItem("Current")
        self.type_box.currentIndexChanged.connect(self.update_hint)

        # PIN and confirm PIN (shown as dots while typing)
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setMaxLength(PIN_LENGTH)
        self.pin_input.setValidator(digits_only)

        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setMaxLength(PIN_LENGTH)
        self.confirm_input.setValidator(digits_only)

        # opening deposit
        self.deposit_input = QLineEdit()
        self.deposit_input.setMaxLength(7)
        self.deposit_input.setValidator(digits_only)

        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Account type:", self.type_box)
        form_layout.addRow("PIN (4 digits):", self.pin_input)
        form_layout.addRow("Confirm PIN:", self.confirm_input)
        form_layout.addRow("Opening deposit (Rs.):", self.deposit_input)
        main_layout.addLayout(form_layout)

        # ---------- hint line (changes with the account type) ----------
        self.hint_label = QLabel("")
        main_layout.addWidget(self.hint_label)

        # ---------- error line (red, empty until something is wrong) ----------
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setWordWrap(True)
        main_layout.addWidget(self.error_label)

        # ---------- buttons ----------
        button_layout = QHBoxLayout()

        create_button = QPushButton("Create Account")
        create_button.setDefault(True)
        create_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(create_button)
        button_layout.addWidget(cancel_button)
        main_layout.addLayout(button_layout)

        self.update_hint()

    def update_hint(self):
        # Tells the user the opening deposit rule for the chosen account type
        if self.type_box.currentText() == "Savings":
            self.hint_label.setText(
                "Savings needs at least Rs. " + str(MIN_SAVINGS_DEPOSIT) + " to open."
            )
            return

        self.hint_label.setText("Current account can be opened with any amount (even 0).")

    def show_error(self, text):
        self.error_label.setText(text)

    def accept(self):
        # Runs when the user presses "Create Account".
        # Every check below stops with return, so the window stays open
        # and the user can fix the mistake.
        name = self.name_input.text().strip()
        account_type = self.type_box.currentText()
        pin = self.pin_input.text()
        confirm_pin = self.confirm_input.text()
        deposit_text = self.deposit_input.text()

        if name == "":
            self.show_error("Please enter the account holder name.")
            return

        if len(pin) != PIN_LENGTH:
            self.show_error("PIN must be exactly 4 digits.")
            return

        if pin != confirm_pin:
            self.show_error("PIN and Confirm PIN do not match.")
            return

        if deposit_text == "":
            self.show_error("Please enter the opening deposit.")
            return

        deposit = int(deposit_text)

        if account_type == "Savings":
            if deposit < MIN_SAVINGS_DEPOSIT:
                self.show_error(
                    "Savings account needs at least Rs. "
                    + str(MIN_SAVINGS_DEPOSIT)
                    + " to open."
                )
                return

        # everything is correct, store the values and close the window
        self.account_data = {
            "name": name,
            "type": account_type,
            "pin": pin,
            "deposit": deposit,
        }
        super().accept()
