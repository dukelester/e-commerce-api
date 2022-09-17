import email
from fastapi import APIRouter, status, Body,HTTPException
from fastapi.responses import JSONResponse

from ..schemas import  AccessToken, UserLogin, UserPublic, CreateUser
from ..crud import create_user, get_user_by_email, get_user_by_phone_number, get_user_by_username
from users import auth_service

router = APIRouter()

@router.post("/create", summary="Creating a new user", tags=['create user'], 
             response_model=UserPublic, status_code=201)
async def user_create(user: CreateUser):
    
    if found_user:=  get_user_by_username(username=user.username):
        raise HTTPException(status_code=400, detail="user with such username already exists! ")
    
    return await create_user(user)

@router.post("/login",summary="User login ", tags=['Login a user'],
              status_code=200)
def user_login(user: UserLogin):
    if found_user := get_user_by_username(username=user.username):
        if auth_service.verify_password(password=user.password, salt=found_user.salt,hashed_password=found_user.password):
            # If the provided password is valid one then we are going to create an access token
            token = auth_service.create_access_token_for_user(user=found_user)
            # print(token, 'TOKENEEEE',found_user)
            access_token = AccessToken(access_token=token, token_type='bearer')
            return { 'access_token': access_token }
            # return UserPublic.from_orm(**found_user.dict(), access_token=access_token)
        raise HTTPException( status_code=401, detail="Invalid password ")
    raise HTTPException( status_code=404, detail="User with those credentials not found! ")