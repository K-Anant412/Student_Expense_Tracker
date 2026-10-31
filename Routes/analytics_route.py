from datetime import date
from flask import Blueprint, request
from Services.analytics_service import AnalyticsService
from Services.demo_data_service import seed_demo_data, clear_demo_data
from Utils.helpers import success_response, error_response

analytics_bp = Blueprint("analytics_bp", __name__)


@analytics_bp.route("/dashboard", methods=["GET"])
def get_dashboard():
    """Retrieve full dashboard summary for selected month and year."""
    try:
        month = request.args.get("month")
        year = request.args.get("year")
        data = AnalyticsService.get_dashboard_summary(month, year)
        return success_response(data=data, message="Dashboard summary retrieved successfully.")
    except Exception as e:
        return error_response(message="Failed to load dashboard summary.", errors=[str(e)], status_code=500)


@analytics_bp.route("/analytics", methods=["GET"])
def get_analytics():
    """Retrieve in-depth spending analytics and comparative insights."""
    try:
        month = request.args.get("month")
        year = request.args.get("year")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        data = AnalyticsService.get_spending_analytics(month, year, start_date, end_date)
        return success_response(data=data, message="Spending analytics loaded successfully.")
    except Exception as e:
        return error_response(message="Failed to load spending analytics.", errors=[str(e)], status_code=500)


@analytics_bp.route("/reports/transactions", methods=["GET"])
def get_report():
    """Retrieve filtered transaction records and report summary for export."""
    try:
        filters = {
            "type": request.args.get("type"),
            "category_id": request.args.get("category_id"),
            "start_date": request.args.get("start_date"),
            "end_date": request.args.get("end_date"),
            "search": request.args.get("search"),
            "sort_by": request.args.get("sort_by", "date"),
            "sort_order": request.args.get("sort_order", "desc"),
        }
        report_data = AnalyticsService.get_report_data(filters)
        return success_response(data=report_data, message="Transaction report data generated.")
    except Exception as e:
        return error_response(message="Failed to generate report data.", errors=[str(e)], status_code=500)


@analytics_bp.route("/demo-data/seed", methods=["POST"])
def seed_demo():
    """Seeds demonstration transactions and budgets."""
    try:
        force = request.args.get("force", "false").lower() == "true"
        success, msg = seed_demo_data(force=force)
        if not success:
            return error_response(message=msg, status_code=400)
        return success_response(message=msg)
    except Exception as e:
        return error_response(message="Failed to seed demo data.", errors=[str(e)], status_code=500)


@analytics_bp.route("/demo-data/clear", methods=["POST"])
def clear_demo():
    """Clears all transactions and budgets for starting fresh."""
    try:
        success, msg = clear_demo_data()
        return success_response(message=msg)
    except Exception as e:
        return error_response(message="Failed to clear data.", errors=[str(e)], status_code=500)
