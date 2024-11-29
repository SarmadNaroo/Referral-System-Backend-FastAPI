from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from enum import Enum as PyEnum
from datetime import datetime

class UserRole(PyEnum):
    SUPER_ADMIN = "super_admin"
    CLIENT_ADMIN = "client_admin"
    REFERRER = "referrer"
    REFERRED = "referred"

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str  

class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
