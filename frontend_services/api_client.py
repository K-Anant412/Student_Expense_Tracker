import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000/api").rstrip("/")
TIMEOUT = 6  # seconds


class APIClient:
    """
    HTTP client for Streamlit UI to communicate with the Flask REST API.
    Guarantees that Streamlit never touches MySQL directly.
    Provides robust offline fallback and informative error reporting.
    """

    @staticmethod
    def _request(method, endpoint, params=None, json_data=None):
        url = f"{API_BASE_URL}/{endpoint.lstrip('/')}"
        try:
            resp = requests.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=TIMEOUT,
                headers={"Content-Type": "application/json"}
            )
            try:
                data = resp.json()
            except ValueError:
                data = {"success": resp.ok, "message": resp.text}

            return {
                "ok": resp.ok,
                "status_code": resp.status_code,
                "data": data.get("data") if isinstance(data, dict) else data,
                "message": data.get("message", "Success") if isinstance(data, dict) else str(data),
                "errors": data.get("errors", []) if isinstance(data, dict) else [],
            }
        except requests.exceptions.ConnectionError:
            return {
                "ok": False,
                "status_code": 503,
                "data": None,
                "message": "Cannot connect to Flask API server. Please ensure Flask is running on http://127.0.0.1:5000.",
                "errors": ["Connection refused"],
            }
        except requests.exceptions.Timeout:
            return {
                "ok": False,
                "status_code": 504,
                "data": None,
                "message": "Request to Flask API timed out. Please try again.",
                "errors": ["Request timeout"],
            }
        except Exception as e:
            return {
                "ok": False,
                "status_code": 500,
                "data": None,
                "message": f"An unexpected network error occurred: {str(e)}",
                "errors": [str(e)],
            }

    # Health Check
    @classmethod
    def check_health(cls):
        return cls._request("GET", "health")

    # Dashboard & Analytics
    @classmethod
    def get_dashboard(cls, month=None, year=None):
        params = {}
        if month:
            params["month"] = month
        if year:
            params["year"] = year
        return cls._request("GET", "dashboard", params=params)

    @classmethod
    def get_analytics(cls, month=None, year=None, start_date=None, end_date=None):
        params = {}
        if month:
            params["month"] = month
        if year:
            params["year"] = year
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return cls._request("GET", "analytics", params=params)

    # Transactions
    @classmethod
    def get_transactions(cls, filters=None):
        return cls._request("GET", "transactions", params=filters)

    @classmethod
    def get_transaction(cls, trans_id):
        return cls._request("GET", f"transactions/{trans_id}")

    @classmethod
    def create_transaction(cls, payload):
        return cls._request("POST", "transactions", json_data=payload)

    @classmethod
    def update_transaction(cls, trans_id, payload):
        return cls._request("PUT", f"transactions/{trans_id}", json_data=payload)

    @classmethod
    def delete_transaction(cls, trans_id):
        return cls._request("DELETE", f"transactions/{trans_id}")

    # Categories
    @classmethod
    def get_categories(cls, cat_type=None):
        params = {"type": cat_type} if cat_type else None
        return cls._request("GET", "categories", params=params)

    @classmethod
    def create_category(cls, payload):
        return cls._request("POST", "categories", json_data=payload)

    @classmethod
    def delete_category(cls, cat_id):
        return cls._request("DELETE", f"categories/{cat_id}")

    # Budgets
    @classmethod
    def get_budgets(cls, month=None, year=None):
        params = {}
        if month:
            params["month"] = month
        if year:
            params["year"] = year
        return cls._request("GET", "budgets", params=params)

    @classmethod
    def get_budget_status(cls, month=None, year=None, threshold=80.0):
        params = {"threshold": threshold}
        if month:
            params["month"] = month
        if year:
            params["year"] = year
        return cls._request("GET", "budgets/status", params=params)

    @classmethod
    def create_budget(cls, payload):
        return cls._request("POST", "budgets", json_data=payload)

    @classmethod
    def update_budget(cls, budget_id, payload):
        return cls._request("PUT", f"budgets/{budget_id}", json_data=payload)

    @classmethod
    def delete_budget(cls, budget_id):
        return cls._request("DELETE", f"budgets/{budget_id}")

    # Reports
    @classmethod
    def get_report_data(cls, filters=None):
        return cls._request("GET", "reports/transactions", params=filters)

    # Demo Data
    @classmethod
    def seed_demo_data(cls, force=True):
        params = {"force": "true" if force else "false"}
        return cls._request("POST", "demo-data/seed", params=params)

    @classmethod
    def clear_demo_data(cls):
        return cls._request("POST", "demo-data/clear")
