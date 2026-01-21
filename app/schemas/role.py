from pydantic import BaseModel
from typing import Optional, List
from .permission import Permission

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Role(RoleBase):
    id: int
    permissions: List[Permission]

    class Config:
        from_attributes = True

class RolePage(BaseModel):
    roles: List[Role]
    total: int
    page: int
    limit: int
    total_pages: int

class RolePermissionUpdate(BaseModel):
    permission_ids: List[int]