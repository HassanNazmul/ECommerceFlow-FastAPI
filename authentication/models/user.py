# authentication/models/user.py
from typing import Optional
from pydantic import field_validator
from sqlmodel import SQLModel, Field


# Database Table Model for User
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False, unique=True)
    first_name: str
    last_name: str
    email: str = Field(index=True, nullable=False, unique=True)
    hashed_password: str


# Schema for User Creation
class UserCreate(SQLModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str

    # Make the username and email lowercase
    @classmethod
    @field_validator("username", "email")
    def normalize_username_and_email(cls, v: str) -> str:
        return v.lower()


# Schema for User Login
class UserLogin(SQLModel):
    username: str
    password: str


# Token Schema
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Schema for User Read
class UserRead(SQLModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str


# Schema for Password Reset
class UserPasswordUpdate(SQLModel):
    old_password: str
    new_password: str


# Schema for User Update
class UserUpdate(SQLModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
