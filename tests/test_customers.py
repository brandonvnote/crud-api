def test_create_customer(client):
    response = client.post("/customers/", json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Alice"
    assert "customer_id" in data

def test_read_customers(client):
    # Arrange: create a customer
    client.post("/customers/", json={
        "first_name": "Bob",
        "last_name": "Jones",
        "email": "bob@example.com"
    })

    # Act: fetch all customers
    response = client.get("/customers/")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["first_name"] == "Bob"
