from pydantic import BaseModel, EmailStr
from typing import Optional


class AgencyResponse(BaseModel):
    agency_id: int
    name: str
    address: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]

    class Config:
        from_attributes = True

class AgencyCreateRequest(BaseModel):
    name: str
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class AgencyUpdateRequest(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None