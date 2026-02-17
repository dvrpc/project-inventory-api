from pydantic import BaseModel, computed_field
from typing import Optional, Union
from datetime import datetime
from src.product.schema import ProductResponse
from src.external_product.schema import ExternalProductResponse

class ProjectResponse(BaseModel):
    project_id: int
    internal: bool
    created_at: datetime
    updated_at: datetime

    product: Optional[Union[ProductResponse, ExternalProductResponse]]

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
