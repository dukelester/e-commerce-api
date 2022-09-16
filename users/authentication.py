import bcrypt
from passlib.context import CryptContext
from .schemas import UserpasswordUpdate

password_context = CryptContext(schemes=['sha256_crypt',], deprecated="auto")

class Authenticate:
    @staticmethod
    def generate_salt() -> str:
        return bcrypt.gensalt().decode()
    
    @staticmethod
    def hashed_password(*, password: str, salt: str) -> str:
        return password_context.hash(password, salt)
        

    def create_salt_hashed_password(self, *, plain_text_password: str) -> UserpasswordUpdate:
        salt = self.generate_salt()
        hash_password = self.hashed_password(password = plain_text_password, salt=salt)
        return UserpasswordUpdate(hash_password=salt, password=hash_password)
    
   
  
