from sqlalchemy import Column, String, UUID, TIMESTAMP
from sqlalchemy.sql import func
from app.core.db import Base
from sqlalchemy import ForeignKey
from app.models.user import User
import uuid
from sqlalchemy.orm import relationship

class Client(Base):
    __tablename__ = "clients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)  # Foreign Key linking to User
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=func.now(), nullable=True)

    # One-to-One relationship with User
    user = relationship("User", back_populates="client")
