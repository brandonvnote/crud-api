import pytest

def test_create_review(client):
    # Arrange: create customer + product first
    customer = client.post("/customers/", json={
        "first_name": "ReviewUser",
        "last_name": "Test",
        "email": "reviewuser@example.com"
    }).json()

    product = client.post("/products/", json={
        "name": "Laptop",
        "category": "Electronics",
        "price": 1299.99
    }).json()

    # Act
    response = client.post("/reviews/", json={
        "customer_id": customer["customer_id"],
        "product_id": product["product_id"],
        "rating": 5
    })

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == 5
    assert data["customer_id"] == customer["customer_id"]
    assert data["product_id"] == product["product_id"]


def test_read_reviews(client):
    response = client.get("/reviews/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_review_by_id(client):
    # Arrange: create review
    customer = client.post("/customers/", json={
        "first_name": "SingleReview",
        "last_name": "User",
        "email": "single@example.com"
    }).json()

    product = client.post("/products/", json={
        "name": "Phone",
        "category": "Electronics",
        "price": 799.99
    }).json()

    review = client.post("/reviews/", json={
        "customer_id": customer["customer_id"],
        "product_id": product["product_id"],
        "rating": 4
    }).json()

    # Act
    response = client.get(f"/reviews/{review['review_id']}")

    # Assert
    assert response.status_code == 200
    assert response.json()["review_id"] == review["review_id"]


def test_read_review_not_found(client):
    response = client.get("/reviews/9999")
    assert response.status_code == 404


def test_update_review(client):
    # Arrange: create review
    customer = client.post("/customers/", json={
        "first_name": "UpdateReview",
        "last_name": "User",
        "email": "update@example.com"
    }).json()

    product = client.post("/products/", json={
        "name": "Monitor",
        "category": "Electronics",
        "price": 199.99
    }).json()

    review = client.post("/reviews/", json={
        "customer_id": customer["customer_id"],
        "product_id": product["product_id"],
        "rating": 2
    }).json()

    # Act: update rating
    response = client.put(f"/reviews/{review['review_id']}", json={"rating": 5})

    # Assert
    assert response.status_code == 200
    assert response.json()["rating"] == 5


def test_update_review_not_found(client):
    response = client.put("/reviews/9999", json={"rating": 3})
    assert response.status_code == 404


def test_delete_review(client):
    # Arrange: create review
    customer = client.post("/customers/", json={
        "first_name": "DeleteReview",
        "last_name": "User",
        "email": "delete@example.com"
    }).json()

    product = client.post("/products/", json={
        "name": "Keyboard",
        "category": "Accessories",
        "price": 49.99
    }).json()

    review = client.post("/reviews/", json={
        "customer_id": customer["customer_id"],
        "product_id": product["product_id"],
        "rating": 3
    }).json()

    # Act
    response = client.delete(f"/reviews/{review['review_id']}")

    # Assert
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]


def test_delete_review_not_found(client):
    response = client.delete("/reviews/9999")
    assert response.status_code == 404
