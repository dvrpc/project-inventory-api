from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProductResponse(BaseModel):
    pub_id: str
    type_code: str
    pub_num: str
    status_code: Optional[str]
    pub_month: Optional[str]
    pub_year: Optional[str]
    title: Optional[str]
    subtitle: Optional[str]
    geography: Optional[str]
    keywords: Optional[str]
    abstract: Optional[str]
    publication_guide: Optional[str]
    cost_code: Optional[str]
    group_code: Optional[int]
    sub_code: Optional[int]
    link: Optional[str]
    note: Optional[str]
    create_date: Optional[date]
    pub_date: Optional[date]
    author: Optional[str]
    owner: Optional[str]
    status: Optional[str]

    class Config:
        from_attributes = True

class ProductCreateRequest(BaseModel):
    pub_id: str
    type_code: str
    pub_num: str
    status_code: Optional[str] = None
    pub_month: Optional[str] = None
    pub_year: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    geography: Optional[str] = None
    keywords: Optional[str] = None
    abstract: Optional[str] = None
    publication_guide: Optional[str] = None
    cost_code: Optional[str] = None
    group_code: Optional[int] = None
    sub_code: Optional[int] = None
    link: Optional[str] = None
    note: Optional[str] = None
    author: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None

class ProductUpdateRequest(BaseModel):
    type_code: Optional[str] = None
    pub_num: Optional[str] = None
    status_code: Optional[str] = None
    pub_month: Optional[str] = None
    pub_year: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    geography: Optional[str] = None
    keywords: Optional[str] = None
    abstract: Optional[str] = None
    publication_guide: Optional[str] = None
    cost_code: Optional[str] = None
    group_code: Optional[int] = None
    sub_code: Optional[int] = None
    link: Optional[str] = None
    note: Optional[str] = None
    author: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None
