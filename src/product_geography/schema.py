from pydantic import BaseModel

class ProjectGeographyResponse(BaseModel):
    pub_id: str
    geography_id: int

    class Config:
        from_attributes = True

class ProjectGeographyCreateRequest(BaseModel):
    pub_id: str
    geography_id: int
