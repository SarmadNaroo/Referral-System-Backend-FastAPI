from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models.user import User

def get_user(email: EmailStr, db:Session):
    user = db.query(User).filter(User.email == email.lower()).first()
    return user
