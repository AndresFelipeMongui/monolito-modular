import uuid
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class PaymentMethod(str, Enum):
    cash = "cash"
    card = "card"
    bank_transfer = "bank_transfer"

class PaymentStatus(str, Enum):
    approved = "approved"
    rejected = "rejected"

class CreatePaymentRequest(BaseModel):
    order_id: uuid.UUID
    amount: float
    method: PaymentMethod


class PaymentResponse(BaseModel):
    id: uuid.UUID
    order_id: uuid.UUID
    amount: float
    method: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}