import pytest
from app import app
from DataBase.database import db
from Modules.models import Category, Transaction, Budget


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"


def test_categories_endpoint(client):
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert len(data["data"]) >= 15  # Default categories seeded


def test_transaction_crud_and_validation(client):
    # 1. Reject transaction with non-positive amount
    resp_invalid = client.post("/api/transactions", json={
        "type": "Expense",
        "category_id": 1,
        "amount": -100,
        "date": "2026-10-31"
    })
    assert resp_invalid.status_code == 400
    assert "greater than zero" in resp_invalid.get_json()["message"]

    # 2. Reject transaction with missing category
    resp_no_cat = client.post("/api/transactions", json={
        "type": "Expense",
        "category_id": 99999,
        "amount": 250.0,
        "date": "2026-10-31"
    })
    assert resp_no_cat.status_code == 400

    # 3. Create valid Expense transaction
    with app.app_context():
        food_cat = Category.query.filter_by(name="Food", type="Expense").first()
        assert food_cat is not None
        food_cat_id = food_cat.id

    resp_create = client.post("/api/transactions", json={
        "type": "Expense",
        "category_id": food_cat_id,
        "amount": 450.00,
        "date": "2026-10-31",
        "payment_method": "UPI",
        "description": "Pytest Cafeteria Lunch"
    })
    assert resp_create.status_code == 201
    created_tx = resp_create.get_json()["data"]
    tx_id = created_tx["id"]
    assert created_tx["amount"] == 450.00
    assert created_tx["type"] == "Expense"

    # 4. Retrieve created transaction by ID
    resp_get = client.get(f"/api/transactions/{tx_id}")
    assert resp_get.status_code == 200
    assert resp_get.get_json()["data"]["id"] == tx_id

    # 5. Update transaction
    resp_update = client.put(f"/api/transactions/{tx_id}", json={
        "amount": 500.00,
        "description": "Updated Cafeteria Lunch"
    })
    assert resp_update.status_code == 200
    assert resp_update.get_json()["data"]["amount"] == 500.00

    # 6. Delete transaction
    resp_del = client.delete(f"/api/transactions/{tx_id}")
    assert resp_del.status_code == 200

    # 7. Verify 404 for deleted transaction
    resp_after = client.get(f"/api/transactions/{tx_id}")
    assert resp_after.status_code == 404


def test_budget_creation_and_duplicate_rejection(client):
    with app.app_context():
        trans_cat = Category.query.filter_by(name="Transport", type="Expense").first()
        assert trans_cat is not None
        cat_id = trans_cat.id

    # Clean existing test budget if any
    with app.app_context():
        Budget.query.filter_by(category_id=cat_id, month=11, year=2026).delete()
        db.session.commit()

    # Create budget
    resp_b1 = client.post("/api/budgets", json={
        "category_id": cat_id,
        "month": 11,
        "year": 2026,
        "amount": 1500.00
    })
    assert resp_b1.status_code == 201

    # Attempt duplicate budget for same category, month, and year -> should reject
    resp_b_dup = client.post("/api/budgets", json={
        "category_id": cat_id,
        "month": 11,
        "year": 2026,
        "amount": 2000.00
    })
    assert resp_b_dup.status_code == 400
    assert "already exists" in resp_b_dup.get_json()["message"]


def test_dashboard_and_analytics_endpoints(client):
    resp_dash = client.get("/api/dashboard?month=10&year=2026")
    assert resp_dash.status_code == 200
    dash_data = resp_dash.get_json()["data"]
    assert "total_income" in dash_data
    assert "total_expenses" in dash_data
    assert "net_balance" in dash_data
    assert "monthly_trend" in dash_data

    resp_an = client.get("/api/analytics?month=10&year=2026")
    assert resp_an.status_code == 200
    an_data = resp_an.get_json()["data"]
    assert "category_distribution" in an_data
    assert "comparison_with_previous" in an_data


def test_reports_endpoint(client):
    resp_rep = client.get("/api/reports/transactions?type=Expense")
    assert resp_rep.status_code == 200
    rep_data = resp_rep.get_json()["data"]
    assert "summary" in rep_data
    assert "transactions" in rep_data
