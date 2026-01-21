from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.crud import user as crud_user
from app.schemas.user import User, UserCreate, UserUpdate, CurrentUser, UserPage
from app.schemas.response import SuccessResponse
from app.dependencies import get_current_user, PermissionChecker

router = APIRouter()

@router.get("/me", response_model=CurrentUser)
def get_me(current_user: User = Depends(get_current_user)):
    return CurrentUser(
        id=current_user.id, 
        username=current_user.username, 
        role=current_user.role.name
    )

@router.post("", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate, 
    db: Session = Depends(get_db), 
    _: bool = Depends(PermissionChecker("user:create"))
):
    crud_user.create_user(db, user=user_in)

    return SuccessResponse(message="User created successfully")

@router.get("", response_model=UserPage)
def get_users(
    db: Session = Depends(get_db), 
    page: int = 1,
    limit: int = 10,
    _: bool = Depends(PermissionChecker("user:view_all"))
):
    offset = (page - 1) * limit

    users = crud_user.get_users(db, skip=offset, limit=limit)
    total = crud_user.get_total_users(db)

    return UserPage(
        users=users,
        total=total,
        page=page,
        limit=limit,
        total_pages=(total + limit - 1) // limit
    )

@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    _: bool = Depends(PermissionChecker("user:view"))
):
    if current_user.role.name == "ADMIN" or current_user.id == user_id:
        user = crud_user.get_user(db, user_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

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

    user = crud_user.update_user(db, user_id=user_id, user=user_in)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
        
    return SuccessResponse(message="User updated successfully")

@router.delete("/{user_id}", response_model=SuccessResponse)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(PermissionChecker("user:delete"))
):
    user = crud_user.delete_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    return SuccessResponse(message="User deleted successfully")

