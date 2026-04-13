import uuid
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"
    
class CreateOrderItemRequest(BaseModel):
    product_id: uuid.UUID
    quantity: int


class OrderItemResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    unit_price: float
    subtotal: float

    model_config = {"from_attributes": True}


class CreateOrderRequest(BaseModel):
    items: list[CreateOrderItemRequest]


class OrderResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    total: float
    status: str
    items: list[OrderItemResponse]
    created_at: datetime

    model_config = {"from_attributes": True}
