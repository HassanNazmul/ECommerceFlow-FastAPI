# authentication/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select
from datetime import datetime

from authentication.db.session import get_session
from authentication.models.revoked_token import RevokedToken
from authentication.models.user import User, UserCreate, UserRead, UserLogin, Token, UserPasswordUpdate, UserUpdate
from authentication.services.auth_service import create_user, change_password
from authentication.services.auth_service import verify_password
from authentication.services.jwt_service import create_access_token, verify_token, is_token_revoked
from authentication.services.user_profile import profile, oauth2_scheme, update_user

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


@router.post("/logout")
def logout(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session)
):
    payload = verify_token(token)
    jti = payload.get("jti")
    user_id = payload.get("sub")

    if not jti:
        raise HTTPException(status_code=400, detail="Missing token ID (jti)")

    revoked = RevokedToken(
        jti=jti,
        user_id=int(user_id),
        expires_at=datetime.fromtimestamp(payload["exp"])
    )

    session.add(revoked)
    session.commit()
    return {"detail": "Successfully logged out"}


@router.get("/profile", response_model=UserRead)
def get_profile(
        current_user: UserRead = Depends(profile),
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session)
):
    payload = verify_token(token)
    jti = payload.get("jti")

    if is_token_revoked(jti, session):
        raise HTTPException(status_code=401, detail="Token has been revoked")

    return current_user


@router.post("/change-password")
def change_user_password(
        password_data: UserPasswordUpdate,
        current_user: UserRead = Depends(profile),
        session: Session = Depends(get_session)
):
    change_password(
        user_id=current_user.id,
        old_password=password_data.old_password,
        new_password=password_data.new_password,
        session=session
    )
    return {"detail": "Password updated successfully"}


@router.put("/update-profile", response_model=UserRead)
def update_profile(
        updates: UserUpdate,
        current_user: UserRead = Depends(profile),
        session: Session = Depends(get_session)
):
    updated_user = update_user(current_user.id, updates, session)
    return updated_user
