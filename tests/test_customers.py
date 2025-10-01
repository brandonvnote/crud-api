from fastapi.testclient import TestClient


def test_create_customer(client: TestClient):
    """Test creating a new customer.

    Args:
        client (TestClient): The test client for making requests.
   
    Returns:
        _type_: The created customer.
    """
    response = client.post("/customers/", json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Alice"
    assert "customer_id" in data

def test_read_customers(client: TestClient):
    """Test reading all customers.

    Args:
        client (TestClient): The test client for making requests.
    
    Returns:
        _type_: List of customers.
    """
    client.post("/customers/", json={
        "first_name": "Bob",
        "last_name": "Jones",
        "email": "bob@example.com"
    })

    response = client.get("/customers/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["first_name"] == "Bob"

def test_read_customer_by_id(client: TestClient):
    """Test reading a customer by ID.

    Args:
        client (TestClient): The test client for making requests.
    Returns:
        _type_: The customer with the specified ID.
    """
    create_response = client.post("/customers/", json={
        "first_name": "Charlie",
        "last_name": "Brown",
        "email": "charlie@example.com"
    })
    created = create_response.json()
    customer_id = created["customer_id"]

    response = client.get(f"/customers/{customer_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Charlie"
    assert data["customer_id"] == customer_id

def test_read_customer_not_found(client: TestClient):
    """Test reading a customer that does not exist.

    Args:
        client (TestClient): The test client for making requests.
    Returns:
        _type_: Error response indicating customer not found.
    """
    response = client.get("/customers/9999")
    print(response.json())
    assert response.status_code == 404
    error = response.json()["detail"]
    assert error["code"] == 404
    assert error["message"] == "Customer not found"
    assert error["resource"] == "Customer"

def test_count_customers(client: TestClient):
    """Test counting all customers.

    Args:
        client (TestClient): The test client for making requests.
    Returns:
        _type_: The count of customers.
    """
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

def test_update_customer(client: TestClient):
    """Test updating an existing customer.

    Args:
        client (TestClient): The test client for making requests.
    Returns:
        _type_: The updated customer.
    """
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

def test_update_customer_not_found(client: TestClient):
    """Test updating a customer that does not exist.

    Args:
        client (TestClient): The test client for making requests.
    Returns:
        _type_: Error response indicating customer not found.
    """
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

def test_delete_customer(client: TestClient):
    """Test deleting an existing customer.

    Args:
        client (TestClient): The test client for making requests.
    Returns:
        _type_: Confirmation of deletion.
    """
    
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

def test_delete_customer_not_found(client: TestClient):
    """Test deleting a customer that does not exist.

    Args:
        client (TestClient): The test client for making requests.
    Returns:
        _type_: Error response indicating customer not found.
    """
    response = client.delete("/customers/9999")  # an ID that won’t exist
    assert response.status_code == 404
    data = response.json()["detail"]
    assert data["code"] == 404
    assert data["message"] == "Customer not found"
    assert data["resource"] == "Customer"
