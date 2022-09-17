import asyncio
import pytest

from backend.users.schemas import CreateUser, UserLogin
from . import init_db
from users.models import User
from app.database import SessionLocal
db = SessionLocal()

class TestApiEndpoints:
    async def remove_user(self, create_new_user):
        test_user = await db.query(User).filter(User.username == create_new_user.username).first()
        await test_user.delete()
    
    @pytest.mark.asyncio
    async def test_create_user(self,client, init_db, create_new_user):
        response = await client.post("/users/create", json=create_new_user.dict())
        assert response.status_code == 201
        assert response['username'] == create_new_user.username
        
        await self.remove_user(create_new_user=create_new_user)
    
    @pytest.mark.asyncio
    async def test_user_create_wrong_email_format(self, client, init_db, create_new_user):
        wrong_user = CreateUser(
            full_name="Wrong user",
            phone_number="073456782",
            email_address="wrong.user@gmail.com",
            username="wrong_user",
            password="wrong_user_password"
        )

        wrong_user.email_address = 'wrong_email'
        res = await client.post('users/create', json=wrong_user.dict())
        print(res.json())
        assert 'value is not a valid email address' == res.json()['detail'][0]['msg']
    
    @pytest.mark.asyncio
    async def test_user_create_wrong_username_format(self, client, init_db, create_new_user):
        wrong_user = CreateUser(
            full_name="Wrong user",
            phone_number="073456082",
            email_address="wrong.user@gmail.com",
            username="wrong_user",
            password="wrong_user_password"
        )

        wrong_user.username = 'asd_sad$?'
        res = await client.post('users/create', json=wrong_user.dict())
        print(res.json())
        assert 'Invalid characters in username.' == res.json()['detail'][0]['msg']

    @pytest.mark.asyncio
    async def test_user_create_wrong_password_format(self, client, init_db, create_new_user):
        wrong_user = CreateUser(
            full_name="Wrong user",
            phone_number="0734567802",
            email_address="wrong.user@gmail.com",
            username="wrong_user",
            password="wrong_user_password"
        )

        wrong_user.password = '13'
        res = await client.post('users/create', json=wrong_user.dict())
        print(res.json())
        assert 'ensure this value has at least 7 characters' == res.json()['detail'][0]['msg']
        
    @pytest.mark.asyncio
    async def test_user_login_with_non_existing_username(self, client, init_db):
        fake_user = UserLogin(
            username="non-existing-username",
            password="fake-password"
        )
        res = await client.post('users/login', json=fake_user.dict())
        print(res.json())
        assert res.status_code == 404
        assert res.json()['detail'] == "User with those credentials not found! "

    @pytest.mark.asyncio
    async def test_user_login_with_wrong_password(self, client, init_db, create_new_user):
        # Create the user
        res = await client.post('users/create', json=create_new_user.dict())
        assert res.json()['username'] == create_new_user.username

        # Try to login with wrong password
        fake_user = UserLogin(
            username="duketest",
            password="fake-password"
        )
        res = await client.post('users/login', json=fake_user.dict())
        print(res.json())
        assert res.status_code == 401
        assert res.json(['detail']) == "Invalid password"
        await self.remove_user(create_new_user=create_new_user)
        
    @pytest.mark.asyncio
    async def test_user_login_with_success(self, client, init_db, create_new_user):
        # Create the user
        res = await client.post('users/create', json=create_new_user.dict())
        assert res.json()['username'] == create_new_user.username

        # Try to login with wrong password
        valid_user = UserLogin(
            username="duketest",
            password="duke@test2022"
        )
        res = await client.post('users/login', json=valid_user.dict())
        assert res.status_code == 200
        assert res.json()['access_token']
        await self.remove_user(create_new_user=create_new_user)