from sqlalchemy import Column, String, Boolean, Enum, UUID, TIMESTAMP, event, DateTime
from sqlalchemy.sql import func
from app.core.db import Base
import uuid
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship

# Enum for roles
class UserRole(PyEnum):
    super_admin = "super_admin"
    client_admin = "client_admin"
    referrer = "referrer"
    referred = "referred"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    is_email_verified = Column(Boolean, default=False)  
    otp = Column(String, nullable=True)  
    otp_expires_at = Column(DateTime, nullable=True) 
    role = Column(Enum(UserRole, name="user_role_enum"), nullable=False)  
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=func.now(), nullable=True)
    is_active = Column(Boolean, default=True)

    # One-to-One relationship with Client
    client = relationship("Client", back_populates="user", uselist=False)
    
@event.listens_for(User, 'before_insert')
def lowercase_email(mapper, connection, target):
    if target.email:
        target.email = target.email.lower()

@event.listens_for(User, 'before_update')
def email_on_update(mapper, connection, target):
    if target.email:
        target.email = target.email.lower()
