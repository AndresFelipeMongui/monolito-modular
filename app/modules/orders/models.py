import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, Integer, String, Uuid as UUIDColumn
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.modules.orders.schemas import OrderStatus

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(UUIDColumn(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    user_id: Mapped[uuid.UUID] = mapped_column(UUIDColumn(as_uuid=True), nullable=False)
    total: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default=OrderStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[uuid.UUID] = mapped_column(UUIDColumn(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    order_id: Mapped[uuid.UUID] = mapped_column(UUIDColumn(as_uuid=True), nullable=False)
    product_id: Mapped[uuid.UUID] = mapped_column(UUIDColumn(as_uuid=True), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
    subtotal: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
