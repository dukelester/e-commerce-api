import pytest
from app.database import SessionLocal

@pytest.yield_fixture()
async def init_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       await db.close()