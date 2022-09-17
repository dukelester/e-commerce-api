import string
from typing import Optional
from datetime import datetime, timedelta
from app.schemas import CoreModel, DateTimeModelMixin, IDModelMixin
from pydantic import  EmailStr, constr, validator
from app.core.config import settings

def validate_username(username: str):
    allowed = string.ascii_letters + string.digits + "-" + "_"
    assert all(char in allowed for char in username), "Invalid username "
    assert len(username ) >= 3, "Username Must exceed 3 characters"
    return username

def validate_phone_number(phone_number: str):
    if len(phone_number) == 10 and int(phone_number[0]) == 0 and int(phone_number[1]) == 7:
        return f'+254{phone_number[1:]}'
    if len(phone_number) == 12 and phone_number[0] == '2' and phone_number[1] == '5' and phone_number[2] == '4':
        return f'+{phone_number}'
    
    if len(phone_number) < 10:
            raise ValueError("Invalid phone number: number too short")
    
    return phone_number

def validate_full_name(full_name: str):
    if " " not in full_name:
        raise ValueError("User full name must contain space ")
    return full_name.title()

class UserBase(CoreModel):
    """ Leave out the password and hashed password """
    username: Optional[str]
    full_name: Optional[str] | None = None
    email_address: Optional[EmailStr]
    phone_number: Optional[str]
    is_email_verified: bool = False
    is_active: bool = True
    is_superuser: bool = False
    
    @validator("full_name", pre=True)
    def validate_full_name(cls, full_name):
        return validate_full_name(full_name)

    @validator("phone_number", pre=True)
    def validate_phone_number(cls, phone_number):
        return validate_phone_number(phone_number)
    
    class Config:
        orm_mode = True
        
    
class CreateUser(CoreModel):
    """ We need the user email, username and password to create user """
    full_name: str | None = None
    phone_number: str | None = None
    username: str
    email_address: EmailStr
    password: constr(min_length=8, max_length=100)
    
    @validator("username", pre=True)
    def validate_username(cls, username):
        return validate_username(username)
    
    @validator("phone_number", pre=True)
    def validate_phone_number(cls, phone_number):
        return validate_phone_number(phone_number)
    
    @validator("full_name", pre=True)
    def validate_full_name(cls, full_name):
        return validate_full_name(full_name)
    
    class Config:
        orm_mode = True
class UserInDB(IDModelMixin, DateTimeModelMixin, UserBase):
    """
    Add in id, created_at, updated_at, and user's password and salt
    """
    password: constr(min_length=8, max_length=100)
    salt: str
    
    class Config:
        orm_mode = True

class AccessToken(CoreModel):
    access_token: str
    token_type: str


class UserPublic(DateTimeModelMixin, UserBase):
    access_token: Optional[AccessToken]
    class Config:
        orm_mode = True

# TODO: UserUpdate for profile update can be here

# TODO: UserPasswordUpdate for password update can be here

class UserpasswordUpdate(CoreModel):
    """
    Users can change their password
    """
    password: constr(min_length=8, max_length=100)
    salt: str
    
    class Config:
        orm_mode = True

    
# JWT SCHEMAS

class JWTMeta(CoreModel):
    iss: str = "azepug.az"
    aud: str = settings.JWT_AUDIENCE
    iat: float = datetime.timestamp(datetime.now())
    exp: float = datetime.timestamp(datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    
class JWTCredentials(CoreModel):
    """How we'll identify users"""
    sub: EmailStr
    username: str
    
class JWTPayload(JWTMeta, JWTCredentials):
    """
    JWT Payload right before it's encoded - combine meta and username
    """
    pass
    

class UserLogin(CoreModel):
    """ Users can only login with email andpassword """
    username: str
    password: constr(min_length=8, max_length=100)
    
    @validator("username", pre=True)
    def validate_username(cls, username):
        return validate_username(username)