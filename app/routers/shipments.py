from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, schemas
from ..database import get_db
from ..routing import create_router, not_found

router = create_router("/shipments", "shipments")


@router.post("/", response_model=schemas.ShipmentResponse)
def create_shipment(shipment: schemas.ShipmentCreate, db: Session = Depends(get_db)):
    """Create a new shipment.

    Args:
        shipment (schemas.ShipmentCreate): The shipment data to create.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the shipment data is invalid.
        HTTPException: If the shipment already exists.

    Returns:
        _type_: The created shipment.
    """
    new_shipment = models.Shipment(**shipment.model_dump())
    db.add(new_shipment)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "shipments_order_id_key" in str(e.orig):
            raise HTTPException(400, "Each order can only have one shipment")
        if "shipments_tracking_number_key" in str(e.orig):
            raise HTTPException(400, "Tracking number must be unique")
        raise
    db.refresh(new_shipment)
    return new_shipment


@router.get("/", response_model=list[schemas.ShipmentResponse])
def read_shipments(db: Session = Depends(get_db)):
    """Get all shipments.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: The list of all shipments.
    """
    return db.query(models.Shipment).all()


@router.get("/{shipment_id}", response_model=schemas.ShipmentResponse)
def read_shipment(shipment_id: int, db: Session = Depends(get_db)):
    """Get a shipment by ID.

    Args:
        shipment_id (int): The ID of the shipment to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        not_found: If the shipment is not found.

    Returns:
        _type_: The shipment with the specified ID.
    """
    shipment = db.query(models.Shipment).filter(models.Shipment.shipment_id == shipment_id).first()
    if not shipment:
        raise not_found("Shipment")
    return shipment


@router.put("/{shipment_id}", response_model=schemas.ShipmentResponse)
def update_shipment(shipment_id: int, shipment_update: schemas.ShipmentUpdate, db: Session = Depends(get_db)):
    """Update a shipment by ID.

    Args:
        shipment_id (int): The ID of the shipment to update.
        shipment_update (schemas.ShipmentUpdate): The updated shipment data.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        not_found: The shipment is not found.
        HTTPException: If the shipment data is invalid.

    Returns:
        _type_: The updated shipment.
    """
    shipment = db.query(models.Shipment).filter(models.Shipment.shipment_id == shipment_id).first()
    if not shipment:
        raise not_found("Shipment")

    for key, value in shipment_update.model_dump(exclude_unset=True).items():
        setattr(shipment, key, value)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "shipments_tracking_number_key" in str(e.orig):
            raise HTTPException(400, "Tracking number must be unique")
        raise
    db.refresh(shipment)
    return shipment


@router.delete("/{shipment_id}")
def delete_shipment(shipment_id: int, db: Session = Depends(get_db)):
    """Delete a shipment by ID.

    Args:
        shipment_id (int): The ID of the shipment to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        not_found: The shipment is not found.

    Returns:
        _type_: A message indicating successful deletion.
    """
    shipment = db.query(models.Shipment).filter(models.Shipment.shipment_id == shipment_id).first()
    if not shipment:
        raise not_found("Shipment")

    db.delete(shipment)
    db.commit()
    return {"message": f"Shipment {shipment_id} deleted successfully"}
