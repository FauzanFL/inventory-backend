from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.crud import role as crud_role
from app.schemas.role import Role, RoleCreate, RoleUpdate
from app.schemas.response import SuccessResponse
from app.models.user import User
from app.dependencies import get_current_user, PermissionChecker

router = APIRouter()

@router.get("", response_model=List[Role])
def get_roles(
    db: Session = Depends(get_db), 
    _: bool = Depends(PermissionChecker("role:view_all"))
):
    return crud_role.get_roles(db)

@router.get("/{role_id}", response_model=Role)
def get_role(
    role_id: int, 
    db: Session = Depends(get_db), 
    _: bool = Depends(PermissionChecker("role:view"))
):
    return crud_role.get_role(db, role_id)

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
    crud_role.update_role(db, role_id, role_in)

    return SuccessResponse(message="Role updated successfully")

@router.delete("/{role_id}", response_model=SuccessResponse)
def delete_role(
    role_id: int, 
    db: Session = Depends(get_db), 
    _: bool = Depends(PermissionChecker("role:delete"))
):
    crud_role.delete_role(db, role_id)

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

    if role.name == "ADMIN" and current_user.role.name != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not enough permissions"
        )
    
    crud_role.assign_role(db, user_id, role_id)

    return SuccessResponse(message="Role assigned to user successfully")

@router.post("/{role_id}/permissions/{permission_id}", response_model=SuccessResponse)
def add_permission_to_role(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(PermissionChecker("role:add_permission"))
):  
    crud_role.add_permission(db, role_id, permission_id)

    return SuccessResponse(message="Permission added to role successfully")

@router.delete("/{role_id}/permissions/{permission_id}", response_model=SuccessResponse)
def remove_permission_from_role(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(PermissionChecker("role:remove_permission"))
):  
    crud_role.remove_permission(db, role_id, permission_id)

    return SuccessResponse(message="Permission removed from role successfully")

