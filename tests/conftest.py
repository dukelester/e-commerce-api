import pytest
from users import auth_service
from users.schemas import CreateUser, UserInDB
from fastapi.testclient import TestClient
import app
from httpx import AsyncClient

client = TestClient(app)

@pytest.fixture(scope="class")
def auth_object ():
    return auth_service

@pytest.fixture(scope="class")
def duke_test_user() -> UserInDB:
    dummy_user = CreateUser(full_name="duke lester", phone_number="0745678920",
                            email_address="duke@gmail.com",password="duke@test2022",
                            username="duketest",
                            )
    new_password = auth_service.create_salt_and_hashed_password(plain_password=dummy_user.password)
    new_user_params = dummy_user.copy(update=new_password.dict())
    return UserInDB(**new_user_params.dict())
    
    
@pytest.yield_fixture
async def client():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/") as async_client:
        yield async_client
        
@pytest.yield_fixture
def create_new_user():
   yield CreateUser(
        full_name="Jane Markings",phone_number="0795272433",email_address="janemark@gmail.com",
        username="jannymarkings", password="Jane@markings2022"
    )