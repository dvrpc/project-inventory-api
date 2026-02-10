from pydantic import BaseModel
from typing import Optional

class GeographyResponse(BaseModel):
    geography_id: int
    name: str
    geo_type: str
    geoid: Optional[str]

    class Config:
        from_attributes = True

class GeographyCreateRequest(BaseModel):
    name: str
    geo_type: str
    geoid: Optional[str] = None

class GeographyUpdateRequest(BaseModel):
    name: Optional[str] = None
    geo_type: Optional[str] = None
    geoid: Optional[str] = None