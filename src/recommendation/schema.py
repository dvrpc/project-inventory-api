from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RecommendationResponse(BaseModel):
    recommendation_id: int
    project_id: int
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RecommendationCreateRequest(BaseModel):
    project_id: int
    description: str

class RecommendationUpdateRequest(BaseModel):
    project_id: Optional[int] = None
    description: Optional[str] = None
