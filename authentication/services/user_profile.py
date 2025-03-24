from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from authentication.models.user import User, UserRead
from authentication.db.session import get_session
from authentication.services.jwt_service import verify_token

# Create OAuth2PasswordBearer Token Extractor
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Get Current User Profile
def profile(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> UserRead:
    payload = verify_token(token)
    user_id: str = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: missing subject")

    user = session.get(User, int(user_id))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserRead.model_validate(user)
