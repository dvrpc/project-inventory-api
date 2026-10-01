from pydantic import BaseModel

class ProductGeographyResponse(BaseModel):
    pub_id: str
    geoid: str

    class Config:
        from_attributes = True

class ProductGeographyCreateRequest(BaseModel):
    pub_id: str
    geoid: str
