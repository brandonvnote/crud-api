from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime

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

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]

class OrderItemResponse(OrderItemCreate):
    product_id: int
    quantity: int
    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    status: str
    order_date: datetime
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)

class OrderUpdate(BaseModel):
    status: str

class ReviewBase(BaseModel):
    customer_id: int
    product_id: int
    rating: int = Field(..., ge=1, le=5)

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)

class ReviewResponse(ReviewBase):
    review_id: int
    order_date: datetime
    model_config = ConfigDict(from_attributes=True)

class ShipmentBase(BaseModel):
    order_id: int
    status: str = "processing"
    tracking_number: Optional[str] = None
    shipped_at: Optional[datetime] = None


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentUpdate(BaseModel):
    status: Optional[str] = None
    tracking_number: Optional[str] = None
    shipped_at: Optional[datetime] = None


class ShipmentResponse(ShipmentBase):
    shipment_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)