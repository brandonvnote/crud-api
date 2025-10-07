from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from .routers import customers, products, orders, reviews, shipments, analytics

app = FastAPI(title="CRUD API")

app.include_router(customers.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(reviews.router)
app.include_router(shipments.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    """Root endpoint.

    Returns:
        dict: A message indicating the API is running.
    """
    return {"message": "API is running"}

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    """Check database connectivity.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A message indicating the database connection status.
    """
    result = db.execute(text("SELECT 1")).scalar()
    return {"db_alive": bool(result)}
