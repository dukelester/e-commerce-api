from fastapi import HTTPException
from . schemas import UserpasswordUpdate,CreateUser, UserInDB
from .models import User
from app.core.config import settings
from . import auth_service
from app.database import SessionLocal
from pydantic import EmailStr

db = SessionLocal()

def get_user_by_username(username: str):
    found_user = db.query(User).filter(User.username == username).first()
    print(username, found_user)
    return found_user or False

async def get_user_by_phone_number(phone_number: str) -> UserInDB:
    found_user = await db.query(User).filter(User.phone_number == phone_number).first()
    return found_user or False

async def get_user_by_email(email_address: EmailStr) -> UserInDB:
    found_user = await db.query(User).filter(User.email_address == email_address).first()
    return found_user or False


async def create_user(new_user: CreateUser) -> UserInDB:
    # This is a UserPasswordUpdate
    new_password = auth_service.create_salt_hashed_password(plain_text_password=new_user.password)
    # Next we extend our CreateUser schema here
    new_user_params = new_user.copy(update=new_password.dict())
    print(new_user_params)
    # if await get_user_by_username(new_user_params.username):
    #     raise HTTPException( status_code=400, detail="User with that username already exixts !")
    # if await get_user_by_email(new_user_params.email_address):
    #     raise HTTPException( status_code=400, detail="User with that email address already exixts !")
    # if await get_user_by_phone_number(new_user_params.phone_number):
    #     raise HTTPException( status_code=400, detail="User with that phone number already exixts !")
    
    new_user = User(
        full_name=new_user_params.full_name,phone_number=new_user_params.phone_number,username=new_user_params.username,
         email_address=new_user_params.email_address,password=new_user_params.password, salt=new_user_params.salt
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    


