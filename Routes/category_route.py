from flask import Blueprint, request
from Services.category_service import CategoryService
from Utils.helpers import success_response, error_response

category_bp = Blueprint("category_bp", __name__)


@category_bp.route("", methods=["GET"])
def get_categories():
    """Retrieve all categories with optional type filtering."""
    try:
        cat_type = request.args.get("type")
        categories = CategoryService.get_all(cat_type)
        return success_response(data=categories, message=f"Retrieved {len(categories)} category(ies).")
    except Exception as e:
        return error_response(message="Failed to fetch categories.", errors=[str(e)], status_code=500)


@category_bp.route("/<int:cat_id>", methods=["GET"])
def get_category(cat_id):
    """Retrieve a single category by ID."""
    try:
        cat = CategoryService.get_by_id(cat_id)
        if not cat:
            return error_response(message=f"Category with ID {cat_id} not found.", status_code=404)
        return success_response(data=cat, message="Category retrieved successfully.")
    except Exception as e:
        return error_response(message="Failed to fetch category.", errors=[str(e)], status_code=500)


@category_bp.route("", methods=["POST"])
def create_category():
    """Create a new category."""
    try:
        payload = request.get_json()
        if not payload:
            return error_response(message="JSON body is required.", status_code=400)

        created, err = CategoryService.create(payload)
        if err:
            return error_response(message=err, status_code=400)

        return success_response(data=created, message="Category created successfully.", status_code=201)
    except Exception as e:
        return error_response(message="Failed to create category.", errors=[str(e)], status_code=500)


@category_bp.route("/<int:cat_id>", methods=["PUT"])
def update_category(cat_id):
    """Update a category."""
    try:
        payload = request.get_json()
        if not payload:
            return error_response(message="JSON body is required.", status_code=400)

        updated, err = CategoryService.update(cat_id, payload)
        if err:
            status_code = 404 if "not found" in err.lower() else 400
            return error_response(message=err, status_code=status_code)

        return success_response(data=updated, message="Category updated successfully.")
    except Exception as e:
        return error_response(message="Failed to update category.", errors=[str(e)], status_code=500)


@category_bp.route("/<int:cat_id>", methods=["DELETE"])
def delete_category(cat_id):
    """Delete a category with foreign key validation."""
    try:
        success, msg = CategoryService.delete(cat_id)
        if not success:
            status_code = 404 if "not found" in msg.lower() else 400
            return error_response(message=msg, status_code=status_code)
        return success_response(data={"id": cat_id}, message=msg)
    except Exception as e:
        return error_response(message="Failed to delete category.", errors=[str(e)], status_code=500)
