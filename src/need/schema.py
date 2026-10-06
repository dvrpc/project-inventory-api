from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NeedResponse(BaseModel):
    need_id: int
    pub_id: int
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NeedCreateRequest(BaseModel):
    pub_id: int
    description: str

class NeedUpdateRequest(BaseModel):
    pub_id: Optional[int] = None
    description: Optional[str] = None
