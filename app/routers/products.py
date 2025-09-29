from fastapi import Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..routing import create_router, not_found

router = create_router("/products", "products")

@router.post("/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/", response_model=list[schemas.ProductResponse])
def read_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@router.get(
    "/{product_id}",
    response_model=schemas.ProductResponse,
    responses={404: {"model": schemas.ErrorResponse}}
)
def read_product(product_id: int, db: Session = Depends(get_db)):
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
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        not_found("Product")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}
