import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.models import User
from app.modules.auth.service import get_current_user
from app.modules.payments.models import Payment
from app.modules.payments.schemas import CreatePaymentRequest, PaymentResponse, PaymentMethod, PaymentStatus
from app.modules.orders.service import get_order_by_id, mark_order_as_paid
from app.modules.orders.schemas import OrderStatus

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("", response_model=PaymentResponse, status_code=201)
def process_payment(
        data: CreatePaymentRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    order = get_order_by_id(db, data.order_id)

    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado para pagar este pedido")

    if order.status != OrderStatus.pending:
        raise HTTPException(
            status_code=400,
            detail=f"El pedido no está pendiente (estado actual: {order.status})",
        )

    if round(data.amount, 2) != round(order.total, 2):
        raise HTTPException(
            status_code=400,
            detail=f"El monto ({data.amount}) no coincide con el total del pedido ({order.total})",
        )

    if order.total > 1_000_000 and data.method != PaymentMethod.bank_transfer:
        raise HTTPException(
            status_code=400,
            detail="Pedidos mayores a $1.000.000 solo pueden pagarse por transferencia bancaria",
        )
    else:
        payment_status = PaymentStatus.approved

    payment = Payment(
        order_id=data.order_id,
        amount=data.amount,
        method=data.method,
        status=payment_status,
    )
    db.add(payment)

    if payment_status == PaymentStatus.approved:
        order.status = OrderStatus.paid

    db.commit()
    db.refresh(payment)
    return payment


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
        payment_id: uuid.UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    order = db.query(Order).filter(Order.id == payment.order_id).first()
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado para ver este pago")
    return payment
