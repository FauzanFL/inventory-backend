from pydantic import BaseModel
from typing import Optional

class PermissionBase(BaseModel):
    name: str
    description: str

class Permission(PermissionBase):
    id: int

    class Config:
        from_attributes = True

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    description: Optional[str] = None