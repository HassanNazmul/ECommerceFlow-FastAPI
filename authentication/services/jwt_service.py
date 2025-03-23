# authentication/services/jwt_service.py
from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import JWTError, jwt

from authentication.core.config import settings


# JWT token creation
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


# JWT token verification
def verify_token(token: str) -> dict:
    try:
        return jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# JWT token expiration check
def is_token_expired(token: str) -> bool:
    try:
        payload = verify_token(token)
        exp = payload.get("exp")
        if exp is None:
            return True
        return datetime.fromtimestamp(exp) < datetime.utcnow()
    except jwt.JWTError:
        return True
