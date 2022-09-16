# define the global schemas here

from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime

class CoreModel(BaseModel):
    """ To be shared among common models in the app """
    pass

class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    @validator("created_at", "updated_at", pre=True, always=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now()
    
class IDModelMixin(BaseModel):
    id: int