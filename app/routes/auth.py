from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead
from app.schemas.client import ClientCreate
from app.services.auth import register_user_and_client
from app.core.db import get_db 
from app.models.user import UserRole  # Import the UserRole Enum

router = APIRouter()

@router.post("/client/register/", response_model=UserRead)
def register_client_user(
    user_create: UserCreate,
    client_create: ClientCreate,
    db: Session = Depends(get_db)
):
    try:
        # Enforce the role to be CLIENT_ADMIN in the backend using the Enum
        user_create.role = UserRole.CLIENT_ADMIN

        # Call the service to register both user and client
        result = register_user_and_client(db, user_create, client_create)
        user = result["user"]
        client = result["client"]

        # Return UserRead object with nested client data if needed
        return UserRead(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active
        )

    except Exception as e:
        # Raise HTTPException with detailed error messages
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error registering client user: {str(e)}"
        )
