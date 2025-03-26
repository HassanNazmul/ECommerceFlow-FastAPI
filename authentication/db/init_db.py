# authentication/db/init_db.py
from sqlmodel import SQLModel

from authentication.db.session import engine
from authentication.models.user import User  # noqa
from authentication.models.revoked_token import RevokedToken  # noqa


def init_db():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized.")
