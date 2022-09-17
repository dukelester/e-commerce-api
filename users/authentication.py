from datetime import datetime, timedelta
import bcrypt
from passlib.context import CryptContext
from .schemas import JWTCredentials, JWTMeta, JWTPayload, UserInDB, UserpasswordUpdate
from app.core.config import settings
import jwt


password_context = CryptContext(schemes=['sha256_crypt',], deprecated="auto")

class Authenticate:
    def create_salt_hashed_password(self, *, plain_text_password: str) -> UserpasswordUpdate:
        salt = self.generate_salt()
        hash_password = self.hash_password(password = plain_text_password, salt=salt)
        return UserpasswordUpdate(salt=salt, password=hash_password)
    
    @staticmethod
    def generate_salt() -> str:
        return bcrypt.gensalt().decode()

    @staticmethod
    def hash_password(*, password: str, salt: str) -> str:
        return password_context.hash(password + salt)
    
    @staticmethod
    def verify_password(*, password: str, salt: str, hashed_password: str):
        return password_context.verify(password+salt, hashed_password)
    
    @staticmethod
    def create_access_token_for_user(*,user: UserInDB, secret_key: str = settings.SECRET_KEY,
                                     audience:str = settings.JWT_AUDIENCE,
                                     expires_in:int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
                                     ):
        if not user:
            return None
        jwt_meta = JWTMeta(
            aud=audience, iat= datetime.timestamp(datetime.now()),
            exp= datetime.timestamp(datetime.now() + timedelta(minutes=expires_in))
        )
        jwt_credentials = JWTCredentials(
            sub= user.email_address,username=user.username
        )
        jwt_token_payload = JWTPayload(
            **jwt_meta.dict(),
            **jwt_credentials.dict()
        )
        return jwt.encode(jwt_token_payload.dict(), secret_key)
    
   
  
