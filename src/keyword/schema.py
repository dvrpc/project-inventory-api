from pydantic import BaseModel
from typing import Optional

class KeywordResponse(BaseModel):
    keyword_id: int
    name: str

    class Config:
        from_attributes = True

class KeywordCreateRequest(BaseModel):
    name: str

class KeywordUpdateRequest(BaseModel):
    name: Optional[str] = None
