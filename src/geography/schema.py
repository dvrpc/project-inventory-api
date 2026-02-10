from pydantic import BaseModel
from typing import Optional

class GeographyResponse(BaseModel):
    geography_id: int
    name: str
    geo_type: str
    geoid: Optional[str]

    class Config:
        from_attributes = True