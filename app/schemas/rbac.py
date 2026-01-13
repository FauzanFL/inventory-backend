from pydantic import BaseModel
from typing import List, Optional

class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None

class Permission(PermissionBase):
    id: int

    class Config:
        from_attributes = True

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class Role(RoleBase):
    id: int
    permissions: List[Permission]

    class Config:
        from_attributes = True