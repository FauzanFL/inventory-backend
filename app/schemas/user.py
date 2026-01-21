from pydantic import BaseModel, EmailStr
from typing import Optional
from .rbac import Role

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class CurrentUser(BaseModel):
    id: int
    username: str
    role: str

class User(UserBase):
    id: int
    role_id: Optional[int] = None
    role: Optional[Role] = None

    class Config:
        from_attributes = True

class UserPage(BaseModel):
    users: list[User]
    total: int
    page: int
    limit: int
    total_pages: int

class UpdatePassword(BaseModel):
    password: str