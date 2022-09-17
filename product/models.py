
from datetime import datetime
from app.database import Base
from sqlalchemy import Column, Integer, String, Numeric,BigInteger, ForeignKey, Unicode,DateTime

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True,  unique=True, nullable=False)
    slug = Column(String, index=True, unique=True, nullable=False)
    

class Product(Base):
    __tablename__ = "product"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(BigInteger, ForeignKey("category.id"))
    name = Column(String, index=True,  unique=True, nullable=False)
    slug = Column(String, index=True, unique=True, nullable=False)
    description = Column(Unicode, nullable=False)
    price = Column(Numeric, nullable=False, index=True)
    image = Column(String, nullable=False)
    thumbnail = Column(String, nullable=False)
    date_added = Column(DateTime, default=datetime.now())
