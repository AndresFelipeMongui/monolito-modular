import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.modules.orders.models import Order
from app.modules.orders.schemas import OrderStatus

def get_order_by_id(db: Session, order_id: uuid.UUID) -> Order:
    """Servicio expuesto para que el módulo de Pagos pueda consultar el pedido."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return order

def mark_order_as_paid(db: Session, order: Order):
    """Servicio expuesto para que el módulo de Pagos pueda actualizar el estado."""
    order.status = OrderStatus.paid