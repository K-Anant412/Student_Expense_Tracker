from calendar import monthrange
from datetime import date
from decimal import Decimal
from DataBase.database import db
from Modules.models import Budget, Category, Transaction
from Utils.helpers import parse_and_validate_amount, calculate_utilization


class BudgetService:
    @staticmethod
    def get_all(month=None, year=None):
        query = Budget.query.join(Category, Budget.category_id == Category.id)
        if month:
            query = query.filter(Budget.month == int(month))
        if year:
            query = query.filter(Budget.year == int(year))
        return [b.to_dict() for b in query.order_by(Budget.year.desc(), Budget.month.desc(), Category.name.asc()).all()]

    @staticmethod
    def get_by_id(budget_id):
        b = db.session.get(Budget, budget_id)
        return b.to_dict() if b else None

    @staticmethod
    def create(data):
        amount, err = parse_and_validate_amount(data.get("amount"))
        if err:
            return None, err

        try:
            category_id = int(data.get("category_id"))
            month = int(data.get("month"))
            year = int(data.get("year"))
        except (ValueError, TypeError):
            return None, "Category, month, and year must be valid numbers."

        if not (1 <= month <= 12):
            return None, "Month must be between 1 and 12."
        if year < 2000 or year > 2100:
            return None, "Year must be a valid 4-digit calendar year."

        cat = db.session.get(Category, category_id)
        if not cat:
            return None, "Category not found."
        if cat.type != "Expense":
            return None, f"Budgets can only be set for Expense categories. '{cat.name}' is an Income category."

        # Check for existing budget for same category, month, and year
        existing = Budget.query.filter_by(category_id=category_id, month=month, year=year).first()
        if existing:
            return None, f"A budget for '{cat.name}' in {month}/{year} already exists. Please edit the existing budget."

        budget = Budget(
            user_id=1,
            category_id=category_id,
            month=month,
            year=year,
            amount=amount,
        )
        db.session.add(budget)
        db.session.commit()
        return budget.to_dict(), None

    @staticmethod
    def update(budget_id, data):
        b = db.session.get(Budget, budget_id)
        if not b:
            return None, "Budget record not found."

        if "amount" in data:
            amount, err = parse_and_validate_amount(data.get("amount"))
            if err:
                return None, err
            b.amount = amount

        if "month" in data or "year" in data or "category_id" in data:
            new_cat_id = int(data.get("category_id", b.category_id))
            new_month = int(data.get("month", b.month))
            new_year = int(data.get("year", b.year))

            if not (1 <= new_month <= 12):
                return None, "Month must be between 1 and 12."

            cat = db.session.get(Category, new_cat_id)
            if not cat or cat.type != "Expense":
                return None, "Invalid expense category."

            # Check duplicate conflict
            conflict = Budget.query.filter(
                Budget.category_id == new_cat_id,
                Budget.month == new_month,
                Budget.year == new_year,
                Budget.id != budget_id
            ).first()
            if conflict:
                return None, f"Another budget already exists for '{cat.name}' in {new_month}/{new_year}."

            b.category_id = new_cat_id
            b.month = new_month
            b.year = new_year

        db.session.commit()
        return b.to_dict(), None

    @staticmethod
    def delete(budget_id):
        b = db.session.get(Budget, budget_id)
        if not b:
            return False, "Budget record not found."
        db.session.delete(b)
        db.session.commit()
        return True, "Budget deleted successfully."

    @staticmethod
    def get_budget_status(month, year, warning_threshold=80.0):
        """
        Calculates category spending against configured budgets for a specific month and year.
        Returns a list of category budget comparisons and summary stats.
        """
        month = int(month)
        year = int(year)

        # Date boundaries for the month
        _, last_day = monthrange(year, month)
        start_date = date(year, month, 1)
        end_date = date(year, month, last_day)

        # Fetch all budgets for this month/year
        budgets = Budget.query.join(Category, Budget.category_id == Category.id)\
            .filter(Budget.month == month, Budget.year == year)\
            .order_by(Category.name.asc()).all()

        # Compute actual expense sums by category for this period
        expense_sums = db.session.query(
            Transaction.category_id,
            db.func.sum(Transaction.amount).label("total_spent")
        ).filter(
            Transaction.type == "Expense",
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).group_by(Transaction.category_id).all()

        spent_dict = {row.category_id: float(row.total_spent or 0.0) for row in expense_sums}

        budget_items = []
        total_budget_sum = 0.0
        total_spent_budgeted = 0.0
        warnings_count = 0
        exceeded_count = 0

        for b in budgets:
            b_amount = float(b.amount)
            spent = spent_dict.get(b.category_id, 0.0)
            remaining = b_amount - spent
            utilization = calculate_utilization(spent, b_amount)
            
            is_exceeded = spent > b_amount
            is_warning = (utilization >= warning_threshold) and not is_exceeded

            if is_exceeded:
                status = "Exceeded"
                exceeded_count += 1
            elif is_warning:
                status = "Warning"
                warnings_count += 1
            else:
                status = "Normal"

            total_budget_sum += b_amount
            total_spent_budgeted += spent

            budget_items.append({
                "budget_id": b.id,
                "category_id": b.category_id,
                "category_name": b.category.name,
                "month": month,
                "year": year,
                "budget_amount": b_amount,
                "spent_amount": round(spent, 2),
                "remaining_amount": round(remaining, 2),
                "utilization_percentage": utilization,
                "is_warning": is_warning,
                "is_exceeded": is_exceeded,
                "status": status,
            })

        overall_utilization = calculate_utilization(total_spent_budgeted, total_budget_sum)

        return {
            "month": month,
            "year": year,
            "total_budget": round(total_budget_sum, 2),
            "total_spent_in_budgeted_categories": round(total_spent_budgeted, 2),
            "overall_remaining": round(total_budget_sum - total_spent_budgeted, 2),
            "overall_utilization": overall_utilization,
            "warnings_count": warnings_count,
            "exceeded_count": exceeded_count,
            "items": budget_items,
        }
