from fastapi import Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..routing import create_router, not_found

router = create_router("/customers", "customers")

@router.post("/", response_model=schemas.CustomerResponse)

def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """_summary_

    Args:
        customer (schemas.CustomerCreate): The customer data to create.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: The created customer.
    """
    new_customer = models.Customer(**customer.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.get("/", response_model=list[schemas.CustomerResponse])

def read_customers(db: Session = Depends(get_db)):
    """Get all customers.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: A list of all customers.
    """
    return db.query(models.Customer).all()

@router.get("/count")
def count_customers(db: Session = Depends(get_db)):
    """Get the total number of customers.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: The total number of customers.
    """
    total = db.query(models.Customer).count()
    return {"count": total}

@router.get(
    "/{customer_id}",
    response_model=schemas.CustomerResponse,
    responses={404: {"model": schemas.ErrorResponse}}
)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    """Get a customer by ID.

    Args:
        customer_id (int): The ID of the customer to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: The customer with the specified ID.
    """
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
    """Update a customer by ID.

    Args:
        customer_id (int): The ID of the customer to update.
        update (schemas.CustomerUpdate): The updated customer data.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: The updated customer.
    """
    customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not customer:
        not_found("Customer")

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
    """Delete a customer by ID.

    Args:
        customer_id (int): The ID of the customer to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: A message indicating successful deletion.
    """
    customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not customer:
        not_found("Customer")

    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted"}
