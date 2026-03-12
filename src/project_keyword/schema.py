from pydantic import BaseModel

class ProjectKeywordResponse(BaseModel):
    project_id: int
    keyword_id: int

    class Config:
        from_attributes = True

class ProjectKeywordCreateRequest(BaseModel):
    project_id: int
    keyword_id: int
