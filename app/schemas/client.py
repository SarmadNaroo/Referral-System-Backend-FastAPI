from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# Schema for creating a client (request model)
class ClientBase(BaseModel):
    name: str

class ClientCreate(ClientBase):
    pass 

class ClientRead(ClientBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
       from_attributes = True
