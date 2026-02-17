from pydantic import BaseModel
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
    createby: Optional[str]
    status: Optional[str]

    class Config:
        from_attributes = True
