from sqlalchemy.orm import Session, joinedload
from app.models.rbac import Role
from app.models.user import User
from app.schemas.role import RoleCreate, RoleUpdate, Role

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Role).options(joinedload(Role.permissions)).offset(skip).limit(limit).all()

def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()

def create_role(db: Session, role: RoleCreate):
    db_role = Role(**role.model_dump(exclude_unset=True))
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, role_id: int, role: RoleUpdate):
    query = db.query(Role).filter(Role.id == role_id)

    db_role = query.first()
    if db_role:
        for key, value in role.model_dump(exclude_unset=True).items():
            setattr(db_role, key, value)
        db.commit()
        db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int):
    query = db.query(Role).filter(Role.id == role_id)

    db_role = query.first()
    if db_role:
        db.delete(db_role)
        db.commit()
    return db_role

def assign_role(db: Session, user_id: int, role_id: int):
    query = db.query(User).filter(User.id == user_id)

    db_user = query.first()
    if db_user:
        db_user.role_id = role_id
        db.commit()
        db.refresh(db_user)
    return db_user

def add_permission(db: Session, role_id: int, permission_id: int):
    query = db.query(Role).filter(Role.id == role_id)

    db_role = query.first()
    if db_role:
        db_role.permissions.append(permission_id)
        db.commit()
        db.refresh(db_role)
    return db_role

def remove_permission(db: Session, role_id: int, permission_id: int):
    query = db.query(Role).filter(Role.id == role_id)

    db_role = query.first()
    if db_role:
        db_role.permissions.remove(permission_id)
        db.commit()
        db.refresh(db_role)
    return db_role