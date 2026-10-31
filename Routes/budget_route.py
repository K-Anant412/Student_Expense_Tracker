from datetime import date
from flask import Blueprint, request
from Services.budget_service import BudgetService
from Utils.helpers import success_response, error_response

budget_bp = Blueprint("budget_bp", __name__)


@budget_bp.route("", methods=["GET"])
def get_budgets():
    """Retrieve monthly category budgets with optional month and year filters."""
    try:
        month = request.args.get("month")
        year = request.args.get("year")
        budgets = BudgetService.get_all(month, year)
        return success_response(data=budgets, message=f"Retrieved {len(budgets)} budget record(s).")
    except Exception as e:
        return error_response(message="Failed to fetch budgets.", errors=[str(e)], status_code=500)


@budget_bp.route("/status", methods=["GET"])
def get_budget_status():
    """Calculates category spending against configured budgets for a month/year."""
    try:
        today = date.today()
        month = request.args.get("month", today.month)
        year = request.args.get("year", today.year)
        threshold = float(request.args.get("threshold", 80.0))

        status_data = BudgetService.get_budget_status(month, year, threshold)
        return success_response(data=status_data, message="Budget status calculated successfully.")
    except Exception as e:
        return error_response(message="Failed to calculate budget status.", errors=[str(e)], status_code=500)


@budget_bp.route("/<int:budget_id>", methods=["GET"])
def get_budget(budget_id):
    """Retrieve a single budget record."""
    try:
        b = BudgetService.get_by_id(budget_id)
        if not b:
            return error_response(message=f"Budget with ID {budget_id} not found.", status_code=404)
        return success_response(data=b, message="Budget record retrieved successfully.")
    except Exception as e:
        return error_response(message="Failed to fetch budget.", errors=[str(e)], status_code=500)


@budget_bp.route("", methods=["POST"])
def create_budget():
    """Create a new monthly category budget."""
    try:
        payload = request.get_json()
        if not payload:
            return error_response(message="JSON body is required.", status_code=400)

        created, err = BudgetService.create(payload)
        if err:
            return error_response(message=err, status_code=400)

        return success_response(data=created, message="Budget set successfully.", status_code=201)
    except Exception as e:
        return error_response(message="Failed to set budget.", errors=[str(e)], status_code=500)


@budget_bp.route("/<int:budget_id>", methods=["PUT"])
def update_budget(budget_id):
    """Update an existing budget."""
    try:
        payload = request.get_json()
        if not payload:
            return error_response(message="JSON body is required.", status_code=400)

        updated, err = BudgetService.update(budget_id, payload)
        if err:
            status_code = 404 if "not found" in err.lower() else 400
            return error_response(message=err, status_code=status_code)

        return success_response(data=updated, message="Budget updated successfully.")
    except Exception as e:
        return error_response(message="Failed to update budget.", errors=[str(e)], status_code=500)


@budget_bp.route("/<int:budget_id>", methods=["DELETE"])
def delete_budget(budget_id):
    """Delete a budget record."""
    try:
        success, msg = BudgetService.delete(budget_id)
        if not success:
            return error_response(message=msg, status_code=404)
        return success_response(data={"id": budget_id}, message=msg)
    except Exception as e:
        return error_response(message="Failed to delete budget.", errors=[str(e)], status_code=500)
