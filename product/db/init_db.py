# db/init_db.py
from sqlmodel import SQLModel

from product.db.database import engine
from product.models.product_model import Product  # noqa


def init_db():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized.")
