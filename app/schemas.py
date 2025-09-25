from pydantic import BaseModel, ConfigDict

class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: str

class CustomerResponse(CustomerCreate):
    customer_id: int

model_config = ConfigDict(from_attributes=True)
