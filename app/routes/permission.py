from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.crud import permission as crud_permission
from app.schemas.permission import Permission, PermissionCreate, PermissionUpdate
from app.schemas.response import SuccessResponse
from app.models.user import User
from app.dependencies import get_current_user, PermissionChecker

router = APIRouter()

@router.get("", response_model=List[Permission])
def get_permissions(
    db: Session = Depends(get_db), 
    _: bool = Depends(PermissionChecker("permission:view_all"))
):
    return crud_permission.get_permissions(db)

@router.get("/{permission_id}", response_model=Permission)
def get_permission(
    permission_id: int, 
    db: Session = Depends(get_db), 
    _: bool = Depends(PermissionChecker("permission:view"))
):
    permission = crud_permission.get_permission(db, permission_id)

    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")

    return permission

@router.post("", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_permission(
    permission_in: PermissionCreate, 
    db: Session = Depends(get_db), 
    _: bool = Depends(PermissionChecker("permission:create"))
):
    crud_permission.create_permission(db, permission_in)

    return SuccessResponse(message="Permission created successfully")

@router.patch("/{permission_id}", response_model=SuccessResponse)
def update_permission(
    permission_id: int, 
    permission_in: PermissionUpdate, 
    db: Session = Depends(get_db), 
    _: bool = Depends(PermissionChecker("permission:update"))
):
    permission = crud_permission.update_permission(db, permission_id, permission_in)

    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")

    return SuccessResponse(message="Permission updated successfully")

@router.delete("/{permission_id}", response_model=SuccessResponse)
def delete_permission(
    permission_id: int, 
    db: Session = Depends(get_db), 
    _: bool = Depends(PermissionChecker("permission:delete"))
):
    permission = crud_permission.delete_permission(db, permission_id)

    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")

    return SuccessResponse(message="Permission deleted successfully")

