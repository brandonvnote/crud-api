from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime

class CustomerCreate(BaseModel):
    """Customer creation schema.

    Args:
        BaseModel (_type_): Pydantic base model.
    Returns:
        _type_: The customer creation schema.
    """
    first_name: str
    last_name: str
    email: str

class CustomerUpdate(BaseModel):
    """Customer update schema.

    Args:
        BaseModel (_type_): Pydantic base model.
    Returns:
        _type_: The customer update schema.
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

class CustomerResponse(CustomerCreate):
    """Customer response schema.

    Args:
        CustomerCreate (_type_): Base customer creation schema.
    Returns:
        _type_: The customer response schema.
    """
    customer_id: int
    model_config = ConfigDict(from_attributes=True)

class ErrorResponse(BaseModel):
    """Error response schema.

    Args:
        BaseModel (_type_): Pydantic base model.
    Returns:
        _type_: The error response schema.
    """
    code: int
    message: str
    resource: str

class ProductCreate(BaseModel):
    """Product creation schema.

    Args:
        BaseModel (_type_): Pydantic base model.
    Returns:
        _type_: The product creation schema.
    """
    name: str
    category: Optional[str] = None
    price: float

class ProductUpdate(BaseModel):
    """Product update schema.

    Args:
        BaseModel (_type_): Pydantic base model.
    Returns:
        _type_: The product update schema.
    """
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None

class ProductResponse(ProductCreate):
    """Product response schema.

    Args:
        ProductCreate (_type_): Base product creation schema.
    Returns:
        _type_: The product response schema.
    """
    product_id: int
    model_config = ConfigDict(from_attributes=True)

class OrderItemCreate(BaseModel):
    """Order item creation schema.

    Args:
        BaseModel (_type_): Pydantic base model.
    Returns:
        _type_: The order item creation schema.
    """
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    """Order creation schema.

    Args:
        BaseModel (_type_): Pydantic base model.
    Returns:
        _type_: The order creation schema.
    """
    customer_id: int
    items: List[OrderItemCreate]

class OrderItemResponse(OrderItemCreate):
    """Order item response schema.

    Args:
        OrderItemCreate (_type_): Base order item creation schema.
    Returns:
        _type_: The order item response schema.
    """
    product_id: int
    quantity: int
    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    """Order response schema.

    Args:
        BaseModel (_type_): Pydantic base model.
    Returns:
        _type_: The order response schema.
    """
    order_id: int
    customer_id: int
    status: str
    order_date: datetime
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)

class OrderUpdate(BaseModel):
    """Order update schema.

    Args:
        BaseModel (_type_): Pydantic base model.
    Returns:
        _type_: The order update schema.
    """
    status: str

class ReviewBase(BaseModel):
    """Review base schema.

    Args:
        BaseModel (_type_): Pydantic base model.
    Returns:
        _type_: The review base schema.
    """
    customer_id: int
    product_id: int
    rating: int = Field(..., ge=1, le=5)

class ReviewCreate(ReviewBase):
    """Review creation schema.

    Args:
        ReviewBase (_type_): Base review schema.
    Returns:
        _type_: The review creation schema.
    """
    product_id: int
    rating: int = Field(..., ge=1, le=5)
    

class ReviewUpdate(BaseModel):
    """Review update schema.

    Args:
        BaseModel (_type_): Pydantic base model.
    Returns:
        _type_: The review update schema.
    """
    rating: Optional[int] = Field(None, ge=1, le=5)

class ReviewResponse(ReviewBase):
    """Review response schema.

    Args:
        ReviewBase (_type_): Base review schema.
    Returns:
        _type_: The review response schema.
    """
    review_id: int
    order_date: datetime
    model_config = ConfigDict(from_attributes=True)

class ShipmentBase(BaseModel):
    """Shipment base schema.

    Args:
        BaseModel (_type_): Pydantic base model.
    Returns:
        _type_: The shipment base schema.
    """
    order_id: int
    status: str = "processing"
    tracking_number: Optional[str] = None
    shipped_at: Optional[datetime] = None


class ShipmentCreate(ShipmentBase):
    """Shipment creation schema.

    Args:
        ShipmentBase (_type_): Base shipment schema.
    Returns:
        _type_: The shipment creation schema.
    """
    pass


class ShipmentUpdate(BaseModel):
    """Shipment update schema.

    Args:
        BaseModel (_type_): Pydantic base model.
    Returns:
        _type_: The shipment update schema.
    """
    status: Optional[str] = None
    tracking_number: Optional[str] = None
    shipped_at: Optional[datetime] = None


class ShipmentResponse(ShipmentBase):
    """Shipment response schema.

    Args:
        ShipmentBase (_type_): Base shipment schema.
    Returns:
        _type_: The shipment response schema.
    """
    shipment_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TopProduct(BaseModel):
    product_id: int
    name: str
    quantity_sold: int

class RevenueByMonth(BaseModel):
    month: str 
    orders: int
    revenue: float

class RevenueByCustomer(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    revenue: float

class RepeatCustomer(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    orders: int

class OrderValueStats(BaseModel):
    avg_value: float
    min_value: float
    max_value: float

class ProductRating(BaseModel):
    product_id: int
    name: str
    avg_rating: float
    reviews: int