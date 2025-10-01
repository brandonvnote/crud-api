from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, timezone
from sqlalchemy.sql import func


class Customer(Base):
    """Customer model for the database.

    Args:
        Base (_type_): The base class for SQLAlchemy models.
    Returns:
        _type_: The Customer model.
    """
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    reviews = relationship("Review", back_populates="customer")

class Product(Base):
    """Product model for the database.

    Args:
        Base (_type_): The base class for SQLAlchemy models.
    Returns:
        _type_: The Product model.
    """
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    reviews = relationship("Review", back_populates="product")

class Order(Base):
    """Order model for the database.

    Args:
        Base (_type_): The base class for SQLAlchemy models.
    Returns:
        _type_: The Order model.
    """
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    status = Column(String, default="pending")
    order_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), server_default=func.now())

    items = relationship("OrderItem", back_populates="order")
    shipment = relationship("Shipment", back_populates="order", uselist=False)
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    """Order item model for the database.

    Args:
        Base (_type_): The base class for SQLAlchemy models.
    Returns:
        _type_: The OrderItem model.
    """
    __tablename__ = "order_items"

    order_id = Column(Integer, ForeignKey("orders.order_id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), primary_key=True)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class Review(Base):
    """Review model for the database.

    Args:
        Base (_type_): The base class for SQLAlchemy models.
    Returns:
        _type_: The Review model.
    """
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    rating = Column(Integer, nullable=False)
    order_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), server_default=func.now())

    
    customer = relationship("Customer", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

class Shipment(Base):
    """Shipment model for the database.

    Args:
        Base (_type_): The base class for SQLAlchemy models.
    Returns:
        _type_: The Shipment model.
    """
    __tablename__ = "shipments"

    shipment_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False, unique=True)
    status = Column(String, default="processing")
    tracking_number = Column(String, unique=True, nullable=True)
    shipped_at = Column(DateTime, nullable=True)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now()
    )

    order = relationship("Order", back_populates="shipment")
