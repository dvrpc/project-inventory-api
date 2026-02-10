from pydantic import BaseModel

class ProjectGeographyResponse(BaseModel):
    project_id: int
    geography_id: int

    class Config:
        from_attributes = True

class ProjectGeographyCreateRequest(BaseModel):
    project_id: int
    geography_id: int
