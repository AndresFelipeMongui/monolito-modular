import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, String, Uuid as UUIDColumn
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(UUIDColumn(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    order_id: Mapped[uuid.UUID] = mapped_column(UUIDColumn(as_uuid=True), nullable=False)
    amount: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
    method: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
