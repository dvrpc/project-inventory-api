from pydantic import BaseModel

class ProductGeographyResponse(BaseModel):
    pub_id: str
    geography_id: int

    class Config:
        from_attributes = True

class ProductGeographyCreateRequest(BaseModel):
    pub_id: str
    geography_id: int
