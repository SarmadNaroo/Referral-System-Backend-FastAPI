from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import hash_password
from app.schemas.user import UserCreate

# Function to register user
def register_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
