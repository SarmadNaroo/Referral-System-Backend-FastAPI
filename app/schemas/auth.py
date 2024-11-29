from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthUserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=32)
    name: str = Field(..., min_length=2, max_length=100)

class UserInfo(BaseModel):
    id: UUID
    name : str
    email : EmailStr
    is_email_verified: bool

    class Config(): 
        from_attributes = True

class ShowUserResponse(BaseModel):
    user: UserInfo

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    password: str

class CurrentUserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    is_email_verified: bool