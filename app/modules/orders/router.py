import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.models import User
from app.modules.auth.service import get_current_user
from app.modules.orders.models import Order, OrderItem
from app.modules.orders.schemas import CreateOrderRequest, OrderResponse, OrderStatus
from app.modules.products.service import reserve_stock

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("", response_model=OrderResponse, status_code=201)
def create_order(
        data: CreateOrderRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    if not data.items:
        raise HTTPException(status_code=400, detail="El pedido debe tener al menos un producto")

    total = 0.0
    resolved_items = []

    for item in data.items:
        if item.quantity <= 0:
            raise HTTPException(status_code=400, detail="La cantidad debe ser mayor que 0")

        product: Product | None = db.get(Product, item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Producto {item.product_id} no encontrado")
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para '{product.name}' (disponible: {product.stock})",
            )

        subtotal = product.price * item.quantity
        total += subtotal
        resolved_items.append((product, item.quantity, product.price, subtotal))

    order = Order(
        user_id=current_user.id,
        total=round(total, 2),
        status=OrderStatus.pending,
    )
    db.add(order)
    db.flush()

    for product, quantity, unit_price, subtotal in resolved_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=round(subtotal, 2),
        )
        db.add(order_item)
        product.stock -= quantity

    db.commit()
    db.refresh(order)
    order.items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    return order