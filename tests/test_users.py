import pytest
import jwt
from app.core.config import settings
from jose import JWTError

@pytest.mark.usefixtures("auth_object")
@pytest.mark.usefixtures("duke_test_user")
class TestAuthenticate:
    def test_create_salt_and_hashed_passwords(self, auth_object):
        test_password = '123456789'
        first_password = auth_object.create_salt_hashed_password(plain_text_password = test_password)
        second_password = auth_object.create_salt_hashed_password(plain_text_password = test_password)
        assert first_password.password is not second_password.password
        
    def test_create_access_token_for_user(self,*,auth_object, duke_test_user):
        token = auth_object.create_access_token_for_user(user=duke_test_user)
        jwt_decode = jwt.decode(token, str(settings.SECRET_KEY),algorithms=[settings.JWT_ALGORITHM],
                                audience=settings.JWT_AUDIENCE
                                )
        assert isinstance(jwt_decode, dict)
        assert jwt_decode['username'] == duke_test_user.username
    
    def test_create_access_token_for_user_wrong_secret_key(self, auth_obj, duke_test_user):
        token = auth_obj.create_access_token_for_user(user=duke_test_user)
        with pytest.raises(JWTError) as jwt_error:
            jwt.decode(
                token,
                str('nice-wrong-secret-key'),
                audience=settings.JWT_AUDIENCE,
                algorithms=settings.JWT_ALGORITHM
            )

        assert 'Signature verification failed' in str(jwt_error.value)

    def test_create_access_token_for_user_wrong_audience(self, auth_obj, duke_test_user):
        token = auth_obj.create_access_token_for_user(user=duke_test_user)
        with pytest.raises(jwt_error) as jwt_error:
            jwt.decode(token,
                        str(settings.SECRET_KEY),
                        audience='heyyy',
                        algorithms=settings.JWT_ALGORITHM)

        assert 'Invalid audience' in str(jwt_error.value)

    def test_create_access_token_for_user_wrong_algo(self, auth_obj, duke_test_user):
        token = auth_obj.create_access_token_for_user(user=duke_test_user)
        with pytest.raises(JWTError) as jwt_error:
            jwt.decode(token,
                        str(settings.SECRET_KEY),
                        audience=settings.JWT_AUDIENCE,
                        algorithms='HMAC')

        assert 'The specified alg value is not allowed' in str(jwt_error.value)
        
    def test_create_access_token_for_user_no_user(self, auth_obj):
        token = auth_obj.create_access_token_for_user(user=None)
        assert token is None

    def test_verify_password(self, auth_obj, duke_test_user):
        is_verified = auth_obj.verify_password(password='testduke2030',
                                                salt=duke_test_user.salt,
                                                hashed_pw=duke_test_user.password)
        assert is_verified is True