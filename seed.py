from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.models.base import Base
from app.models.rbac import Role, Permission
from app.models.user import User
from app.core.security import get_password_hash
from app.models import *

def seed_data():
    db: Session = SessionLocal()

    perms_data = [
        {"name": "item:view_all", "desc": "Bisa melihat daftar barang"},
        {"name": "item:view", "desc": "Bisa melihat satu barang"},
        {"name": "item:create", "desc": "Bisa menambah barang baru"},
        {"name": "item:update", "desc": "Bisa mengedit barang"},
        {"name": "item:delete", "desc": "Bisa menghapus barang"},
        {"name": "permission:view_all", "desc": "Bisa melihat daftar permission"},
        {"name": "permission:view", "desc": "Bisa melihat satu permission"},
        {"name": "permission:create", "desc": "Bisa menambah permission baru"},
        {"name": "permission:update", "desc": "Bisa mengedit permission"},
        {"name": "permission:delete", "desc": "Bisa menghapus permission"},
        {"name": "role:view_all", "desc": "Bisa melihat daftar role"},
        {"name": "role:view", "desc": "Bisa melihat satu role"},
        {"name": "role:create", "desc": "Bisa menambah role baru"},
        {"name": "role:update", "desc": "Bisa mengedit role"},
        {"name": "role:delete", "desc": "Bisa menghapus role"},
        {"name": "role:assign", "desc": "Bisa menambahkan role ke user"},
        {"name": "role:add_permission", "desc": "Bisa menambahkan permission ke role"},
        {"name": "role:remove_permission", "desc": "Bisa menghapus permission dari role"},
        {"name": "user:view_all", "desc": "Bisa melihat daftar user"},
        {"name": "user:view", "desc": "Bisa melihat satu user"},
        {"name": "user:create", "desc": "Bisa menambah user baru"},
        {"name": "user:update", "desc": "Bisa mengedit user"},
        {"name": "user:delete", "desc": "Bisa menghapus user"},
    ]

    perms_obj = {}
    for p in perms_data:
        perm = db.query(Permission).filter(Permission.name == p["name"]).first()
        if not perm:
            perm = Permission(name=p["name"], description=p["desc"])
            db.add(perm)
            db.commit()
            db.refresh(perm)
        perms_obj[p["name"]] = perm
    
    admin_role = db.query(Role).filter(Role.name == "ADMIN").first()
    if not admin_role:
        admin_role = Role(name="ADMIN", description="Full access Admin")
        admin_role.permissions = [perms_obj[n] for n in perms_obj]
        db.add(admin_role)

    staff_role = db.query(Role).filter(Role.name == "STAFF").first()
    if not staff_role:
        staff_role = Role(name="STAFF", description="Storage staff")
        staff_role.permissions = [
            perms_obj["item:view_all"],
            perms_obj["item:view"], 
            perms_obj["item:create"],
            perms_obj["user:view"],
            perms_obj["user:update"]
        ]
        db.add(staff_role)
    
    db.commit()
    db.refresh(admin_role)
    db.refresh(staff_role)

    user_data = [
        {
            "username": "admin",
            "email": "admin@company.com",
            "password": "password123",
            "role_id": admin_role.id
        },
        {
            "username": "staff_joko",
            "email": "joko@company.com",
            "password": "password123",
            "role_id": staff_role.id
        }
    ]

    for u in user_data:
        user_exists = db.query(User).filter(User.username == u["username"]).first()
        if not user_exists:
            hashed = get_password_hash(u["password"])

            user = User(
                username=u["username"],
                email=u["email"],
                password=hashed,
                role_id=u["role_id"]
            )
            db.add(user)
            db.commit()

    print("Seed data success")
    db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_data()