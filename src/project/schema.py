from pydantic import BaseModel, Field
from typing import Optional, Union, List
from datetime import datetime
from src.geography.schema import GeographyResponse
from src.keyword.schema import KeywordResponse
from src.need.schema import NeedResponse
from src.product.schema import ProductResponse
from src.external_product.schema import ExternalProductResponse
from src.recommendation.schema import RecommendationResponse

class ProjectResponse(BaseModel):
    project_id: int
    internal: bool
    created_at: datetime
    updated_at: datetime

    product: Optional[Union[ProductResponse, ExternalProductResponse]]
    needs: List[NeedResponse] = Field(default_factory=list)
    recommendations: List[RecommendationResponse] = Field(default_factory=list)
    geographies: List[GeographyResponse] = Field(default_factory=list)
    keywords: List[KeywordResponse] = Field(default_factory=list)

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

class ProjectFilters(BaseModel):
    bbox: Optional[str] = None
    geographies: Optional[str] = None
    keywords: Optional[str] = None
    sort: Optional[str] = None

    @classmethod
    def as_query(cls, bbox: Optional[str] = None, geographies: Optional[str] = None, keywords: Optional[str] = None, sort: Optional[str] = None) -> "ProjectFilters":
        return cls(bbox=bbox, geographies=geographies, keywords=keywords, sort=sort)
