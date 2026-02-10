from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectResponse(BaseModel):
    project_id: int
    product_id: Optional[str]
    external_product_id: Optional[int]
    internal: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProjectCreateRequest(BaseModel):
    product_id: Optional[str] = None
    external_product_id: Optional[int] = None
    internal: bool

class ProjectUpdateRequest(BaseModel):
    product_id: Optional[str] = None
    external_product_id: Optional[int] = None
    internal: Optional[bool] = None
