from calendar import monthrange, month_name
from datetime import date, datetime, timedelta
from decimal import Decimal
from sqlalchemy import func, extract
from DataBase.database import db
from Modules.models import Transaction, Category, Budget
from Services.budget_service import BudgetService
from Utils.helpers import calculate_utilization, parse_and_validate_date


class AnalyticsService:
    @staticmethod
    def get_dashboard_summary(month=None, year=None):
        today = date.today()
        sel_month = int(month) if month else today.month
        sel_year = int(year) if year else today.year

        _, last_day = monthrange(sel_year, sel_month)
        start_date = date(sel_year, sel_month, 1)
        end_date = date(sel_year, sel_month, last_day)

        # 1. Total Income for month
        total_income = db.session.query(func.coalesce(func.sum(Transaction.amount), 0))\
            .filter(
                Transaction.type == "Income",
                Transaction.date >= start_date,
                Transaction.date <= end_date
            ).scalar()
        total_income = float(total_income or 0.0)

        # 2. Total Expenses for month
        total_expenses = db.session.query(func.coalesce(func.sum(Transaction.amount), 0))\
            .filter(
                Transaction.type == "Expense",
                Transaction.date >= start_date,
                Transaction.date <= end_date
            ).scalar()
        total_expenses = float(total_expenses or 0.0)

        # 3. Net Recorded Balance
        net_balance = round(total_income - total_expenses, 2)

        # 4. Number of transactions
        transaction_count = Transaction.query.filter(
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).count()

        # 5. Highest-spending expense category
        top_cat = db.session.query(
            Category.name,
            func.sum(Transaction.amount).label("total")
        ).join(Category, Transaction.category_id == Category.id)\
            .filter(
                Transaction.type == "Expense",
                Transaction.date >= start_date,
                Transaction.date <= end_date
            ).group_by(Category.name)\
            .order_by(func.sum(Transaction.amount).desc())\
            .first()

        highest_spending_category = {
            "name": top_cat[0] if top_cat else "None",
            "amount": float(top_cat[1]) if top_cat else 0.0
        }

        # 6. Budget status & utilization
        budget_status = BudgetService.get_budget_status(sel_month, sel_year)
        total_budget = budget_status["total_budget"]
        budget_utilization = budget_status["overall_utilization"]

        # Budget warnings
        budget_warnings = [
            item for item in budget_status["items"] if item["is_warning"] or item["is_exceeded"]
        ]

        # 7. Category-wise expense chart data
        category_breakdown = db.session.query(
            Category.name,
            func.sum(Transaction.amount).label("amount")
        ).join(Category, Transaction.category_id == Category.id)\
            .filter(
                Transaction.type == "Expense",
                Transaction.date >= start_date,
                Transaction.date <= end_date
            ).group_by(Category.name)\
            .order_by(func.sum(Transaction.amount).desc()).all()

        category_expenses = [
            {"category": row[0], "amount": float(row[1])} for row in category_breakdown
        ]

        # 8. Monthly Income vs Expenses (Last 6 months trend)
        monthly_trend = []
        for i in range(5, -1, -1):
            # calculate year and month i months ago
            m = sel_month - i
            y = sel_year
            while m <= 0:
                m += 12
                y -= 1
            _, m_last = monthrange(y, m)
            m_start = date(y, m, 1)
            m_end = date(y, m, m_last)

            inc = db.session.query(func.coalesce(func.sum(Transaction.amount), 0))\
                .filter(Transaction.type == "Income", Transaction.date >= m_start, Transaction.date <= m_end).scalar()
            exp = db.session.query(func.coalesce(func.sum(Transaction.amount), 0))\
                .filter(Transaction.type == "Expense", Transaction.date >= m_start, Transaction.date <= m_end).scalar()

            monthly_trend.append({
                "month_name": f"{month_name[m][:3]} {y}",
                "month": m,
                "year": y,
                "income": float(inc or 0.0),
                "expense": float(exp or 0.0),
                "net": float((inc or 0.0) - (exp or 0.0))
            })

        # 9. Recent transactions
        recent_records = Transaction.query.order_by(Transaction.date.desc(), Transaction.id.desc()).limit(8).all()
        recent_transactions = [t.to_dict() for t in recent_records]

        return {
            "selected_month": sel_month,
            "selected_year": sel_year,
            "selected_month_name": month_name[sel_month],
            "total_income": round(total_income, 2),
            "total_expenses": round(total_expenses, 2),
            "net_balance": net_balance,
            "total_budget": total_budget,
            "budget_utilization": budget_utilization,
            "transaction_count": transaction_count,
            "highest_spending_category": highest_spending_category,
            "budget_warnings": budget_warnings,
            "category_expenses": category_expenses,
            "monthly_trend": monthly_trend,
            "recent_transactions": recent_transactions,
        }

    @staticmethod
    def get_spending_analytics(month=None, year=None, start_date=None, end_date=None):
        today = date.today()
        sel_month = int(month) if month else today.month
        sel_year = int(year) if year else today.year

        if start_date and end_date:
            d_start, _ = parse_and_validate_date(start_date)
            d_end, _ = parse_and_validate_date(end_date)
        else:
            _, last_day = monthrange(sel_year, sel_month)
            d_start = date(sel_year, sel_month, 1)
            d_end = date(sel_year, sel_month, last_day)

        # Total income & expense in period
        inc = db.session.query(func.coalesce(func.sum(Transaction.amount), 0))\
            .filter(Transaction.type == "Income", Transaction.date >= d_start, Transaction.date <= d_end).scalar()
        exp = db.session.query(func.coalesce(func.sum(Transaction.amount), 0))\
            .filter(Transaction.type == "Expense", Transaction.date >= d_start, Transaction.date <= d_end).scalar()

        total_income = float(inc or 0.0)
        total_expenses = float(exp or 0.0)
        net_savings = round(total_income - total_expenses, 2)

        # Category distribution
        cat_data = db.session.query(
            Category.name,
            func.sum(Transaction.amount).label("total")
        ).join(Category, Transaction.category_id == Category.id)\
            .filter(Transaction.type == "Expense", Transaction.date >= d_start, Transaction.date <= d_end)\
            .group_by(Category.name)\
            .order_by(func.sum(Transaction.amount).desc()).all()

        category_distribution = []
        for row in cat_data:
            c_name = row[0]
            c_amt = float(row[1])
            pct = round((c_amt / total_expenses * 100), 2) if total_expenses > 0 else 0.0
            category_distribution.append({
                "category": c_name,
                "amount": c_amt,
                "percentage": pct
            })

        # Top 5 spending categories
        top_categories = category_distribution[:5]

        # Previous month comparison
        prev_m = sel_month - 1
        prev_y = sel_year
        if prev_m <= 0:
            prev_m = 12
            prev_y -= 1
        _, prev_last = monthrange(prev_y, prev_m)
        p_start = date(prev_y, prev_m, 1)
        p_end = date(prev_y, prev_m, prev_last)

        prev_inc = db.session.query(func.coalesce(func.sum(Transaction.amount), 0))\
            .filter(Transaction.type == "Income", Transaction.date >= p_start, Transaction.date <= p_end).scalar()
        prev_exp = db.session.query(func.coalesce(func.sum(Transaction.amount), 0))\
            .filter(Transaction.type == "Expense", Transaction.date >= p_start, Transaction.date <= p_end).scalar()

        prev_income = float(prev_inc or 0.0)
        prev_expenses = float(prev_exp or 0.0)

        expense_change_amount = round(total_expenses - prev_expenses, 2)
        income_change_amount = round(total_income - prev_income, 2)
        expense_change_pct = round(((total_expenses - prev_expenses) / prev_expenses) * 100, 2) if prev_expenses > 0 else 0.0

        # Multi-month history for average calculations
        months_history = []
        for i in range(11, -1, -1):
            m = sel_month - i
            y = sel_year
            while m <= 0:
                m += 12
                y -= 1
            _, m_last = monthrange(y, m)
            m_s = date(y, m, 1)
            m_e = date(y, m, m_last)

            m_inc = db.session.query(func.coalesce(func.sum(Transaction.amount), 0))\
                .filter(Transaction.type == "Income", Transaction.date >= m_s, Transaction.date <= m_e).scalar()
            m_exp = db.session.query(func.coalesce(func.sum(Transaction.amount), 0))\
                .filter(Transaction.type == "Expense", Transaction.date >= m_s, Transaction.date <= m_e).scalar()

            months_history.append({
                "period": f"{month_name[m][:3]} {y}",
                "month": m,
                "year": y,
                "income": float(m_inc or 0.0),
                "expense": float(m_exp or 0.0),
                "savings": float((m_inc or 0.0) - (m_exp or 0.0)),
            })

        active_expense_months = [m["expense"] for m in months_history if m["expense"] > 0]
        avg_monthly_expense = round(sum(active_expense_months) / len(active_expense_months), 2) if active_expense_months else round(total_expenses, 2)

        return {
            "start_date": d_start.strftime("%Y-%m-%d"),
            "end_date": d_end.strftime("%Y-%m-%d"),
            "selected_month": sel_month,
            "selected_year": sel_year,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_savings": net_savings,
            "category_distribution": category_distribution,
            "top_categories": top_categories,
            "avg_monthly_expense": avg_monthly_expense,
            "comparison_with_previous": {
                "previous_month_name": f"{month_name[prev_m]} {prev_y}",
                "previous_income": prev_income,
                "previous_expenses": prev_expenses,
                "expense_change_amount": expense_change_amount,
                "expense_change_pct": expense_change_pct,
                "income_change_amount": income_change_amount,
            },
            "history_trend": months_history,
        }

    @staticmethod
    def get_report_data(filters=None):
        from Services.transaction_service import TransactionService

        transactions = TransactionService.get_all(filters)

        total_income = sum(t["amount"] for t in transactions if t["type"] == "Income")
        total_expenses = sum(t["amount"] for t in transactions if t["type"] == "Expense")
        net_balance = round(total_income - total_expenses, 2)

        return {
            "period": {
                "start_date": filters.get("start_date") if filters else None,
                "end_date": filters.get("end_date") if filters else None,
                "type": filters.get("type", "All"),
                "category_id": filters.get("category_id", "All")
            },
            "summary": {
                "total_transactions": len(transactions),
                "total_income": round(total_income, 2),
                "total_expenses": round(total_expenses, 2),
                "net_recorded_balance": net_balance
            },
            "transactions": transactions
        }
