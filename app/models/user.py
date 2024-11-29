from sqlalchemy import Column, String, Boolean, Enum, UUID, TIMESTAMP
from sqlalchemy.sql import func
from app.core.db import Base
import uuid
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship

# Enum for roles
class UserRole(PyEnum):
    SUPER_ADMIN = "super_admin"
    CLIENT_ADMIN = "client_admin"
    REFERRER = "referrer"
    REFERRED = "referred"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole, name="user_role_enum"), nullable=False)  
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=func.now(), nullable=True)
    is_active = Column(Boolean, default=True)

    # One-to-One relationship with Client
    client = relationship("Client", back_populates="user", uselist=False)
