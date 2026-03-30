from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductWpidResponse(BaseModel):
    PRODUCTID: str
    WORKPROGRAMID: str
    ID: int
    ADDBY: Optional[str]
    ADDTIME: Optional[datetime]

    class Config:
        from_attributes = True
