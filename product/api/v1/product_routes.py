# api/v1/product_routes.py
from fastapi import APIRouter, Depends
from sqlmodel import Session

from product.db.database import get_session
from product.models.product_model import Product
from product.services.product_service import create_product, get_all_products
from product.services.jwt_service import verify_token


router = APIRouter()


@router.get("/ping")
def ping(user: dict = Depends(verify_token)):
    return {"message": "Product Service is running!", "username": user["username"]}


# Create a new product
@router.post("/new-product")
def create(product: Product, session: Session = Depends(get_session)):
    return create_product(session, product)


# Get all products
@router.get("/products")
def get_all(session: Session = Depends(get_session)):
    return get_all_products(session)
