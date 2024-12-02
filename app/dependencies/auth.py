from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status,  Response, Request, Depends
from pydantic import EmailStr
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import CurrentUserResponse, CurrentUserWithRoleResponse
from app.core.db import get_db
from app.utils.user import get_user
from app.utils.auth import create_token
from app.utils.cookies import set_cookies
from jose import JWTError, jwt
from app.models.user import UserRole
from typing import List, Callable

def role_validator(allowed_roles: List[str]) -> Callable:
    async def validate_user_role(
        request: Request,
        response: Response,
        db: Session = Depends(get_db)
    ) -> CurrentUserWithRoleResponse:
        """
        Validates the user's role and returns extended user information.
        """
        current_user = await get_current_user(request, response, db)

        user = get_user(current_user.email, db)
        if not user or user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Insufficient permissions.",
            )

        return CurrentUserWithRoleResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            is_email_verified=user.is_email_verified,
            role=user.role
        )
    return validate_user_role

async def get_current_user(request: Request, response: Response, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials"
    )
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    email = None
    if access_token:
        try:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: EmailStr = payload.get("sub")
        except JWTError:
            pass  
    if not email and refresh_token:
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: EmailStr = payload.get("sub")
            if email:
                new_access_token = create_token(
                    data={"sub": email},
                    token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
                )
                set_cookies(response, key="access_token", token=new_access_token, token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        except JWTError:
            raise credentials_exception

    if not email:
        raise credentials_exception

    user = get_user(email, db)
    if not user:
        raise credentials_exception
    
    return CurrentUserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        is_email_verified=user.is_email_verified
    )
    