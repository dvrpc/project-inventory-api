from pydantic import BaseModel

class GeographyResponse(BaseModel):
    geoid: str
    name: str
    geo_type: str
    dvrpc_reg: bool

    class Config:
        from_attributes = True

