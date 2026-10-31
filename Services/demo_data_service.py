from datetime import date
from decimal import Decimal
from DataBase.database import db, seed_default_categories
from Modules.models import Category, Transaction, Budget, User


def seed_demo_data(force=False):
    """
    Seeds realistic student financial records for academic demonstration.
    Avoids duplicate runs unless force=True.
    """
    seed_default_categories()

    # If transactions exist and force is False, do not duplicate
    if not force and Transaction.query.count() > 0:
        return False, "Transactions already exist. Use clear first or force=True to re-seed."

    categories = {c.name: c.id for c in Category.query.all()}

    # Realistic demo data spanning recent months (e.g., Aug, Sep, Oct 2026)
    demo_transactions = [
        # August 2026
        {"type": "Income", "cat": "Allowance", "amount": 10000.0, "date": date(2026, 8, 1), "method": "Net Banking", "desc": "Monthly allowance from parents"},
        {"type": "Income", "cat": "Freelancing", "amount": 4500.0, "date": date(2026, 8, 12), "method": "UPI", "desc": "Landing page UI design gig"},
        {"type": "Expense", "cat": "Food", "amount": 2800.0, "date": date(2026, 8, 5), "method": "UPI", "desc": "Monthly hostel mess subscription"},
        {"type": "Expense", "cat": "Education", "amount": 1650.0, "date": date(2026, 8, 8), "method": "Debit Card", "desc": "Core Java & DBMS textbooks"},
        {"type": "Expense", "cat": "Transport", "amount": 650.0, "date": date(2026, 8, 10), "method": "UPI", "desc": "Monthly bus pass renewal"},
        {"type": "Expense", "cat": "Bills", "amount": 699.0, "date": date(2026, 8, 15), "method": "UPI", "desc": "Quarterly mobile prepaid pack"},
        {"type": "Expense", "cat": "Entertainment", "amount": 450.0, "date": date(2026, 8, 20), "method": "Cash", "desc": "Weekend movie ticket & popcorn"},
        {"type": "Expense", "cat": "Shopping", "amount": 1200.0, "date": date(2026, 8, 24), "method": "UPI", "desc": "College formal shoes"},

        # September 2026
        {"type": "Income", "cat": "Allowance", "amount": 10000.0, "date": date(2026, 9, 1), "method": "Net Banking", "desc": "Monthly allowance from parents"},
        {"type": "Income", "cat": "Scholarship", "amount": 5000.0, "date": date(2026, 9, 10), "method": "Net Banking", "desc": "Merit semester scholarship"},
        {"type": "Income", "cat": "Part-time Work", "amount": 3000.0, "date": date(2026, 9, 18), "method": "UPI", "desc": "Maths tutoring junior students"},
        {"type": "Expense", "cat": "Food", "amount": 3200.0, "date": date(2026, 9, 3), "method": "UPI", "desc": "Mess fees and grocery fruits"},
        {"type": "Expense", "cat": "Transport", "amount": 750.0, "date": date(2026, 9, 7), "method": "UPI", "desc": "Metro card reload & auto fare"},
        {"type": "Expense", "cat": "Education", "amount": 850.0, "date": date(2026, 9, 12), "method": "Debit Card", "desc": "Practical lab assignment journal"},
        {"type": "Expense", "cat": "Shopping", "amount": 1550.0, "date": date(2026, 9, 16), "method": "UPI", "desc": "Raincoat & waterproof backpack"},
        {"type": "Expense", "cat": "Entertainment", "amount": 500.0, "date": date(2026, 9, 22), "method": "Cash", "desc": "Department freshers social contribution"},
        {"type": "Expense", "cat": "Healthcare", "amount": 420.0, "date": date(2026, 9, 25), "method": "UPI", "desc": "Doctor consultation & fever medicines"},
        {"type": "Expense", "cat": "Bills", "amount": 350.0, "date": date(2026, 9, 28), "method": "UPI", "desc": "Hostel room shared Wi-Fi bill"},

        # October 2026 (Current Active Month)
        {"type": "Income", "cat": "Allowance", "amount": 10000.0, "date": date(2026, 10, 1), "method": "Net Banking", "desc": "Monthly allowance from parents"},
        {"type": "Income", "cat": "Freelancing", "amount": 6000.0, "date": date(2026, 10, 8), "method": "UPI", "desc": "Python Flask backend consulting"},
        {"type": "Income", "cat": "Gift", "amount": 1500.0, "date": date(2026, 10, 15), "method": "UPI", "desc": "Birthday gift from elder brother"},
        {"type": "Expense", "cat": "Food", "amount": 2900.0, "date": date(2026, 10, 3), "method": "UPI", "desc": "Hostel mess & canteen coupons"},
        {"type": "Expense", "cat": "Food", "amount": 380.0, "date": date(2026, 10, 11), "method": "UPI", "desc": "Evening tea and snacks with group"},
        {"type": "Expense", "cat": "Transport", "amount": 800.0, "date": date(2026, 10, 5), "method": "UPI", "desc": "Monthly bus pass recharge"},
        {"type": "Expense", "cat": "Transport", "amount": 180.0, "date": date(2026, 10, 14), "method": "Cash", "desc": "Auto fare for project field visit"},
        {"type": "Expense", "cat": "Education", "amount": 1250.0, "date": date(2026, 10, 9), "method": "Debit Card", "desc": "Software Engineering project printout & binding"},
        {"type": "Expense", "cat": "Accommodation", "amount": 600.0, "date": date(2026, 10, 7), "method": "Cash", "desc": "Hostel room laundry services"},
        {"type": "Expense", "cat": "Bills", "amount": 499.0, "date": date(2026, 10, 12), "method": "UPI", "desc": "Monthly high-speed data recharge"},
        {"type": "Expense", "cat": "Shopping", "amount": 850.0, "date": date(2026, 10, 18), "method": "UPI", "desc": "Stationery pens, notebook & flash drive"},
        {"type": "Expense", "cat": "Entertainment", "amount": 620.0, "date": date(2026, 10, 22), "method": "UPI", "desc": "Fest weekend food court celebration"},
    ]

    for item in demo_transactions:
        cat_id = categories.get(item["cat"])
        if cat_id:
            t = Transaction(
                user_id=1,
                category_id=cat_id,
                type=item["type"],
                amount=Decimal(str(item["amount"])),
                date=item["date"],
                payment_method=item["method"],
                description=item["desc"],
            )
            db.session.add(t)

    # Monthly Budgets for October 2026
    demo_budgets = [
        {"cat": "Food", "amount": 3500.0, "month": 10, "year": 2026},
        {"cat": "Transport", "amount": 1200.0, "month": 10, "year": 2026},
        {"cat": "Education", "amount": 2000.0, "month": 10, "year": 2026},
        {"cat": "Shopping", "amount": 1500.0, "month": 10, "year": 2026},
        {"cat": "Bills", "amount": 600.0, "month": 10, "year": 2026},
        {"cat": "Entertainment", "amount": 800.0, "month": 10, "year": 2026},
        {"cat": "Accommodation", "amount": 800.0, "month": 10, "year": 2026},
    ]

    for b_item in demo_budgets:
        cat_id = categories.get(b_item["cat"])
        if cat_id:
            existing = Budget.query.filter_by(category_id=cat_id, month=b_item["month"], year=b_item["year"]).first()
            if not existing:
                b = Budget(
                    user_id=1,
                    category_id=cat_id,
                    month=b_item["month"],
                    year=b_item["year"],
                    amount=Decimal(str(b_item["amount"]))
                )
                db.session.add(b)

    db.session.commit()
    return True, "Successfully loaded demo transactions and monthly budgets."


def clear_demo_data():
    """
    Clears transactions and budgets for starting with a fresh clean slate.
    Preserves user profile and categories.
    """
    Transaction.query.delete()
    Budget.query.delete()
    db.session.commit()
    return True, "All transactions and budgets cleared successfully."
