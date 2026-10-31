from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from flask import jsonify


def success_response(data=None, message="Operation successful", status_code=200):
    """Generates a standardized JSON success response."""
    response = {
        "success": True,
        "message": message,
        "data": data if data is not None else {}
    }
    return jsonify(response), status_code


def error_response(message="An error occurred", errors=None, status_code=400):
    """Generates a standardized JSON error response."""
    response = {
        "success": False,
        "message": message,
        "errors": errors or []
    }
    return jsonify(response), status_code


def parse_and_validate_amount(val):
    """
    Validates that amount is positive and greater than zero.
    Returns (Decimal, None) or (None, error_message).
    """
    if val is None or val == "":
        return None, "Amount is required."
    try:
        amt = Decimal(str(val).strip())
        if amt <= 0:
            return None, "Amount must be strictly greater than zero."
        return amt, None
    except (InvalidOperation, ValueError, TypeError):
        return None, "Amount must be a valid positive number."


def parse_and_validate_date(val):
    """
    Validates date string in YYYY-MM-DD format.
    Returns (datetime.date, None) or (None, error_message).
    """
    if not val:
        return date.today(), None
    if isinstance(val, date):
        return val, None
    try:
        d = datetime.strptime(str(val).strip(), "%Y-%m-%d").date()
        return d, None
    except (ValueError, TypeError):
        return None, "Date must be in valid YYYY-MM-DD format."


def calculate_utilization(spent, budget):
    """
    Calculates budget utilization percentage safely.
    Handles zero budget, negative values, and None safely.
    """
    if not budget or float(budget) <= 0:
        return 0.0
    spent_val = float(spent or 0.0)
    budget_val = float(budget)
    return round((spent_val / budget_val) * 100.0, 2)


def format_inr(val):
    """Formats a number into Indian Rupee representation (e.g., ₹1,500.00)."""
    if val is None:
        return "₹0.00"
    try:
        return f"₹{float(val):,.2f}"
    except (ValueError, TypeError):
        return "₹0.00"
