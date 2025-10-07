from fastapi.testclient import TestClient
from datetime import datetime, timezone
import pytest
from tests.conftest import create_product, create_customer, create_order, add_review

def test_top_products(client: TestClient):
    """Test the top products endpoint.

    Args:
        client (TestClient): The test client.
    Returns:
        None
    """
    p1 = create_product(client, "Prod A", 10.0)
    p2 = create_product(client, "Prod B", 20.0)
    c = create_customer(client, 1)

    create_order(client, c["customer_id"], [
        {"product_id": p1["product_id"], "quantity": 3},
        {"product_id": p2["product_id"], "quantity": 1},
    ])
    create_order(client, c["customer_id"], [
        {"product_id": p1["product_id"], "quantity": 2},
    ])

    resp = client.get("/analytics/top-products?limit=2")
    assert resp.status_code == 200
    data = resp.json()

    assert len(data) == 2
    assert data[0]["name"] == "Prod A"
    assert data[0]["quantity_sold"] == 5
    assert data[1]["name"] == "Prod B"
    assert data[1]["quantity_sold"] == 1

def test_revenue_by_month(client: TestClient):
    """Test revenue by month.

    Args:
        client (TestClient): The test client.
    Returns:
        None
    """
    c = create_customer(client, 2)
    p1 = create_product(client, "Phone", 500.0)
    p2 = create_product(client, "Case", 20.0)


    create_order(client, c["customer_id"], [
        {"product_id": p1["product_id"], "quantity": 1},
        {"product_id": p2["product_id"], "quantity": 2},
    ])


    create_order(client, c["customer_id"], [
        {"product_id": p1["product_id"], "quantity": 2},
    ])

    expected_total = 1540.0
    this_month = datetime.now(timezone.utc).strftime("%Y-%m")

    resp = client.get("/analytics/revenue-by-month")
    assert resp.status_code == 200
    data = resp.json()

    row = next((r for r in data if r["month"] == this_month), None)
    assert row is not None, f"Expected a row for {this_month}, got {data}"
    assert row["revenue"] == pytest.approx(expected_total)
    assert row["orders"] >= 2

def test_revenue_by_customer(client: TestClient):
    """Test revenue by customer.

    Args:
        client (TestClient): The test client.
    Returns:
        None
    """
    c1 = create_customer(client, 3)
    c2 = create_customer(client, 4)
    p = create_product(client, "Widget", 50.0)

    create_order(client, c1["customer_id"], [
        {"product_id": p["product_id"], "quantity": 1}
    ])

    create_order(client, c2["customer_id"], [
        {"product_id": p["product_id"], "quantity": 3}
    ])

    resp = client.get("/analytics/revenue-by-customer?limit=2")
    assert resp.status_code == 200
    data = resp.json()

    assert len(data) >= 2

    assert data[0]["customer_id"] == c2["customer_id"]
    assert data[0]["revenue"] == pytest.approx(150.0)

    assert data[1]["customer_id"] == c1["customer_id"]
    assert data[1]["revenue"] == pytest.approx(50.0)

def test_repeat_customers(client: TestClient):
    c1 = create_customer(client, 5)
    c2 = create_customer(client, 6)
    p = create_product(client, "Thing", 10.0)

    for _ in range(3):
        create_order(client, c1["customer_id"], [
            {"product_id": p["product_id"], "quantity": 1}
        ])

    create_order(client, c2["customer_id"], [
        {"product_id": p["product_id"], "quantity": 1}
    ])

    resp = client.get("/analytics/repeat-customers?min_orders=2")
    assert resp.status_code == 200
    data = resp.json()

    ids = [r["customer_id"] for r in data]
    assert c1["customer_id"] in ids
    assert c2["customer_id"] not in ids

def test_order_value_stats(client: TestClient):
    """Test order value statistics.

    Args:
        client (TestClient): The test client.
    Returns:
        None
    """
    c = create_customer(client, 7)
    p1 = create_product(client, "A", 10.0)
    p2 = create_product(client, "B", 25.0)

    create_order(client, c["customer_id"], [
        {"product_id": p1["product_id"], "quantity": 1}
    ])

    create_order(client, c["customer_id"], [
        {"product_id": p2["product_id"], "quantity": 2}
    ])

    create_order(client, c["customer_id"], [
        {"product_id": p1["product_id"], "quantity": 1},
        {"product_id": p2["product_id"], "quantity": 2}
    ])

    resp = client.get("/analytics/order-value-stats")
    assert resp.status_code == 200
    data = resp.json()

    assert data["min_value"] == pytest.approx(10.0)
    assert data["max_value"] == pytest.approx(60.0)
    assert data["avg_value"] == pytest.approx((10 + 50 + 60) / 3)

def test_product_ratings_with_customer(client: TestClient):
    """Test product ratings analytics using reviews tied to customers.

    Args:
        client (TestClient): The test client.
    Returns:
        None
    """
    c1 = create_customer(client, 1)
    c2 = create_customer(client, 2)

    p1 = create_product(client, "Headphones", 50.0)
    p2 = create_product(client, "Speaker", 100.0)

    add_review(client, c1["customer_id"], p1["product_id"], 5)
    add_review(client, c2["customer_id"], p1["product_id"], 4)
    add_review(client, c1["customer_id"], p2["product_id"], 3)
    add_review(client, c2["customer_id"], p2["product_id"], 2)

    resp = client.get("/analytics/review-summary")
    assert resp.status_code == 200
    data = resp.json()

    assert isinstance(data, list)
    assert len(data) == 2

    row1 = next(r for r in data if r["product_id"] == p1["product_id"])
    assert row1["avg_rating"] == pytest.approx(4.5)
    assert row1["review_count"] == 2

    row2 = next(r for r in data if r["product_id"] == p2["product_id"])
    assert row2["avg_rating"] == pytest.approx(2.5)
    assert row2["review_count"] == 2
