from decimal import Decimal

# Simple interest: principal * rate * time, spread over a number of months.
# annual_rate should be a decimal like 0.035 for 3.5 percent, not 3.5.
def simple_interest(principal, annual_rate, months):
    principal = Decimal(str(principal))
    annual_rate = Decimal(str(annual_rate))
    months = Decimal(str(months))

    if months < 0:
        raise ValueError("months cannot be negative")

    return principal * annual_rate * months / Decimal("12")


# Compound interest, compounded monthly. Returns just the interest earned,
# not the new total balance, so it matches simple_interest's return style.
def compound_interest(principal, annual_rate, months):
    principal = Decimal(str(principal))
    annual_rate = Decimal(str(annual_rate))
    months = int(months)

    if months < 0:
        raise ValueError("months cannot be negative")

    monthly_rate = annual_rate / Decimal("12")
    new_balance = principal * (1 + monthly_rate) ** months
    return new_balance - principal


# Goes through every account and credits one month of simple interest to
# the ones that qualify. Meant to be called once per month, for example
# from a scheduled job or a "run interest" menu option.
def apply_monthly_interest(accounts, current_month):
    credited = []

    for account_number, account in accounts.items():
        # Only accounts with an interest_rate attribute earn interest.
        # Current accounts simply won't have this, so they're skipped.
        rate = getattr(account, "interest_rate", None)
        if rate is None:
            continue

        # Frozen accounts don't earn interest. Default to "active" for
        # older account objects that don't have a status field yet.
        status = getattr(account, "status", "active")
        if status != "active":
            continue

        # Guards against running this twice in the same month and paying
        # interest twice. last_interest_month is stamped below once paid.
        last_month = getattr(account, "last_interest_month", None)
        if last_month == current_month:
            continue

        interest = simple_interest(account.balance, rate, 1)
        account.balance = account.balance + interest
        account.last_interest_month = current_month

        credited.append((account_number, interest))

    return credited