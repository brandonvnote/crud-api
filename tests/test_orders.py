from fastapi.testclient import TestClient


def test_create_order(client: TestClient):
    # Arrange: create customer + product first
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

    # Act: create order with one item
    response = client.post("/orders/", json={
        "customer_id": customer["customer_id"],
        "items": [
            {"product_id": product["product_id"], "quantity": 2}
        ]
    })

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == customer["customer_id"]
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product["product_id"]
    assert data["items"][0]["quantity"] == 2

def test_read_orders(client: TestClient):
    # Arrange: create customer + product + order
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

    # Act
    response = client.get("/orders/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["customer_id"] == customer["customer_id"]

def test_read_order_by_id(client: TestClient):
    # Arrange
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

    # Act
    response = client.get(f"/orders/{order_id}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == order_id
    assert data["customer_id"] == customer["customer_id"]


def test_read_order_not_found(client: TestClient):
    response = client.get("/orders/9999")
    assert response.status_code == 404
    error = response.json()["detail"]
    assert error["code"] == 404
    assert error["message"] == "Order not found"
    assert error["resource"] == "Order"

def test_update_order_status(client: TestClient):
    # Arrange: create order
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

    # Act
    response = client.put(f"/orders/{order_id}", json={"status": "shipped"})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "shipped"


def test_update_order_not_found(client: TestClient):
    response = client.put("/orders/9999", json={"status": "canceled"})
    assert response.status_code == 404
    error = response.json()["detail"]
    assert error["message"] == "Order not found"

def test_delete_order(client: TestClient):
    # Arrange
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

    # Act
    response = client.delete(f"/orders/{order_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Order deleted"

    # Verify gone
    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 404

def test_delete_order_not_found(client: TestClient):
    response = client.delete("/orders/9999")
    assert response.status_code == 404
    error = response.json()["detail"]
    assert error["message"] == "Order not found"