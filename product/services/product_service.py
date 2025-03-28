# services/product_service.py
from sqlmodel import Session, select

from product.models.product_model import Product


# Create a new product
def create_product(session: Session, product: Product) -> Product:
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


# Get all products
def get_all_products(session: Session):
    return session.exec(select(Product)).all()
