# product/main.py
from fastapi import FastAPI

from product.core.config import settings
from product.api.v1.product_routes import router as product_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
)

# Include the routes
app.include_router(product_router, prefix="/product", tags=["product"])
