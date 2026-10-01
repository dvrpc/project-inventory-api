from pydantic import BaseModel

class ProductKeywordResponse(BaseModel):
    pub_id: str
    keyword_id: int

    class Config:
        from_attributes = True

class ProductKeywordCreateRequest(BaseModel):
    pub_id: str
    keyword_id: int
