from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.crud import item as crud_item
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.models.user import User
from app.dependencies import get_current_user, PermissionChecker

router = APIRouter()

@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(
    item_in: ItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _: bool = Depends(PermissionChecker("item:create"))
):
    return crud_item.create_item(db, item_in, user_id=current_user.id)


@router.get("", response_model=List[Item])
def get_items(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    _: bool = Depends(PermissionChecker("item:view"))
):
    if current_user.role.name == "ADMIN":
        return crud_item.get_items(db)
    return crud_item.get_user_items(db, user_id=current_user.id)

@router.get("/{item_id}", response_model=Item)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(PermissionChecker("item:view"))
):
    return crud_item.get_item(db, item_id)

@router.patch("/{item_id}", response_model=Item)
def update_item(
    item_id: int,
    item_in: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(PermissionChecker("item:update"))
):
    is_admin = current_user.role.name == "ADMIN"
    item = crud_item.update_item(db, user_id=current_user.id, item_id=item_id, item=item_in, is_admin=is_admin)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or you don't have permission",
        )
    else:
        return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(PermissionChecker("item:delete"))
):
    is_admin = current_user.role.name == "ADMIN"
    item = crud_item.delete_item(db, user_id=current_user.id, item_id=item_id, is_admin=is_admin)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or you don't have permission",
        )
    else:
        return