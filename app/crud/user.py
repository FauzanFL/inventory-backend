from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from sqlalchemy import or_

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(User)
    if search:
        query = query.filter(or_(User.username.ilike(f"%{search}%"), User.email.ilike(f"%{search}%")))
    return query.order_by(User.id.desc()).offset(skip).limit(limit).all()

def get_total_users(db: Session, search: str = None):
    query = db.query(User)
    if search:
        query = query.filter(or_(User.username.ilike(f"%{search}%"), User.email.ilike(f"%{search}%")))
    return query.count()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user: UserUpdate):
    query = db.query(User).filter(User.id == user_id)

    db_user = query.first()
    if db_user:
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def update_password(db: Session, user_id: int, password: str):
    query = db.query(User).filter(User.id == user_id)

    db_user = query.first()
    if db_user:
        db_user.password = get_password_hash(password)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    query = db.query(User).filter(User.id == user_id)

    db_user = query.first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user