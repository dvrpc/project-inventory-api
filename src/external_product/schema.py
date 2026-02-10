from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExternalProductResponse(BaseModel):
    product_id: int
    title: str
    link: str
    abstract: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ExternalProductCreateRequest(BaseModel):
    title: str
    link: str
    abstract: str

class ExternalProductUpdateRequest(BaseModel):
    title: Optional[str] = None
    link: Optional[str] = None
    abstract: Optional[str] = None
