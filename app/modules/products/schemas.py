import uuid
from datetime import datetime
from pydantic import BaseModel

class CreateProductRequest(BaseModel):
    name: str
    price: float
    stock: int


class ProductResponse(BaseModel):
    id: uuid.UUID
    name: str
    price: float
    stock: int
    created_at: datetime

    model_config = {"from_attributes": True}
