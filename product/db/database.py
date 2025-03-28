# db/database.py
from sqlmodel import create_engine, Session

from product.core.config import settings

# Create the database engine
engine = create_engine(settings.DATABASE_URL, echo=True)


# Dependency to get DB session
def get_session():
    with Session(engine) as session:
        yield session
