import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.modules.products.models import Product

def reserve_stock(db: Session, product_id: uuid.UUID, quantity: int) -> Product:
    """Servicio expuesto para que el módulo de Orders pueda descontar stock."""
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Producto {product_id} no encontrado")
    if product.stock < quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Stock insuficiente para '{product.name}' (disponible: {product.stock})"
        )
    product.stock -= quantity
    return product