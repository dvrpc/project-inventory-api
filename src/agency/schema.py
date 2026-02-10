from pydantic import BaseModel
from typing import Optional

class AgencyResponse(BaseModel):
    agency_id: int
    name: str
    address: Optional[str]
    email: Optional[str]
    phone: Optional[str]

    class Config:
        from_attributes = True

class AgencyCreateRequest(BaseModel):
    name: str
    address: Optional[str]
    email: Optional[str]
    phone: Optional[str]