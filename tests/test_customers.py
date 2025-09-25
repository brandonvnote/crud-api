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

def test_read_customer_by_id(client):
    # Arrange: create a customer
    create_response = client.post("/customers/", json={
        "first_name": "Charlie",
        "last_name": "Brown",
        "email": "charlie@example.com"
    })
    created = create_response.json()
    customer_id = created["customer_id"]

    # Act: fetch the customer by ID
    response = client.get(f"/customers/{customer_id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Charlie"
    assert data["customer_id"] == customer_id

def test_read_customer_not_found(client):
    response = client.get("/customers/9999")  # ID that doesn't exist
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Customer not found"
