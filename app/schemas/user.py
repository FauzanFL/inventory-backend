from pydantic import BaseModel, EmailStr
from typing import Optional
from .rbac import Role

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role_id: int
    role: Optional[Role] = None

    class Config:
        from_attributes = True