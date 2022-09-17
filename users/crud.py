from . schemas import UserpasswordUpdate,CreateUser, UserInDB
from sqlalchemy.orm import Session
from .models import User
from app.core.config import settings
from . import auth_service
from app.database import SessionLocal

db = SessionLocal()
async def create_user(new_user: CreateUser) -> UserInDB:
    # This is a UserPasswordUpdate
    new_password = auth_service.create_salt_hashed_password(plain_text_password=new_user.password)
    # Next we extend our CreateUser schema here
    new_user_params = new_user.copy(update=new_password.dict())
    print(new_user_params)
    new_user = User(
        full_name=new_user_params.full_name,phone_number=new_user_params.phone_number,username=new_user_params.username,
         email_address=new_user_params.email_address,password=new_user_params.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
