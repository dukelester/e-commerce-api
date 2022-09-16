from email.policy import default
from operator import index
from xmlrpc.client import Boolean
from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    email_address = Column(String,  index=True)
    phone_number = Column(String, index=True)
    password = Column(String)
    hash_password = Column(String)
    is_email_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False,  nullable=False)
    
