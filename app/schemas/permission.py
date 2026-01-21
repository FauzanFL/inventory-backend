from pydantic import BaseModel
from typing import Optional, List

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
    name: Optional[str] = None
    description: Optional[str] = None

class PermissionPage(BaseModel):
    permissions: List[Permission]
    total: int
    page: int
    limit: int
    total_pages: int