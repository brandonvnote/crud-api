from fastapi import Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..routing import create_router, not_found

router = create_router("/customers", "customers")

@router.post("/", response_model=schemas.CustomerResponse)

def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    new_customer = models.Customer(**customer.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.get("/", response_model=list[schemas.CustomerResponse])
def read_customers(db: Session = Depends(get_db)):
    return db.query(models.Customer).all()

@router.get("/count")
def count_customers(db: Session = Depends(get_db)):
    total = db.query(models.Customer).count()
    return {"count": total}

@router.get(
    "/{customer_id}",
    response_model=schemas.CustomerResponse,
    responses={404: {"model": schemas.ErrorResponse}}
)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not customer:
        not_found("Customer")
    return customer

@router.put(
    "/{customer_id}",
    response_model=schemas.CustomerResponse,
    responses={404: {"model": schemas.ErrorResponse}}
)
def update_customer(customer_id: int, update: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not customer:
        not_found("Customer")

    # update only provided fields
    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)
    return customer

@router.delete(
    "/{customer_id}",
    responses={404: {"model": schemas.ErrorResponse}}
)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not customer:
        not_found("Customer")

    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted"}
