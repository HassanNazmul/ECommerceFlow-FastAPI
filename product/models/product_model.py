# models/product_model.py
from sqlmodel import SQLModel, Field
from typing import Optional


# Product model class
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True
