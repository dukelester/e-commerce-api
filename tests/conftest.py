import pytest
from users import auth_service
from users.schemas import CreateUser, UserInDB

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
    