import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db, DATABASE_URL
from app.main import app

# Create a new engine for the test DB
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    # Reset schema before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db):
    # Override get_db for the app
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def create_customer(client, i=1):
    return client.post("/customers/", json={
        "first_name": f"User{i}",
        "last_name": "Test",
        "email": f"user{i}@example.com"
    }).json()

def create_product(client, name, price, category="Test"):
    return client.post("/products/", json={
        "name": name,
        "category": category,
        "price": price
    }).json()

def create_order(client, customer_id, items):
    return client.post("/orders/", json={
        "customer_id": customer_id,
        "items": items
    }).json()

def add_review(client, product_id, rating):
    return client.post("/reviews/", json={
        "product_id": product_id,
        "rating": rating
    }).json()
