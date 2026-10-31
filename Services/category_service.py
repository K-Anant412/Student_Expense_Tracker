from DataBase.database import db
from Modules.models import Category, Transaction, Budget


class CategoryService:
    @staticmethod
    def get_all(type_filter=None):
        query = Category.query
        if type_filter in ["Income", "Expense"]:
            query = query.filter_by(type=type_filter)
        return [c.to_dict() for c in query.order_by(Category.name.asc()).all()]

    @staticmethod
    def get_by_id(cat_id):
        cat = db.session.get(Category, cat_id)
        return cat.to_dict() if cat else None

    @staticmethod
    def create(data):
        name = str(data.get("name", "")).strip()
        cat_type = str(data.get("type", "")).strip().capitalize()
        description = str(data.get("description", "")).strip()

        if not name:
            return None, "Category name is required."
        if cat_type not in ["Income", "Expense"]:
            return None, "Category type must be either 'Income' or 'Expense'."

        # Check for duplicate
        existing = Category.query.filter(
            db.func.lower(Category.name) == name.lower(),
            Category.type == cat_type
        ).first()
        if existing:
            return None, f"A category named '{name}' already exists under '{cat_type}'."

        category = Category(
            name=name,
            type=cat_type,
            description=description,
            is_default=False
        )
        db.session.add(category)
        db.session.commit()
        return category.to_dict(), None

    @staticmethod
    def update(cat_id, data):
        cat = db.session.get(Category, cat_id)
        if not cat:
            return None, "Category not found."

        name = str(data.get("name", cat.name)).strip()
        cat_type = str(data.get("type", cat.type)).strip().capitalize()
        description = str(data.get("description", cat.description or "")).strip()

        if not name:
            return None, "Category name cannot be empty."
        if cat_type not in ["Income", "Expense"]:
            return None, "Category type must be either 'Income' or 'Expense'."

        # Check duplicate
        existing = Category.query.filter(
            db.func.lower(Category.name) == name.lower(),
            Category.type == cat_type,
            Category.id != cat_id
        ).first()
        if existing:
            return None, f"Another category named '{name}' already exists under '{cat_type}'."

        cat.name = name
        cat.type = cat_type
        cat.description = description
        db.session.commit()
        return cat.to_dict(), None

    @staticmethod
    def delete(cat_id):
        cat = db.session.get(Category, cat_id)
        if not cat:
            return False, "Category not found."

        # Prevent unsafe deletion if referenced by transactions
        trans_count = Transaction.query.filter_by(category_id=cat_id).count()
        if trans_count > 0:
            return False, f"Cannot delete category '{cat.name}' because it is used by {trans_count} transaction(s)."

        # Prevent unsafe deletion if referenced by active budgets
        budget_count = Budget.query.filter_by(category_id=cat_id).count()
        if budget_count > 0:
            return False, f"Cannot delete category '{cat.name}' because it is referenced by {budget_count} budget(s)."

        db.session.delete(cat)
        db.session.commit()
        return True, f"Category '{cat.name}' deleted successfully."
