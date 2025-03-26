# authentication/models/revoked_token.py
from sqlmodel import SQLModel, Field
from datetime import datetime


class RevokedToken(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    jti: str
    user_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
