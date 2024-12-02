from fastapi import Depends, APIRouter, Response, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.dependencies.auth import role_validator
from app.schemas.auth import CurrentUserWithRoleResponse
from app.models.user import User, UserRole

router = APIRouter()

@router.get("/admin/dashboard", response_model=dict)
async def client_admin_dashboard(
    user: CurrentUserWithRoleResponse = Depends(role_validator([UserRole.client_admin])),
):
    """
    A protected route accessible only to client_admin users.
    """
    return {
        "message": "Welcome to the Client Admin Dashboard!",
        "user": user
    }
