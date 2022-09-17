from fastapi import APIRouter, status, Body,HTTPException
from fastapi.responses import JSONResponse

from ..schemas import  AccessToken, UserLogin, UserPublic, CreateUser
from ..crud import create_user, get_user_by_username
from users import auth_service

router = APIRouter()

@router.post("/create", summary="Creating a new user", tags=['create user'], 
             response_model=UserPublic, status_code=201)
async def user_create(user: CreateUser):
    return await create_user(user)

@router.post("/login",summary="User login ", tags=['Login a user'],
             response_model=UserPublic, status_code=200)
def user_login(user: UserLogin):
    found_user = get_user_by_username(username=user.username)
    if auth_service.verify_password(password=user.password, salt=found_user.salt,hashed_password=found_user.password):
        # If the provided password is valid one then we are going to create an access token
        print(found_user.username,found_user.salt, 'found user')
        # token = auth_service.create_access_token_for_user(user=found_user)
        # print(token, 'TOKENEEEE')
        return found_user

    raise HTTPException( status_code=401, detail="Invalid password ")
    # raise HTTPException( status_code=400, detail="User with those credentials not found! ")
            
            
    
    
# found_user = await get_user_by_username(user_name=user.username)
#     if auth_service.verify_password(password=user.password, salt=found_user.salt, hashed_pw=found_user.password):
#         # If the provided password is valid one then we are going to create an access token
#         token = auth_service.create_access_token_for_user(user=found_user)
#         access_token = AccessToken(access_token=token, token_type='bearer')
#         return UserPublic(**found_user.dict(), access_token=access_token)