from pydantic import BaseModel

class ProjectKeywordResponse(BaseModel):
    pub_id: str
    keyword_id: int

    class Config:
        from_attributes = True

class ProjectKeywordCreateRequest(BaseModel):
    pub_id: str
    keyword_id: int
