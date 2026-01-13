from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    sku: str
    quantity: int

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    sku: Optional[str] = None
    quantity: Optional[int] = None

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True