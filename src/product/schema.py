from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class ProductResponse(BaseModel):
    pub_id: str
    typecode: str
    pub_num: str
    title: Optional[str]
    subtitle: Optional[str]
    keywords: Optional[str]
    abstract: Optional[str]
    createdate: Optional[datetime]
    livedate: Optional[datetime]
    lastupdatedate: Optional[datetime]
    pub_date: Optional[datetime]
    s1: Optional[str]
    s1_id: Optional[str]
    status: Optional[str]
    wpids: Optional[list[str]]

    @field_validator("wpids", mode="before")
    @classmethod
    def extract_wpids(cls, v):
        if not v:
            return v
        return [
            item.WORKPROGRAMID if hasattr(item, "WORKPROGRAMID") else item for item in v
        ]

    class Config:
        from_attributes = True
