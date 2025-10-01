from fastapi import Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..routing import create_router, not_found

router = create_router("/orders", "orders")

@router.post("/", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Create order
    new_order = models.Order(customer_id=order.customer_id)
    db.add(new_order)
    db.flush()  # get order_id before commit

    # Add items
    for item in order.items:
        db.add(models.OrderItem(order_id=new_order.order_id, product_id=item.product_id, quantity=item.quantity))

    db.commit()
    db.refresh(new_order)
    return new_order

@router.get("/", response_model=list[schemas.OrderResponse])
def read_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

@router.get(
    "/{order_id}",
    response_model=schemas.OrderResponse,
    responses={404: {"model": schemas.ErrorResponse}}
)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not order:
        not_found("Order")
    return order

@router.put(
    "/{order_id}",
    response_model=schemas.OrderResponse,
    responses={404: {"model": schemas.ErrorResponse}}
)
def update_order(order_id: int, update: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not order:
        not_found("Order")

    order.status = update.status
    db.commit()
    db.refresh(order)
    return order

@router.delete(
    "/{order_id}",
    responses={404: {"model": schemas.ErrorResponse}}
)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not order:
        not_found("Order")

    db.delete(order)
    db.commit()
    return {"message": "Order deleted"}