from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.crud import item as crud_item
from app.schemas.item import Item, ItemCreate, ItemUpdate, ItemPage
from app.schemas.response import SuccessResponse
from app.models.user import User
from app.dependencies import get_current_user, PermissionChecker

router = APIRouter()

@router.post("", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item_in: ItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    _: bool = Depends(PermissionChecker("item:create"))
):
    crud_item.create_item(db, item=item_in, user_id=current_user.id)

    return SuccessResponse(message="Item created successfully")


@router.get("", response_model=ItemPage)
def get_items(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    _: bool = Depends(PermissionChecker("item:view_all"))
):
    offset = (page - 1) * limit
    is_admin = current_user.role.name == "ADMIN"

    if is_admin:
        items = crud_item.get_items(db, skip=offset, limit=limit, search=search)
        total = crud_item.get_total_items(db, search=search)
    else:
        items = crud_item.get_user_items(db, user_id=current_user.id, skip=offset, limit=limit, search=search)
        total = crud_item.get_user_total_items(db, user_id=current_user.id, search=search)

    return ItemPage(
        items=items,
        total=total,
        page=page,
        limit=limit,
        total_pages=(total + limit - 1) // limit
    )

@router.get("/{item_id}", response_model=Item)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(PermissionChecker("item:view"))
):
    return crud_item.get_item(db, item_id)

@router.put("/{item_id}", response_model=SuccessResponse)
def update_item(
    item_id: int,
    item_in: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(PermissionChecker("item:update"))
):
    is_admin = current_user.role.name == "ADMIN"

    if not is_admin and item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this item",
        )

    item = crud_item.get_item(db, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    crud_item.update_item(db, item_id=item_id, item=item_in)
    
    return SuccessResponse(message="Item updated successfully")

@router.delete("/{item_id}", response_model=SuccessResponse)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(PermissionChecker("item:delete"))
):
    is_admin = current_user.role.name == "ADMIN"
    
    if not is_admin and item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this item",
        )

    item = crud_item.get_item(db, item_id=item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    
    
    crud_item.delete_item(db, item_id=item_id)
    
    return SuccessResponse(message="Item deleted successfully")