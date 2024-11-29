from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.models.client import Client
from app.schemas.user import UserCreate
from app.schemas.client import ClientCreate
from app.utils.security import hash_password

def register_user_and_client(db: Session, user_create: UserCreate, client_create: ClientCreate):
    try:
        # Create the User
        user = User(
            name=user_create.name,
            email=user_create.email,
            password_hash=hash_password(user_create.password), 
            role=user_create.role,
        )
        
        db.add(user)
        db.commit() 
        db.refresh(user)

        # Create the Client and link to the User
        client = Client(
            name=client_create.name,
            user_id=user.id 
        )

        db.add(client)
        db.commit() 
        db.refresh(client)  

        # Update the User with the `client_id`
        user.client_id = client.id 
        db.commit()

        # Return the created user and client as a dictionary
        return {"user": user, "client": client}

    except SQLAlchemyError as e:
        db.rollback() 
        raise Exception(f"Database error: {str(e)}")

    except Exception as e:
        db.rollback()  
        raise Exception(f"Unexpected error: {str(e)}")
