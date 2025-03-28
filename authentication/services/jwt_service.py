# authentication/services/jwt_service.py
import uuid
from sqlmodel import Session, select
from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import JWTError, jwt

from authentication.core.config import settings
from authentication.models.revoked_token import RevokedToken

# Load RSA private key
with open("authentication/keys/private_key.pem", "r") as f:
    PRIVATE_KEY = f.read()


# JWT token creation
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    jti = str(uuid.uuid4())  # Generate a unique token ID

    to_encode.update({
        "exp": expire,
        "jti": jti
    })

    return jwt.encode(to_encode, PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM)


# JWT token verification
def verify_token(token: str) -> dict:
    try:
        # Note: In other services, verify using public key.
        return jwt.decode(token, PRIVATE_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# Check if token is expired
def is_token_expired(token: str) -> bool:
    try:
        payload = verify_token(token)
        exp = payload.get("exp")
        if exp is None:
            return True
        return datetime.fromtimestamp(exp) < datetime.utcnow()
    except JWTError:
        return True


# Check if token is revoked
def is_token_revoked(jti: str, session: Session) -> bool:
    return session.exec(
        select(RevokedToken).where(RevokedToken.jti == jti)
    ).first() is not None
