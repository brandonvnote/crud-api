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
