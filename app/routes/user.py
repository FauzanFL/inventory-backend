from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.crud import user as crud_user
from app.schemas.user import User, UserCreate, UserUpdate
from app.schemas.response import SuccessResponse
from app.dependencies import get_current_user, PermissionChecker

router = APIRouter()

@router.post("", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate, 
    db: Session = Depends(get_db), 
    _: bool = Depends(PermissionChecker("user:create"))
):
    crud_user.create_user(db, user_in)

    return SuccessResponse(message="User created successfully")

@router.get("", response_model=List[User])
def get_users(
    db: Session = Depends(get_db), 
    _: bool = Depends(PermissionChecker("user:view_all"))
):
    return crud_user.get_users(db)

@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    _: bool = Depends(PermissionChecker("user:view"))
):
    return crud_user.get_user(db, user_id)

@router.patch("/{user_id}", response_model=SuccessResponse)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(PermissionChecker("user:update"))
):
    is_admin = current_user.role.name == "ADMIN"
    is_owner = current_user.id == user_id

    if not (is_admin or is_owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    db_user = crud_user.update_user(db, user_id=user_id, user_in=user_in)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")
        
    return SuccessResponse(message="User updated successfully")

@router.delete("/{user_id}", response_model=SuccessResponse)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(PermissionChecker("user:delete"))
):
    crud_user.delete_user(db, user_id)

    return SuccessResponse(message="User deleted successfully")

