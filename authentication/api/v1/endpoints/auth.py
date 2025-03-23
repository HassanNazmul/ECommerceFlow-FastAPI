# authentication/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from authentication.db.session import get_session
from authentication.models.user import User, UserCreate, UserRead, UserLogin, Token
from authentication.services.auth_service import create_user
from authentication.services.auth_service import verify_password
from authentication.services.jwt_service import create_access_token

router = APIRouter()


@router.get("/ping")
async def ping():
    return {"message": "Authentication Service is running!"}


@router.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    new_user = create_user(user, session)
    return new_user


@router.post("/login", response_model=Token)
def login(data: UserLogin, session: Session = Depends(get_session)):
    normalized_username = data.username.lower()

    # Check if the user exists
    user = session.exec(
        select(User).where(User.username == normalized_username)
    ).first()

    # Check if the user exists and the password is correct
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create a JWT token
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
