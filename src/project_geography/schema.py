from pydantic import BaseModel

class ProjectGeographyResponse(BaseModel):
    pub_id: str
    geoid: str

    class Config:
        from_attributes = True

