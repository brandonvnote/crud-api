def test_create_order(client):
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
