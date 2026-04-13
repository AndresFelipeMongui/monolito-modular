import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.database import engine, Base

from app.modules.auth.models import User
from app.modules.products.models import Product
from app.modules.orders.models import Order, OrderItem
from app.modules.payments.models import Payment

from app.modules.auth.router import router as auth_router
from app.modules.products.router import router as products_router
from app.modules.orders.router import router as orders_router
from app.modules.payments.router import router as payments_router

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Monolito Modular")

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Excepción no manejada: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Ocurrió un error inesperado. Por favor intenta de nuevo más tarde."},
    )

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(payments_router)