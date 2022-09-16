from . schemas import UserpasswordUpdate,CreateUser, UserInDB
from sqlalchemy.orm import Session
from .models import User
from app.core.config import settings
from . import auth_service

db = Session()
async def create_user(new_user: CreateUser) -> UserInDB:
    # This is a UserPasswordUpdate
    new_password = auth_service.create_salt_hashed_password(plain_text_password=new_user.password)
    # Next we extend our CreateUser schema here
    new_user_params = new_user.copy(update=new_password.dict())
    # Updated and extended CreateUser schema was passed to UserInDB
    new_user_updated = UserInDB(**new_user_params.dict())
    # Just printing the result
    print(new_user_updated)

    # Here we are openning one time connection
    async with db.with_bind(settings.DATABASE_URI) as engine:
        # Database model User creation happens here
        created_user = await User.create(**new_user_updated.dict())

    # And now we nicely return from_orm with UserInDB
    return UserInDB.from_orm(created_user)