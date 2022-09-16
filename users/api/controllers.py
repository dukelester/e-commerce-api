from fastapi import APIRouter, status, Body
from fastapi.responses import JSONResponse

from ..schemas import  UserPublic, CreateUser
from ..crud import create_user

router = APIRouter()

@router.post("/create", summary="Creating a new user", tags=['create user'], 
             response_model=UserPublic, status_code=201)
async def user_create(user: CreateUser):
    return await create_user(user)
    
