from datetime import datetime
from typing import Optional

from pydantic import EmailStr, BaseModel


class UserOptional(BaseModel):
    full_name: Optional[str]
    telegram_id: Optional[int]


class UserSpec(BaseModel):
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    _verification_code: Optional[str]


class UserBase(UserOptional):
    email: Optional[EmailStr]
    username: Optional[str]


class UserCreateBase(UserBase):
    password: Optional[str]
    password_confirm: Optional[str]


class UserCreate(UserCreateBase, UserSpec):
    pass


class UserCreateOpen(UserCreateBase, UserOptional):
    pass


class UserUpdate(UserCreate, UserSpec):
    pass


class UserUpdateMe(UserOptional):
    pass


class User(UserBase, UserSpec):
    id: Optional[str] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
