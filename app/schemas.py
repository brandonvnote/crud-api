from pydantic import BaseModel, ConfigDict
from typing import Optional

class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: str

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

class CustomerResponse(CustomerCreate):
    customer_id: int
    model_config = ConfigDict(from_attributes=True)

class ErrorResponse(BaseModel):
    code: int
    message: str
    resource: str

class ProductCreate(BaseModel):
    name: str
    category: Optional[str] = None
    price: float

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None

class ProductResponse(ProductCreate):
    product_id: int
    model_config = ConfigDict(from_attributes=True)