from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from src.agency.schema import AgencyResponse

class ExternalProductResponse(BaseModel):
    product_id: int
    agency: AgencyResponse
    title: str
    link: str
    abstract: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ExternalProductCreateRequest(BaseModel):
    agency_id: int
    title: str
    link: str
    abstract: str

class ExternalProductUpdateRequest(BaseModel):
    agency_id: Optional[int] = None
    title: Optional[str] = None
    link: Optional[str] = None
    abstract: Optional[str] = None
