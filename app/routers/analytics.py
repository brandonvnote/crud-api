from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any

from .. import models
from ..database import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/top-products")
def top_products(limit: int = 10, db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Get the top products by quantity sold.

    Args:
        limit (int, optional): The maximum number of products to return. Defaults to 10.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing product information.
    """
    q = (
        db.query(
            models.Product.product_id,
            models.Product.name,
            func.sum(models.OrderItem.quantity).label("quantity_sold"),
        )
        .join(models.OrderItem, models.Product.product_id == models.OrderItem.product_id)
        .group_by(models.Product.product_id, models.Product.name)
        .order_by(func.sum(models.OrderItem.quantity).desc())
        .limit(limit)
        .all()
    )

    results = []
    for row in q:
        results.append({
            "product_id": row.product_id,
            "name": row.name,
            "quantity_sold": int(row.quantity_sold),
        })
    return results

@router.get("/revenue-by-month")
def revenue_by_month(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Get revenue by month.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing revenue information.
    """
    amount = (models.OrderItem.quantity * models.Product.price).label("line_total")
    month = func.to_char(func.date_trunc("month", models.Order.order_date), "YYYY-MM").label("month")

    q = (
        db.query(
            month,
            func.sum(amount).label("revenue"),
            func.count(func.distinct(models.Order.order_id)).label("orders"),
        )
        .join(models.OrderItem, models.Order.order_id == models.OrderItem.order_id)
        .join(models.Product, models.Product.product_id == models.OrderItem.product_id)
        .group_by(month)
        .order_by(month)
        .all()
    )

    results = []
    for row in q:
        results.append({
            "month": row.month,
            "revenue": float(row.revenue),
            "orders": int(row.orders),
        })
    return results

@router.get("/revenue-by-customer")
def revenue_by_customer(limit: int = 10, db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Get revenue by customer.

    Args:
        limit (int, optional): The maximum number of customers to return. Defaults to 10.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing customer revenue information.
    """
    amount = (models.OrderItem.quantity * models.Product.price).label("line_total")

    q = (
        db.query(
            models.Customer.customer_id,
            func.sum(amount).label("revenue"),
        )
        .join(models.Order, models.Customer.customer_id == models.Order.customer_id)
        .join(models.OrderItem, models.Order.order_id == models.OrderItem.order_id)
        .join(models.Product, models.Product.product_id == models.OrderItem.product_id)
        .group_by(models.Customer.customer_id)
        .order_by(func.sum(amount).desc())
        .limit(limit)
        .all()
    )

    results = []
    for row in q:
        results.append({
            "customer_id": row.customer_id,
            "revenue": float(row.revenue),
        })
    return results

@router.get("/repeat-customers")
def repeat_customers(min_orders: int = 2, db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Get repeat customers.

    Args:
        min_orders (int, optional): The minimum number of orders a customer must have placed to be considered a repeat customer. Defaults to 2.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[Dict[str, Any]]: A list of repeat customers.
    """
    q = (
        db.query(
            models.Customer.customer_id,
            func.count(models.Order.order_id).label("order_count"),
        )
        .join(models.Order, models.Customer.customer_id == models.Order.customer_id)
        .group_by(models.Customer.customer_id)
        .having(func.count(models.Order.order_id) >= min_orders)
        .all()
    )

    results = []
    for row in q:
        results.append({
            "customer_id": row.customer_id,
            "order_count": int(row.order_count),
        })
    return results

@router.get("/order-value-stats")
def order_value_stats(db: Session = Depends(get_db)) -> Dict[str, float]:
    """Get order value statistics.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Dict[str, float]: A dictionary containing the average, minimum, and maximum order values.
    """
    order_totals = (
        db.query(
            models.Order.order_id,
            func.sum(models.OrderItem.quantity * models.Product.price).label("order_total"),
        )
        .join(models.OrderItem, models.Order.order_id == models.OrderItem.order_id)
        .join(models.Product, models.Product.product_id == models.OrderItem.product_id)
        .group_by(models.Order.order_id)
        .subquery()
    )

    agg = db.query(
        func.avg(order_totals.c.order_total).label("avg_value"),
        func.min(order_totals.c.order_total).label("min_value"),
        func.max(order_totals.c.order_total).label("max_value"),
    ).one()

    return {
        "avg_value": float(agg.avg_value),
        "min_value": float(agg.min_value),
        "max_value": float(agg.max_value),
    }

@router.get("/review-summary")
def review_summary(db: Session = Depends(get_db)):
    """Get a summary of product reviews.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: A list of dictionaries containing product review summaries.
    """
    q = (
        db.query(
            models.Product.product_id,
            models.Product.name,
            func.avg(models.Review.rating).label("avg_rating"),
            func.count(models.Review.review_id).label("review_count"),
        )
        .join(models.Review, models.Product.product_id == models.Review.product_id)
        .group_by(models.Product.product_id, models.Product.name)
        .order_by(models.Product.product_id)
        .all()
    )

    return [
        {
            "product_id": row.product_id,
            "name": row.name,
            "avg_rating": float(row.avg_rating),
            "review_count": int(row.review_count),
        }
        for row in q
    ]