from datetime import date
from sqlalchemy import or_
from DataBase.database import db
from Modules.models import Transaction, Category
from Utils.helpers import parse_and_validate_amount, parse_and_validate_date


class TransactionService:
    @staticmethod
    def get_all(filters=None):
        filters = filters or {}
        query = Transaction.query.join(Category, Transaction.category_id == Category.id)

        # Filter by type
        t_type = filters.get("type")
        if t_type in ["Income", "Expense"]:
            query = query.filter(Transaction.type == t_type)

        # Filter by category
        cat_id = filters.get("category_id")
        if cat_id:
            try:
                query = query.filter(Transaction.category_id == int(cat_id))
            except (ValueError, TypeError):
                pass

        # Filter by date range
        start_date = filters.get("start_date")
        if start_date:
            d, err = parse_and_validate_date(start_date)
            if d:
                query = query.filter(Transaction.date >= d)

        end_date = filters.get("end_date")
        if end_date:
            d, err = parse_and_validate_date(end_date)
            if d:
                query = query.filter(Transaction.date <= d)

        # Filter by month and year if explicitly provided
        month = filters.get("month")
        year = filters.get("year")
        if month:
            try:
                query = query.filter(db.extract("month", Transaction.date) == int(month))
            except (ValueError, TypeError):
                pass
        if year:
            try:
                query = query.filter(db.extract("year", Transaction.date) == int(year))
            except (ValueError, TypeError):
                pass

        # Search keyword
        search = filters.get("search")
        if search:
            search_term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Transaction.description.ilike(search_term),
                    Transaction.payment_method.ilike(search_term),
                    Category.name.ilike(search_term),
                )
            )

        # Sorting
        sort_by = filters.get("sort_by", "date").lower()
        sort_order = filters.get("sort_order", "desc").lower()

        if sort_by == "amount":
            order_col = Transaction.amount.asc() if sort_order == "asc" else Transaction.amount.desc()
        else:
            order_col = Transaction.date.asc() if sort_order == "asc" else Transaction.date.desc()

        # Secondary sort by ID desc for consistent ordering
        query = query.order_by(order_col, Transaction.id.desc())

        limit = filters.get("limit")
        if limit:
            try:
                query = query.limit(int(limit))
            except (ValueError, TypeError):
                pass

        return [t.to_dict() for t in query.all()]

    @staticmethod
    def get_by_id(trans_id):
        t = db.session.get(Transaction, trans_id)
        return t.to_dict() if t else None

    @staticmethod
    def create(data):
        # Validate Amount
        amount, err = parse_and_validate_amount(data.get("amount"))
        if err:
            return None, err

        # Validate Type
        t_type = str(data.get("type", "")).strip().capitalize()
        if t_type not in ["Income", "Expense"]:
            return None, "Transaction type must be 'Income' or 'Expense'."

        # Validate Category
        category_id = data.get("category_id")
        if not category_id:
            return None, "Category is required."
        try:
            category_id = int(category_id)
        except (ValueError, TypeError):
            return None, "Invalid category identifier."

        cat = db.session.get(Category, category_id)
        if not cat:
            return None, "Selected category does not exist."
        if cat.type != t_type:
            return None, f"Category '{cat.name}' is an {cat.type} category, but transaction is '{t_type}'."

        # Validate Date
        t_date, err = parse_and_validate_date(data.get("date"))
        if err:
            return None, err

        payment_method = str(data.get("payment_method", "UPI")).strip() or "UPI"
        description = str(data.get("description", "")).strip()

        transaction = Transaction(
            user_id=1,
            category_id=category_id,
            type=t_type,
            amount=amount,
            date=t_date,
            payment_method=payment_method,
            description=description,
        )

        db.session.add(transaction)
        db.session.commit()
        return transaction.to_dict(), None

    @staticmethod
    def update(trans_id, data):
        t = db.session.get(Transaction, trans_id)
        if not t:
            return None, "Transaction not found."

        # Amount update if supplied
        if "amount" in data:
            amount, err = parse_and_validate_amount(data.get("amount"))
            if err:
                return None, err
            t.amount = amount

        # Type update if supplied
        if "type" in data:
            t_type = str(data.get("type", "")).strip().capitalize()
            if t_type not in ["Income", "Expense"]:
                return None, "Transaction type must be 'Income' or 'Expense'."
            t.type = t_type

        # Category update if supplied
        if "category_id" in data:
            try:
                cat_id = int(data.get("category_id"))
                cat = db.session.get(Category, cat_id)
                if not cat:
                    return None, "Selected category does not exist."
                if cat.type != t.type:
                    return None, f"Category '{cat.name}' type ({cat.type}) must match transaction type ({t.type})."
                t.category_id = cat_id
            except (ValueError, TypeError):
                return None, "Invalid category identifier."

        # Date update if supplied
        if "date" in data:
            t_date, err = parse_and_validate_date(data.get("date"))
            if err:
                return None, err
            t.date = t_date

        if "payment_method" in data:
            t.payment_method = str(data.get("payment_method", "UPI")).strip() or "UPI"

        if "description" in data:
            t.description = str(data.get("description", "")).strip()

        db.session.commit()
        return t.to_dict(), None

    @staticmethod
    def delete(trans_id):
        t = db.session.get(Transaction, trans_id)
        if not t:
            return False, "Transaction not found."
        db.session.delete(t)
        db.session.commit()
        return True, "Transaction deleted successfully."
