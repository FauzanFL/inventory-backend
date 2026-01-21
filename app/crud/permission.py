from sqlalchemy.orm import Session
from app.models.rbac import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate


def get_permissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Permission).order_by(Permission.id.desc()).offset(skip).limit(limit).all()

def get_total_permissions(db: Session):
    return db.query(Permission).count()

def get_permission(db: Session, permission_id: int):
    return db.query(Permission).filter(Permission.id == permission_id).first()

def create_permission(db: Session, permission: PermissionCreate):
    db_permission = Permission(**permission.model_dump())
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def update_permission(db: Session, permission_id: int, permission: PermissionUpdate):
    query = db.query(Permission).filter(Permission.id == permission_id)

    db_permission = query.first()
    if db_permission:
        for key, value in permission.model_dump(exclude_unset=True).items():
            setattr(db_permission, key, value)
        db.commit()
        db.refresh(db_permission)
    return db_permission

def delete_permission(db: Session, permission_id: int):
    query = db.query(Permission).filter(Permission.id == permission_id)

    db_permission = query.first()
    if db_permission:
        db.delete(db_permission)
        db.commit()
    return db_permission