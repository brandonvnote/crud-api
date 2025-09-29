def test_create_product(client):
    response = client.post("/products/", json={
        "name": "Laptop",
        "category": "Electronics",
        "price": 1299.99
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Laptop"
    assert "product_id" in data

def test_read_products(client):
    
    client.post("/products/", json={
        "name": "Phone",
        "category": "Electronics",
        "price": 599.99
    })

    
    response = client.get("/products/")

    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Phone"

def test_read_product_by_id(client):
    
    create_response = client.post("/products/", json={
        "name": "Tablet",
        "category": "Electronics",
        "price": 299.99
    })
    created = create_response.json()
    product_id = created["product_id"]

    
    response = client.get(f"/products/{product_id}")

    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Tablet"
    assert data["product_id"] == product_id


def test_read_product_not_found(client):
    response = client.get("/products/9999")
    assert response.status_code == 404
    error = response.json()["detail"]
    assert error["code"] == 404
    assert error["message"] == "Product not found"
    assert error["resource"] == "Product"

def test_update_product(client):
    
    create_response = client.post("/products/", json={
        "name": "Monitor",
        "category": "Electronics",
        "price": 199.99
    })
    created = create_response.json()
    product_id = created["product_id"]

    
    response = client.put(f"/products/{product_id}", json={
        "name": "Monitor Updated",
        "price": 179.99
    })

    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Monitor Updated"
    assert data["price"] == 179.99


def test_update_product_not_found(client):
    response = client.put("/products/9999", json={"name": "Ghost"})
    assert response.status_code == 404
    error = response.json()["detail"]
    assert error["code"] == 404
    assert error["message"] == "Product not found"
    assert error["resource"] == "Product"

def test_delete_product(client):
    # Arrange
    create_response = client.post("/products/", json={
        "name": "Keyboard",
        "category": "Accessories",
        "price": 49.99
    })
    created = create_response.json()
    product_id = created["product_id"]

    # Act
    response = client.delete(f"/products/{product_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Product deleted"

    # Verify it’s gone
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404


def test_delete_product_not_found(client):
    response = client.delete("/products/9999")
    assert response.status_code == 404
    error = response.json()["detail"]
    assert error["code"] == 404
    assert error["message"] == "Product not found"
    assert error["resource"] == "Product"
