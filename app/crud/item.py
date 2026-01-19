from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).order_by(Item.id.desc()).offset(skip).limit(limit).all()

def get_user_items(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Item).filter(Item.owner_id == user_id).order_by(Item.id.desc()).offset(skip).limit(limit).all()

def get_total_items(db: Session):
    return db.query(Item).count()

def get_user_total_items(db: Session, user_id: int):
    return db.query(Item).filter(Item.owner_id == user_id).count()

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def create_item(db: Session, item: ItemCreate, user_id: int):
    db_item = Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: ItemUpdate):
    query = db.query(Item).filter(Item.id == item_id)

    db_item = query.first()
    if db_item:
        for key, value in item.model_dump(exclude_unset=True).items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        
    return db_item

def delete_item(db: Session, item_id: int):
    query = db.query(Item).filter(Item.id == item_id)

    db_item = query.first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item