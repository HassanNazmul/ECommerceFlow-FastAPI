# authentication/services/auth_service.py
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlmodel import Session, select

from authentication.models.user import UserCreate, User

# Initialize password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Password hashing for security
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# User creation service
def create_user(user_data: UserCreate, session: Session) -> User:
    normalized_username = user_data.username.lower()
    normalized_email = user_data.email.lower()

    # Check if email or username already exists
    existing_user = session.exec(
        select(User).where(
            (User.email == normalized_email) | (User.username == normalized_username)
        )
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists.")

    # Hash the password
    hashed_pw = get_password_hash(user_data.password)

    # Create and save user
    user = User(
        username=normalized_username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=normalized_email,
        hashed_password=hashed_pw,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# Password verification
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
