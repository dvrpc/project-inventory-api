from pydantic import BaseModel
from typing import Optional

class GeographyResponse(BaseModel):
    geoid: str
    name: str
    geo_type: str
    dvrpc_reg: bool

    class Config:
        from_attributes = True

class GeographyCreateRequest(BaseModel):
    geoid: str
    name: str
    geo_type: str

class GeographyUpdateRequest(BaseModel):
    name: Optional[str] = None
    geo_type: Optional[str] = None
