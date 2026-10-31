from flask import Blueprint, request
from Services.transaction_service import TransactionService
from Utils.helpers import success_response, error_response

transaction_bp = Blueprint("transaction_bp", __name__)


@transaction_bp.route("", methods=["GET"])
def get_transactions():
    """Retrieve transactions with optional filtering and sorting."""
    try:
        filters = {
            "type": request.args.get("type"),
            "category_id": request.args.get("category_id"),
            "start_date": request.args.get("start_date"),
            "end_date": request.args.get("end_date"),
            "month": request.args.get("month"),
            "year": request.args.get("year"),
            "search": request.args.get("search"),
            "sort_by": request.args.get("sort_by", "date"),
            "sort_order": request.args.get("sort_order", "desc"),
            "limit": request.args.get("limit"),
        }
        transactions = TransactionService.get_all(filters)
        return success_response(data=transactions, message=f"Retrieved {len(transactions)} transaction(s).")
    except Exception as e:
        return error_response(message="Failed to retrieve transactions.", errors=[str(e)], status_code=500)


@transaction_bp.route("/<int:trans_id>", methods=["GET"])
def get_transaction(trans_id):
    """Retrieve a single transaction by ID."""
    try:
        t = TransactionService.get_by_id(trans_id)
        if not t:
            return error_response(message=f"Transaction with ID {trans_id} not found.", status_code=404)
        return success_response(data=t, message="Transaction retrieved successfully.")
    except Exception as e:
        return error_response(message="Failed to fetch transaction.", errors=[str(e)], status_code=500)


@transaction_bp.route("", methods=["POST"])
def create_transaction():
    """Create a new financial transaction."""
    try:
        payload = request.get_json()
        if not payload:
            return error_response(message="JSON body is required.", status_code=400)

        created, err = TransactionService.create(payload)
        if err:
            return error_response(message=err, status_code=400)

        return success_response(data=created, message="Transaction recorded successfully.", status_code=201)
    except Exception as e:
        return error_response(message="Failed to create transaction.", errors=[str(e)], status_code=500)


@transaction_bp.route("/<int:trans_id>", methods=["PUT"])
def update_transaction(trans_id):
    """Update an existing transaction."""
    try:
        payload = request.get_json()
        if not payload:
            return error_response(message="JSON body is required.", status_code=400)

        updated, err = TransactionService.update(trans_id, payload)
        if err:
            status_code = 404 if "not found" in err.lower() else 400
            return error_response(message=err, status_code=status_code)

        return success_response(data=updated, message="Transaction updated successfully.")
    except Exception as e:
        return error_response(message="Failed to update transaction.", errors=[str(e)], status_code=500)


@transaction_bp.route("/<int:trans_id>", methods=["DELETE"])
def delete_transaction(trans_id):
    """Delete a transaction by ID."""
    try:
        success, msg = TransactionService.delete(trans_id)
        if not success:
            return error_response(message=msg, status_code=404)
        return success_response(data={"id": trans_id}, message=msg)
    except Exception as e:
        return error_response(message="Failed to delete transaction.", errors=[str(e)], status_code=500)
