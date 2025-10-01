from fastapi import Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..routing import create_router, not_found

router = create_router("/reviews", "reviews")


@router.post("/", response_model=schemas.ReviewResponse)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    """Create a new review.

    Args:
        review (schemas.ReviewCreate): The review data to create.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: The created review.
    """
    new_review = models.Review(**review.model_dump())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@router.get("/", response_model=list[schemas.ReviewResponse])
def read_reviews(db: Session = Depends(get_db)):
    """Get all reviews.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: The list of all reviews.
    """
    return db.query(models.Review).all()


@router.get("/{review_id}", response_model=schemas.ReviewResponse)
def read_review(review_id: int, db: Session = Depends(get_db)): 
    """Get a review by ID.

    Args:
        review_id (int): The ID of the review to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: The review with the specified ID.
    """
    review = db.query(models.Review).filter(models.Review.review_id == review_id).first()
    if not review:
        raise not_found("Review")
    return review


@router.put("/{review_id}", response_model=schemas.ReviewResponse)
def update_review(review_id: int, review_update: schemas.ReviewUpdate, db: Session = Depends(get_db)):
    """Update a review by ID.

    Args:
        review_id (int): The ID of the review to update.
        review_update (schemas.ReviewUpdate): The updated review data.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        not_found: If the review is not found.

    Returns:
        _type_: The updated review.
    """
    review = db.query(models.Review).filter(models.Review.review_id == review_id).first()
    if not review:
        raise not_found("Review")

    for key, value in review_update.model_dump(exclude_unset=True).items():
        setattr(review, key, value)

    db.commit()
    db.refresh(review)
    return review


@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    """Delete a review by ID.

    Args:
        review_id (int): The ID of the review to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        not_found: If the review is not found.

    Returns:
        _type_: A message indicating successful deletion.
    """
    review = db.query(models.Review).filter(models.Review.review_id == review_id).first()
    if not review:
        raise not_found("Review")

    db.delete(review)
    db.commit()
    return {"message": f"Review {review_id} deleted successfully"}
