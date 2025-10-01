import pytest

def test_create_shipment(client):
    customer = client.post("/customers/", json={
        "first_name": "ShipUser",
        "last_name": "Test",
        "email": "shipcreate@example.com"
    }).json()

    product = client.post("/products/", json={
        "name": "Camera",
        "category": "Electronics",
        "price": 499.99
    }).json()

    order = client.post("/orders/", json={
        "customer_id": customer["customer_id"],
        "items": [{"product_id": product["product_id"], "quantity": 1}]
    }).json()

    response = client.post("/shipments/", json={
        "order_id": order["order_id"],
        "status": "processing",
        "tracking_number": "TRACK-CREATE"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == order["order_id"]
    assert data["tracking_number"] == "TRACK-CREATE"


def test_read_shipments(client):
    response = client.get("/shipments/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_shipment_by_id(client):
    customer = client.post("/customers/", json={
        "first_name": "ShipSingle",
        "last_name": "User",
        "email": "shipread@example.com"
    }).json()

    product = client.post("/products/", json={
        "name": "Mouse",
        "category": "Accessories",
        "price": 29.99
    }).json()

    order = client.post("/orders/", json={
        "customer_id": customer["customer_id"],
        "items": [{"product_id": product["product_id"], "quantity": 1}]
    }).json()

    shipment = client.post("/shipments/", json={
        "order_id": order["order_id"],
        "tracking_number": "TRACK-READ"
    }).json()

    response = client.get(f"/shipments/{shipment['shipment_id']}")
    assert response.status_code == 200
    assert response.json()["shipment_id"] == shipment["shipment_id"]


def test_read_shipment_not_found(client):
    response = client.get("/shipments/9999")
    assert response.status_code == 404


def test_update_shipment(client):
    customer = client.post("/customers/", json={
        "first_name": "ShipUpdate",
        "last_name": "User",
        "email": "shipupdate@example.com"
    }).json()

    product = client.post("/products/", json={
        "name": "Keyboard",
        "category": "Accessories",
        "price": 59.99
    }).json()

    order = client.post("/orders/", json={
        "customer_id": customer["customer_id"],
        "items": [{"product_id": product["product_id"], "quantity": 1}]
    }).json()

    shipment = client.post("/shipments/", json={
        "order_id": order["order_id"],
        "tracking_number": "TRACK-UPDATE"
    }).json()

    response = client.put(f"/shipments/{shipment['shipment_id']}", json={
        "status": "shipped",
        "tracking_number": "TRACK-UPDATED"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "shipped"
    assert data["tracking_number"] == "TRACK-UPDATED"


def test_update_shipment_not_found(client):
    response = client.put("/shipments/9999", json={"status": "delivered"})
    assert response.status_code == 404


def test_delete_shipment(client):
    customer = client.post("/customers/", json={
        "first_name": "ShipDelete",
        "last_name": "User",
        "email": "shipdelete@example.com"
    }).json()

    product = client.post("/products/", json={
        "name": "Tablet",
        "category": "Electronics",
        "price": 399.99
    }).json()

    order = client.post("/orders/", json={
        "customer_id": customer["customer_id"],
        "items": [{"product_id": product["product_id"], "quantity": 1}]
    }).json()

    shipment = client.post("/shipments/", json={
        "order_id": order["order_id"],
        "tracking_number": "TRACK-DELETE"
    }).json()

    response = client.delete(f"/shipments/{shipment['shipment_id']}")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]


def test_delete_shipment_not_found(client):
    response = client.delete("/shipments/9999")
    assert response.status_code == 404


def test_create_duplicate_shipment_for_order(client):
    customer = client.post("/customers/", json={
        "first_name": "ShipConstraint",
        "last_name": "User",
        "email": "shipdup@example.com"
    }).json()

    product = client.post("/products/", json={
        "name": "Console",
        "category": "Electronics",
        "price": 299.99
    }).json()

    order = client.post("/orders/", json={
        "customer_id": customer["customer_id"],
        "items": [{"product_id": product["product_id"], "quantity": 1}]
    }).json()

    first = client.post("/shipments/", json={
        "order_id": order["order_id"],
        "tracking_number": "TRACK-DUP-1"
    })
    assert first.status_code == 200

    second = client.post("/shipments/", json={
        "order_id": order["order_id"],
        "tracking_number": "TRACK-DUP-2"
    })
    assert second.status_code == 400
    assert "only have one shipment" in second.json()["detail"]


def test_create_duplicate_tracking_number(client):
    customer1 = client.post("/customers/", json={
        "first_name": "ShipTrack1",
        "last_name": "User",
        "email": "shiptrack1@example.com"
    }).json()

    product1 = client.post("/products/", json={
        "name": "Phone",
        "category": "Electronics",
        "price": 699.99
    }).json()

    order1 = client.post("/orders/", json={
        "customer_id": customer1["customer_id"],
        "items": [{"product_id": product1["product_id"], "quantity": 1}]
    }).json()

    customer2 = client.post("/customers/", json={
        "first_name": "ShipTrack2",
        "last_name": "User",
        "email": "shiptrack2@example.com"
    }).json()

    product2 = client.post("/products/", json={
        "name": "Laptop",
        "category": "Electronics",
        "price": 1299.99
    }).json()

    order2 = client.post("/orders/", json={
        "customer_id": customer2["customer_id"],
        "items": [{"product_id": product2["product_id"], "quantity": 1}]
    }).json()

    first = client.post("/shipments/", json={
        "order_id": order1["order_id"],
        "tracking_number": "TRACK-UNIQUE"
    })
    assert first.status_code == 200

    second = client.post("/shipments/", json={
        "order_id": order2["order_id"],
        "tracking_number": "TRACK-UNIQUE"
    })
    assert second.status_code == 400
    assert "Tracking number must be unique" in second.json()["detail"]
