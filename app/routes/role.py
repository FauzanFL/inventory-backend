from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.crud import role as crud_role
from app.schemas.role import Role, RoleCreate, RoleUpdate, RolePage, RolePermissionUpdate
from app.schemas.response import SuccessResponse
from app.models.user import User
from app.dependencies import get_current_user, PermissionChecker

router = APIRouter()

@router.get("", response_model=RolePage)
def get_roles(
    db: Session = Depends(get_db), 
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    _: bool = Depends(PermissionChecker("role:view_all"))
):
    offset = (page - 1) * limit

    roles = crud_role.get_roles(db, skip=offset, limit=limit, search=search)
    total = crud_role.get_total_roles(db, search=search)

    return RolePage(
        roles=roles,
        total=total,
        page=page,
        limit=limit,
        total_pages=(total + limit - 1) // limit
    )

@router.get("/{role_id}", response_model=Role)
def get_role(
    role_id: int, 
    db: Session = Depends(get_db), 
    _: bool = Depends(PermissionChecker("role:view"))
):
    role = crud_role.get_role(db, role_id)

    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    return role

@router.post("", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    role_in: RoleCreate, 
    db: Session = Depends(get_db), 
    _: bool = Depends(PermissionChecker("role:create"))
):
    role_in.name = role_in.name.upper()
    crud_role.create_role(db, role_in)

    return SuccessResponse(message="Role created successfully")

@router.put("/{role_id}", response_model=SuccessResponse)
def update_role(
    role_id: int, 
    role_in: RoleUpdate, 
    db: Session = Depends(get_db), 
    _: bool = Depends(PermissionChecker("role:update"))
):
    role = crud_role.update_role(db, role_id, role_in)

    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    return SuccessResponse(message="Role updated successfully")

@router.delete("/{role_id}", response_model=SuccessResponse)
def delete_role(
    role_id: int, 
    db: Session = Depends(get_db), 
    _: bool = Depends(PermissionChecker("role:delete"))
):
    role = crud_role.delete_role(db, role_id)

    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    return SuccessResponse(message="Role deleted successfully")

@router.post("/{role_id}/users/{user_id}", response_model=SuccessResponse)
def assign_role_to_user(
    role_id: int, 
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user), 
    _: bool = Depends(PermissionChecker("role:assign"))
):  
    role = crud_role.get_role(db, role_id)

    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    if role.name == "ADMIN" and current_user.role.name != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not enough permissions"
        )
    
    user = crud_role.assign_role(db, user_id, role_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return SuccessResponse(message="Role assigned to user successfully")

@router.put("/{role_id}/permissions", response_model=SuccessResponse)
def update_role_permissions(
    role_id: int,
    role_permission_in: RolePermissionUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(PermissionChecker("role:update_permissions"))
):
    role = crud_role.get_role(db, role_id)

    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    updated_role = crud_role.sync_permissions(db, role_id, role_permission_in.permission_ids)

    if updated_role is None:
        raise HTTPException(status_code=400, detail="Failed to update permissions")

    return SuccessResponse(
        message="Role permissions updated successfully"
    )

