import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.models import User
from app.modules.auth.service import get_current_user
from app.modules.products.models import Product
from app.modules.products.schemas import CreateProductRequest, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(
        data: CreateProductRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    if data.price <= 0:
        raise HTTPException(status_code=400, detail="El precio debe ser mayor que 0")
    if data.stock < 0:
        raise HTTPException(status_code=400, detail="El stock no puede ser negativo")

    product = Product(name=data.name, price=data.price, stock=data.stock)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("", response_model=list[ProductResponse])
def list_products(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return db.query(Product).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
        product_id: uuid.UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    product: Product | None = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product