from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True , max_length=50)
    display_name: str = Field(unique=True, max_length=50)
    state: str = Field(max_length=50, default="online")
    about_me: str | None = Field(max_length=255, default=None)
    birth_date: datetime
    verified: bool = Field(default=False)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserUpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


class ResetUserPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
    

class VerifyAccount(SQLModel):
    token: str
