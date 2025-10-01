from fastapi.testclient import TestClient


def test_create_order(client: TestClient):
    """Test creating a new order.

    Args:
        client (TestClient): The test client for making requests.
    Returns:
        _type_: The created order.
    """
    customer = client.post("/customers/", json={
        "first_name": "OrderUser",
        "last_name": "Test",
        "email": "orderuser@example.com"
    }).json()

    product = client.post("/products/", json={
        "name": "Headphones",
        "category": "Audio",
        "price": 89.99
    }).json()

    response = client.post("/orders/", json={
        "customer_id": customer["customer_id"],
        "items": [
            {"product_id": product["product_id"], "quantity": 2}
        ]
    })

    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == customer["customer_id"]
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product["product_id"]
    assert data["items"][0]["quantity"] == 2

def test_read_orders(client: TestClient):
    """Test reading all orders.

    Args:
        client (TestClient): The test client for making requests.

    Returns:
        _type_: List of orders.
    """
    customer = client.post("/customers/", json={
        "first_name": "Read",
        "last_name": "Tester",
        "email": "read@test.com"
    }).json()

    product = client.post("/products/", json={
        "name": "Read Product",
        "category": "Test",
        "price": 15.99
    }).json()

    client.post("/orders/", json={
        "customer_id": customer["customer_id"],
        "items": [{"product_id": product["product_id"], "quantity": 1}]
    })

    response = client.get("/orders/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["customer_id"] == customer["customer_id"]

def test_read_order_by_id(client: TestClient):
    """Test reading an order by ID.

    Args:
        client (TestClient): The test client for making requests.

    Returns:
        _type_: The order with the specified ID.
    """
    customer = client.post("/customers/", json={
        "first_name": "Single",
        "last_name": "Tester",
        "email": "single@test.com"
    }).json()

    product = client.post("/products/", json={
        "name": "Single Product",
        "category": "Test",
        "price": 25.00
    }).json()

    created = client.post("/orders/", json={
        "customer_id": customer["customer_id"],
        "items": [{"product_id": product["product_id"], "quantity": 3}]
    }).json()
    order_id = created["order_id"]

    response = client.get(f"/orders/{order_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == order_id
    assert data["customer_id"] == customer["customer_id"]

def test_read_order_not_found(client: TestClient):
    """Test reading an order that does not exist.

    Args:
        client (TestClient): The test client for making requests.
    Returns:
        _type_: Error response indicating order not found.
    """
    response = client.get("/orders/9999")
    assert response.status_code == 404
    error = response.json()["detail"]
    assert error["code"] == 404
    assert error["message"] == "Order not found"
    assert error["resource"] == "Order"

def test_update_order_status(client: TestClient):
    """Test updating the status of an existing order.

    Args:
        client (TestClient): The test client for making requests.

    Returns:
        _type_: The updated order.
    """
    customer = client.post("/customers/", json={
        "first_name": "Update",
        "last_name": "Tester",
        "email": "update@test.com"
    }).json()

    product = client.post("/products/", json={
        "name": "Update Product",
        "category": "Test",
        "price": 40.00
    }).json()

    created = client.post("/orders/", json={
        "customer_id": customer["customer_id"],
        "items": [{"product_id": product["product_id"], "quantity": 2}]
    }).json()
    order_id = created["order_id"]

    response = client.put(f"/orders/{order_id}", json={"status": "shipped"})

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "shipped"

def test_update_order_not_found(client: TestClient):
    """Test updating an order that does not exist.

    Args:
        client (TestClient): The test client for making requests.
    Returns:
        _type_: Error response indicating order not found.
    """
    response = client.put("/orders/9999", json={"status": "canceled"})
    assert response.status_code == 404
    error = response.json()["detail"]
    assert error["message"] == "Order not found"

def test_delete_order(client: TestClient):
    """Test deleting an existing order.

    Args:
        client (TestClient): The test client for making requests.
    Returns:
        _type_: A message indicating successful deletion.
    """
    customer = client.post("/customers/", json={
        "first_name": "Delete",
        "last_name": "Tester",
        "email": "delete@test.com"
    }).json()

    product = client.post("/products/", json={
        "name": "Delete Product",
        "category": "Test",
        "price": 15.00
    }).json()

    created = client.post("/orders/", json={
        "customer_id": customer["customer_id"],
        "items": [{"product_id": product["product_id"], "quantity": 1}]
    }).json()
    order_id = created["order_id"]

    response = client.delete(f"/orders/{order_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Order deleted"

    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 404

def test_delete_order_not_found(client: TestClient):
    """Test deleting an order that does not exist.

    Args:
        client (TestClient): The test client for making requests.
    Returns:
        _type_: Error response indicating order not found.
    """
    response = client.delete("/orders/9999")
    assert response.status_code == 404
    error = response.json()["detail"]
    assert error["message"] == "Order not found"