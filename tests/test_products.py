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