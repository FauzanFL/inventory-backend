from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)

    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)

    role = relationship("Role", back_populates="users")
    items = relationship("Item", back_populates="owner")