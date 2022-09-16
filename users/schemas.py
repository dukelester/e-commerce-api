import string
from typing import Optional

from backend.app.schemas import CoreModel, DateTimeModelMixin, IDModelMixin
from pydantic import  EmailStr, constr, validator

def validate_username(username: str):
    allowed = string.ascii_letters + string.digits + "-" + "_"
    assert all(char in allowed for char in username), "Invalid username "
    assert len(username ) >= 3, "Username Must exceed 3 characters"
    return username

class UserBase(CoreModel):
    """ Leave out the password and hashed password """
    username: Optional[str]
    full_name: Optional[str] | None = None
    email_address: Optional[EmailStr]
    phone_number: Optional[str]
    is_email_verified: bool = False
    is_active: bool = True
    is_superuser: bool = False
    
class CreateUser(CoreModel):
    """ We need the user email, username and password to create user """
    username: str
    email_address: EmailStr
    password: constr(min_length=8, max_length=100)
    
    @validator("username", pre=True)
    def validate_username(cls, username):
        return validate_username(username)
    
class userInDB(IDModelMixin, DateTimeModelMixin, UserBase):
    """
    Add in id, created_at, updated_at, and user's password and salt
    """
    password: constr(min_length=8, max_length=100)
    hash_password: str
    
class UserPublic(DateTimeModelMixin, UserBase):
    pass

# TODO: UserUpdate for profile update can be here

# TODO: UserPasswordUpdate for password update can be here
    
    

    
