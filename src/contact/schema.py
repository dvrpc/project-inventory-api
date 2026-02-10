from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ContactResponse(BaseModel):
    contact_id: int
    agency_id: Optional[int]
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str]
    job_title: Optional[str]
    verified: Optional[bool]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ContactCreateRequest(BaseModel):
    agency_id: Optional[int] = None
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    job_title: Optional[str] = None
    verified: Optional[bool] = False

class ContactUpdateRequest(BaseModel):
    agency_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    job_title: Optional[str] = None
    verified: Optional[bool] = None
