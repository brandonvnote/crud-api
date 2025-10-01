from fastapi import Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..routing import create_router, not_found

router = create_router("/products", "products")

@router.post("/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Create a new product.

    Args:
        product (schemas.ProductCreate): Product data.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: The created product.
    """
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/", response_model=list[schemas.ProductResponse])
def read_products(db: Session = Depends(get_db)):
    """Get all products.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: The list of all products.
    """
    return db.query(models.Product).all()

@router.get(
    "/{product_id}",
    response_model=schemas.ProductResponse,
    responses={404: {"model": schemas.ErrorResponse}}
)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """Get a product by ID.

    Args:
        product_id (int): The ID of the product to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: The product with the specified ID.
    """
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        not_found("Product")
    return product

@router.put(
    "/{product_id}",
    response_model=schemas.ProductResponse,
    responses={404: {"model": schemas.ErrorResponse}}
)
def update_product(product_id: int, update: schemas.ProductUpdate, db: Session = Depends(get_db)):
    """Update a product by ID.

    Args:
        product_id (int): The ID of the product to update.
        update (schemas.ProductUpdate): The updated product data.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: The updated product.
    """
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        not_found("Product")

    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product

@router.delete(
    "/{product_id}",
    responses={404: {"model": schemas.ErrorResponse}}
)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product by ID.

    Args:
        product_id (int): The ID of the product to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: A message indicating successful deletion.
    """
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        not_found("Product")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}
