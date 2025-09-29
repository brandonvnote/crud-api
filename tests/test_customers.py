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
    print(response.json())
    assert response.status_code == 404
    error = response.json()["detail"]
    assert error["code"] == 404
    assert error["message"] == "Customer not found"
    assert error["resource"] == "Customer"

def test_count_customers(client):
    
    client.post("/customers/", json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice_count@example.com"
    })
    client.post("/customers/", json={
        "first_name": "Bob",
        "last_name": "Jones",
        "email": "bob_count@example.com"
    })

    
    response = client.get("/customers/count")

    
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2

def test_update_customer(client):
    
    create_response = client.post("/customers/", json={
        "first_name": "Dana",
        "last_name": "White",
        "email": "dana@example.com"
    })
    created = create_response.json()
    customer_id = created["customer_id"]

    
    response = client.put(f"/customers/{customer_id}", json={
        "first_name": "DanaUpdated",
        "last_name": "White",
        "email": "dana.updated@example.com"
    })

    
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "DanaUpdated"
    assert data["email"] == "dana.updated@example.com"

def test_update_customer_not_found(client):
    response = client.put("/customers/9999", json={
        "first_name": "Ghost",
        "last_name": "User",
        "email": "ghost@example.com"
    })
    assert response.status_code == 404
    data = response.json()["detail"]
    assert data["code"] == 404
    assert data["message"] == "Customer not found"
    assert data["resource"] == "Customer"

def test_delete_customer(client):
    
    create_response = client.post("/customers/", json={
        "first_name": "Eve",
        "last_name": "Stone",
        "email": "eve@example.com"
    })
    created = create_response.json()
    customer_id = created["customer_id"]

    
    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Customer deleted"

    
    get_response = client.get(f"/customers/{customer_id}")
    assert get_response.status_code == 404

def test_delete_customer_not_found(client):
    response = client.delete("/customers/9999")  # an ID that won’t exist
    assert response.status_code == 404
    data = response.json()["detail"]
    assert data["code"] == 404
    assert data["message"] == "Customer not found"
    assert data["resource"] == "Customer"
