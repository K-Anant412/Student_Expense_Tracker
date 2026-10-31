import pytest
from decimal import Decimal
from Utils.helpers import (
    calculate_utilization,
    parse_and_validate_amount,
    parse_and_validate_date,
    format_inr
)


def test_financial_calculations_benchmark():
    """
    Benchmark Test from Project Requirements:
    - Recorded income: ₹10,000
    - Recorded expenses: ₹4,000
    - Net recorded balance: ₹6,000
    - Category budget: ₹5,000
    - Category expenses: ₹4,000
    - Budget utilization: 80.0%
    - Remaining category budget: ₹1,000
    """
    income = 10000.00
    expenses = 4000.00
    net_balance = round(income - expenses, 2)
    assert net_balance == 6000.00

    budget = 5000.00
    category_expenses = 4000.00
    utilization = calculate_utilization(category_expenses, budget)
    remaining = round(budget - category_expenses, 2)

    assert utilization == 80.0
    assert remaining == 1000.00


def test_budget_utilization_edge_cases():
    # Zero budget should return 0.0 without division by zero error
    assert calculate_utilization(500, 0) == 0.0
    assert calculate_utilization(0, 0) == 0.0
    assert calculate_utilization(None, 0) == 0.0

    # Over budget (>100%)
    assert calculate_utilization(6000, 5000) == 120.0

    # Zero spending
    assert calculate_utilization(0, 5000) == 0.0


def test_parse_and_validate_amount():
    # Valid positive amounts
    amt, err = parse_and_validate_amount("250.50")
    assert err is None
    assert amt == Decimal("250.50")

    amt, err = parse_and_validate_amount(100)
    assert err is None
    assert amt == Decimal("100")

    # Invalid non-positive amounts
    amt, err = parse_and_validate_amount("0")
    assert amt is None
    assert "greater than zero" in err.lower()

    amt, err = parse_and_validate_amount("-50")
    assert amt is None
    assert "greater than zero" in err.lower()

    # Invalid string format
    amt, err = parse_and_validate_amount("abc")
    assert amt is None
    assert "valid positive number" in err.lower()

    amt, err = parse_and_validate_amount("")
    assert amt is None
    assert "required" in err.lower()


def test_parse_and_validate_date():
    from datetime import date
    d, err = parse_and_validate_date("2026-10-15")
    assert err is None
    assert d == date(2026, 10, 15)

    d, err = parse_and_validate_date("invalid-date")
    assert d is None
    assert "format" in err.lower()


def test_currency_formatting():
    assert format_inr(1500) == "₹1,500.00"
    assert format_inr(0) == "₹0.00"
    assert format_inr(1000000.5) == "₹1,000,000.50"
