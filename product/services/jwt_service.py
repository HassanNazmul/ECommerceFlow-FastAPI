from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

import os

# Load public key
with open("product/keys/public_key.pem", "r") as f:
    PUBLIC_KEY = f.read()

# Using same algorithm as your authentication service
ALGORITHM = os.getenv("JWT_ALGORITHM", "RS256")

# Reuse FastAPI's token parsing dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token missing user ID")
        return {"user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")