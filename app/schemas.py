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
