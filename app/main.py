from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from .routers import customers, products, orders, reviews, shipments

app = FastAPI(title="CRUD API")

app.include_router(customers.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(reviews.router)
app.include_router(shipments.router)

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).scalar()
    return {"db_alive": bool(result)}
