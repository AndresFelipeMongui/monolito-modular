import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, Integer, String, Uuid as UUIDColumn
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(UUIDColumn(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    price: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
