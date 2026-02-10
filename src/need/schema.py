from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NeedResponse(BaseModel):
    need_id: int
    project_id: int
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NeedCreateRequest(BaseModel):
    project_id: int
    description: str

class NeedUpdateRequest(BaseModel):
    project_id: Optional[int] = None
    description: Optional[str] = None
